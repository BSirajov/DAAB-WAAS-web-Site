# -*- coding: utf-8 -*-
import json
from pathlib import Path

p = Path(__file__).with_name("_cv_az_batch1_en.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = Path(__file__).with_name("_cv_az_batch1_split")
out.mkdir(exist_ok=True)
for i, x in enumerate(d):
    (out / f"{i:02d}_{x['base']}.json").write_text(
        json.dumps(x, ensure_ascii=False, indent=2), encoding="utf-8"
    )
print("wrote", len(d), "files to", out)
