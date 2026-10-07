#!/usr/bin/env node
// Self test: two fake speakers with different tones join a room, and the capture bot records them.
// The test passes when each captured file contains only the tone of the speaker in its label.
//
//   node selftest.js --url https://<jitsi host>/<room>
//
// The room must open without a login. meet.jit.si does not permit this.
import { execFileSync, spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

import { report } from './report.js';

const { values: opt } = parseArgs({
    options: {
        url: { type: 'string' },
        out: { type: 'string', default: 'out/selftest' },
        seconds: { type: 'string', default: '30' }
    }
});

if (!opt.url) {
    console.log('Usage: node selftest.js --url <jitsi room url> [--out <dir>] [--seconds <n>]');
    process.exit(2);
}

const here = dirname(fileURLToPath(import.meta.url));
const outDir = resolve(opt.out);
const seconds = Number(opt.seconds);
const speakers = [
    { name: 'Chris', hz: 440, delay: 5, seconds: seconds - 5, muteAfter: 12 },
    { name: 'Kris', hz: 880, delay: 13, seconds: seconds - 18, renameAfter: 6, renameTo: 'Kris (renamed)' }
];

mkdirSync(outDir, { recursive: true });

for (const s of speakers) {
    s.wav = join(outDir, `${s.name}.wav`);
    execFileSync('ffmpeg', [ '-hide_banner', '-loglevel', 'error', '-y', '-f', 'lavfi',
        '-i', `sine=frequency=${s.hz}:duration=10`, '-ac', '2', '-ar', '48000', s.wav ]);
}

const run = (script, args) => new Promise(done => {
    spawn(process.execPath, [ join(here, script), ...args ], { stdio: 'inherit' }).on('exit', done);
});
const sleep = s => new Promise(r => setTimeout(r, s * 1000));

const capture = spawn(process.execPath, [ join(here, 'capture.js'), '--url', opt.url, '--out', outDir,
    '--wait-minutes', '2', '--alone-minutes', '0.15', '--max-minutes', String((seconds + 30) / 60) ], { stdio: 'inherit' });
const captureDone = new Promise(done => capture.on('exit', done));

await Promise.all(speakers.map(async s => {
    await sleep(s.delay);

    const args = [ '--url', opt.url, '--name', s.name, '--wav', s.wav, '--seconds', String(s.seconds) ];

    s.muteAfter && args.push('--mute-after', String(s.muteAfter));
    s.renameAfter && args.push('--rename-after', String(s.renameAfter), '--rename-to', s.renameTo);
    await run('speak.js', args);
}));

if (await captureDone !== 0) {
    console.log('FAIL: the capture bot did not complete.');
    process.exit(1);
}

// Signal power at one frequency (Goertzel), as a fraction of the total power. The result is the
// mean of 100 ms blocks, because the phase of the tone is not stable for the full file.
function toneShare(file, hz) {
    const rate = 16000;
    const block = rate / 10;
    const pcm = execFileSync('ffmpeg', [ '-hide_banner', '-loglevel', 'error', '-i', file, '-ac', '1', '-ar', String(rate),
        '-f', 's16le', '-' ], { maxBuffer: 1 << 28 });
    const coeff = 2 * Math.cos(2 * Math.PI * hz / rate);
    let sum = 0;
    let blocks = 0;

    for (let start = 0; start + block <= pcm.length / 2; start += block) {
        let s1 = 0;
        let s2 = 0;
        let total = 0;

        for (let i = start; i < start + block; i++) {
            const x = pcm.readInt16LE(i * 2);
            const s0 = x + coeff * s1 - s2;

            s2 = s1;
            s1 = s0;
            total += x * x;
        }

        // Ignore blocks that are almost silent.
        if (total / block > 100) {
            sum += (s1 * s1 + s2 * s2 - coeff * s1 * s2) / (total * block / 2);
            blocks++;
        }
    }

    return blocks ? sum / blocks : 0;
}

console.log('');

const rows = report(outDir);
let ok = rows.length > 0;

console.log('');
for (const s of speakers) {
    const own = rows.filter(r => r.name === s.name || r.name === s.renameTo);
    const other = speakers.find(o => o !== s);

    if (!own.length) {
        console.log(`FAIL: no file has the label of ${s.name}.`);
        ok = false;
    }
    for (const r of own) {
        const file = join(outDir, r.file);
        const good = toneShare(file, s.hz);
        const bad = toneShare(file, other.hz);
        const pass = good > 0.8 && bad < 0.01;

        console.log(`${pass ? 'ok  ' : 'FAIL'} ${r.file} label "${r.name}": ${s.hz} Hz share ${good.toFixed(3)}, `
            + `${other.hz} Hz share ${bad.toFixed(4)}`);
        ok &&= pass;
    }
}
for (const r of rows) {
    const drift = Math.abs(r.duration_s - (r.end_s - r.start_s));

    if (!(drift < 1.5)) {
        console.log(`FAIL: ${r.file} has ${r.duration_s.toFixed(1)} s of audio, but the events give ${(r.end_s - r.start_s).toFixed(1)} s.`);
        ok = false;
    }
}

console.log(ok ? '\nPASS: each file contains only the speaker in its label.' : '\nFAIL');
process.exit(ok ? 0 : 1);
