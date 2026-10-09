/* Local-only stand-in for livekit-client: fake people, cameras (landscape + portrait), voices, a screen share,
   hands, chat and reactions, so the room UI can be exercised without an SFU. ?mock=default|solo|duo|crowd|share|events
   plus &me=cam to start with your own camera on. Never shipped. */
(function () {
  const Q = new URLSearchParams(location.search);
  const MODE = Q.get('mock') || 'default';
  const RoomEvent = {
    Disconnected: 'disconnected', Reconnecting: 'reconnecting', Reconnected: 'reconnected',
    ParticipantConnected: 'participantConnected', ParticipantDisconnected: 'participantDisconnected',
    TrackSubscribed: 'trackSubscribed', TrackUnsubscribed: 'trackUnsubscribed', TrackMuted: 'trackMuted', TrackUnmuted: 'trackUnmuted',
    LocalTrackPublished: 'localTrackPublished', LocalTrackUnpublished: 'localTrackUnpublished',
    ActiveSpeakersChanged: 'activeSpeakersChanged', ParticipantPermissionsChanged: 'participantPermissionsChanged',
    ConnectionQualityChanged: 'connectionQualityChanged', DataReceived: 'dataReceived', AudioPlaybackStatusChanged: 'audioPlaybackChanged',
  };
  const Source = { Camera: 'camera', Microphone: 'microphone', ScreenShare: 'screen_share', ScreenShareAudio: 'screen_share_audio' };
  const preset = (w, h) => ({ resolution: { width: w, height: h } });
  const VideoPresets = { h180: preset(320, 180), h360: preset(640, 360), h720: preset(1280, 720) };
  const AudioPresets = { speech: {} };

  const imgCache = {};
  function img(src) { if (!imgCache[src]) { const i = new Image(); i.src = src; imgCache[src] = i; } return imgCache[src]; }

  // a "camera": the person's photo, cover-fitted, gently breathing, with room tone
  function cameraStream(picture, portrait, seed) {
    const c = document.createElement('canvas');
    c.width = portrait ? 540 : 960; c.height = portrait ? 960 : 540;
    const x = c.getContext('2d'), im = img(picture);
    let t = seed || 0;
    (function draw() {
      t += 0.016;
      const g = x.createLinearGradient(0, 0, c.width, c.height);
      g.addColorStop(0, '#3b3450'); g.addColorStop(1, '#1d1a2a');
      x.fillStyle = g; x.fillRect(0, 0, c.width, c.height);
      if (im.complete && im.naturalWidth) {
        const s = Math.max(c.width / im.naturalWidth, c.height / im.naturalHeight) * (1.04 + Math.sin(t * 0.9) * 0.012);
        const w = im.naturalWidth * s, h = im.naturalHeight * s;
        x.drawImage(im, (c.width - w) / 2 + Math.sin(t * 0.6) * 4, (c.height - h) / 2 + Math.cos(t * 0.5) * 3, w, h);
      }
      const v = x.createRadialGradient(c.width / 2, c.height / 2, c.height * 0.2, c.width / 2, c.height / 2, c.height * 0.9);
      v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.35)');
      x.fillStyle = v; x.fillRect(0, 0, c.width, c.height);
      setTimeout(draw, 1000 / 20);
    })();
    return c.captureStream(20);
  }
  // a shared screen: a slide from the growth review
  function screenStream() {
    const c = document.createElement('canvas'); c.width = 1600; c.height = 900;
    const x = c.getContext('2d'); let t = 0;
    (function draw() {
      t += 0.02;
      x.fillStyle = '#fbfaff'; x.fillRect(0, 0, 1600, 900);
      x.fillStyle = '#6147c7'; x.fillRect(0, 0, 1600, 10);
      x.fillStyle = '#222439'; x.font = '300 64px Geist, Arial'; x.fillText('Onboarding, two steps', 110, 170);
      x.fillStyle = '#6c6e88'; x.font = '400 28px Geist, Arial'; x.fillText('Completion by step, new creators, September', 112, 222);
      const vals = [100, 86, 74, 68], labels = ['Visit', 'Connect X', 'Set rates', 'Live'];
      vals.forEach((v, i) => {
        const w = 1100 * v / 100, y = 300 + i * 130;
        x.fillStyle = i === 3 ? '#6147c7' : '#d9d3fb'; x.beginPath(); x.roundRect(260, y, w * (0.96 + Math.sin(t + i) * 0.01), 84, 16); x.fill();
        x.fillStyle = '#222439'; x.font = '500 30px Geist, Arial'; x.fillText(labels[i], 110, y + 54);
        x.fillStyle = i === 3 ? '#fff' : '#4a3aa6'; x.fillText(v + '%', 290, y + 54);
      });
      setTimeout(draw, 1000 / 10);
    })();
    return c.captureStream(10);
  }

  class Track {
    constructor(kind, source, stream) { this.kind = kind; this.source = source; this.stream = stream; this.isMuted = false; this._els = []; }
    attach(el) {
      el = el || document.createElement(this.kind === 'audio' ? 'audio' : 'video');
      if (this.stream) { el.srcObject = this.stream; el.muted = true; el.autoplay = true; el.playsInline = true; el.play && el.play().catch(() => {}); }
      this._els.push(el); return el;
    }
    detach() { const e = this._els; this._els = []; return e; }
  }
  class Pub {
    constructor(source, track) { this.source = source; this.track = track; this.isMuted = false; }
    setVideoDimensions() {}
  }
  class Participant {
    constructor(identity, name, role, picture) {
      this.identity = identity; this.name = name; this.metadata = JSON.stringify({ role, picture });
      this.trackPublications = new Map(); this.audioLevel = 0; this.picture = picture;
    }
    getTrackPublication(src) { for (const p of this.trackPublications.values()) if (p.source === src) return p; return null; }
    add(pub) { this.trackPublications.set(pub.source + ':' + Math.random(), pub); return pub; }
    remove(src) { for (const [k, p] of this.trackPublications) if (p.source === src) this.trackPublications.delete(k); }
  }

  const PEOPLE = [
    ['1002', 'Maya Chen', 'attendee', 'maya'], ['1003', 'Kenji Watanabe', 'moderator', 'kenji'], ['1004', 'Sofía Álvarez', 'attendee', 'sofia'],
    ['1005', 'Marcus Hale', 'attendee', 'marcus'], ['1006', 'Lena Park', 'attendee', 'lena'], ['1007', 'Ethan Brooks', 'attendee', 'ethan'],
    ['1008', 'Zara Ali', 'attendee', 'zara'], ['1009', 'Noah Kim', 'attendee', 'noah'], ['1010', 'Imani Ross', 'attendee', 'imani'],
    ['1011', 'Jordan Lee', 'attendee', 'jordan'], ['1012', 'Tomás Rivera', 'attendee', 'tomas'], ['1013', 'Aisha Khan', 'attendee', 'aisha'],
    ['1014', 'Ryo Tanaka', 'attendee', 'ryo'], ['1015', 'Chloe Martin', 'attendee', 'chloe'], ['1016', 'Leo Duarte', 'attendee', 'leo'],
  ];
  const SCEN = {
    default: { n: 5, cams: { '1002': 'land', '1004': 'port', '1006': 'land' } },
    solo: { n: 0, cams: {} },
    duo: { n: 1, cams: { '1002': 'land' } },
    crowd: { n: 15, cams: { '1002': 'land', '1004': 'port', '1006': 'land', '1009': 'port', '1012': 'land' } },
    share: { n: 5, cams: { '1002': 'land', '1004': 'port', '1006': 'land' }, share: '1002' },
    phones: { n: 3, cams: { '1002': 'port', '1003': 'port', '1004': 'port' } },
    events: { n: 5, cams: { '1003': 'land' } },
  }[MODE] || { n: 5, cams: {} };

  class Room {
    constructor() {
      this.handlers = {}; this.state = 'disconnected'; this.canPlaybackAudio = true; this.remoteParticipants = new Map();
      const cfg = JSON.parse(document.getElementById('cfg').textContent);
      const me = new Participant(cfg.me.sub, cfg.me.name, cfg.me.role, cfg.me.picture);
      Object.assign(me, {
        isMicrophoneEnabled: false, isCameraEnabled: false, isScreenShareEnabled: false,
        setMicrophoneEnabled: async (on) => { me.isMicrophoneEnabled = on; me.remove(Source.Microphone);
          if (on) { const p = me.add(new Pub(Source.Microphone, new Track('audio', Source.Microphone))); this.emit(RoomEvent.LocalTrackPublished, p); } },
        setCameraEnabled: async (on) => { me.isCameraEnabled = on; me.remove(Source.Camera);
          if (on) { const p = me.add(new Pub(Source.Camera, new Track('video', Source.Camera, cameraStream(me.picture, false, 3)))); this.emit(RoomEvent.LocalTrackPublished, p); } },
        setScreenShareEnabled: async (on) => { me.isScreenShareEnabled = on; me.remove(Source.ScreenShare);
          if (on) { const p = me.add(new Pub(Source.ScreenShare, new Track('video', Source.ScreenShare, screenStream()))); this.emit(RoomEvent.LocalTrackPublished, p); }
          else this.emit(RoomEvent.LocalTrackUnpublished, new Pub(Source.ScreenShare, null)); },
        publishData: () => {},
      });
      this.localParticipant = me;
      const stats = { forEach: (fn) => fn({ type: 'candidate-pair', state: 'succeeded', currentRoundTripTime: 0.034 + Math.random() * 0.01 }) };
      this.engine = { pcManager: { subscriber: { pc: { getStats: async () => stats } } } };
      PEOPLE.slice(0, SCEN.n).forEach(([sub, name, role, av], i) => {
        const p = new Participant(sub, name, role, '/__img/' + av + '.webp');
        p.add(new Pub(Source.Microphone, new Track('audio', Source.Microphone)));
        p.getTrackPublication(Source.Microphone).isMuted = i % 3 === 2;
        const cam = SCEN.cams[sub];
        if (cam) p.add(new Pub(Source.Camera, new Track('video', Source.Camera, cameraStream(p.picture, cam === 'port', i))));
        this.remoteParticipants.set(sub, p);
      });
    }
    on(evt, fn) { (this.handlers[evt] = this.handlers[evt] || []).push(fn); return this; }
    emit(evt, ...a) { (this.handlers[evt] || []).forEach((fn) => { try { fn(...a); } catch (e) { console.error(e); } }); }
    async connect() {
      this.state = 'connected';
      setTimeout(() => this.emit(RoomEvent.ConnectionQualityChanged, 'excellent', this.localParticipant), 400);
      if (Q.get('me') === 'cam') setTimeout(() => this.localParticipant.setCameraEnabled(true).then(() => document.dispatchEvent(new Event('mock-cam'))), 300);
      this._life();
      return true;
    }
    _life() {
      const remotes = [...this.remoteParticipants.values()], enc = new TextEncoder();
      const data = (o, from) => this.emit(RoomEvent.DataReceived, enc.encode(JSON.stringify(o)), from, 0, o.type);
      if (SCEN.share) setTimeout(() => {
        const p = this.remoteParticipants.get(SCEN.share);
        p.add(new Pub(Source.ScreenShare, new Track('video', Source.ScreenShare, screenStream())));
        this.emit(RoomEvent.TrackSubscribed, p.getTrackPublication(Source.ScreenShare).track, p.getTrackPublication(Source.ScreenShare), p);
      }, 700);
      if (remotes.find((p) => p.identity === '1005')) setTimeout(() => data({ type: 'hand', sub: '1005', raised: true }), 1200);
      // voices: one or two people talk at a time, levels flicker like speech
      const talkers = remotes.filter((p) => !p.getTrackPublication(Source.Microphone).isMuted);
      let k = 0;
      const speak = () => {
        if (!talkers.length) return;
        const now = [talkers[k % talkers.length]]; if (k % 4 === 3 && talkers.length > 1) now.push(talkers[(k + 1) % talkers.length]);
        remotes.forEach((p) => { p._on = now.includes(p); });
        this.emit(RoomEvent.ActiveSpeakersChanged, now);
        k++;
      };
      if (Q.get('still') !== '1') { speak(); setInterval(speak, 3200); } else { speak(); }
      setInterval(() => { remotes.forEach((p) => { p.audioLevel = p._on ? 0.18 + Math.random() * 0.3 : 0; }); if (this.localParticipant.isMicrophoneEnabled) this.localParticipant.audioLevel = Math.random() * 0.2; }, 100);
      if (remotes.length > 1) {
        setTimeout(() => data({ type: 'reaction', e: '🎉' }, remotes[1]), 1800);
        setTimeout(() => data({ type: 'chat', id: 901, message: 'Sharing the funnel numbers in a sec', name: remotes[0].name, sub: remotes[0].identity,
          role: 'attendee', picture: remotes[0].picture, created_at: new Date().toISOString() }), 2400);
      }
    }
    async startAudio() {}
    async disconnect() { this.state = 'disconnected'; }
  }
  window.LivekitClient = { Room, RoomEvent, Track: { Source }, VideoPresets, AudioPresets };
})();
