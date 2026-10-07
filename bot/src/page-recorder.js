// This function runs inside the Jitsi Meet page. Puppeteer serializes it, so it must not use
// anything from the module scope.
//
// It records one WebM/Opus file for each (audio track, owner) pair. The speaker identity comes
// from the track owner that lib-jitsi-meet reports, never from the audio content.
export function installRecorder({ pollMs, bitrate }) {
    const room = window.APP.conference._room;
    const ctx = new AudioContext();
    const t0 = performance.now();
    const active = new Map(); // key -> segment
    const known = new Map(); // participant id -> display name
    const tasks = [];
    let seq = 0;

    ctx.resume();

    const now = () => Math.round(performance.now() - t0) / 1000;
    const emit = (type, data = {}) => window.__ntEvent({ t: now(), wall: new Date().toISOString(), type, ...data });
    const nameOf = id => room.getParticipantById(id)?.getDisplayName() || null;

    function toBase64(buffer) {
        const bytes = new Uint8Array(buffer);
        let binary = '';

        for (let i = 0; i < bytes.length; i += 0x8000) {
            binary += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
        }

        return btoa(binary);
    }

    // With SSRC rewriting the bridge gives a track to a different participant. The active
    // peer connection always reports the current owner.
    function audioTracks() {
        let tracks = [];

        try {
            tracks = room.getActivePeerConnection()?.getRemoteTracks(undefined, 'audio') ?? [];
        } catch (e) {
            tracks = [];
        }
        if (!tracks.length) {
            tracks = room.getParticipants().flatMap(p => p.getTracksByMediaType('audio'));
        }

        return tracks.filter(t => t.getParticipantId() && t.getTrack()?.readyState === 'live');
    }

    function start(key, track) {
        const participantId = track.getParticipantId();
        const stream = new MediaStream([ track.getTrack() ]);

        // Chromium sends remote WebRTC audio to Web Audio only when a media element also uses it.
        const sink = new Audio();

        sink.muted = true;
        sink.srcObject = stream;
        sink.play().catch(() => {});

        // Web Audio gives a continuous signal, so a muted participant becomes silence and the
        // time line of the file has no gaps.
        const source = ctx.createMediaStreamSource(stream);
        const dest = ctx.createMediaStreamDestination();

        dest.channelCount = 1;
        source.connect(dest);

        const rec = new MediaRecorder(dest.stream, { mimeType: 'audio/webm;codecs=opus', audioBitsPerSecond: bitrate });
        const file = `${String(++seq).padStart(3, '0')}-${participantId}.webm`;
        const segment = { file, participantId, track, rec, source, sink, muted: track.isMuted(), chain: Promise.resolve() };

        rec.ondataavailable = event => {
            if (event.data.size) {
                segment.chain = segment.chain
                    .then(() => event.data.arrayBuffer())
                    .then(buffer => window.__ntChunk(file, toBase64(buffer)));
            }
        };
        segment.stopped = new Promise(resolve => {
            rec.onstop = resolve;
        });

        rec.start(1000);
        active.set(key, segment);
        emit('segment_start', { file, participantId, name: nameOf(participantId), muted: segment.muted });
    }

    function stop(key, reason) {
        const segment = active.get(key);

        active.delete(key);
        emit('segment_end', { file: segment.file, participantId: segment.participantId, reason });
        segment.rec.stop();
        tasks.push(segment.stopped.then(() => segment.chain).then(() => {
            segment.source.disconnect();
            segment.sink.srcObject = null;
        }));
    }

    function sync() {
        const participants = new Map(room.getParticipants()
            .filter(p => !p.isHidden())
            .map(p => [ p.getId(), p.getDisplayName() || null ]));

        for (const [ id, name ] of participants) {
            if (!known.has(id)) {
                emit('participant_joined', { participantId: id, name });
            } else if (known.get(id) !== name) {
                emit('name_changed', { participantId: id, name, oldName: known.get(id) });
            }
            known.set(id, name);
        }
        for (const id of [ ...known.keys() ]) {
            if (!participants.has(id)) {
                emit('participant_left', { participantId: id, name: known.get(id) });
                known.delete(id);
            }
        }

        const present = new Map();

        for (const track of audioTracks()) {
            present.set(`${track.getTrack().id}|${track.getParticipantId()}`, track);
        }
        for (const key of [ ...active.keys() ]) {
            if (!present.has(key)) {
                stop(key, 'track removed or owner changed');
            }
        }
        for (const [ key, track ] of present) {
            const segment = active.get(key);

            if (!segment) {
                start(key, track);
            } else if (segment.muted !== track.isMuted()) {
                segment.muted = track.isMuted();
                emit(segment.muted ? 'muted' : 'unmuted', { file: segment.file, participantId: segment.participantId });
            }
        }
    }

    const safeSync = () => {
        try {
            sync();
        } catch (e) {
            emit('error', { message: String(e?.stack || e) });
        }
    };
    const timer = setInterval(safeSync, pollMs);

    // The events only make the reaction faster. The poll is the source of truth.
    const events = window.JitsiMeetJS?.events?.conference;

    for (const name of [ 'TRACK_ADDED', 'TRACK_REMOVED', 'USER_JOINED', 'USER_LEFT', 'DISPLAY_NAME_CHANGED' ]) {
        events?.[name] && room.on(events[name], safeSync);
    }

    window.__nt = {
        status: () => ({
            joined: room.isJoined(),
            participants: known.size,
            segments: active.size,
            audioContext: ctx.state
        }),
        stop: async () => {
            clearInterval(timer);
            for (const key of [ ...active.keys() ]) {
                stop(key, 'capture stopped');
            }
            await Promise.all(tasks);
            emit('capture_end');
        }
    };

    emit('capture_start', { sampleRate: ctx.sampleRate, audioContext: ctx.state });
    safeSync();
}
