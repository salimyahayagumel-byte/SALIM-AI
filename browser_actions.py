"""SALIM AI: bilingual direct app, website and search commands for Termux."""
import re
import shutil
import subprocess
import urllib.parse
import webbrowser

SITES = {
    "youtube": "https://www.youtube.com", "facebook": "https://www.facebook.com",
    "twitter": "https://x.com", "x": "https://x.com", "wikipedia": "https://www.wikipedia.org",
    "google": "https://www.google.com", "gmail": "https://mail.google.com",
    "instagram": "https://www.instagram.com", "tiktok": "https://www.tiktok.com",
    "github": "https://github.com", "whatsapp": "https://www.whatsapp.com",
    "telegram": "https://telegram.org", "reddit": "https://www.reddit.com",
}
# Android package names. Actual app launch is attempted first; missing apps fall back to a website.
APPS = {
    "facebook": ("com.facebook.katana", SITES["facebook"]),
    "whatsapp": ("com.whatsapp", SITES["whatsapp"]),
    "youtube": ("com.google.android.youtube", SITES["youtube"]),
    "instagram": ("com.instagram.android", SITES["instagram"]),
    "tiktok": ("com.zhiliaoapp.musically", SITES["tiktok"]),
    "telegram": ("org.telegram.messenger", SITES["telegram"]),
    "gmail": ("com.google.android.gm", SITES["gmail"]),
    "chrome": ("com.android.chrome", "https://www.google.com"),
    "settings": ("com.android.settings", None),
    "play store": ("com.android.vending", "https://play.google.com/store"),
    "google maps": ("com.google.android.apps.maps", "https://maps.google.com"),
    "maps": ("com.google.android.apps.maps", "https://maps.google.com"),
    "phone": ("com.google.android.dialer", None),
    "camera": ("com.android.camera2", None),
}

def _open_url(url):
    try:
        if shutil.which("termux-open-url"):
            subprocess.Popen(["termux-open-url", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True, f"Na aika hanyar buɗewa a wayarka: {url}"
        if webbrowser.open(url):
            return True, f"Na buɗe: {url}"
        return False, f"Ban iya buɗe shi kai tsaye ba. Ga hanyar: {url}"
    except Exception:
        return False, f"Ban iya buɗe shi kai tsaye ba. Ga hanyar: {url}"

def _launch_app(name):
    package, fallback = APPS[name]
    # monkey is available on Android/Termux and launches the installed package.
    if shutil.which("monkey"):
        try:
            result = subprocess.run(["monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=8)
            output = result.stdout.lower()
            if result.returncode == 0 and "no activities found" not in output and "monkey aborted" not in output:
                return True, f"Na aika buɗe app ɗin {name.title()}."
        except Exception:
            pass
    if fallback:
        ok, msg = _open_url(fallback)
        if ok:
            return True, f"Ban samu damar buɗe app ɗin {name.title()} kai tsaye ba; na buɗe shafinsa maimakon haka: {fallback}"
        return True, msg
    return True, f"Ban iya buɗe {name.title()} kai tsaye ba. Tabbatar cewa app ɗin yana wayarka kuma an ba Termux izinin buɗewa."

def _clean(text):
    text = text.strip()
    text = re.sub(r"^[\s,.:;!-]*(?:salim(?:\s+ai)?[\s,:-]*)+", "", text, flags=re.I)
    # Remove common Hausa/English politeness and command fillers.
    text = re.sub(r"^(?:don Allah|dan Allah|please|kindly)\s+", "", text, flags=re.I)
    return text.strip(" \t,.:;!")

def handle_command(text):
    """Return (handled, message). Handles common English and Hausa commands offline."""
    original = _clean(text)
    s = original.lower()
    if not s:
        return True, "Ina sauraro. Ka faɗi ko ka rubuta umarninka."

    # Search patterns: Hausa and English.
    patterns = [
        r"^(?:search\s+(youtube|google|wikipedia)\s+(?:for\s+)?)(.+)$",
        r"^(?:bincika|nemo|yi bincike(?:\s+kan)?)\s+(?:a\s+)?(youtube|google|wikipedia)\s+(?:don\s+)?(.+)$",
    ]
    m = re.match(patterns[0], original, re.I)
    if m:
        site, query = m.group(1).lower(), m.group(2).strip()
    else:
        m = re.match(patterns[1], original, re.I)
        if m:
            site, query = m.group(1).lower(), m.group(2).strip()
        else:
            site, query = None, None
    if site and query:
        base = {"youtube": "https://www.youtube.com/results?search_query=", "wikipedia": "https://en.wikipedia.org/w/index.php?search=", "google": "https://www.google.com/search?q="}[site]
        return True, _open_url(base + urllib.parse.quote_plus(query))[1]

    m = re.match(r"^(?:search\s+(?:for\s+)?|find\s+|look\s+up\s+|bincika\s+|nemo\s+|yi bincike\s+(?:kan\s+)?)(.+)$", original, re.I)
    if m:
        query = m.group(1).strip()
        return True, _open_url("https://www.google.com/search?q=" + urllib.parse.quote_plus(query))[1]

    # Normalize phrases into an action + target. Includes common Hausa variants.
    command = re.sub(r"^(?:open|launch|start|run|visit|go to|buɗe|bude|buɗemin|bude min|buɗe min|buɗa|shiga|je|kai ni zuwa|ka buɗe|ka bude|ina so in buɗe|ina so in bude)\s+", "", original, flags=re.I).strip().lower()
    command = re.sub(r"^(?:min|mini|mani|my|the|app(?:\s+din)?|application(?:\s+din)?|manhajar|manhaja(?:r)?|shafin|shafi(?:n)?|din|ɗin)\s+", "", command, flags=re.I).strip()
    command = re.sub(r"\s+(?:please|now|yanzu|don Allah)$", "", command, flags=re.I).strip()
    # Common synonyms / spoken phrasing.
    aliases = {
        "face book": "facebook", "what's app": "whatsapp", "whats app": "whatsapp",
        "you tube": "youtube", "tik tok": "tiktok", "insta": "instagram",
        "play store": "play store", "google map": "google maps", "settings app": "settings",
        "saituna": "settings", "wasiku": "gmail", "wasikar gmail": "gmail",
    }
    command = aliases.get(command, command)
    if command in APPS:
        return _launch_app(command)
    if command in SITES:
        return True, _open_url(SITES[command])[1]

    # Match an app name inside a longer phrase, e.g. "je min Facebook".
    for name in sorted(set(APPS) | set(SITES), key=len, reverse=True):
        if re.search(r"\b" + re.escape(name) + r"\b", s):
            # Only treat as opening when an action word is present.
            if re.search(r"\b(open|launch|start|run|buɗe|bude|shiga|je|kai ni|manhajar|app din|app ɗin)\b", s):
                return _launch_app(name) if name in APPS else (True, _open_url(SITES[name])[1])

    if s in ("help", "commands", "taimaka", "umarnai", "yaya ake amfani da kai"):
        return True, (
            "Misalan umarni (Hausa da Turanci):\n"
            "• SALIM, buɗe min WhatsApp\n• open Facebook\n• je YouTube\n"
            "• buɗe Settings / bude saituna\n• bincika labaran Najeriya\n"
            "• search YouTube for Hausa comedy\n• voice — umarnin murya\n• exit — fita"
        )
    return False, ""
