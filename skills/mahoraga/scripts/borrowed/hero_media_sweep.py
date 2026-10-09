"""Hero video masters and a quality sweep. Masters: the Veo take made seamless (drop the first 0.5s, crossfade the tail
in), Veo's letterbox cropped, 1920x1080, light denoise, all in 10-bit so gradients stay smooth; stored lossless (FFV1).
Sweep: encode the careers master at a few quality levels per codec and score each against the master (SSIM) and size.
usage: python hero_media_sweep.py masters | sweep
Works in WORK_DIR (default: the folder you run from), which holds the Veo takes named in SRC."""
import concurrent.futures as cf
import os, pathlib, re, subprocess, sys
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
H = pathlib.Path(os.environ.get('WORK_DIR', '.'))
SRC = {'careers': 'careers-orb-loop2.mp4', 'playmakers': 'pm-sphere-loop5.mp4'}
F, L = 0.5, 8.0


def run(*args):
	subprocess.run([FF, '-v', 'error', '-y', *args], check=True)


def master(name):
	out = H / f'master-{name}.mkv'
	graph = (
		f'[0:v]trim={F}:{L},setpts=PTS-STARTPTS,fps=24,format=yuv420p10le[body];'
		f'[0:v]trim=0:{F},setpts=PTS-STARTPTS,fps=24,format=yuv420p10le[head];'
		f'[body][head]xfade=transition=fade:duration={F}:offset={L - 2 * F:.3f},'
		'crop=iw-36:ih-20:18:10,scale=1920:1080:flags=lanczos,hqdn3d=1:1:3:3,format=yuv420p10le[out]'
	)
	run('-i', str(H / SRC[name]), '-filter_complex', graph, '-map', '[out]', '-an', '-c:v', 'ffv1', '-level', '3', str(out))
	return out


def args(codec, crf):
	if codec == 'av1':
		return ['-c:v', 'libaom-av1', '-crf', str(crf), '-b:v', '0', '-cpu-used', '3', '-row-mt', '1', '-tiles', '2x2', '-pix_fmt', 'yuv420p10le', '-g', '192', '-keyint_min', '192']
	if codec == 'hevc':
		return ['-c:v', 'libx265', '-preset', 'slow', '-crf', str(crf), '-pix_fmt', 'yuv420p10le', '-tag:v', 'hvc1', '-x265-params', 'aq-mode=3:keyint=192:min-keyint=192:no-open-gop=1:log-level=error']
	return ['-c:v', 'libx264', '-preset', 'slower', '-crf', str(crf), '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-x264-params', 'aq-mode=3:keyint=192:min-keyint=192']


def ssim(enc, ref):
	r = subprocess.run([FF, '-v', 'info', '-i', str(enc), '-i', str(ref), '-lavfi', '[0:v]format=yuv420p10le[a];[1:v]format=yuv420p10le[b];[a][b]ssim', '-f', 'null', '-'], capture_output=True, text=True)
	m = re.search(r'All:([\d.]+)', r.stderr)
	return float(m.group(1)) if m else -1


def trial(item):
	codec, crf = item
	out = H / 'sweep' / f'careers-{codec}-{crf}.mp4'
	run('-i', str(H / 'master-careers.mkv'), '-an', *args(codec, crf), '-movflags', '+faststart', str(out))
	return codec, crf, out.stat().st_size / 1e6, ssim(out, H / 'master-careers.mkv')


if __name__ == '__main__':
	if sys.argv[1] == 'masters':
		with cf.ThreadPoolExecutor(2) as ex:
			for out in ex.map(master, SRC):
				print('master', out.name, f'{out.stat().st_size / 1e6:.0f} MB')
	else:
		(H / 'sweep').mkdir(exist_ok=True)
		grid = [('av1', c) for c in (26, 30, 34)] + [('hevc', c) for c in (20, 23, 26)] + [('h264', c) for c in (17, 20, 23)]
		with cf.ThreadPoolExecutor(4) as ex:
			for codec, crf, mb, s in sorted(ex.map(trial, grid)):
				print(f'{codec:5} crf {crf}: {mb:5.2f} MB  {mb * 8 / 7.5:4.2f} Mbps  SSIM {s:.5f}')
