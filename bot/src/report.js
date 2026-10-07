#!/usr/bin/env node
// Print a table of the captured segments: speaker, time offsets, measured duration, and level.
//
//   node report.js out/test1
import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

import { buildManifest } from './manifest.js';

export function measure(file) {
    // WebM from MediaRecorder has no duration header, so ffmpeg must decode the file.
    // ffmpeg writes the result to stderr.
    const text = spawnSync('ffmpeg', [ '-hide_banner', '-nostats', '-i', file, '-af', 'volumedetect', '-f', 'null', '-' ],
        { encoding: 'utf8' }).stderr ?? '';
    const samples = Number([ ...text.matchAll(/n_samples: (\d+)/g) ].at(-1)?.[1] ?? NaN);
    const rate = Number(/Audio: .*?(\d+) Hz/.exec(text)?.[1] ?? NaN);

    return {
        duration_s: samples / rate,
        mean_dB: Number(/mean_volume: (-?[\d.]+|-inf)/.exec(text)?.[1] ?? NaN),
        max_dB: Number(/max_volume: (-?[\d.]+|-inf)/.exec(text)?.[1] ?? NaN)
    };
}

export function report(dir) {
    const manifestFile = join(dir, 'manifest.json');
    let manifest;

    if (existsSync(manifestFile)) {
        manifest = JSON.parse(readFileSync(manifestFile, 'utf8'));
    } else {
        // The capture did not stop cleanly. The events file has the same data.
        const events = readFileSync(join(dir, 'events.jsonl'), 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l));

        manifest = buildManifest(events, { stopReason: 'no manifest, made from events.jsonl' });
    }
    const rows = manifest.segments.map(s => ({ ...s, ...measure(join(dir, s.file)) }));

    console.log(`Capture start: ${manifest.captureStart}   Stop reason: ${manifest.stopReason}`);
    console.log('file                   start_s    end_s  expect_s  actual_s  mean_dB  max_dB  name');
    for (const r of rows) {
        const n = (v, w) => (Number.isFinite(v) ? v.toFixed(1) : '-').padStart(w);

        console.log(`${r.file.padEnd(20)} ${n(r.start_s, 9)} ${n(r.end_s, 8)} ${n(r.end_s - r.start_s, 9)} ${n(r.duration_s, 9)} `
            + `${n(r.mean_dB, 8)} ${n(r.max_dB, 7)}  ${r.name ?? '(no name)'}`);
    }

    return rows;
}

if (import.meta.url === `file://${process.argv[1]}`) {
    if (!process.argv[2]) {
        console.log('Usage: node report.js <capture directory>');
        process.exit(2);
    }
    report(process.argv[2]);
}
