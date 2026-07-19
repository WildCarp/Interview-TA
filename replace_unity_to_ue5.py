"""
把 parts/ 下所有 JSON 题库里的 Unity 字面替换为 UE5。
策略：
1. 先处理 "Unity/UE" / "Unity / UE" / "Unity/UE4" / "Unity / UE4" 并列情况 -> "UE5"
   （避免通用替换后变成 "UE5/UE" 这种尴尬表述）
2. 再字面替换 "Unity" -> "UE5"
3. 统计每个文件替换次数
4. 不重新生成 questions.json（由 merge_parts.py 负责）
"""
import json
import re
from pathlib import Path

PARTS_DIR = Path(r"C:\Users\Administrator\WorkBuddy\2026-07-19-19-08-08\parts")

# 先处理的并列情况（顺序很重要：先长后短，先并列后单独）
# 注意：这些必须在通用 Unity -> UE5 之前执行
SPECIAL_PATTERNS = [
    ("Unity / UE4", "UE5"),
    ("Unity/UE4", "UE5"),
    ("Unity / UE", "UE5"),
    ("Unity/UE", "UE5"),
]

# 通用替换
GENERIC_PATTERN = ("Unity", "UE5")

# UE5 对应概念里仍含 Unity 专有 API 的关键词（用于复核清单）
UNITY_API_KEYWORDS = [
    "ShaderLab", "HLSLPROGRAM", "CGPROGRAM", "ENCODED_UV",
    "unity_Matrix", "unity_ObjectToWorld", "unity_WorldToObject",
    "unity_Time", "unity_SpecCube0",
    "Renderer Feature", "ScriptableRenderPass", "RenderFeature",
    "ShaderGraph", "SubGraph", "Shader Graph",
    "URP", "HDRP", "SRP Batcher", "SRPBatcher",
    "AssetBundle", "Addressables", "Addressable",
    "UGUI", "FGUI",
    "Canvas", "CanvasRenderer", "GraphicRebuildQueue",
    "MaterialPropertyBlock",
    "Shader.Find", "Shader.Find",
    "Late Binding",
    "HLSLPROGRAM",
    "UnityEditor", "UnityEngine",
    "EditorGUILayout",
    "AssetPostprocessor",
    "ScriptableObject",
    "CustomEditor",
    "OnPostprocessAllAssets",
    "MonoBehaviour",
    "ProjectWindowUtil",
    "AssetDatabase",
    "Selection.activeObject",
]


def replace_in_text(text: str) -> tuple[str, int]:
    """返回 (替换后文本, 替换次数)"""
    count = 0
    for old, new in SPECIAL_PATTERNS:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            count += c
    # 通用替换
    old, new = GENERIC_PATTERN
    c = text.count(old)
    if c:
        text = text.replace(old, new)
        count += c
    return text, count


def find_api_keywords(text: str, qid: str) -> list[str]:
    """扫描文本里残留的 Unity 专有 API 关键词"""
    hits = []
    for kw in UNITY_API_KEYWORDS:
        if kw in text:
            hits.append(kw)
    return hits


def main():
    total_replaced = 0
    review_list = []  # (file, qid, category, question, hits)

    for p in sorted(PARTS_DIR.glob("questions_*.json")):
        with open(p, "r", encoding="utf-8") as f:
            raw = f.read()

        new_text, n = replace_in_text(raw)
        total_replaced += n

        if new_text != raw:
            with open(p, "w", encoding="utf-8") as f:
                f.write(new_text)
            print(f"[OK] {p.name}: 替换 {n} 处")
        else:
            print(f"[SKIP] {p.name}: 无 Unity 字样")

        # 验证 JSON 合法 + 扫描残留 API
        try:
            data = json.loads(new_text)
        except json.JSONDecodeError as e:
            print(f"  [ERR] JSON 解析失败: {e}")
            continue

        # 兼容 list / dict 两种结构
        if isinstance(data, dict):
            questions = data.get("questions", [])
            cat = data.get("category", p.stem)
        else:
            questions = data
            cat = p.stem.replace("questions_", "")

        for q in questions:
            qid = q.get("id", "?")
            question = q.get("question", "")
            answer = q.get("answer", "")
            tags = " ".join(q.get("tags", []))
            full_text = f"{question} {answer} {tags}"
            hits = find_api_keywords(full_text, qid)
            if hits:
                review_list.append((p.name, qid, cat, question, hits))

    print(f"\n--- 总替换次数: {total_replaced} ---")
    print(f"--- 需复核题目: {len(review_list)} ---\n")

    # 输出复核清单到 markdown
    review_md = Path(r"C:\Users\Administrator\WorkBuddy\2026-07-19-19-08-08\需复核题目_Unity_API残留.md")
    with open(review_md, "w", encoding="utf-8") as f:
        f.write("# 需人工复核的题目清单\n\n")
        f.write("> 已完成 Unity → UE5 字面替换。以下题目的**答案**或**题干**仍含 Unity 专有 API/概念，")
        f.write("在 UE5 里有对应实现，建议逐题对照修改答案后再用于面试准备。\n\n")
        f.write("| # | 文件 | 题号 | 分类 | 题干 | 残留 Unity API | UE5 对应概念 |\n")
        f.write("|---|------|------|------|------|----------------|--------------|\n")
        ue5_map = {
            "ShaderLab": "UE5 Material Editor (节点图) / Material Attribute",
            "HLSLPROGRAM": "Custom HLSL node (Material Editor)",
            "CGPROGRAM": "Custom HLSL node",
            "unity_Matrix": "ViewProjection / LocalToWorld 等内置节点",
            "unity_ObjectToWorld": "LocalToWorld / ObjectToWorld 节点",
            "unity_WorldToObject": "WorldToObject 节点",
            "unity_Time": "Time / View.GameTime 节点",
            "unity_SpecCube0": "ReflectionVectorWS / SkyLight",
            "Renderer Feature": "Post Process Material / Render Pass (UE5 Plugin)",
            "ScriptableRenderPass": "FRenderPass / RDG (Render Dependency Graph)",
            "RenderFeature": "Post Process Material / RDG Pass",
            "ShaderGraph": "Material Editor / Material Graph",
            "SubGraph": "Material Function",
            "URP": "UE5 默认前向渲染管线 / Forward+",
            "HDRP": "UE5 Lumen + Nanite + Path Tracing",
            "SRP Batcher": "UE5 自动 Instancing + Mesh Draw Pipeline",
            "AssetBundle": "Pak / Chunk / Asset Registry",
            "Addressables": "Pak Chunk + Asset Manager",
            "UGUI": "UMG (Unreal Motion Graphics)",
            "FGUI": "FairyGUI (UE5 插件，第三方，可保留)",
            "Canvas": "UMG Canvas Panel",
            "CanvasRenderer": "UMG Slate / Widget Renderer",
            "GraphicRebuildQueue": "UMG Widget Tick / Invalidate",
            "MaterialPropertyBlock": "UE5 ScalarParameter / VectorParameter + Material Instance Dynamic",
            "Shader.Find": "Material Instance Dynamic / Load Object",
            "UnityEditor": "UProperty / Editor Utility Widget",
            "UnityEngine": "UObject / AActor",
            "EditorGUILayout": "Detail Customization / Editor Utility Widget",
            "AssetPostprocessor": "UAssetManager / Asset Import Delegate",
            "ScriptableObject": "UDataAsset / UPrimaryDataAsset",
            "CustomEditor": "FPropertyEditor / DetailCustomization",
            "OnPostprocessAllAssets": "AssetPostImportDelegate / UAssetManager",
            "MonoBehaviour": "UActorComponent / UPrimaryDataAsset",
            "AssetDatabase": "UAssetManager / FAssetRegistryModule",
            "Selection.activeObject": "GEditor->GetSelectedActors",
            "Late Binding": "Soft Object Path / Async Load",
            "ENCODED_UV": "Texture Coordinate 节点",
        }
        for i, (fname, qid, cat, question, hits) in enumerate(review_list, 1):
            short_q = question[:50].replace("|", "/").replace("\n", " ")
            if len(question) > 50:
                short_q += "..."
            hits_str = ", ".join(sorted(set(hits)))
            ue5_str = "; ".join(sorted({ue5_map.get(h, "(查文档)") for h in hits}))
            f.write(f"| {i} | {fname} | `{qid}` | {cat} | {short_q} | {hits_str} | {ue5_str} |\n")

        f.write("\n## 复核建议\n\n")
        f.write("1. **优先改 shader 分类**：ShaderLab/URP/HLSLPROGRAM 是 Unity 专有，UE5 里对应 Material Editor + Custom HLSL node，答案需重写。\n")
        f.write("2. **rendering 分类**：URP/HDRP/SRP Batcher 在 UE5 里不存在，对应 UE5 Forward+/Lumen/Nanite/Mesh Draw Pipeline。\n")
        f.write("3. **ui 分类**：UGUI → UMG，Canvas → Canvas Panel，UGUI 组件名需换成 UMG 控件名。\n")
        f.write("4. **pipeline 分类**：AssetBundle → Pak，Addressables → Pak Chunk + Asset Manager，ScriptableObject → UDataAsset。\n")
        f.write("5. **texture/vfx/lighting 分类**：多为通用概念，字面替换后基本可用，少数 API 名需核对。\n")
        f.write("\n> 这份清单是 TA 视角的对照建议，不是强制要求。你可以按面试重点选择性修改。\n")

    print(f"复核清单已写入: {review_md}")
    return total_replaced, len(review_list)


if __name__ == "__main__":
    main()
