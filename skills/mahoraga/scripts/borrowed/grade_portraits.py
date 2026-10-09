"""Generate the example Redditors' profile pictures for the showcase mocks (fictional people, example data)."""
import base64
import io
import os
import sys
from pathlib import Path

from google import genai
from PIL import Image

ENV = Path(os.environ.get('MAHORAGA_ENV', '.env'))  # a .env holding GEMINI_API_KEY; never print the key
for line in ENV.read_text(encoding='utf-8').splitlines():
    if line.startswith('GEMINI_API_KEY='):
        os.environ['GEMINI_API_KEY'] = line.split('=', 1)[1].strip().strip('"').strip("'")
OUT = Path(os.environ.get('PEOPLE_DIR', 'public/karma/people'))
OUT.mkdir(parents=True, exist_ok=True)

client = genai.Client()
ix = client.interactions
rc = ix.sdk_configuration.retry_config
rc.max_retries, rc.retry_connection_errors = 0, False

LOOK = (
    'Head and shoulders, face centred, looking at the camera with a relaxed, genuine expression. Shot on a phone at '
    'arm length, shallow depth of field, natural skin texture, no retouching. Cinematic grade: warm orange window '
    'light from the left, a soft violet glow from the right, a little haze in the background. Square crop.'
)
CAST = {
    'quiet_harbor': 'a woman in her late twenties, East Asian, shoulder length hair, oversized cream cardigan, at a tidy home desk',
    'dry_pine_88': 'a man in his thirties, South Asian, round glasses and a short beard, navy overshirt, bookshelves behind',
    'mild_brook': 'a woman in her mid twenties, Black, natural curly hair, small gold hoops, a bathroom shelf of skincare softly blurred behind',
    'calm_meadow': 'a man in his late twenties, Filipino, plain grey tee, a small balcony with plants behind',
    'steady_kiln': 'a man in his forties, white, sandy stubble, canvas work apron over a flannel shirt, a workshop pegboard with tools behind',
    'paper_lantern': 'a woman in her thirties, Latina, freckles, hair tied back, linen shirt, a kitchen with warm lights behind',
    'glass_orchard': 'a non binary person in their twenties, dyed lilac short hair, silver nose ring, black hoodie, a desk with a mechanical keyboard behind',
    'north_fern': 'a woman in her fifties, white, short grey hair, fleece jacket, a forest trail behind',
    'low_tide': 'a man in his thirties, Middle Eastern, sun tanned, light linen shirt, a beach at dusk behind',
    'amber_loom': 'a woman in her forties, South Asian, small nose stud, mustard knit jumper, a shelf of yarn behind',
    'maple_ledger': 'a young man in his twenties, mixed heritage, curly hair, denim jacket, a coffee shop behind',
    'rowan_offcut': 'a man in his late thirties, Black, short twists, wood shavings on a dark green work shirt, a joinery bench behind',
    'wren_ledger': 'a woman in her early thirties, white, auburn bob, thin gold glasses, oatmeal sweater, a sunny home office behind',
    'picked_bench': 'a woman in her twenties, Korean, long straight hair, a grey sweatshirt, a small apartment with plants behind',
    'passed_bench': 'a man in his fifties, Indian, salt and pepper beard, a checked shirt, a garden shed behind',
    'barred_bench': 'a man in his twenties, white, buzz cut, black tee, a skate park at golden hour behind',
    'waiting_bench': 'a woman in her forties, Nigerian, colourful head wrap, a denim shirt, a market street behind',
}

only = set(sys.argv[1:])
for handle, who in CAST.items():
    if only and handle not in only:
        continue
    dest = OUT / f'{handle}.jpg'
    if dest.exists():
        print('skip', handle)
        continue
    prompt = f'A natural profile photo someone would use as their Reddit avatar: {who}. {LOOK}'
    try:
        it = ix.create(
            model='gemini-3.1-flash-image',
            input=prompt,
            response_format={'type': 'image', 'aspect_ratio': '1:1', 'image_size': '512'},
            timeout=180,
        )
        im = Image.open(io.BytesIO(base64.b64decode(it.output_image.data))).convert('RGB').resize((256, 256), Image.LANCZOS)
        im.save(dest, quality=84, optimize=True, progressive=True)
        print('ok', handle, dest.stat().st_size)
    except Exception as e:  # keep going; a missing face falls back to a letter
        print('fail', handle, str(e)[:160])
