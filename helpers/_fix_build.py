from pathlib import Path
import re

p = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site\helpers\_build_batch_cvs.py")
t = p.read_text(encoding="utf-8")
t = t.replace('\\"', "'")
t = re.sub(
    r"f'(<div class=\"callout\">)\{bib\(",
    r"'<div class=\"callout\">' + bib(",
    t,
)
t = re.sub(r"\)\}</div>'\)", r") + '</div>')", t)
t = re.sub(r"\)\}</div>',", r") + '</div>',", t)
p.write_text(t, encoding="utf-8")
print("fixed", p)
