# src/fix_bom.py
# Reads the file using utf-8-sig (which handles BOM) and writes it back as plain utf-8 (no BOM).
p = "logs/sample_logs.jsonl"
with open(p, "r", encoding="utf-8-sig") as f:
    data = f.read()
with open(p, "w", encoding="utf-8") as f:
    f.write(data)
print("Rewrote", p, "without BOM")
