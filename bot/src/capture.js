#!/usr/bin/env node
// Capture test: join a Jitsi meeting as a guest and record one audio file for each participant.
//
//   node capture.js --url https://meet.jit.si/SomeRoom --out out/test1
import { appendFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { parseArgs } from 'node:util';

import { joinRoom, launch, roomUrl } from './join.js';
import { buildManifest } from './manifest.js';
import { installRecorder } from './page-recorder.js';

const { values: opt } = parseArgs({
    options: {
        url: { type: 'string' },
        out: { type: 'string' },
        name: { type: 'string', default: 'Crow - AI Notetaker' },
        'wait-minutes': { type: 'string', default: '15' },
        'alone-minutes': { type: 'string', default: '5' },
        'max-minutes': { type: 'string', default: '120' },
        bitrate: { type: 'string', default: '32000' },
        headful: { type: 'boolean', default: false },
        help: { type: 'boolean', short: 'h', default: false }
    }
});

if (opt.help || !opt.url) {
    console.log(`Usage: node capture.js --url <jitsi room url> [options]

  --out <dir>            output directory (default: out/<time stamp>)
  --name <text>          display name of the bot
  --wait-minutes <n>     maximum wait for the room to open (default 15)
  --alone-minutes <n>    leave after this time with no other participant (default 5)
  --max-minutes <n>      maximum capture duration (default 120)
  --bitrate <n>          Opus bit rate for each track (default 32000)
  --headful              show the browser window

Stop the capture with Ctrl+C. The files are complete after the bot leaves.`);
    process.exit(opt.help ? 0 : 2);
}

const minutes = key => Number(opt[key]) * 60000;
const outDir = resolve(opt.out || join('out', new Date().toISOString().replace(/[:.]/g, '-')));
const eventsFile = join(outDir, 'events.jsonl');
const events = [];
const log = message => console.log(`[${new Date().toISOString().slice(11, 19)}] ${message}`);

mkdirSync(outDir, { recursive: true });

let stopReason = null;

process.on('SIGINT', () => {
    stopReason ??= 'stopped by the operator';
});
process.on('SIGTERM', () => {
    stopReason ??= 'stopped by the operator';
});

function onEvent(event) {
    events.push(event);
    appendFileSync(eventsFile, `${JSON.stringify(event)}\n`);

    const who = event.name ? `"${event.name}" (${event.participantId})` : event.participantId || '';

    if (event.type === 'error') {
        log(`page error: ${event.message}`);
    } else if (event.type !== 'capture_start' && event.type !== 'capture_end') {
        log(`${event.t.toFixed(1).padStart(7)}s ${event.type} ${who} ${event.file || ''}`);
    }
}

function writeManifest(reason) {
    const manifest = buildManifest(events, { url: opt.url, botName: opt.name, stopReason: reason });

    writeFileSync(join(outDir, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);
}

const browser = await launch({ headful: opt.headful });
let exitCode = 0;

try {
    const page = await joinRoom(browser, roomUrl(opt.url, { name: opt.name }), { waitMs: minutes('wait-minutes'), log });

    if (page.failed) {
        await page.page.screenshot({ path: join(outDir, 'not-joined.png') }).catch(() => {});
        log(`The bot did not get into the conference. See ${join(outDir, 'not-joined.png')}.`);
        exitCode = 1;
    } else {
        log('joined the conference');
        await page.exposeFunction('__ntEvent', onEvent);
        await page.exposeFunction('__ntChunk', (file, base64) => appendFileSync(join(outDir, file), Buffer.from(base64, 'base64')));
        await page.evaluate(installRecorder, { pollMs: 200, bitrate: Number(opt.bitrate) });

        const started = Date.now();
        let aloneSince = Date.now();

        while (!stopReason) {
            await new Promise(r => setTimeout(r, 1000));

            const status = await page.evaluate(() => window.__nt.status()).catch(() => null);

            if (!status || !status.joined) {
                stopReason = 'the conference ended or removed the bot';
            } else if (Date.now() - started > minutes('max-minutes')) {
                stopReason = 'maximum duration';
            } else if (status.participants > 0) {
                aloneSince = Date.now();
            } else if (Date.now() - aloneSince > minutes('alone-minutes')) {
                stopReason = 'no other participant';
            }
        }

        log(`stop: ${stopReason}`);
        await Promise.race([
            page.evaluate(() => window.__nt.stop()),
            new Promise(r => setTimeout(r, 10000))
        ]).catch(e => log(`stop error: ${e.message}`));
        await page.evaluate(() => window.APP.conference.hangup?.(false)).catch(() => {});
        writeManifest(stopReason);
        log(`output: ${outDir}`);
    }
} finally {
    await browser.close().catch(() => {});
}

process.exit(exitCode);
