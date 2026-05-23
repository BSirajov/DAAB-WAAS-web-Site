from pathlib import Path
OUT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site\cv\eldar_veliyev.html")
PART = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site\helpers\eldar_veliyev_body.html")
OUT.write_text(PART.read_text(encoding="utf-8"), encoding="utf-8")
print("OK", OUT.stat().st_size)