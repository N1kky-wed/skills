"""Turn a client's film (or a generated clip) into web-ready pieces with ffmpeg.

    python video_web.py probe  film.mp4
    python video_web.py film   film.mp4 public/video/launch.mp4             # H.264 CRF 26, AAC 128k, faststart
    python video_web.py loop   film.mp4 public/video/loop.mp4 --start 47.5 --dur 7 --crop-bottom 0.18
    python video_web.py poster film.mp4 public/video/poster.webp --at 50 --crop-bottom 0.18
    python video_web.py stills film.mp4 public/img --at 51.5 80 86.5 --names nurse patient ward --crop-bottom 0.16
    python video_web.py silk   veo.mp4  public/video/silk.mp4 --crop-edges 4             # slow, seamless, quiet
    python video_web.py silk   veo.mp4  public/video/silk-rose.mp4 --tint 24             # tint baked in
    python video_web.py silk   veo.mp4  public/video/silk-night.mp4 --night              # night twin of the day file

--crop-bottom removes a burned-in lower third (logos, captions) so your own title can sit on the frame. A muted loop
(5-8 s, 1280 wide, no audio) is what plays on a card; the full film only loads when someone opens it.
silk is the background-footage recipe from 8x.tweets and 8x Meets: crop black edge rows, slow 2x with motion
interpolation, crossfade the tail into the head so it loops without a seam, optionally bake a hue turn or the night
grade (never a CSS filter on playing video), then denoise and encode so gradients don't band. Run it again with
--width 1280 for the phone source, and `poster` on the result for the still under it.
Uses ffmpeg from PATH, else the imageio-ffmpeg binary.
"""
import argparse, os, shutil, subprocess, sys


def ffmpeg():
    exe = shutil.which('ffmpeg')
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        sys.exit('ffmpeg not found (pip install imageio-ffmpeg)')


def run(args):
    print(' '.join(args[1:6]), '...')
    subprocess.run(args, check=True)


def crop_filter(frac):
    return f'crop=iw:trunc(ih*{1 - frac:.3f}/2)*2:0:0' if frac else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['probe', 'film', 'loop', 'poster', 'stills', 'silk'])
    ap.add_argument('src')
    ap.add_argument('out', nargs='?')
    ap.add_argument('--start', type=float, default=0)
    ap.add_argument('--dur', type=float, default=7)
    ap.add_argument('--at', type=float, nargs='*', default=[0])
    ap.add_argument('--names', nargs='*')
    ap.add_argument('--crop-bottom', type=float, default=0)
    ap.add_argument('--width', type=int, help='output width (loop: 1280; silk: the source width)')
    ap.add_argument('--crf', type=int, default=26)
    ap.add_argument('--vf', help='extra ffmpeg filters for film/loop/poster/stills, e.g. a baked grade: "hue=s=0,eq=contrast=1.08"')
    ap.add_argument('--slow', type=float, default=2, help='silk: slow-down factor')
    ap.add_argument('--fade', type=float, default=1.5, help='silk: loop crossfade seconds')
    ap.add_argument('--crop-edges', type=int, default=0, help='silk: rows to cut top and bottom (Veo black lines)')
    ap.add_argument('--tint', type=float, default=0, help='silk: hue turn in degrees (24 = toward rose)')
    ap.add_argument('--night', action='store_true', help='silk: invert lightness, keep hue (the night twin)')
    a = ap.parse_args()
    ff = ffmpeg()

    if a.cmd == 'silk':
        import av
        c = av.open(a.src)
        length = c.duration / 1e6 * a.slow
        c.close()
        f = a.fade
        pre = [f'crop=iw:ih-{2 * a.crop_edges}:0:{a.crop_edges}' if a.crop_edges else None,
               f'setpts={a.slow}*PTS', 'minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1']
        grade = [f'hue=h={a.tint}:s=1.06' if a.tint else None,
                 'negate,hue=h=180:s=1.15,eq=gamma=0.85:contrast=1.08' if a.night else None,
                 f'scale={a.width}:-2' if a.width else None, 'hqdn3d=1.5:1.5:4:4', 'format=yuv420p']
        graph = (f"[0:v]{','.join(x for x in pre if x)},split[a][b];"
                 f"[a]trim=start={f},setpts=PTS-STARTPTS,fps=30[body];[b]trim=end={f},setpts=PTS-STARTPTS,fps=30[head];"
                 f"[body][head]xfade=transition=fade:duration={f}:offset={length - 2 * f:.3f},{','.join(x for x in grade if x)}[out]")
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        run([ff, '-v', 'error', '-y', '-i', a.src, '-filter_complex', graph, '-map', '[out]', '-an', '-c:v', 'libx264',
             '-preset', 'slow', '-crf', '23', '-x264-params', 'aq-mode=3', '-movflags', '+faststart', a.out])
        print('ok', a.out, f'{length - f:.1f}s', f'{os.path.getsize(a.out) / 1e6:.1f} MB')
        return

    if a.cmd == 'probe':
        import av
        c = av.open(a.src)
        v = c.streams.video[0]
        au = c.streams.audio[0] if c.streams.audio else None
        print(f'duration {c.duration / 1e6:.1f}s  video {v.codec_context.name} {v.width}x{v.height} {v.average_rate}fps  audio {au.codec_context.name if au else None}')
        print(f'size {os.path.getsize(a.src) / 1e6:.1f} MB')
        return

    os.makedirs(os.path.dirname(os.path.abspath(a.out)) if a.cmd != 'stills' else a.out, exist_ok=True)
    crop = ','.join(f for f in [crop_filter(a.crop_bottom), a.vf] if f) or None

    if a.cmd == 'film':
        vf = ['-vf', crop] if crop else []
        run([ff, '-v', 'error', '-y', '-i', a.src, *vf, '-c:v', 'libx264', '-preset', 'slow', '-crf', str(a.crf), '-profile:v', 'high',
             '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', a.out])
    elif a.cmd == 'loop':
        vf = ','.join(f for f in [crop, f'scale={a.width or 1280}:-2', 'fps=25'] if f)
        run([ff, '-v', 'error', '-y', '-ss', str(a.start), '-t', str(a.dur), '-i', a.src, '-an', '-vf', vf, '-c:v', 'libx264', '-preset', 'slow',
             '-crf', str(a.crf + 1), '-pix_fmt', 'yuv420p', '-movflags', '+faststart', a.out])
    elif a.cmd in ('poster', 'stills'):
        from PIL import Image
        names = a.names or [f'still-{i}' for i in range(len(a.at))]
        for t, name in zip(a.at, names):
            tmp = os.path.join(os.path.dirname(os.path.abspath(a.out if a.cmd == 'poster' else os.path.join(a.out, 'x'))), f'_frame_{name}.png')
            vf = ['-vf', crop] if crop else []
            run([ff, '-v', 'error', '-y', '-ss', str(t), '-i', a.src, '-frames:v', '1', *vf, tmp])
            im = Image.open(tmp).convert('RGB')
            dest = a.out if a.cmd == 'poster' else os.path.join(a.out, f'{name}.webp')
            im.save(dest, 'WEBP', quality=82)
            os.remove(tmp)
            print('ok', dest, im.size)
    if a.cmd in ('film', 'loop'):
        print('ok', a.out, f'{os.path.getsize(a.out) / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
