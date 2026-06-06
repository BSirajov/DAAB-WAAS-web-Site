"""Append the main translate_profile_html function to _az_profile_translator.py."""
from pathlib import Path

fn = Path(__file__).parent / "_az_profile_translator.py"

code = '''

# ---------------------------------------------------------------------------
# 4. MAIN TRANSLATION FUNCTION
# ---------------------------------------------------------------------------

_ALL_PHRASES: list[tuple[str, str]] = (
    sorted(UNIQUE_TRANSLATIONS, key=lambda p: -len(p[0]))
    + sorted(UI_REPLACEMENTS, key=lambda p: -len(p[0]))
)


def translate_profile_html(html: str, name: str = "") -> str:
    """Translate a full Azerbaijani profile HTML page to English."""
    out = html

    # lang attribute
    out = out.replace(\'lang="az"\', \'lang="en"\')

    # phrase replacements (longest first)
    for az_phrase, en_phrase in _ALL_PHRASES:
        if az_phrase in out:
            out = out.replace(az_phrase, en_phrase)

    # template regex patterns
    for pattern, replacement in TEMPLATE_PATTERNS:
        if callable(replacement):
            out = pattern.sub(replacement, out)
        else:
            out = pattern.sub(str(replacement), out)

    # footer replacement
    if FOOTER_EN and \'class="footer-pro"\' in out:
        footer_start = out.find(\'<footer class="footer-pro">\')
        footer_end = out.find(\'</footer>\', footer_start)
        if footer_start != -1 and footer_end != -1:
            out = (
                out[:footer_start]
                + FOOTER_EN
                + out[footer_end + len("</footer>"):]
            )

    return out
'''

with fn.open("a", encoding="utf-8") as f:
    f.write(code)

print("Appended translate_profile_html to", fn.name)
