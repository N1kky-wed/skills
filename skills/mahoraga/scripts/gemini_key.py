"""Find the Gemini API key for the scripts that generate images or video, and explain how to set one when it is missing.

    python gemini_key.py                    # is a key available? says where it came from, never prints it
    python gemini_key.py --env path/to/.env

A Gemini API key is REQUIRED for gemini_image.py and for the borrowed gen_*.py / grade_portraits.py scripts (and for
any Veo or Omni video you generate). Nothing else in this skill needs one. Get a key at
https://aistudio.google.com/apikey (generation is billed per call to the key's Google project).

Where the key is looked for, first match wins:
    1. GEMINI_API_KEY in the environment
    2. a GEMINI_API_KEY=... line in the .env file named by --env (gemini_image.py) or $MAHORAGA_ENV
    3. a GEMINI_API_KEY=... line in ./.env (the folder you run the script from)
"""
import os
import sys

NAME = 'GEMINI_API_KEY'
KEY_URL = 'https://aistudio.google.com/apikey'


def _from_file(path):
    with open(path, encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line.startswith('export '):
                line = line[len('export '):].lstrip()
            if line.startswith(NAME + '='):
                value = line.split('=', 1)[1].strip().strip('"').strip("'")
                if value:
                    return value
    return None


def find_key(env_file=None):
    """(key, where it came from), or (None, the places looked)."""
    if os.environ.get(NAME, '').strip():
        return os.environ[NAME].strip(), 'the environment'
    named = [p for p in (env_file, os.environ.get('MAHORAGA_ENV')) if p]
    looked = ['the environment']
    for path in named + ['.env']:
        path = os.path.abspath(os.path.expanduser(path))
        if path in looked:
            continue
        looked.append(path)
        if os.path.isfile(path):
            key = _from_file(path)
            if key:
                return key, path
    return None, looked


def missing_message(looked, script=None):
    who = f'{script} calls' if script else 'The image and video scripts call'
    return f"""
{NAME} is required: {who} the Gemini API to generate images or video, and no key was found.
Looked in: {', '.join(looked)}

1. Get a key at {KEY_URL}
2. Then do ONE of these:
   - set it for this shell (it lasts until the shell closes):
       macOS / Linux:        export {NAME}="your-key"
       Windows PowerShell:   $env:{NAME}="your-key"
       Windows cmd:          set {NAME}=your-key
   - or put the line  {NAME}=your-key  in a .env file in the folder you run from,
     or anywhere else and point MAHORAGA_ENV at it (gemini_image.py also takes --env path/to/.env).
Never commit the key; the scripts never print it.
"""


def refused(error):
    """Setup advice when an API error means the key itself was refused, else None."""
    text = str(error)
    if any(s in text for s in ('API_KEY_INVALID', 'API key not valid', 'PERMISSION_DENIED', 'API_KEY_SERVICE_BLOCKED')):
        return (f'The Gemini API refused {NAME}: {text[:200]}\n'
                f'Check the key (or make a new one) at {KEY_URL}; some image and video models also need billing turned '
                'on for the key\'s Google project.')
    return None


def load_key(env_file=None, script=None):
    """The key, also exported as GEMINI_API_KEY for the SDK; exits with setup instructions when there is none."""
    key, where = find_key(env_file)
    if not key:
        sys.exit(missing_message(where, script or os.path.basename(sys.argv[0]) or None))
    os.environ[NAME] = key
    return key


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Check that a Gemini API key is available (the key itself is never printed).')
    ap.add_argument('--env', help='a .env file holding GEMINI_API_KEY=...')
    a = ap.parse_args()
    key, where = find_key(a.env)
    if not key:
        sys.exit(missing_message(where))
    print(f'{NAME} found in {where} ({len(key)} characters). Image and video generation can run.')
