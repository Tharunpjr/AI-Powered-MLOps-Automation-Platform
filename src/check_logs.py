# src/check_logs.py
import json
p = 'logs/sample_logs.jsonl'
with open(p, 'r', encoding='utf-8') as f:
    for i, l in enumerate(f, 1):
        s = l.rstrip('\n')
        if not s.strip():
            print(f"BLANK line {i}")
            continue
        try:
            json.loads(s)
            print(f"OK   line {i}")
        except Exception as e:
            print(f"BAD  line {i} -> {e}")
