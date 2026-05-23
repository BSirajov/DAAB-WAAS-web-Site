from pathlib import Path

p = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site\helpers\_build_batch_cvs.py")
t = p.read_text(encoding="utf-8")
t = t.replace('")}</div>\'', '") + \'</div>\'')
p.write_text(t, encoding="utf-8")
print("fixed closing tags")
