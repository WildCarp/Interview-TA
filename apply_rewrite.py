"""
通用重写应用脚本：读取 rewrite_data/*.json，按 id 匹配并替换 parts/questions_*.json 里的题目。
重写数据 JSON 格式：{ "题号": {"question": "...", "answer": "...", "tags": [...]} }
"""
import json
from pathlib import Path

BASE = Path(r"C:\Users\Administrator\WorkBuddy\2026-07-19-19-08-08")
PARTS_DIR = BASE / "parts"
DATA_DIR = BASE / "rewrite_data"

# 分类 → part 文件映射
CAT_TO_FILE = {
    "shader": "questions_shader.json",
    "rendering": "questions_rendering.json",
    "ui": "questions_ui.json",
    "vfx": "questions_vfx.json",
    "optimization": "questions_optimization.json",
    "pipeline": "questions_pipeline.json",
    "texture": "questions_texture.json",
    "lighting": "questions_lighting.json",
}


def apply_rewrite(cat: str, data_file: str):
    """对某个分类应用重写"""
    fpath = PARTS_DIR / CAT_TO_FILE[cat]
    dpath = DATA_DIR / data_file

    if not dpath.exists():
        print(f"[SKIP] {cat}: 数据文件不存在 {dpath}")
        return 0

    with open(dpath, "r", encoding="utf-8") as f:
        rewrites = json.load(f)

    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 兼容 list / dict
    if isinstance(data, dict):
        questions = data["questions"]
    else:
        questions = data

    replaced = 0
    not_found = []
    for q in questions:
        qid = q["id"]
        if qid in rewrites:
            nd = rewrites[qid]
            q["question"] = nd["question"]
            q["answer"] = nd["answer"]
            q["tags"] = nd.get("tags", q["tags"])
            replaced += 1
        elif qid in [k for k in rewrites.keys()]:
            pass  # 已处理

    # 检查哪些没匹配到
    existing_ids = {q["id"] for q in questions}
    for k in rewrites:
        if k not in existing_ids:
            not_found.append(k)

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 验证 JSON
    with open(fpath, "r", encoding="utf-8") as f:
        json.load(f)

    print(f"[OK] {cat}: 重写 {replaced} 题" + (f", 未匹配 {len(not_found)}: {not_found}" if not_found else ""))
    return replaced


def main():
    import sys
    if len(sys.argv) < 2:
        print("用法: python apply_rewrite.py <category> [data_file]")
        print("或:   python apply_rewrite.py all  (应用所有 rewrite_data/*.json)")
        return

    arg = sys.argv[1]
    if arg == "all":
        total = 0
        for data_file in sorted(DATA_DIR.glob("*.json")) if DATA_DIR.exists() else []:
            # 文件名格式: rewrite_<cat>.json 或 rewrite_<cat>_partN.json
            name = data_file.stem  # 如 rewrite_shader
            cat = name.replace("rewrite_", "").split("_part")[0]
            if cat in CAT_TO_FILE:
                total += apply_rewrite(cat, data_file.name)
        print(f"\n--- 总计重写 {total} 题 ---")
    else:
        cat = arg
        data_file = sys.argv[2] if len(sys.argv) > 2 else f"rewrite_{cat}.json"
        apply_rewrite(cat, data_file)


if __name__ == "__main__":
    main()
