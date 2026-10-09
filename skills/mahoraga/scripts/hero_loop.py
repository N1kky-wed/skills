"""Encode the hero loop for the web from one 4K Veo take that returns to its first frame.

    python hero_loop.py OUT_DIR TAKE.mp4 [--name hero] [--slow 2] [--speed 4]

The take is cut at the tail frame that best matches its first frame, so the loop needs no crossfade. --slow 2
doubles its length with motion-compensated interpolation at 24fps: every other frame is one Veo rendered, and
the step across the seam is interpolated like any other (frames past the seam are kept as targets, then
dropped). Interpolation runs at each output's own size, landscape 2560x1440 and a portrait 1080x1920 cut of
the frame's centre, into near-lossless masters; every web file is encoded from a master.

Needs an ffmpeg with libaom-av1, libx264 and libwebp: the one on PATH, else the imageio-ffmpeg binary.

Outputs (muted, BT.709 tagged, +faststart so playback starts before the download ends):
    <name>-1440.av1.mp4    2560x1440 AV1 10-bit (10-bit keeps the sky gradient from banding)
    <name>-1080.h264.mp4   1920x1080 H.264 High 4.1, where AV1 does not decode
    <name>-phone.av1.mp4   1080x1920 AV1 10-bit, the centre of the frame, which is what a phone hero shows
    <name>-phone.h264.mp4  720x1280 H.264 High 3.1, the same cut
    <name>-poster.webp     1920x1080, the loop's first frame, converted as a browser shows the video
"""
import argparse
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor


def find_ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        sys.exit("ffmpeg not found: install it (brew/apt/winget install ffmpeg) or pip install imageio-ffmpeg")


FF = find_ffmpeg()
# On the frames, not as encoder options: those wrote the matrix alone, and with primaries and transfer unknown
# Chromium decoded the loop as BT.601, a visible shift from the poster under it.
TAG = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"


def small_frames(path, w=96, h=54):
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                         check=True, capture_output=True).stdout
    n = w * h
    return [raw[i:i + n] for i in range(0, len(raw), n)]


def diff(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def run(args):
    print("  writing", os.path.basename(args[-1]), flush=True)
    subprocess.run([FF, "-v", "error", "-y", *args], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("take")
    ap.add_argument("--name", default="hero")
    ap.add_argument("--slow", type=int, default=2)
    ap.add_argument("--speed", type=int, default=4, help="libaom cpu-used: 3 is slower and a little better")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    j = lambda f: os.path.join(a.out, f)  # noqa: E731

    fr = small_frames(a.take)
    seam = min(range(len(fr) - 24, len(fr)), key=lambda i: diff(fr[0], fr[i]))
    step = sum(diff(fr[i], fr[i + 1]) for i in range(len(fr) - 1)) / (len(fr) - 1)
    print(f"seam at frame {seam} of {len(fr)}: diff {diff(fr[0], fr[seam]):.2f} vs mean step {step:.2f}")
    if diff(fr[0], fr[seam]) > max(1.5 * step, 2):
        sys.exit("no clean seam in the tail; pick another take")
    frames = seam * a.slow
    print(f"loop: {frames} frames, {frames / 24:.2f}s at 24fps")

    slow = (f",setpts={a.slow}*PTS,minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:scd=none"
            if a.slow > 1 else "")

    def master(geometry, out):
        # two frames past the seam: the interpolator emits nothing for the last gap it is given
        run(["-i", a.take, "-vf", f"trim=end_frame={seam + 2},setpts=PTS-STARTPTS,{geometry}{slow}", "-frames:v",
             str(frames), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "4", "-pix_fmt", "yuv420p", out])

    land, tall = j(f"{a.name}-master-land.mp4"), j(f"{a.name}-master-tall.mp4")
    with ThreadPoolExecutor(2) as ex:
        list(ex.map(lambda g: master(*g), [("scale=2560:1440:flags=lanczos", land),
                                            ("crop=trunc(ih*9/16/2)*2:ih,scale=1080:1920:flags=lanczos", tall)]))

    def av1(src, vf, crf, out):
        run(["-i", src, "-vf", f"{vf},{TAG}", "-an", "-c:v", "libaom-av1", "-crf", str(crf), "-b:v", "0", "-cpu-used",
             str(a.speed), "-row-mt", "1", "-tiles", "2x2", "-pix_fmt", "yuv420p10le", "-movflags", "+faststart", j(out)])

    def h264(src, vf, crf, level, out):
        # an explicit level and four references, or x264 labels the stream 6.2 and old decoders refuse it
        run(["-i", src, "-vf", f"{vf},{TAG}", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-profile:v",
             "high", "-level:v", level, "-refs", "4", "-pix_fmt", "yuv420p", "-x264-params", "aq-mode=3", "-movflags",
             "+faststart", j(out)])

    jobs = [
        lambda: av1(land, "null", 30, f"{a.name}-1440.av1.mp4"),
        lambda: h264(land, "scale=1920:1080:flags=lanczos", 22, "4.1", f"{a.name}-1080.h264.mp4"),
        lambda: av1(tall, "null", 32, f"{a.name}-phone.av1.mp4"),
        lambda: h264(tall, "scale=720:1280:flags=lanczos", 23, "3.1", f"{a.name}-phone.h264.mp4"),
        lambda: run(["-i", land, "-frames:v", "1", "-vf",
                     "scale=1920:1080:flags=lanczos:in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24",
                     "-c:v", "libwebp", "-quality", "82", j(f"{a.name}-poster.webp")]),
    ]
    with ThreadPoolExecutor(len(jobs)) as ex:
        for f in [ex.submit(job) for job in jobs]:
            f.result()
    for f in sorted(os.listdir(a.out)):
        if f.startswith(a.name) and "master" not in f:
            print(f"{f:26s} {os.path.getsize(j(f)) / 1e6:6.2f} MB")


if __name__ == "__main__":
    main()
