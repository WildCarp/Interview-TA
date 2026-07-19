"""
合并 8 个分类题库 part 文件为最终 questions.json
- 统一 difficulty 命名（easy→初级, medium→中级, hard→高级）
- 输出新的 8 分类 metadata
"""
import json
import os
from pathlib import Path

PARTS_DIR = Path(r"C:\Users\Administrator\WorkBuddy\2026-07-19-19-08-08\parts")
OUTPUT = Path(r"C:\Users\Administrator\WorkBuddy\2026-07-19-19-08-08\questions.json")

# 8 分类元数据（顺序即显示顺序）
CATEGORIES = [
    {"id": "shader",     "name": "材质/Shader", "color": "#a78bfa", "icon": "◆"},
    {"id": "vfx",        "name": "特效",        "color": "#ff6b6b", "icon": "✦"},
    {"id": "ui",         "name": "UI",         "color": "#4ecdc4", "icon": "◧"},
    {"id": "rendering",  "name": "渲染管线",    "color": "#60a5fa", "icon": "▦"},
    {"id": "optimization","name": "性能优化",   "color": "#f59e0b", "icon": "⚡"},
    {"id": "pipeline",   "name": "管线/工具",   "color": "#f472b6", "icon": "⚙"},
    {"id": "texture",    "name": "贴图",        "color": "#34d399", "icon": "▦"},
    {"id": "lighting",   "name": "灯光",        "color": "#fbbf24", "icon": "☀"},
]

# 难度映射（统一为中文）
DIFF_MAP = {
    "easy": "初级",
    "medium": "中级",
    "hard": "高级",
    # 兼容已有的中文
    "初级": "初级",
    "中级": "中级",
    "高级": "高级",
}

# part 文件加载顺序 + 对应分类 id（与 CATEGORIES 一致）
# 注：旧文件是 list 结构（直接是题目数组），新文件是 dict（含 category + questions）
PART_FILES = [
    ("questions_shader.json",      "shader"),
    ("questions_vfx.json",         "vfx"),
    ("questions_ui.json",          "ui"),
    ("questions_rendering.json",   "rendering"),
    ("questions_optimization.json","optimization"),
    ("questions_pipeline.json",    "pipeline"),
    ("questions_texture.json",     "texture"),
    ("questions_lighting.json",    "lighting"),
]

def main():
    all_questions = []
    seen_ids = set()

    for fname, expected_cat in PART_FILES:
        fpath = PARTS_DIR / fname
        if not fpath.exists():
            print(f"[WARN] 缺失文件: {fpath}")
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 兼容 list 和 dict 两种结构
        if isinstance(data, dict):
            qs = data.get("questions", [])
            cat = data.get("category", expected_cat)
        elif isinstance(data, list):
            qs = data
            cat = expected_cat
        else:
            print(f"[WARN] {fname}: 未知结构 {type(data)}")
            continue
        count = 0
        for q in qs:
            # 校验必需字段
            qid = q.get("id")
            if not qid:
                print(f"[WARN] 缺 id: {q}")
                continue
            if qid in seen_ids:
                print(f"[WARN] 重复 id: {qid}")
                continue
            seen_ids.add(qid)
            # 统一 difficulty
            diff = q.get("difficulty", "medium")
            q["difficulty"] = DIFF_MAP.get(diff, diff)
            # 强制 category 与 part 文件一致
            q["category"] = cat
            all_questions.append(q)
            count += 1
        print(f"  {fname}: {count} 题 (category={cat})")

    # 校验每个分类数量
    print("\n--- 分类统计 ---")
    cat_counts = {c["id"]: 0 for c in CATEGORIES}
    for q in all_questions:
        cid = q["category"]
        if cid not in cat_counts:
            print(f"[WARN] 未知分类: {cid} (qid={q['id']})")
            continue
        cat_counts[cid] += 1
    for c in CATEGORIES:
        print(f"  {c['id']:12s}: {cat_counts[c['id']]} 题")
    print(f"  总计: {len(all_questions)} 题")

    # 难度分布
    print("\n--- 难度分布 ---")
    diff_counts = {"初级": 0, "中级": 0, "高级": 0}
    for q in all_questions:
        d = q.get("difficulty", "中级")
        diff_counts[d] = diff_counts.get(d, 0) + 1
    for k, v in diff_counts.items():
        print(f"  {k}: {v} 题")

    # 构建最终题库
    bank = {
        "version": "2.0",
        "updatedAt": "2026-07-19",
        "title": "技术美术面试题库 — 8 大方向 300 题",
        "description": "为 TA 面试准备的复习题库，涵盖 材质/Shader、特效、UI、渲染管线、性能优化、管线/工具、贴图、灯光 共 8 大方向 300 题。材质/特效/UI 占比 60%。掌握阈值=3 表示连续答对 3 次后移出题库。",
        "masterThreshold": 3,
        "categories": CATEGORIES,
        "questions": all_questions,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] 已写出: {OUTPUT}")
    print(f"     文件大小: {OUTPUT.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
