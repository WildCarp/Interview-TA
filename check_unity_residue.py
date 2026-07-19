import json, re

with open("questions.json", encoding="utf-8") as f:
    bank = json.load(f)

# Unity 专有 API 关键词
unity_apis = [
    "ShaderLab", "URP", "HDRP", "SRP Batcher", "SRPBatcher", "ShaderGraph",
    "SubGraph", "GrabPass", "Renderer Feature", "ScriptableRenderPass",
    "HLSLPROGRAM", "unity_Matrix", "MaterialPropertyBlock", "UGUI", "Canvas",
    "AssetBundle", "Addressables", "ScriptableObject", "AssetPostprocessor",
    "GetMainLight", "Shader.Find", "Camera.main"
]

# 对比段落标记词
compare_markers = ["对比", "区别", "替代", "Unity 对应", "Unity 的", "Unity 中", "vs", "VS", "迁移", "对应", "类似", "相当于", "Unity\u3002", "Unity，", "Unity、"]

results = []
for q in bank["questions"]:
    qid = q["id"]
    answer = q.get("answer", "")
    question = q.get("question", "")
    full_text = question + "\n" + answer
    
    for api in unity_apis:
        # 找所有出现位置
        start = 0
        while True:
            idx = full_text.find(api, start)
            if idx == -1:
                break
            # 取上下文 80 字符
            ctx_start = max(0, idx - 40)
            ctx_end = min(len(full_text), idx + len(api) + 40)
            context = full_text[ctx_start:ctx_end].replace("\n", " ")
            
            # 判断是否在对比段落（前后 80 字符内含对比标记词）
            wider_start = max(0, idx - 80)
            wider_end = min(len(full_text), idx + len(api) + 80)
            wider_ctx = full_text[wider_start:wider_end]
            in_compare = any(m in wider_ctx for m in compare_markers) or "Unity" in wider_ctx
            
            results.append({
                "id": qid,
                "api": api,
                "in_compare": in_compare,
                "context": context
            })
            start = idx + len(api)

print(f"总残留: {len(results)}")
print(f"对比段落内: {sum(1 for r in results if r['in_compare'])}")
print(f"非对比段落: {sum(1 for r in results if not r['in_compare'])}")
print()
print("=== 非对比段落残留 ===")
for r in results:
    if not r["in_compare"]:
        print(f"[{r['id']}] {r['api']}")
        print(f"  {r['context']}")
        print()
