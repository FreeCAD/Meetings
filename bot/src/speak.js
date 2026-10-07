#!/usr/bin/env node
// Test helper: join a Jitsi meeting and play a WAV file as the microphone. The file loops.
//
//   node speak.js --url https://example.org/Room --name "Chris" --wav /abs/path/chris.wav --seconds 30
import { resolve } from 'node:path';
import { parseArgs } from 'node:util';

import { joinRoom, launch, roomUrl } from './join.js';

const { values: opt } = parseArgs({
    options: {
        url: { type: 'string' },
        name: { type: 'string', default: 'Test speaker' },
        wav: { type: 'string' },
        seconds: { type: 'string', default: '30' },
        'rename-after': { type: 'string' },
        'rename-to': { type: 'string' },
        'mute-after': { type: 'string' },
        'mute-seconds': { type: 'string', default: '5' }
    }
});

if (!opt.url || !opt.wav) {
    console.log('Usage: node speak.js --url <jitsi room url> --wav <file> [--name <text>] [--seconds <n>]');
    process.exit(2);
}

const log = message => console.log(`[speaker ${opt.name}] ${message}`);
const browser = await launch({ fakeAudioFile: resolve(opt.wav) });

try {
    const page = await joinRoom(browser, roomUrl(opt.url, { name: opt.name, micMuted: false, config: { disableAP: true } }), { waitMs: 60000, log });

    if (page.failed) {
        log('did not get into the conference');
        process.exitCode = 1;
    } else {
        // Some hosts set disableInitialGUM, so the microphone starts muted.
        await page.evaluate(() => window.APP.conference.isLocalAudioMuted() && window.APP.conference.muteAudio(false));
        log('joined');
        if (opt['rename-after']) {
            setTimeout(() => {
                page.evaluate(n => window.APP.conference._room.setDisplayName(n), opt['rename-to']).catch(() => {});
            }, Number(opt['rename-after']) * 1000);
        }
        if (opt['mute-after']) {
            const mute = muted => page.evaluate(m => window.APP.conference.muteAudio(m), muted).catch(() => {});

            setTimeout(() => mute(true), Number(opt['mute-after']) * 1000);
            setTimeout(() => mute(false), (Number(opt['mute-after']) + Number(opt['mute-seconds'])) * 1000);
        }
        await new Promise(r => setTimeout(r, Number(opt.seconds) * 1000));
        await page.evaluate(() => window.APP.conference.hangup?.(false)).catch(() => {});
    }
} finally {
    await browser.close().catch(() => {});
}
