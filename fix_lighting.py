"""修复 lighting.json 中的控制字符问题，并验证所有 part 文件 JSON 合法性。"""
import json
from pathlib import Path

PARTS_DIR = Path(r"C:\Users\Administrator\WorkBuddy\2026-07-19-19-08-08\parts")

# 1. 修复 lighting.json：把 ``` 后的原始换行 + 孤立 'n' 还原为转义 \n
lighting = PARTS_DIR / "questions_lighting.json"
raw = lighting.read_text(encoding="utf-8")
# 坏序列：三个反引号 + 真实换行 + 字母n + 空格 + spec_ambient
bad = "```\nn     spec_ambient"
good = "```\\n     spec_ambient"  # 字面 \n（反斜杠+n）
if bad in raw:
    raw = raw.replace(bad, good)
    lighting.write_text(raw, encoding="utf-8")
    print(f"[FIX] lighting.json: 修复控制字符")
else:
    print(f"[INFO] lighting.json: 未发现坏序列（可能已修复）")

# 2. 验证所有 part 文件
print("\n--- 验证所有 part 文件 ---")
for f in sorted(PARTS_DIR.glob("*.json")):
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        if isinstance(d, dict):
            qs = d.get("questions", [])
            cat = d.get("category", "?")
            print(f"  [OK] {f.name}: dict, category={cat}, {len(qs)} 题")
        elif isinstance(d, list):
            print(f"  [OK] {f.name}: list, {len(d)} 题")
        else:
            print(f"  [WARN] {f.name}: 未知结构 {type(d)}")
    except json.JSONDecodeError as e:
        print(f"  [ERR] {f.name}: {e}")
