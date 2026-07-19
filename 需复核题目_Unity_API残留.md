# 需人工复核的题目清单

> 已完成 Unity → UE5 字面替换。以下题目的**答案**或**题干**仍含 Unity 专有 API/概念，在 UE5 里有对应实现，建议逐题对照修改答案后再用于面试准备。

| # | 文件 | 题号 | 分类 | 题干 | 残留 Unity API | UE5 对应概念 |
|---|------|------|------|------|----------------|--------------|
| 1 | questions_lighting.json | `lighting_001` | lighting | 游戏引擎里的灯光有哪些类型？分别用在什么场景？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 2 | questions_lighting.json | `lighting_008` | lighting | 什么是 IBL？PBR 里怎么用？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 3 | questions_lighting.json | `lighting_010` | lighting | 怎么优化灯光数量？移动端灯光预算怎么定？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 4 | questions_optimization.json | `optimization-003` | optimization | draw call 数过高的常见原因和优化？ | SRP Batcher, URP | UE5 自动 Instancing + Mesh Draw Pipeline; UE5 默认前向渲染管线 / Forward+ |
| 5 | questions_optimization.json | `optimization-009` | optimization | 资源加载优化？同步 vs 异步 vs 预加载？ | Addressable, Addressables | (查文档); Pak Chunk + Asset Manager |
| 6 | questions_optimization.json | `optimization-010` | optimization | 移动端渲染优化策略？和 PC 的区别？ | SRP Batcher | UE5 自动 Instancing + Mesh Draw Pipeline |
| 7 | questions_optimization.json | `optimization-016` | optimization | CPU 优化的常见手段？ | SRP Batcher | UE5 自动 Instancing + Mesh Draw Pipeline |
| 8 | questions_optimization.json | `optimization-018` | optimization | Addressables 是什么？比 Resources 好在哪？ | Addressable, Addressables, AssetBundle | (查文档); Pak / Chunk / Asset Registry; Pak Chunk + Asset Manager |
| 9 | questions_optimization.json | `optimization-021` | optimization | 热更新机制的实现？ | Addressable, Addressables | (查文档); Pak Chunk + Asset Manager |
| 10 | questions_optimization.json | `optimization-023` | optimization | Vulkan 和 OpenGL ES 的区别？为什么移动端用 Vulkan？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 11 | questions_optimization.json | `optimization-024` | optimization | 异步计算（Async Compute）是什么？怎么用？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 12 | questions_optimization.json | `optimization-025` | optimization | 可变着色率（VRS）是什么？怎么用？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 13 | questions_optimization.json | `optimization-028` | optimization | Profiler Marker 怎么用？自定义性能分析？ | MonoBehaviour | UActorComponent / UPrimaryDataAsset |
| 14 | questions_optimization.json | `optimization-030` | optimization | 性能优化的完整工作流？从项目开始到上线？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 15 | questions_pipeline.json | `pipeline_001` | pipeline | 什么是美术资源管线（Art Pipeline）？它包含哪些关键环节？ | Addressable, Addressables | (查文档); Pak Chunk + Asset Manager |
| 16 | questions_pipeline.json | `pipeline_007` | pipeline | 美术资源在导入引擎时常见的错误有哪些？怎么用工具拦截？ | AssetPostprocessor | UAssetManager / Asset Import Delegate |
| 17 | questions_pipeline.json | `pipeline_008` | pipeline | UE5 的 AssetPostprocessor 怎么用？写一个自动设置贴图导入的例子。 | AssetPostprocessor | UAssetManager / Asset Import Delegate |
| 18 | questions_pipeline.json | `pipeline_010` | pipeline | 美术资源 review 流程应该怎么设计？ | AssetPostprocessor | UAssetManager / Asset Import Delegate |
| 19 | questions_pipeline.json | `pipeline_011` | pipeline | UE5 中如何用脚本批量处理资源（改名 / 改导入设置 / 生成 LOD）？ | AssetDatabase | UAssetManager / FAssetRegistryModule |
| 20 | questions_pipeline.json | `pipeline_013` | pipeline | 如何设计一个可扩展的美术资产校验框架？ | AssetPostprocessor | UAssetManager / Asset Import Delegate |
| 21 | questions_pipeline.json | `pipeline_014` | pipeline | 讲讲你对 AssetBundle / Addressables 在管线里使用实践。 | Addressable, Addressables, AssetBundle | (查文档); Pak / Chunk / Asset Registry; Pak Chunk + Asset Manager |
| 22 | questions_pipeline.json | `pipeline_015` | pipeline | 如何做美术资产的依赖分析？怎么找出没被使用的废弃资源？ | Addressable, Addressables, AssetDatabase, ScriptableObject, Shader.Find | (查文档); Material Instance Dynamic / Load Object; Pak Chunk + Asset Manager; UAssetManager / FAssetRegistryModule; UDataAsset / UPrimaryDataAsset |
| 23 | questions_pipeline.json | `pipeline_017` | pipeline | 如何把 Substance Painter / Designer 集成进引擎管线？ | AssetPostprocessor, URP | UAssetManager / Asset Import Delegate; UE5 默认前向渲染管线 / Forward+ |
| 24 | questions_pipeline.json | `pipeline_019` | pipeline | Maya/Blender 的渲染器预览能代替引擎内 review 吗？为什么？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 25 | questions_pipeline.json | `pipeline_023` | pipeline | Unreal 的 Asset Pipeline（UAT / UBT）和 UE5 有什么本质区别？ | AssetDatabase | UAssetManager / FAssetRegistryModule |
| 26 | questions_rendering.json | `rendering-001` | rendering | 前向渲染（Forward）和延迟渲染（Deferred）的区别？各自适合什么？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 27 | questions_rendering.json | `rendering-002` | rendering | Forward+（分簇前向渲染）是什么？解决了什么问题？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 28 | questions_rendering.json | `rendering-003` | rendering | 延迟渲染的 G-Buffer 包含什么？MRT 是什么？ | HDRP | UE5 Lumen + Nanite + Path Tracing |
| 29 | questions_rendering.json | `rendering-006` | rendering | SRP 的渲染流程？UE5 URP 一帧都做了什么？ | Renderer Feature, URP | Post Process Material / Render Pass (UE5 Plugin); UE5 默认前向渲染管线 / Forward+ |
| 30 | questions_rendering.json | `rendering-007` | rendering | UE5 的 Renderer Feature 和 ScriptableRenderPass 的关系？ | Renderer Feature, ScriptableRenderPass, URP | FRenderPass / RDG (Render Dependency Graph); Post Process Material / Render Pass (UE5 Plugin); UE5 默认前向渲染管线 / Forward+ |
| 31 | questions_rendering.json | `rendering-011` | rendering | MSAA、FXAA、TAA 三种抗锯齿的原理和区别？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 32 | questions_rendering.json | `rendering-016` | rendering | Draw Call 和 Batch 是什么？为什么是性能瓶颈？ | SRP Batcher | UE5 自动 Instancing + Mesh Draw Pipeline |
| 33 | questions_rendering.json | `rendering-017` | rendering | 静态合批、动态合批、GPU Instancing、SRP Batcher 的区别？ | SRP Batcher, SRPBatcher, URP | (查文档); UE5 自动 Instancing + Mesh Draw Pipeline; UE5 默认前向渲染管线 / Forward+ |
| 34 | questions_rendering.json | `rendering-018` | rendering | Frame Debugger 怎么用？能分析什么？ | SRP Batcher | UE5 自动 Instancing + Mesh Draw Pipeline |
| 35 | questions_rendering.json | `rendering-020` | rendering | 全局光照（GI）的方案：实时 GI、烘焙 GI、混合 GI？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 36 | questions_rendering.json | `rendering-022` | rendering | Light Probe（光照探针）是什么？什么场景用？ | HDRP | UE5 Lumen + Nanite + Path Tracing |
| 37 | questions_rendering.json | `rendering-026` | rendering | GPU Instancing 的原理和限制？怎么写支持 Instancing 的 Shader？ | MaterialPropertyBlock | UE5 ScalarParameter / VectorParameter + Material Instance Dynamic |
| 38 | questions_rendering.json | `rendering-029` | rendering | 渲染中的 Render Target 切换为什么贵？移动端怎么避免？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 39 | questions_rendering.json | `rendering-030` | rendering | 渲染中的 Rebuild / Dirty 是什么？ | Canvas | UMG Canvas Panel |
| 40 | questions_rendering.json | `rendering-032` | rendering | URP 的 Volume 系统是什么？怎么用？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 41 | questions_shader.json | `shader-001` | shader | ShaderLab 文件的基本结构是什么？Properties、SubShader、Pass、Fal... | CGPROGRAM, HLSLPROGRAM, ShaderLab | Custom HLSL node; Custom HLSL node (Material Editor); UE5 Material Editor (节点图) / Material Attribute |
| 42 | questions_shader.json | `shader-002` | shader | Shader Properties 支持哪些类型？如何在 C# 脚本中访问和修改它们？ | MaterialPropertyBlock | UE5 ScalarParameter / VectorParameter + Material Instance Dynamic |
| 43 | questions_shader.json | `shader-004` | shader | 渲染队列 Queue 的数值范围是怎样的？为什么透明物体要放在 Transparent 队列？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 44 | questions_shader.json | `shader-010` | shader | Shader 中一个 Pass 意味着一次 draw call 吗？多 Pass 的代价和优化？ | HDRP, SRP Batcher, URP | UE5 Lumen + Nanite + Path Tracing; UE5 自动 Instancing + Mesh Draw Pipeline; UE5 默认前向渲染管线 / Forward+ |
| 45 | questions_shader.json | `shader-013` | shader | 法线从模型空间变换到世界空间时，为什么有时要用法线矩阵的逆转置？ | unity_ObjectToWorld, unity_WorldToObject | LocalToWorld / ObjectToWorld 节点; WorldToObject 节点 |
| 46 | questions_shader.json | `shader-017` | shader | MVP 矩阵变换的完整过程？UE5 中相关内置矩阵的命名？ | URP, unity_ObjectToWorld, unity_WorldToObject | LocalToWorld / ObjectToWorld 节点; UE5 默认前向渲染管线 / Forward+; WorldToObject 节点 |
| 47 | questions_shader.json | `shader-019` | shader | SRP（Scriptable Render Pipeline）是什么？URP 和 HDRP 的定位差... | HDRP, SRP Batcher, URP | UE5 Lumen + Nanite + Path Tracing; UE5 自动 Instancing + Mesh Draw Pipeline; UE5 默认前向渲染管线 / Forward+ |
| 48 | questions_shader.json | `shader-020` | shader | URP 下写自定义 Shader 为什么推荐 HLSLPROGRAM 而非 CGPROGRAM？ | CGPROGRAM, HLSLPROGRAM, SRP Batcher, SRPBatcher, URP | (查文档); Custom HLSL node; Custom HLSL node (Material Editor); UE5 自动 Instancing + Mesh Draw Pipeline; UE5 默认前向渲染管线 / Forward+ |
| 49 | questions_shader.json | `shader-021` | shader | URP 的 ShaderLibrary 提供哪些常用函数？Core/Lighting/SpaceTr... | URP | UE5 默认前向渲染管线 / Forward+ |
| 50 | questions_shader.json | `shader-022` | shader | URP 中如何接入主光源和附加光？GetMainLight() 的用法？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 51 | questions_shader.json | `shader-023` | shader | URP 的 Renderer Feature（如 Render Objects）怎么用？做描边或自定... | Renderer Feature, ScriptableRenderPass, URP | FRenderPass / RDG (Render Dependency Graph); Post Process Material / Render Pass (UE5 Plugin); UE5 默认前向渲染管线 / Forward+ |
| 52 | questions_shader.json | `shader-024` | shader | 内置管线的 Shader 和 URP 的 Shader 能互用吗？迁移要点？ | CGPROGRAM, HLSLPROGRAM, SRP Batcher, URP | Custom HLSL node; Custom HLSL node (Material Editor); UE5 自动 Instancing + Mesh Draw Pipeline; UE5 默认前向渲染管线 / Forward+ |
| 53 | questions_shader.json | `shader-025` | shader | HDRP 的材质模型和 URP 有何不同？Mask Map 是什么？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 54 | questions_shader.json | `shader-026` | shader | URP 中 Shader Pass 的 LightMode Tag（UniversalForward... | URP | UE5 默认前向渲染管线 / Forward+ |
| 55 | questions_shader.json | `shader-031` | shader | 环境光（IBL）在 PBR 中如何贡献？漫反射积分和高光预滤波分别是什么？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 56 | questions_shader.json | `shader-038` | shader | UE5 的 Shader Complex（复杂度）可视化工具怎么用？红黄绿含义？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 57 | questions_shader.json | `shader-042` | shader | Shader 变体爆炸问题怎么解决？如何控制变体数量？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 58 | questions_shader.json | `shader-046` | shader | URP 的变体剥离（Stripping）怎么配置？默认剥离哪些？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 59 | questions_shader.json | `shader-047` | shader | ShaderGraph 的优劣？什么场景适合用，什么场景不适合？ | HDRP, SRP Batcher, ShaderGraph, SubGraph, URP | Material Editor / Material Graph; Material Function; UE5 Lumen + Nanite + Path Tracing; UE5 自动 Instancing + Mesh Draw Pipeline; UE5 默认前向渲染管线 / Forward+ |
| 60 | questions_shader.json | `shader-048` | shader | ShaderGraph 的 SubGraph 机制？如何复用？ | Shader Graph, ShaderGraph, SubGraph | (查文档); Material Editor / Material Graph; Material Function |
| 61 | questions_shader.json | `shader-049` | shader | ShaderGraph 的 Custom Function Node 怎么用？有什么限制？ | ShaderGraph | Material Editor / Material Graph |
| 62 | questions_shader.json | `shader-050` | shader | ShaderGraph 生成的代码性能和手写相比如何？ | ShaderGraph | Material Editor / Material Graph |
| 63 | questions_shader.json | `shader-051` | shader | ShaderGraph 中如何做顶点位移（Vertex Displacement）？ | ShaderGraph, URP | Material Editor / Material Graph; UE5 默认前向渲染管线 / Forward+ |
| 64 | questions_shader.json | `shader-054` | shader | 水面 Shader 的核心要素？法线流动、菲涅尔、折射、泡沫怎么实现？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 65 | questions_shader.json | `shader-056` | shader | 热空气扭曲（Distortion）特效的屏幕抓取原理？GrabPass 在移动端的代价？ | Renderer Feature, URP | Post Process Material / Render Pass (UE5 Plugin); UE5 默认前向渲染管线 / Forward+ |
| 66 | questions_shader.json | `shader-058` | shader | 屏幕空间反射（SSR）原理和限制？ | Renderer Feature, URP | Post Process Material / Render Pass (UE5 Plugin); UE5 默认前向渲染管线 / Forward+ |
| 67 | questions_shader.json | `shader-063` | shader | 为什么移动端慎用 GrabPass 和全屏后处理？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 68 | questions_shader.json | `shader-066` | shader | HLSL、GLSL、CG 的关系和区别？UE5 用哪种？ | CGPROGRAM, HDRP, HLSLPROGRAM, URP | Custom HLSL node; Custom HLSL node (Material Editor); UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 69 | questions_shader.json | `shader-067` | shader | Shader 中的变长循环和动态索引为什么慢？怎么避免？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 70 | questions_shader.json | `shader-069` | shader | SRP Batcher 的原理？为什么能减少 CPU 开销？ | HLSLPROGRAM, SRP Batcher, SRPBatcher, URP, unity_ObjectToWorld | (查文档); Custom HLSL node (Material Editor); LocalToWorld / ObjectToWorld 节点; UE5 自动 Instancing + Mesh Draw Pipeline; UE5 默认前向渲染管线 / Forward+ |
| 71 | questions_shader.json | `shader-070` | shader | MaterialPropertyBlock 是什么？为什么用它而不直接改 Material？ | MaterialPropertyBlock, SRP Batcher | UE5 ScalarParameter / VectorParameter + Material Instance Dynamic; UE5 自动 Instancing + Mesh Draw Pipeline |
| 72 | questions_texture.json | `texture_005` | texture | PBR 贴图有哪些通道？怎么打包能省内存？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 73 | questions_texture.json | `texture_008` | texture | 什么是 Sprite Atlas？UE5 里怎么用？ | Late Binding | Soft Object Path / Async Load |
| 74 | questions_texture.json | `texture_018` | texture | Substance Painter 导出的贴图怎么对应到 UE5 URP / HDRP？ | AssetPostprocessor, HDRP, URP | UAssetManager / Asset Import Delegate; UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 75 | questions_texture.json | `texture_019` | texture | 贴图通道打包（Channel Packing）有哪些最佳实践？ | HDRP | UE5 Lumen + Nanite + Path Tracing |
| 76 | questions_texture.json | `texture_020` | texture | 如何用 Python 脚本批量给团队美术重置贴图导入设置？ | AssetDatabase | UAssetManager / FAssetRegistryModule |
| 77 | questions_ui.json | `ui-001` | ui | UGUI 和 FairyGUI（FGUI）的区别？各自适合什么场景？ | FGUI, UGUI | FairyGUI (UE5 插件，第三方，可保留); UMG (Unreal Motion Graphics) |
| 78 | questions_ui.json | `ui-002` | ui | Canvas 的作用？为什么 Canvas 的 Render Mode 选 Screen Space... | Canvas, UGUI | UMG (Unreal Motion Graphics); UMG Canvas Panel |
| 79 | questions_ui.json | `ui-003` | ui | 为什么要把 Canvas 拆分成多个子 Canvas？拆分的原则？ | Canvas | UMG Canvas Panel |
| 80 | questions_ui.json | `ui-004` | ui | 图集（Sprite Atlas）的作用？为什么 UI 必须用图集？ | Late Binding | Soft Object Path / Async Load |
| 81 | questions_ui.json | `ui-005` | ui | UI 的 Overdraw 问题？和 3D 特效 Overdraw 的区别？ | Canvas | UMG Canvas Panel |
| 82 | questions_ui.json | `ui-007` | ui | 多分辨率适配怎么做？Anchor、Canvas Scaler、SafeArea？ | Canvas | UMG Canvas Panel |
| 83 | questions_ui.json | `ui-008` | ui | UI Rebuild 是什么？怎么排查 Rebuild 性能问题？ | Canvas | UMG Canvas Panel |
| 84 | questions_ui.json | `ui-009` | ui | UI 和粒子叠加的方案？怎么避免 UI 粒子打断合批？ | Canvas, CanvasRenderer, UGUI | UMG (Unreal Motion Graphics); UMG Canvas Panel; UMG Slate / Widget Renderer |
| 85 | questions_ui.json | `ui-010` | ui | UGUI 的 Batching（合批）规则？什么情况会打断合批？ | Canvas, UGUI | UMG (Unreal Motion Graphics); UMG Canvas Panel |
| 86 | questions_ui.json | `ui-012` | ui | UI Shader 用 Material 和 MaterialPropertyBlock 的坑？ | Canvas, CanvasRenderer, MaterialPropertyBlock, UGUI | UE5 ScalarParameter / VectorParameter + Material Instance Dynamic; UMG (Unreal Motion Graphics); UMG Canvas Panel; UMG Slate / Widget Renderer |
| 87 | questions_ui.json | `ui-013` | ui | UGUI 的基本组件有哪些？Image、Text、Button、Toggle 各自的用途？ | Canvas, CanvasRenderer, UGUI | UMG (Unreal Motion Graphics); UMG Canvas Panel; UMG Slate / Widget Renderer |
| 88 | questions_ui.json | `ui-015` | ui | UI 的事件系统（EventSystem）怎么工作？Raycast 怎么优化？ | Canvas, UGUI | UMG (Unreal Motion Graphics); UMG Canvas Panel |
| 89 | questions_ui.json | `ui-018` | ui | UI 的动画方案？DOTween、Animation、Animator？ | FGUI | FairyGUI (UE5 插件，第三方，可保留) |
| 90 | questions_ui.json | `ui-020` | ui | UI 的 Loading 流程？怎么避免卡顿？ | Addressable, Addressables, Canvas | (查文档); Pak Chunk + Asset Manager; UMG Canvas Panel |
| 91 | questions_ui.json | `ui-022` | ui | UI 的分辨率无关设计？怎么保证不同分辨率显示一致？ | Canvas | UMG Canvas Panel |
| 92 | questions_ui.json | `ui-023` | ui | UI 和 3D 场景的交互？点击 3D 物体？ | Canvas | UMG Canvas Panel |
| 93 | questions_ui.json | `ui-024` | ui | UI 的图集打包策略？按什么分？ | Late Binding | Soft Object Path / Async Load |
| 94 | questions_ui.json | `ui-025` | ui | UI 的性能监控和优化流程？ | Canvas | UMG Canvas Panel |
| 95 | questions_ui.json | `ui-026` | ui | UI 的 UI Toolkit 是什么？和 UGUI 的区别？ | Canvas, UGUI | UMG (Unreal Motion Graphics); UMG Canvas Panel |
| 96 | questions_ui.json | `ui-027` | ui | UI 的 SafeArea 适配具体怎么做？代码示例？ | Canvas, MonoBehaviour | UActorComponent / UPrimaryDataAsset; UMG Canvas Panel |
| 97 | questions_ui.json | `ui-028` | ui | UI 的 Pool 怎么实现？和特效池的区别？ | Canvas, MonoBehaviour | UActorComponent / UPrimaryDataAsset; UMG Canvas Panel |
| 98 | questions_ui.json | `ui-029` | ui | UI 的 Shader 怎么写？和普通 Shader 的区别？ | Canvas, CanvasRenderer, MaterialPropertyBlock | UE5 ScalarParameter / VectorParameter + Material Instance Dynamic; UMG Canvas Panel; UMG Slate / Widget Renderer |
| 99 | questions_ui.json | `ui-030` | ui | UI 的描边、阴影、发光怎么做？性能影响？ | UGUI | UMG (Unreal Motion Graphics) |
| 100 | questions_ui.json | `ui-032` | ui | UI 的 Filled 模式怎么用？血条、技能 CD？ | Canvas | UMG Canvas Panel |
| 101 | questions_ui.json | `ui-033` | ui | UI 的输入框（InputField）怎么做？移动端键盘适配？ | Canvas | UMG Canvas Panel |
| 102 | questions_ui.json | `ui-035` | ui | UI 的 SortingLayer 和 SortingOrder？怎么控制 UI 层级？ | Canvas | UMG Canvas Panel |
| 103 | questions_ui.json | `ui-037` | ui | UI 的 AB 包管理和加载？ | Addressable, Addressables, AssetBundle | (查文档); Pak / Chunk / Asset Registry; Pak Chunk + Asset Manager |
| 104 | questions_ui.json | `ui-038` | ui | UI 的图集和 Sprite 的引用关系？Late Binding？ | Addressable, Addressables, Late Binding | (查文档); Pak Chunk + Asset Manager; Soft Object Path / Async Load |
| 105 | questions_ui.json | `ui-040` | ui | UI 的 HUD（血条、伤害数字）优化？ | Canvas | UMG Canvas Panel |
| 106 | questions_ui.json | `ui-042` | ui | UI 的弹窗（Popup）管理？模态/非模态？ | Canvas | UMG Canvas Panel |
| 107 | questions_ui.json | `ui-046` | ui | UI 的 Shader 变体怎么管理？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 108 | questions_ui.json | `ui-047` | ui | UI 和后处理的关系？UI 要不要参与 Bloom？ | Canvas | UMG Canvas Panel |
| 109 | questions_ui.json | `ui-048` | ui | UI 的设计规范和美术协作？ | FGUI | FairyGUI (UE5 插件，第三方，可保留) |
| 110 | questions_ui.json | `ui-050` | ui | UI 的性能预算和指标？ | Canvas | UMG Canvas Panel |
| 111 | questions_ui.json | `ui-052` | ui | UI 的热更新？资源热更 vs 代码热更？ | Addressable, Addressables | (查文档); Pak Chunk + Asset Manager |
| 112 | questions_ui.json | `ui-053` | ui | UI 的性能 Review 流程？TA 怎么把关 UI 性能？ | Canvas | UMG Canvas Panel |
| 113 | questions_ui.json | `ui-055` | ui | 从零搭建 UI 系统要做什么？ | Canvas, FGUI, Late Binding, UGUI | FairyGUI (UE5 插件，第三方，可保留); Soft Object Path / Async Load; UMG (Unreal Motion Graphics); UMG Canvas Panel |
| 114 | questions_vfx.json | `vfx-008` | vfx | VFX Graph 和传统 ParticleSystem 的区别？什么时候用 VFX Graph？ | HDRP, ShaderGraph, URP | Material Editor / Material Graph; UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 115 | questions_vfx.json | `vfx-011` | vfx | Color Grading（颜色分级）的 LUT 是什么？如何制作和应用？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 116 | questions_vfx.json | `vfx-014` | vfx | 运动模糊（Motion Blur）的实现原理？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 117 | questions_vfx.json | `vfx-016` | vfx | 镜头光晕（Lens Flare）和光晕（Halo）的区别和实现？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 118 | questions_vfx.json | `vfx-028` | vfx | 屏幕震屏（Screen Shake）和时停（Hit Stop）怎么实现？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 119 | questions_vfx.json | `vfx-033` | vfx | Niagara（UE）和 VFX Graph（UE5）的对比？ | HDRP, URP | UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 120 | questions_vfx.json | `vfx-035` | vfx | Decal（贴花）在特效中的作用？实现方式？ | HDRP, Renderer Feature, URP | Post Process Material / Render Pass (UE5 Plugin); UE5 Lumen + Nanite + Path Tracing; UE5 默认前向渲染管线 / Forward+ |
| 121 | questions_vfx.json | `vfx-039` | vfx | 后处理栈（Post Processing Stack）的执行顺序怎么定？ | URP | UE5 默认前向渲染管线 / Forward+ |
| 122 | questions_vfx.json | `vfx-055` | vfx | 从零搭建一个特效系统（项目级）要做什么？ | URP | UE5 默认前向渲染管线 / Forward+ |

## 复核建议

1. **优先改 shader 分类**：ShaderLab/URP/HLSLPROGRAM 是 Unity 专有，UE5 里对应 Material Editor + Custom HLSL node，答案需重写。
2. **rendering 分类**：URP/HDRP/SRP Batcher 在 UE5 里不存在，对应 UE5 Forward+/Lumen/Nanite/Mesh Draw Pipeline。
3. **ui 分类**：UGUI → UMG，Canvas → Canvas Panel，UGUI 组件名需换成 UMG 控件名。
4. **pipeline 分类**：AssetBundle → Pak，Addressables → Pak Chunk + Asset Manager，ScriptableObject → UDataAsset。
5. **texture/vfx/lighting 分类**：多为通用概念，字面替换后基本可用，少数 API 名需核对。

> 这份清单是 TA 视角的对照建议，不是强制要求。你可以按面试重点选择性修改。
