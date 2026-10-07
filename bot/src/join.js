// Shared helpers: launch Chromium, open a Jitsi room, wait until the conference is joined.
import puppeteer from 'puppeteer-core';

export const CHROMIUM_PATH = process.env.CHROMIUM_PATH || '/usr/bin/chromium';

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

// Jitsi Meet reads config overrides from the URL hash. Each value is JSON.
export function roomUrl(url, { name, micMuted = true, config = {} }) {
    const u = new URL(url);
    const params = {
        'config.prejoinConfig.enabled': false,
        'config.startWithAudioMuted': micMuted,
        'config.startWithVideoMuted': true,
        'config.disableDeepLinking': true,
        'userInfo.displayName': name,
        ...Object.fromEntries(Object.entries(config).map(([ key, value ]) => [ `config.${key}`, value ]))
    };

    u.hash = Object.entries(params)
        .map(([ key, value ]) => `${key}=${encodeURIComponent(JSON.stringify(value))}`)
        .join('&');

    return u.toString();
}

export function launch({ headful = false, fakeAudioFile = null } = {}) {
    const args = [
        '--use-fake-ui-for-media-stream',
        '--use-fake-device-for-media-stream',
        '--autoplay-policy=no-user-gesture-required',
        '--mute-audio',
        '--no-first-run',
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding',
        '--disable-backgrounding-occluded-windows',
        '--window-size=1280,720'
    ];

    if (fakeAudioFile) {
        args.push(`--use-file-for-fake-audio-capture=${fakeAudioFile}`);
    }

    // Puppeteer must not handle the signals: its handlers end the process at once, before the
    // caller can stop the capture and write its files.
    return puppeteer.launch({
        executablePath: CHROMIUM_PATH,
        headless: !headful,
        args,
        handleSIGINT: false,
        handleSIGTERM: false,
        handleSIGHUP: false
    });
}

function pageState() {
    const room = window.APP?.conference?._room;
    const dialog = document.querySelector('[role="dialog"]');

    return {
        joined: Boolean(room?.isJoined?.()),
        prejoin: Boolean(document.querySelector('[data-testid="prejoin.joinMeeting"]')),
        waiting: /no moderators have yet arrived|Asking to join/i.test(document.body?.innerText ?? ''),
        dialog: dialog ? dialog.innerText.replace(/\s+/g, ' ').slice(0, 160) : null
    };
}

// Opens the room and waits until the bot is in the conference.
// On meet.jit.si a person with an account must open the room first, so this can wait a long time.
export async function joinRoom(browser, url, { waitMs, reloadMs = 120000, log = () => {} }) {
    const page = await browser.newPage();
    const deadline = Date.now() + waitMs;
    let lastLoad = 0;
    let lastState = '';
    let waiting = false;

    while (Date.now() < deadline) {
        // The page of a room that is not open joins by itself when a moderator arrives. Do not load it again.
        if (!lastLoad || (!waiting && Date.now() - lastLoad > reloadMs)) {
            log(lastLoad ? 'not in the conference yet, load the page again' : `open ${url}`);
            lastLoad = Date.now();
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(e => log(`load error: ${e.message}`));
        }

        // The page can navigate while we look at it; ignore those errors.
        const state = await page.evaluate(pageState).catch(() => null);

        if (state?.joined) {
            return page;
        }
        waiting = Boolean(state?.waiting);
        if (state?.prejoin) {
            await page.click('[data-testid="prejoin.joinMeeting"]').catch(() => {});
        }

        const text = JSON.stringify(state);

        if (state && text !== lastState) {
            lastState = text;
            log(`state: ${state.waiting ? 'the room is not open, or a moderator must admit the bot; wait'
                : state.dialog ? `dialog "${state.dialog}"` : state.prejoin ? 'prejoin page' : 'not joined'}`);
        }
        await sleep(1000);
    }

    return { failed: true, page };
}
