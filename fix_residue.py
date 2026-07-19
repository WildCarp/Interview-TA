#!/usr/bin/env python3
"""修复残留 Unity API 的 7 道题（正文中把 GrabPass 当通用概念引用 + texture_015 残留 Unity C# 代码）。"""
import json, os

PARTS_DIR = "parts"

# 每道题的精确字符串替换（old -> new），按 part 文件分组
FIXES = {
    "shader": [
        {
            "id": "shader-037",
            "replacements": [
                ("注意：GrabPass / 屏幕纹理采样代价更高（全屏带宽），移动端慎用。",
                 "注意：SceneTexture（SceneColor / PostProcessInput0）采样代价更高（全屏带宽），移动端慎用。"),
            ],
        },
        {
            "id": "shader-062",
            "replacements": [
                ("- 不支持 GrabPass（用 Opaque Texture 代替）。",
                 "- 全屏 SceneTexture 抓屏代价高（移动端 TBR 下切 RT 贵），需用 Separate Translucency / 降分辨率后处理代替。"),
            ],
        },
    ],
    "rendering": [
        {
            "id": "rendering-004",
            "replacements": [
                ("- render target 切换贵（GrabPass、多 pass 后处理）。",
                 "- render target 切换贵（SceneTexture 抓屏、多 pass 后处理）。"),
            ],
        },
        {
            "id": "rendering-028",
            "replacements": [
                ("- 纹理采样多、render target 切换、GrabPass。",
                 "- 纹理采样多、render target 切换、全屏 SceneTexture 采样。"),
                ("- 优化：减纹理采样、合并通道、避免 GrabPass。",
                 "- 优化：减纹理采样、合并通道、避免全屏抓屏采样。"),
            ],
        },
    ],
    "optimization": [
        {
            "id": "optimization-011",
            "replacements": [
                ("- 行为差异（如 GrabPass、Compute Shader 支持）。",
                 "- 行为差异（如 SceneTexture 抓屏、Compute Shader 支持）。"),
            ],
        },
    ],
    "pipeline": [
        {
            "id": "pipeline_015",
            "replacements": [
                ("- `FShaderCodeLibrary` 的 Shader.Find、Paper2D 间接引用要单独处理",
                 "- `FShaderCodeLibrary::FindShaderCode`、Paper2D 间接引用要单独处理"),
            ],
        },
    ],
}

# texture_015 需要整题重写答案（残留 Unity C# 代码 + RawImage + Reflection Probe）
TEXTURE_015_NEW_ANSWER = """**Render Texture（RT）**：在 GPU 显存里的可渲染贴图，相机可渲染到它，Shader 可采样它。UE5 里对应 `UTextureRenderTarget2D`。

**用途**：

1. **后处理**：
   - 主相机渲染到 RT → Post Process Material → 屏幕
   - Bloom、Blur、Color Grading 等

2. **小地图 / 俯视图**：
   - 顶部 SceneCapture2D 渲染到 RT → 显示在 UMG Image（用 Brush 绑定 RT）
   - UE5 的 SceneCaptureComponent2D 比 Unity 额外相机更轻量

3. **反射 / 折射**：
   - SSR：屏幕空间反射，G-Buffer 计算
   - 水面反射：SceneCapture2D 镜像渲染到 RT
   - 折射：Pixel Normal Offset 采样 SceneColor（UE5 用 Separate Translucency + Custom Depth 方案）

4. **CCTV / 监视器**：
   - 场景里的电视屏幕显示另一个 SceneCapture 画面

5. **动态环境贴图**：
   - Reflection Capture（球面/方形捕获，实时或烘焙 Cubemap）
   - Planar Reflection（平面反射组件，实时高质量）

6. **特效**：
   - 节奏光波、扫描线
   - 离屏粒子

**UE5 实现**：
```cpp
// C++ 创建 RT
UTextureRenderTarget2D* RT = NewObject<UTextureRenderTarget2D>();
RT->InitAutoFormat(1024, 1024);  // 自动选格式
RT->UpdateResource();

// 绑定到 SceneCapture2D
SceneCaptureComp->TextureTarget = RT;
```

**蓝图**：Create Render Target 2D → Scene Capture Component 2D 设 Texture Target → UMG Image 的 Brush 设为 RT。

**坑与优化**：

- **内存**：RT 占用 = 分辨率 × 像素字节，1080p HDR RT ≈ 16MB
- **重用**：避免每帧 new RT，UE5 内部 `FRenderTargetPool` 自动池化，业务层复用同一 RT 资源即可
- **Format**：
  - RTF RGBA8：8bit/channel，普通用
  - RTF RGBA16f：16bit，HDR
  - RTF RGBA32f：32bit，超高精度
- **DepthBuffer**：需要深度时设 24/32bit，否则 0 省内存
- **Anti-aliasing**：移动端慎用 MSAA RT，性能开销大，用 FXAA/TAA 代替"""


def fix_part(cat, fixes):
    path = os.path.join(PARTS_DIR, f"questions_{cat}.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    questions = data if isinstance(data, list) else data.get("questions", [])
    fix_map = {fx["id"]: fx["replacements"] for fx in fixes}
    changed = 0
    
    for q in questions:
        if q["id"] in fix_map:
            for old, new in fix_map[q["id"]]:
                if old in q["answer"]:
                    q["answer"] = q["answer"].replace(old, new)
                    changed += 1
                    print(f"  [OK] {q['id']}: 替换成功")
                else:
                    print(f"  [MISS] {q['id']}: 未找到 '{old[:40]}...'")
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  {path}: {changed} 处替换，已写入")
    return changed


def fix_texture_015():
    path = os.path.join(PARTS_DIR, "questions_texture.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    questions = data if isinstance(data, list) else data.get("questions", [])
    changed = 0
    for q in questions:
        if q["id"] == "texture_015":
            q["answer"] = TEXTURE_015_NEW_ANSWER
            changed += 1
            print(f"  [OK] texture_015: 整题答案重写")
            break
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  {path}: {changed} 处替换，已写入")
    return changed


def main():
    total = 0
    for cat, fixes in FIXES.items():
        print(f"\n=== 修复 {cat} ===")
        total += fix_part(cat, fixes)
    
    print(f"\n=== 修复 texture_015（整题重写）===")
    total += fix_texture_015()
    
    print(f"\n总计: {total} 处修复")


if __name__ == "__main__":
    main()
