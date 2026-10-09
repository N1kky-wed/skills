"""Find a company's films and media: video sources in their pages' HTML, plus every video on their Vimeo account,
with titles, lengths and posters.

    python find_media.py --site https://example.com --paths / /product /about
    python find_media.py --vimeo-user carenexthealth --posters public/video
    python find_media.py --vimeo-ids 569912638 639698564 --posters public/video

A Vimeo user page lists ids in its links (open it in the browser pane: vimeo.com/<user>); oEmbed gives title,
duration, description and thumbnail without an API key. Self-hosted .mp4 files are worth downloading (with the
user's go-ahead) and re-encoding with video_web.py: their own servers are often too slow to stream from.
"""
import argparse, io, json, os, re, urllib.request


def get(url, timeout=40):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def oembed(vid):
    d = json.loads(get(f'https://vimeo.com/api/oembed.json?url=https://vimeo.com/{vid}&width=1280'))
    return {k: d.get(k) for k in ('title', 'duration', 'description', 'thumbnail_url', 'width', 'height')}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--site')
    ap.add_argument('--paths', nargs='*', default=['/'])
    ap.add_argument('--vimeo-user')
    ap.add_argument('--vimeo-ids', nargs='*', default=[])
    ap.add_argument('--posters', help='folder to save <slug>-poster.webp files')
    a = ap.parse_args()

    found = {}
    if a.site:
        pat = re.compile(r"""(https?:)?//[^"' )]*(youtube\.com/[^"' )]*|youtu\.be/[^"' )]*|vimeo\.com/[^"' )]*|\.mp4[^"' )]*|\.webm[^"' )]*)""", re.I)
        for p in a.paths:
            url = a.site.rstrip('/') + '/' + p.lstrip('/')
            try:
                html = get(url).decode('utf-8', 'ignore')
            except Exception as e:
                print('fail', url, str(e)[:80]); continue
            for m in set(x.group(0) for x in pat.finditer(html)):
                found.setdefault(m.replace('&amp;', '&'), []).append(p)
        for src, pages in found.items():
            print('media', src, '<-', ', '.join(pages))
            m = re.search(r'vimeo\.com/(?:video/)?(\d+)', src)
            if m and m.group(1) not in a.vimeo_ids:
                a.vimeo_ids.append(m.group(1))

    if a.vimeo_user:
        html = get(f'https://vimeo.com/{a.vimeo_user}').decode('utf-8', 'ignore')
        for vid in re.findall(r'vimeo\.com/(\d{6,})', html):
            if vid not in a.vimeo_ids:
                a.vimeo_ids.append(vid)
        print(f'vimeo user {a.vimeo_user}: {len(a.vimeo_ids)} ids (if few, open the page in the browser pane and read the links)')

    for vid in a.vimeo_ids:
        try:
            d = oembed(vid)
        except Exception as e:
            print('vimeo', vid, 'not public?', str(e)[:60]); continue
        mins = f"{(d['duration'] or 0) // 60}:{(d['duration'] or 0) % 60:02d}"
        print(f"vimeo {vid}  {d['title']}  {mins}  {(d['description'] or '')[:120]}")
        if a.posters and d.get('thumbnail_url'):
            from PIL import Image
            os.makedirs(a.posters, exist_ok=True)
            slug = re.sub(r'[^a-z0-9]+', '-', (d['title'] or vid).lower()).strip('-')
            im = Image.open(io.BytesIO(get(d['thumbnail_url']))).convert('RGB')
            out = os.path.join(a.posters, f'{slug}-poster.webp')
            im.save(out, 'WEBP', quality=84)
            print('   poster', out, im.size)


if __name__ == '__main__':
    main()
