// Build the segment list from the capture events.
export function buildManifest(events, meta = {}) {
    const segments = new Map();
    const start = events.find(e => e.type === 'capture_start');
    const last = events.at(-1);

    for (const e of events) {
        if (e.type === 'segment_start') {
            segments.set(e.file, { file: e.file, participantId: e.participantId, name: e.name, start_s: e.t, end_s: null });
        } else if (e.type === 'segment_end') {
            segments.get(e.file).end_s = e.t;
        } else if (e.type === 'name_changed') {
            // Keep the name that the participant had at the end of the segment.
            for (const s of segments.values()) {
                if (s.participantId === e.participantId && s.end_s === null) {
                    s.name = e.name;
                }
            }
        }
    }

    // A capture that did not stop cleanly has segments with no end event.
    for (const s of segments.values()) {
        s.end_s ??= last.t;
    }

    return { ...meta, captureStart: start?.wall ?? null, segments: [ ...segments.values() ] };
}
