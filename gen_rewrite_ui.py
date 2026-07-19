# -*- coding: utf-8 -*-
"""生成 UE5 UMG 视角的重写数据（37 题），分两个 part 输出。"""
import json
from pathlib import Path

OUT = Path(r"C:\Users\Administrator\WorkBuddy\2026-07-19-19-08-08\rewrite_data")

# ============ Part 1 (18 题) ============
part1 = {}

part1["ui-001"] = {
    "question": "UMG 和 FairyGUI（FGUI）的区别？各自适合什么场景？（FGUI 为 UE5 第三方插件）",
    "answer": "**UMG（UE5 内置）**：\n- 基于 Slate 框架，蓝图/C++ 双驱动，所见即所得。\n- 优点：和 UE5 生态深度融合、源码开放、可挂 Widget Component 进 3D 场景、材质可定制。\n- 缺点：复杂动效需手动搭、跨项目复用难、深层 Widget 树 Tick 开销不小。\n- 适合：3D 场景内 UI（血条、名牌）、HUD、需要自定义材质的 UI、和 Gameplay 深度交互。\n\n**FairyGUI（FGUI，UE5 第三方插件）**：\n- 独立编辑器，导出包体运行时加载。\n- 优点：动效系统强（时间轴、缓动）、组件复用好、跨引擎（UE5/Unity/Cocos）、编辑器高效。\n- 缺点：需集成插件、和 UE5 原生组件联动弱、调试不如 UMG 直观。\n- 适合：2D 重 UI 手游（卡牌、RPG 大量界面）、动效密集 UI、快速迭代。\n\n**选择**：重 UI 2D 手游 → FGUI；3D 游戏少量 UI、需要材质控制 → UMG；混用：HUD 用 UMG，菜单用 FGUI。\n\n**和 Unity 的对比**：Unity 对应 UGUI（内置）+ FGUI（插件）；UE5 对应 UMG（内置）+ FGUI（插件）。UMG 基于 Slate，UGUI 基于 GameObject+Component。\n\n**面试加分点**：UMG 底层是 Slate C++（编辑器 UI 也用 Slate）；Widget Component 可把 UMG 贴 3D 物体；FGUI 在 UE5 上需手动集成插件（非官方）；UMG 的 Tick 是按 Widget 树遍历，深层级要控制。",
    "tags": ["UMG", "FGUI", "对比", "UE5"]
}

part1["ui-002"] = {
    "question": "UMG Canvas Panel 的作用？为什么 UI 渲染选 Screen（Viewport）还是 Widget Component（3D World Space）？",
    "answer": "UMG 没有 Unity Canvas 的\"全局根\"概念，所有 UMG Widget 树根节点是 UMG Widget（如 Canvas Panel）。Canvas Panel 负责子 Widget 的绝对定位/锚定布局。\n\n**渲染方式**：\n\n**Screen / Viewport（对应 Unity Screen Space - Overlay）**：\n- `AddToViewport` 把 Widget 直接画到屏幕最上层，无相机。\n- 优点：最简单、永远在最前、性能最好。\n- 缺点：不能后处理、不能 3D 变换、不参与场景 Depth。\n- 适合：HUD、菜单、弹窗。\n\n**Widget Component（对应 Unity World Space Canvas）**：\n- 把 UMG Widget 贴到 3D 场景的 Mesh 平面上，参与场景渲染。\n- 优点：可 3D 变换、自动遮挡、有透视、可后处理。\n- 缺点：性能贵（参与场景渲染、每帧 Render Target）、需调 DPI Scale。\n- 适合：游戏内交互屏（电脑、招牌）、VR UI、世界空间 HUD。\n\n**Render Target 贴图（对应 Unity Screen Space - Camera）**：\n- Widget 渲染到 Render Target，再贴到场景材质上。\n- 适合：监视器画面、反射镜 UI。\n\n性能：AddToViewport 最快，Widget Component 最贵。\n\n**面试加分点**：UMG 没有\"Canvas Root\"强制要求，任意 Widget 都能 AddToViewport；Widget Component 内部用 Render Target + Transparent Material；VR UI 必须用 Widget Component（World Space）；UMG 的 DPI Scale 在 Widget Component 上要手动设。",
    "tags": ["UMG", "CanvasPanel", "WidgetComponent", "UE5"]
}

part1["ui-003"] = {
    "question": "为什么要把 UMG 拆分成多个 Widget Tree / Retainer Box？拆分的原则？",
    "answer": "UMG Slate 合批规则：**同一 Slate 批次内的 Widget 才合批**。但 Widget 树任意元素变化，整棵树会 Invalidate（重算几何/布局）。\n\n**问题**：一个大 Widget 树（整个界面），任何 UI 变化（血条、计时器）→ 整个界面 Invalidate，CPU 卡。\n\n**拆分原则**：\n\n**1. 静态/动态分离**：静态 UI（背景、标题）一个 Widget；动态 UI（血条、列表项、动画）独立子 Widget。动态变化只 Invalidate 自己的子树。\n\n**2. 频率分离**：高频更新（每帧血条）独立 Widget；低频更新（按钮点击）可共用。\n\n**3. Retainer Box**：UE5 特有，强制把子 Widget 渲染到离屏 Render Target 再贴回，隔离 Invalidate 传播，且能合批成一个 draw call。代价是额外 RT 内存。\n\n**4. 合批 vs Invalidate 权衡**：拆太细 → 每个 Widget 独立合批，draw call 增加；拆太粗 → Invalidate 范围大。平衡：动态部分用 Retainer Box 隔离，静态部分合并。\n\n**和 Unity 的对比**：Unity 拆子 Canvas；UE5 拆子 Widget Blueprint + Retainer Box。Unity 子 Canvas 独立 Rebuild；UE5 Retainer Box 独立 Render Target。\n\n**面试加分点**：Retainer Box 是 UMG 性能优化神器（隔离 + 合批）；UMG 的 Invalidate 比 Unity Rebuild 粒度更细（Slate 按需重算）；深层 Widget 树 Tick 顺序自底向上，要控制深度；用 `SInvalidationPanel`（C++）做更底层缓存。",
    "tags": ["UMG", "RetainerBox", "Invalidate", "拆分", "UE5"]
}

part1["ui-004"] = {
    "question": "图集（Texture Atlas / Paper2D Sprite Atlas）的作用？为什么 UMG UI 必须用图集？",
    "answer": "**1. 减少 Draw Call**：不同贴图的 UI 不能合批（材质不同）。同图集的 Brush 共享材质 → 合批到一个 draw call。100 个散图 = 100 draw call，1 个图集 = 1 draw call。\n\n**2. 减少内存**：散图各有 mipmap、padding 浪费；图集紧凑打包，内存利用率高；图集可整体压缩（ASTC/BC7）。\n\n**3. 带宽友好**：同图集的 Brush 在 GPU 纹理缓存命中率高，减少纹理切换。\n\n**UE5 做法**：\n- UMG 的 Image Widget 用 Brush（FSlateBrush）引用 Texture2D / Paper2D Sprite。\n- Paper2D Sprite 可配 Atlas（Sprite Sheet），多 Sprite 共享一张 Texture2D。\n- UE5 没有内置的\"运行时自动合图集\"功能，通常编辑时手动打 Atlas 或用 Paper2D。\n- 插件：UI 美术常用 Paper2D Sprite Atlas 或第三方 Dynamic Atlas 插件。\n\n**注意**：图集大小移动 1024/2048，PC 4096；按使用频率/界面分图集；动态加载 UI 用独立图集；图集内 padding 防 mipmap 渗色。UMG Brush 默认关 mipmap。\n\n**和 Unity 的对比**：Unity 有 SpriteAtlas 资源 + Late Binding；UE5 用 Paper2D Sprite Atlas 或手动 Texture2D，无原生 Late Binding，靠 Soft Object Path 异步加载。\n\n**面试加分点**：UMG Brush 的 Tiling 模式（Tile/Stretch）影响图集 Sprite 切边；UE5 的 Paper2D Sprite 支持九宫格；移动端 UMG draw call 控制关键就是图集 + 同材质；可写 Editor Utility 自动合并散图为 Atlas。",
    "tags": ["图集", "TextureAtlas", "Paper2D", "DrawCall", "UE5"]
}

part1["ui-005"] = {
    "question": "UMG UI 的 Overdraw 问题？和 3D 特效 Overdraw 的区别？",
    "answer": "UI Overdraw：多个 UMG Widget 叠加覆盖同一像素。\n\n**来源**：半透明 UI 面板叠加；背景图 + 文字 + 图标 + 装饰层；全屏特效 UI（渐变、光晕）；多个 Widget 树重叠。\n\n**和 3D 特效区别**：\n- UMG 全是 AlphaBlend，无 Early-Z（透明不写深度）。\n- UI 通常全屏，覆盖每个像素。\n- UI 层数容易多（一个界面 5-10 层）。\n- 移动端 UI Overdraw 是主要 GPU 开销之一。\n\n**检测**：\n- UE5 `ProfileGPU` 看 UI pass 耗时和 overdraw。\n- `r.Slate.AllowSlateOverdraw` 查看过绘制。\n- `stat Slate` 看 UMG 渲染统计。\n- Viewport → Buffer Visualizer → Shader Complexity。\n\n**优化**：\n- 减少不必要层级（合并装饰层）。\n- 静态背景烘焙成一张图（或用 Retainer Box 缓存）。\n- 隐藏不可见 UI（`SetVisibility(Hidden)` 或 `Collapsed`）而非 alpha=0（仍渲染）。\n- 减少全屏渐变/光晕。\n- 移动端 UI overdraw ≤3-4 层，PC ≤6。\n\n**和 Unity 的对比**：Unity 用 Scene 视图 Overdraw 模式 + Frame Debugger；UE5 用 ProfileGPU + Stat Slate。UMG 的 `Collapsed`（不占布局不渲染）比 Unity `SetActive(false)` 粒度更细（保留实例）。\n\n**面试加分点**：UMG 的 `SetVisibility` 有多档（Visible/Collapsed/Hidden/HitTestInvisible/All），Collapsed 省 render+layout；Retainer Box 能把多层静态 UI 烘成一张 RT 降 overdraw；半透明 UI 全屏渐变在移动端是 GPU 杀手。",
    "tags": ["Overdraw", "UMG", "性能", "移动端", "UE5"]
}

part1["ui-007"] = {
    "question": "多分辨率适配怎么做？UMG Anchors、DPI Scale、Safe Zone？",
    "answer": "**DPI Scale（对应 Unity Canvas Scaler）**：\n- Project Settings → Engine → User Interface → DPI Scale Rule。\n- Scale Rule：常选 `ShortestSide` 或 `LongestSide`。\n- DPI Curve：按最短边分档（如 <1080 缩 1.0，<1440 缩 1.5，<2160 缩 2.0）。\n- 设计基准分辨率（如 1920×1080）作为 1.0 DPI。\n\n**UMG Anchors（锚点）**：\n- 每个 Widget 在其 Slot 里设 Anchors（9 宫格 + 拉伸模式）。\n- 角落元素 anchor 四角；中心元素 anchor 中心；HUD 边缘元素 anchor 对应边。\n- 正确设锚点避免拉伸变形。\n\n**Safe Zone（对应 Unity SafeArea）**：\n- UMG 内置 SafeZone Widget，自动避开刘海、圆角、手势条。\n- 把 SafeZone 作为根容器，关键 UI 放里面。\n- 背景图可全屏（放 SafeZone 外）。\n\n**适配策略**：\n- DPI Scale + Anchors 适配主流比例。\n- 极端比例（19.5:9、iPad 4:3）用 SafeZone + 动态布局。\n- 横竖屏切换：监听 `OnViewportResized`，重排 UI。\n- 测试覆盖：16:9、18:9、19.5:9、4:3、20:9。\n\n**和 Unity 的对比**：Unity Canvas Scaler + Anchor + Screen.safeArea 脚本；UE5 DPI Scale + UMG Anchors + SafeZone Widget（内置，无需写脚本）。\n\n**面试加分点**：UE5 的 SafeZone 是原生 Widget，不用手写；DPI Scale Rule 选 `ShortestSide` 适配横竖屏都稳；`GetViewportSize`/`GetViewportScale` 运行时查询；Anchors 的拉伸模式（Stretch）适合全屏背景。",
    "tags": ["适配", "DPIScale", "SafeZone", "UMG", "UE5"]
}

part1["ui-008"] = {
    "question": "UMG Invalidate / Rebuild 是什么？怎么排查 UI Tick / Rebuild 性能问题？",
    "answer": "Invalidate：UMG Slate 标记 Widget 几何/布局/绘制为脏，下一帧重算。发生在 Widget 变化时（位置、颜色、文本内容、Brush 切换）。\n\n**触发 Invalidate**：\n- 任何 Widget 的 transform/Color/Text 变化。\n- Image Brush 切换。\n- Horizontal/Vertical/Grid Panel 重新布局。\n- 动态字体加新字符（字体纹理重建）。\n\n**问题**：大 Widget 树一次 Invalidate 涉及几千元素，CPU 卡；每帧 Invalidate = 持续卡顿。\n\n**排查**：\n1. UE5 Profiler → Slate 模块，看 `SWidget::Paint` / `Tick` / `Invalidate` 耗时。\n2. `stat Slate` 看每帧 Slate 更新/绘制时间。\n3. `stat UMG` 看 UMG 事件耗时。\n4. ProfileGPU 看 UI draw call。\n5. 用 `SlateInsights`（Slate 跟踪工具）精确定位。\n\n**优化**：\n- 拆 Widget 树（动态部分独立 Blueprint）。\n- 用 Retainer Box 隔离 Invalidate 传播。\n- 避免每帧改 UI（缓存、仅必要时改）。\n- UMG Layout Panel（Horizontal/Vertical/Grid）慎用，复杂列表用 List View。\n- 隐藏 UI 用 `SetVisibility(Collapsed)`（不 Tick 不 Render）而非 alpha=0。\n- 文字内容变化最小化（用 StringBuilder，避免每帧 string 拼接 GC）。\n\n**和 Unity 的对比**：Unity `Canvas.SendWillRenderCanvases` Rebuild；UE5 Slate `Tick` + `Invalidate`。Unity 是整 Canvas Rebuild；UE5 是脏 Widget 局部 Invalidate，粒度更细。\n\n**面试加分点**：UMG 的 `Invalidate(EInvalidateWidgetReason)` 可指定原因（Layout/Paint/...）做细粒度脏标记；Retainer Box 强制隔离；`bCanTick` 关闭不需要 Tick 的 Widget；List View 自带 Entry Widget Pool 避免大量 Item Tick。",
    "tags": ["Invalidate", "Rebuild", "UMG", "性能", "UE5"]
}

part1["ui-009"] = {
    "question": "UMG UI 和 Niagara 粒子叠加的方案？怎么避免 UI 粒子打断合批？",
    "answer": "问题：Niagara 粒子是场景 Actor，UMG Widget 是 Slate 渲染，两者材质体系不同，叠加时合批被打断。\n\n**方案一：UI 上的 Niagara（UI Particle 插件）**\n- 第三方插件把 Niagara 渲染到 UMG Widget。\n- 粒子和 UI 同 Render Target，可合批。\n- 缺点：需插件、性能略降。\n\n**方案二：分层渲染**\n- UI 用 AddToViewport（Screen），粒子用场景 Niagara。\n- 粒子在场景里渲染，UI 叠在最上。\n- 优点：粒子性能好（GPU 仿真）。\n- 缺点：合批断（不同渲染管线）。\n\n**方案三：UI 特效用 Material（Shader）**\n- 不用粒子，用材质做特效（流光、扫描、溶解、UV 动画）。\n- UMG Image + 特效材质。\n- 同材质合批不中断。\n- 适合简单特效（按钮流光、扫描线）。\n\n**方案四：UI 上叠 Sprite 序列帧**\n- 用 UMG Image 切换 Brush 模拟帧动画（Sprite Sheet）。\n- 合批友好。\n- 适合固定特效。\n\n**选择**：简单特效 → 材质或序列帧；复杂特效 → UI 粒子插件或分层渲染；性能优先 → 分层（接受合批断）。\n\n**和 Unity 的对比**：Unity 用 UIParticle 插件或分层 Canvas；UE5 用 UI Niagara 插件或 AddToViewport + 场景 Niagara。UE5 的 Widget Component 可把粒子放 3D 空间和 UI 遮挡。\n\n**面试加分点**：UMG 材质做流光用 `Time` 节点 + UV 平移；Retainer Box 能把多层 UI + 特效烘成一张 RT 合批；Niagara 可渲染到 Render Target 再贴 UMG Image；打断合批多几个 draw call 不一定是瓶颈，先 Profile 再优化。",
    "tags": ["UI粒子", "Niagara", "合批", "UMG", "UE5"]
}

part1["ui-010"] = {
    "question": "UMG Slate 的 Batching（合批）规则？什么情况会打断合批？",
    "answer": "合批条件（全部满足）：\n- 同一 Slate 批次（同 Widget 树/同 Retainer Box）。\n- 同一材质（含同 Texture / Atlas）。\n- 同一 Z-Order 层级。\n- 层级相邻（无不同材质的元素穿插）。\n\n**打断合批的因素**：\n\n**1. 不同图集/材质**：Widget 用不同 Texture（非同图集）。\n\n**2. 穿插渲染**：A（材质1）、B（材质2）、C（材质1），合批被 B 打断，A、C 无法合批（要按顺序渲染）。\n\n**3. 不同 Z-Order**：Slot Z-Order 不同不合批。\n\n**4. 不同 Texture**：字体纹理、图集分开。\n\n**5. Mask / Clipping**：UMG 的 Widget Clipping（Clip to Bounds）会打断合批。\n\n**6. Retainer Box 边界**：Retainer Box 内外不合批（独立 RT）。\n\n**7. Material Instance**：不同 MID（Material Instance Dynamic）参数不同视为不同材质，打断合批。\n\n**优化**：\n- Widget 按材质/图集分组排列，减少穿插。\n- 同类 UI（按钮组）用同图集。\n- 避免不必要的 Clipping。\n- 用 ProfileGPU / `stat Slate` 看 draw call 拆分原因。\n- 静态 UI 用 Retainer Box 合并。\n\n**和 Unity 的对比**：Unity 合批看 Canvas + 材质 + SortingLayer；UE5 合批看 Slate 批次 + 材质 + Z-Order。Unity 用 Frame Debugger；UE5 用 ProfileGPU + `stat Slate`。\n\n**面试加分点**：UMG 的 `Z-Order` 在 Slot 里设（不是 SortingLayer）；Retainer Box 是 UE5 合批利器（强合并 + 隔离）；Slate 底层用 Vertex Buffer 批处理；`stat SlateDebug` 看详细 batch 信息；MID 会破坏合批，能用顶点色就用顶点色。",
    "tags": ["合批", "Batching", "UMG", "Slate", "UE5"]
}

part1["ui-012"] = {
    "question": "UMG Shader 用 Material 和 MID（Material Instance Dynamic）的坑？",
    "answer": "问题：UMG Widget 共享材质才能合批，但有时要 per-element 不同效果（如不同颜色的流光）。\n\n**Material 实例化（MID）**：\n- `CreateDynamicMaterialInstance` 创建 MID → 合批断。\n- 100 个 Widget 各一个 MID = 100 draw call。\n- 不可取。\n\n**MaterialPropertyBlock 在 UE5 的对应**：\n- UE5 有 `ScalarParameterValue` / `VectorParameterValue` on MID，但和 Unity 一样，不同参数的 MID 视为不同材质，打断 Slate 合批。\n- UMG Slate 合批要求同材质实例，MID 破坏合批。\n\n**替代方案**：\n\n**1. 顶点色（Vertex Color）**：\n- UMG Widget 的 Color and Opacity（Tint）是 per-instance，材质里乘顶点色。\n- 不破坏合批。\n- 适合颜色变化。\n\n**2. Brush Tint**：\n- UMG Image 的 Tint 是 per-instance，等价顶点色。\n\n**3. 分组多材质**：\n- 同效果的 Widget 用同材质，分组渲染。\n- 接受 draw call 增加。\n\n**4. 烘焙到贴图**：\n- per-element 效果预烘焙到 sprite，不用 shader。\n\n**5. 全屏后处理式特效**：\n- 整个 UI 渲染后做一次特效（流光扫过），不分 per-element。\n- 用 Post Process Material 或 Retainer Box 后材质。\n\n要点：UMG 要 per-element 效果，优先顶点色/Tint；真要材质参数，接受 draw call 或用 Retainer Box 隔离。\n\n**和 Unity 的对比**：Unity UGUI 不支持 MaterialPropertyBlock（CanvasRenderer 限制）；UE5 UMG MID 破坏合批。两者都推荐用顶点色。\n\n**面试加分点**：UMG 的 Tint 走顶点色通道，免费 per-instance；Retainer Box 内的 Widget 共享一个 RT，可对 RT 整体做材质特效（一次 draw call）；Post Process Material 的 Blending Location 可插入 UI 后处理；能用顶点色就别开 MID。",
    "tags": ["UIShader", "Material", "MID", "UMG", "UE5"]
}

part1["ui-013"] = {
    "question": "UMG 的基本组件有哪些？Image、Text Block、Button、CheckBox 各自的用途？",
    "answer": "**核心 Widget**：\n- **Canvas Panel**：绝对定位容器（对应 Unity Canvas 的布局功能）。\n- **Panel Widgets**：Horizontal Box / Vertical Box / Grid Panel / Wrap Box / Uniform Grid Panel（对应 Unity Layout Group）。\n- **Image**：显示 Texture/Sprite/Material，支持 Simple/Sliced/Tiled 模式（对应 Unity Image）。\n- **Text Block**：显示文本（对应 Unity Text/TMP）。\n- **Rich Text Block**：富文本（支持样式标记）。\n- **Button**：按钮（对应 Unity Button）。\n- **CheckBox**：开关（对应 Unity Toggle）。\n- **Slider**：滑块（对应 Unity Slider）。\n- **Scroll Box**：滚动区域（对应 Unity ScrollRect）。\n- **Editable Text / EditableTextBox**：输入框（对应 Unity InputField）。\n- **Border**：带边框/背景的容器，可设 Clip（对应 Unity RectMask2D）。\n- **Retainer Box**：渲染子 Widget 到 RT 再贴回（UE5 特有，合批/隔离用）。\n- **Safe Zone**：避开刘海/手势条（对应 Unity SafeArea 脚本）。\n- **Spacer**：占位空白。\n- **Invalidation Box**：缓存 Widget 几何，减少 Invalidate（UE5 特有）。\n\n**Image 模式**：\n- Brush Tiling：None（Simple）/ Horizontal/Vertical/Both（Tiled）。\n- Sliced：九宫格（需 Sprite 设 border）。\n- 对应 Unity Image 的 Simple/Sliced/Tiled/Filled。\n\n**和 Unity 的对比**：Unity 用 GameObject + Component；UE5 用 Widget（UObject，非 Actor）。UMG 的 Panel Widget 同时承担布局 + 容器；Unity 拆成 Layout Group + 容器。\n\n**面试加分点**：UMG 的 Widget 是 Slate 的 UMG 包装层；Invalidation Box 是性能利器（缓存几何）；Retainer Box 做合批和材质特效；Text Block 默认用 Canvas Font，可换 SDF Font。",
    "tags": ["UMG", "Widget", "组件", "基础", "UE5"]
}

part1["ui-015"] = {
    "question": "UMG 的输入事件系统怎么工作？Slate HitTest 怎么优化？",
    "answer": "UMG 输入：基于 Slate 的输入路由系统。\n\n**工作流程**：\n1. 输入（点击/触摸）→ Slate 获取屏幕坐标。\n2. HitTest：从顶层 Widget 树到底层，对每个 Widget 做命中检测（按 Z-Order 和 Visibility）。\n3. 命中的 Widget 按 Z-Order 排序，最上层接收事件。\n4. 派发事件（On Clicked / On Hovered / On Pressed / On Released）。\n5. 事件可冒泡或拦截（按 Widget 的 Visibility 设置）。\n\n**HitTest 代价**：\n- 每次输入对整棵 Widget 树做检测。\n- Widget 多（上千）→ HitTest 慢。\n- 每帧都跑（即使没输入，Hover 检测）。\n\n**优化**：\n\n**1. Visibility 设置**：\n- `Visible`：可见可交互（参与 HitTest）。\n- `HitTestInvisible`：可见不可交互（不参与 HitTest，省检测）。\n- `SelfHitTestInvisible`：自己不参与，子可参与。\n- `Hidden`/`Collapsed`：不渲染不交互。\n- 纯装饰 Widget（背景图、文字）设 `HitTestInvisible`，可减少 50%+ HitTest。\n\n**2. 减少 Widget 层级**：深层 Widget 树 HitTest 慢，用 Panel Widget 扁平化。\n\n**3. 按需禁用**：非交互状态用 `SetIsEnabled(false)` 或 `SetVisibility(HitTestInvisible)`。\n\n**和 Unity 的对比**：Unity EventSystem + GraphicRaycaster + Raycast Target 勾选；UE5 Slate HitTest + Visibility 多档。Unity 要手动取消 Raycast Target；UE5 用 Visibility 档位控制。\n\n**面试加分点**：UMG 的 `HitTestInvisible` 是 UI 性能优化关键（对应 Unity 取消 Raycast Target）；Slate HitTest 自顶向下按 Z-Order；`On Mouse Enter`/`On Mouse Leave` 做 Hover 反馈；`SetIsEnabled` 整组禁用；深层 Widget 树 Tick + HitTest 都贵，要控制深度。",
    "tags": ["UMG", "HitTest", "Slate", "输入", "优化", "UE5"]
}

part1["ui-018"] = {
    "question": "UMG 的动画方案？UMG Animation、Timeline、Lerp？",
    "answer": "**UMG Animation（Widget Blueprint 内置）**：\n- Widget Blueprint 的 Animation 面板，时间轴编辑，可视化。\n- 优点：设计师可编辑、支持曲线、可绑定任意 Widget 属性。\n- 缺点：每个动画一个 Track，管理麻烦；播放有开销。\n- 适合：复杂 UI 动画（弹出、过场、状态切换）。\n\n**Timeline（C++ / Blueprint 通用）**：\n- 代码驱动的时间轴，可插值任意值。\n- 优点：灵活、可程序控制。\n- 缺点：每动画一个 Timeline 对象。\n- 适合：程序控制的 UI 动画（弹出、滑动、淡入）。\n\n**Lerp + Tick**：\n- 每帧 `Lerp(a, b, alpha)` 插值，手动设 alpha。\n- 优点：最轻量、可控。\n- 缺点：要手写 Tick 逻辑。\n- 适合：简单程序动画（血条平滑、淡入）。\n\n**选择**：简单程序动画 → Lerp + Tick；设计师做的复杂动画 → UMG Animation；状态切换 → Timeline；FGUI 项目 → FGUI 动效。\n\n注意：UI 动画每帧改 Widget 属性 → Invalidate，控制频率和范围。\n\n**和 Unity 的对比**：Unity DOTween（代码 tween）/ Animation Clip / Animator；UE5 UMG Animation / Timeline / Lerp。UE5 没有原生 DOTween 等价，常用 Timeline + Lerp 或第三方 tween 插件。\n\n**面试加分点**：UMG Animation 的 `PlayAnimation` / `Reverse` / `SetPlaybackSpeed` 灵活控制；Timeline 的 Event Track 可触发自定义事件；Lerp + `FMath::SmoothStep` 缓动；动画期间 Widget 持续 Invalidate，长动画要评估性能；Retainer Box 可缓存动画首帧避免重复计算。",
    "tags": ["动画", "UMGAnimation", "Timeline", "Lerp", "UE5"]
}

part1["ui-020"] = {
    "question": "UMG UI 的 Loading 流程？怎么避免卡顿？",
    "answer": "卡顿来源：加载 UI Widget Blueprint + 资源（贴图、字体）瞬间内存暴涨；实例化大量 Widget；初始化逻辑（绑定事件、数据填充）。\n\n**优化流程**：\n\n**1. 异步加载**：\n- `LoadObjectAsync` / `StreamableManager` 异步加载资源。\n- `UAssetManager` 的 async load（对应 Unity Addressables）。\n- 资源分帧加载，不一次性。\n- 加载进度条显示。\n\n**2. 预加载**：\n- 常用 UI（HUD）开局加载，常驻内存。\n- 非常用 UI 按需加载，退出卸载。\n\n**3. 分帧实例化**：\n- 大列表分帧创建（每帧 10 项）。\n- 用 Timeline / Tick 分帧。\n- UMG List View 自带分帧实例化（Entry Widget Pool）。\n\n**4. 对象池**：\n- UI Widget 池化（按钮、列表项）。\n- 复用而非新建。\n- List View / Tile View 内置 Entry Widget Pool。\n\n**5. 资源依赖管理**：\n- Pak/Chunk + UAssetManager 管理依赖。\n- 引用计数卸载（避免重复加载/卸载）。\n- `TSoftObjectPtr` / `Soft Object Path` 延迟加载。\n\n**6. Loading 界面**：\n- 加载时显示 Loading 界面（独立 Widget，最简）。\n- 加载完成后切换。\n- 过场动画掩盖加载。\n\n**7. 渐进显示**：\n- UI 出现时分元素淡入（UMG Animation sequence）。\n- 掩盖初始化时间。\n\n注意：移动端内存有限，加载大 UI 前先卸载旧 UI。\n\n**和 Unity 的对比**：Unity `Resources.LoadAsync` / Addressables；UE5 `StreamableManager` / `UAssetManager` / `LoadObjectAsync`。Unity 用协程分帧；UE5 用 Timeline / Tick / Async Task。\n\n**面试加分点**：UMG List View 的 Entry Widget Pool 自动分帧 + 复用；`UAssetManager` 的 `LoadPrimaryAssets` 做分块加载；`SetVisibility(Collapsed)` 隐藏的 Widget 不占渲染；Loading 界面用独立 Root Widget 避免和主 UI 树耦合。",
    "tags": ["Loading", "卡顿", "异步", "UAssetManager", "UMG", "UE5"]
}

part1["ui-022"] = {
    "question": "UMG 的分辨率无关设计？怎么保证不同分辨率显示一致？",
    "answer": "原则：以设计分辨率为基准，等比缩放，关键元素不被裁剪。\n\n**DPI Scale 配置（对应 Canvas Scaler）**：\n- Project Settings → DPI Scale Rule：`ShortestSide`（推荐）。\n- DPI Curve：设计分辨率（1920×1080）为 1.0，按最短边分档缩放。\n- 横竖屏都稳。\n\n**UMG Anchors 策略**：\n- 角落元素：anchor 四角（stretch 时 top/bottom/left/right=0）。\n- 中心元素：anchor 中心。\n- HUD 边缘元素：anchor 对应边。\n- 全屏背景：anchor 拉伸四角。\n\n**Safe Zone**：\n- 刘海/圆角/手势条区域不放关键 UI。\n- SafeZone Widget 自动适配（内置，无需脚本）。\n\n**极端比例处理**：\n- 19.5:9（长屏）：两侧留黑边或拉伸背景。\n- 4:3（iPad）：上下留黑边或重新布局。\n- 方案：背景全屏拉伸 + UI 元素 anchor 边缘 + SafeZone。\n\n**测试**：\n- Device Profiles 模拟各分辨率。\n- 真机测试覆盖主流比例。\n- 关注：UI 是否被裁、是否留大黑边、文字是否溢出。\n\n**美术规范**：\n- 设计稿按设计分辨率。\n- 字体大小用相对值（UMG 自动 DPI 缩放）。\n- 图标尺寸考虑缩放后可点击（最小 44pt）。\n\n**和 Unity 的对比**：Unity Canvas Scaler + Anchor + Screen.safeArea；UE5 DPI Scale + UMG Anchors + SafeZone Widget。UE5 的 SafeZone 是原生 Widget，不用写脚本。\n\n**面试加分点**：UE5 的 DPI Scale 在 Project Settings 全局配，所有 UMG 自动应用；`GetViewportSize` + `GetViewportScale` 运行时查询；SafeZone 支持平台原生（iOS/Android/Console）；`OnViewportResized` 委托响应分辨率变化。",
    "tags": ["分辨率", "适配", "DPIScale", "SafeZone", "UMG", "UE5"]
}

part1["ui-023"] = {
    "question": "UMG UI 和 3D 场景的交互？点击 3D 物体？",
    "answer": "**3D 物体点击**：\n\n**1. Line Trace（射线检测）**：\n- 从相机发射射线，检测 Collision。\n- `GetPlayerController->GetHitResultUnderCursor`。\n- 命中物体处理点击。\n- 优点：精确。\n- 缺点：每点击一次 trace，UI 也要先检查。\n\n**2. UE5 Input 事件**：\n- Actor 挂 `OnClicked` / `OnBeginCursorOver` 事件（需组件启用碰撞）。\n- PlayerController 的 `bEnableClickEvents` / `bEnableMouseOverEvents`。\n- 优点：和 UI 统一输入路由。\n- 支持 hover/drag。\n\n**3. UI 拦截**：\n- 点击先到 UMG，UI 命中则不传 3D。\n- `GetHitResultUnderCursor` 先检测 UI（Slate HitTest）。\n- 检查鼠标是否在 UI 上。\n\n**3D HUD（血条、名字）**：\n\n**方案一：Screen Space UMG**：\n- HUD 是 UMG Widget，每帧把 3D 位置投影到屏幕。\n- `PlayerController->ProjectWorldLocationToScreen`。\n- HUD 永远在最前。\n- 缺点：3D 物体被遮挡时 HUD 还显示（需检测遮挡）。\n\n**方案二：Widget Component（对应 World Space Canvas）**：\n- HUD 作为 3D 物体，在场景里。\n- 优点：自动遮挡、有透视。\n- 缺点：性能贵（参与场景渲染）、缩放需调整。\n\n**选择**：大量 HUD → Screen Space UMG + 遮挡检测；少量重要 HUD → Widget Component。\n\n**和 Unity 的对比**：Unity `Physics.Raycast` / `PhysicsRaycaster` + EventSystem；UE5 `Line Trace` / `GetHitResultUnderCursor`。Unity `Camera.WorldToScreenPoint`；UE5 `ProjectWorldLocationToScreen`。\n\n**面试加分点**：UE5 的 Widget Component 支持 World Space + Screen Space 两种；`ProjectWorldLocationToScreen` 配合 Slate HitTest 做 UI 拦截；遮挡检测用 LineTrace 到物体确认无墙挡；大量 HUD 用一个 UMG 容器 + 池化，不要每角色一个 Widget Component。",
    "tags": ["3D交互", "LineTrace", "HUD", "WidgetComponent", "UE5"]
}

part1["ui-024"] = {
    "question": "UMG 的图集打包策略？按什么分？",
    "answer": "策略原则：**按使用场景分组，平衡合批和内存**。\n\n**分组方式**：\n\n**1. 按界面分**：每个界面（主菜单、背包、商店）独立图集。加载界面时加载图集，退出卸载。优点：内存可控。缺点：跨界面共用素材重复。\n\n**2. 按功能分**：通用 UI（按钮、边框、图标）一个共享图集，常驻。特殊界面素材独立图集。优点：复用、合批好。缺点：共享图集可能大。\n\n**3. 按加载时机分**：启动加载（HUD、主菜单）；按需加载（商店、设置）；临时（活动界面）。\n\n**大小控制**：单图集移动 1024-2048，PC 4096；单 sprite ≤256（移动）；padding 2-4px。\n\n**UE5 做法**：\n- 用 Paper2D Sprite Atlas（编辑时打包）或手动 Texture2D。\n- Pak/Chunk 分包：按界面/功能分包，`UAssetManager` 管理。\n- 共享 UI（按钮、图标）一个 Chunk 常驻。\n- 动态加载 UI 用独立 Chunk（按需加载）。\n\n**优化**：\n- 定期审查图集利用率（没用的 sprite 删除）。\n- 图集合并/拆分根据实际使用调整。\n- 内存紧张时降级图集分辨率（Device Profile 切 LOD）。\n\n**和 Unity 的对比**：Unity 有 SpriteAtlas 资源 + Include in Build + Late Binding + Variant；UE5 用 Paper2D Sprite Atlas 或手动 Texture2D + Pak/Chunk + `TSoftObjectPtr` 异步加载，无原生 Late Binding。\n\n**面试加分点**：UE5 的 Pak/Chunk + UAssetManager 是原生分包方案（对应 Unity Addressables）；`TSoftObjectPtr` / `Soft Object Path` 做延迟加载；Device Profile 按设备分级加载图集；Editor Utility 自动检查图集利用率；Paper2D Sprite 支持九宫格 border。",
    "tags": ["图集", "打包", "Pak", "Chunk", "UAssetManager", "UE5"]
}

part1["ui-025"] = {
    "question": "UMG UI 的性能监控和优化流程？",
    "answer": "监控工具：\n\n**1. UE5 Profiler**：\n- Slate 模块：`SWidget::Paint` / `Tick` / `Invalidate` 耗时。\n- Render：UI draw call 数、batch 数。\n- Memory：UI 资源内存。\n- `stat Slate` / `stat UMG` 看每帧统计。\n\n**2. ProfileGPU**：\n- 逐 draw call 看 UI 渲染。\n- 找打断合批的原因。\n- 看 UI pass 耗时。\n\n**3. Slate Insights**：\n- Slate 跟踪工具，精确 Widget 级别耗时。\n- 看 Tick / Paint / Invalidate 路径。\n\n**4. 内存 Profiler**：\n- `Memory Report` 命令。\n- 看 UI 资源占用。\n- 找大贴图、未卸载资源。\n- `obj list class=Texture2D` 看贴图。\n\n**优化流程**：\n\n**1. 定位瓶颈**：\n- CPU 卡 → Slate Tick？Invalidate？实例化？\n- GPU 卡 → draw call 多？overdraw 高？\n- 内存高 → 贴图大？图集多？\n\n**2. 针对优化**：\n- Slate Tick：拆 Widget 树、用 Invalidation Box 缓存。\n- Draw Call：合批、图集、减少穿插、Retainer Box。\n- Overdraw：减少层级、`Collapsed` 隐藏。\n- 内存：压缩、裁剪、按需加载。\n\n**3. 测试验证**：真机测试（不只编辑器）；低端机测试；长时间运行（内存泄漏）。\n\n**4. 持续监控**：上线后 telemetry 收集性能数据；定期 review 热点界面。\n\n**和 Unity 的对比**：Unity Profiler UI Module + Frame Debugger + Overdraw 视图；UE5 Profiler Slate + ProfileGPU + Slate Insights + `stat Slate`。\n\n**面试加分点**：`stat Slate` 看每帧 Slate 更新/绘制时间；`stat UMG` 看 UMG 事件；`r.Slate.AllowSlateOverdraw` 查看过绘制；`SlateInsights` 是 UE5 的 UI 性能分析利器；Invalidation Box 缓存 Widget 几何减少 Tick；自动化用 Editor Utility 跑性能回归。",
    "tags": ["监控", "性能", "Profiler", "UMG", "Slate", "UE5"]
}

# ============ Part 2 (19 题) ============
part2 = {}

part2["ui-026"] = {
    "question": "UE5 UMG 和 Slate 的区别？什么时候用 Slate C++？",
    "answer": "**UMG（Unreal Motion Graphics）**：\n- UE5 主流 UI 系统，蓝图/C++ 双驱动。\n- Widget Blueprint 可视化编辑，所见即所得。\n- 基于 Slate 包装层。\n- 适合：游戏内 UI、HUD、菜单、设计师友好。\n\n**Slate**：\n- UE5 底层 UI 框架，纯 C++，声明式语法。\n- 编辑器 UI 全用 Slate。\n- 性能更好（无 UMG 包装开销）。\n- 适合：编辑器工具、自定义 Widget、性能敏感 UI。\n\n**区别**：\n\n| 维度 | UMG | Slate |\n|------|-----|-------|\n| 编辑 | Widget Blueprint 可视化 | 纯 C++ 声明式 |\n| 蓝图 | 支持 | 不支持 |\n| 性能 | 中等（包装开销） | 高 |\n| 生态 | 游戏主流 | 编辑器主流 |\n| 学习 | 直观 | C++ + Slate 语法 |\n\n**适合**：\n- 游戏运行时 UI：UMG 首选。\n- 编辑器工具 UI：Slate 首选（UMG 也行）。\n- 自定义复杂 Widget：Slate C++ 写底层，UMG 包装。\n- 性能敏感 UI：Slate 或 UMG + Invalidation Box。\n\n**未来**：UE5 推动 UMG，Slate 是基石。两者共存，UMG 不会替代 Slate。\n\n**和 Unity 的对比**：Unity UGUI（GameObject+Component）+ UI Toolkit（Web 风格）；UE5 UMG（Blueprint）+ Slate（C++）。Unity UI Toolkit 对应 Slate 的\"非 GameObject\"思路；UMG 对应 UGUI 的\"可视化编辑\"。\n\n**面试加分点**：UMG 的 Widget 底层是 `SWidget`（Slate）；可自定义 Slate Widget 再用 UMG 包装（`UWidget` 派生）；Slate 的声明式语法 `SNew(SButton).Text(FText::FromString(\"...\"))`；编辑器插件 UI 必须 Slate 或 UMG；`Invalidation Box` 是 UMG 包装 Slate 缓存机制的性能工具。",
    "tags": ["UMG", "Slate", "对比", "UE5"]
}

part2["ui-027"] = {
    "question": "UMG 的 Safe Zone 适配具体怎么做？蓝图/C++ 示例？",
    "answer": "Safe Zone：屏幕安全区域（避开刘海、圆角、手势条）。\n\n**UMG 原生做法（推荐）**：\n- Widget Blueprint 里放一个 SafeZone Widget 作为根容器。\n- SafeZone 自动适配平台（iOS/Android/Console）。\n- 所有关键 UI 放 SafeZone 内。\n- 背景图可全屏（放 SafeZone 外）。\n\n**SafeZone 属性**：\n- `Safe Area Padings`：手动覆盖（一般不设，用自动）。\n- `Left/Right/Top/Bottom`：勾选要适配的边。\n- `Scale Safe Zone Ratio`：缩放比例（一般 1.0）。\n\n**C++ 动态查询**：\n```cpp\nFMargin SafeZone = FCoreDelegates::GetSafeZoneSize.Execute();\n// 或\nFVector4 SafeZone = FSlateApplicationBase::Get().GetSafeZoneSize();\n```\n\n**监听安全区变化（横竖屏切换）**：\n```cpp\nvoid UMyWidget::NativeOnSafeFrameChanged()\n{\n    Super::NativeOnSafeFrameChanged();\n    // 重新布局\n}\n```\n\n**使用**：\n- 根 Widget 下挂一个 SafeZone 容器。\n- 所有关键 UI 放这个容器内。\n- 背景图可全屏（不被 SafeZone 限制）。\n\n**注意**：\n- iOS 刘海、Android 不同机型各异。\n- 横竖屏切换 SafeZone 变化，SafeZone Widget 自动响应。\n- 旧设备无 SafeZone（全屏），自动兼容。\n\n**和 Unity 的对比**：Unity 需写 `SafeAreaFitter` 脚本读 `Screen.safeArea`；UE5 SafeZone 是原生 Widget，无需脚本，自动响应变化。\n\n**面试加分点**：UE5 SafeZone 支持 `On Safe Frame Changed` 事件响应横竖屏切换；`Safe Area Padings` 可手动微调；SafeZone 底层调 `FPlatformMisc::GetSafeZoneArea`；Console 平台（PS5/Xbox）也支持 SafeZone（TV 过扫）。",
    "tags": ["SafeZone", "适配", "UMG", "UE5"]
}

part2["ui-028"] = {
    "question": "UMG Widget 的对象池怎么实现？和特效池的区别？",
    "answer": "UMG Widget 池和特效池类似，但要注意 Widget 树层级。\n\n**实现（C++）**：\n```cpp\nclass UWidgetPool\n{\n    TSubclassOf<UUserWidget> WidgetClass;\n    UPanelWidget* PoolParent;\n    TArray<UUserWidget*> Pool;\n\npublic:\n    UUserWidget* Get(UPanelWidget* Parent)\n    {\n        UUserWidget* Widget;\n        if (Pool.Num() > 0)\n        {\n            Widget = Pool.Pop();\n            Parent->AddChild(Widget);\n            Widget->SetVisibility(ESlateVisibility::Visible);\n        }\n        else\n        {\n            Widget = CreateWidget<UUserWidget>(GetWorld(), WidgetClass);\n            Parent->AddChild(Widget);\n        }\n        return Widget;\n    }\n\n    void Return(UUserWidget* Widget)\n    {\n        Widget->RemoveFromParent();\n        PoolParent->AddChild(Widget);\n        Widget->SetVisibility(ESlateVisibility::Collapsed);\n        Pool.Add(Widget);\n    }\n};\n```\n\n**UMG 内置 Pool**：\n- List View / Tile View 自带 Entry Widget Pool（推荐用）。\n- `SetEntryWidgetClass` 设模板，自动复用。\n\n**和特效池区别**：\n- Widget 池要处理 AddChild/RemoveFromParent（Widget 树层级），改变父节点会触发 Invalidate。\n- Widget 复用要重置状态（颜色、文本、回调）。\n- Widget 池的 parent 要正确（同 Widget 树内才能合批）。\n\n**注意**：AddChild/RemoveFromParent 性能差（重新计算层级），尽量减少；复用时清理事件监听（避免内存泄漏）；池容量上限，超出销毁；预热度（开局预创建）。\n\n**典型用例**：列表项、弹窗、提示气泡、伤害数字。\n\n**和 Unity 的对比**：Unity `SetParent` + `SetActive`；UE5 `AddChild` + `SetVisibility`。Unity 改父节点触发 Canvas Rebuild；UE5 改父节点触发 Slate Invalidate。\n\n**面试加分点**：UMG List View / Tile View 内置 Entry Widget Pool（`UListView`），优先用；`SetVisibility(Collapsed)` 不渲染不 Tick；`RemoveFromParent` 后 Widget 仍存在（UObject），可复用；池要预热度 + 上限；复用时 `NativeOnListItemObjectSet` 重置状态。",
    "tags": ["WidgetPool", "对象池", "UMG", "ListView", "UE5"]
}

part2["ui-029"] = {
    "question": "UMG 的材质（Material）怎么写？和普通 3D 材质的区别？",
    "answer": "区别：\n- UMG 材质要兼容 Slate 的顶点格式（顶点色、UV）。\n- UMG 不需要光照（Unlit）。\n- UMG 要支持 Clipping（Border / Widget Clipping）。\n- UMG 用 Slate 合批，不能 per-instance MID（破坏合批）。\n- UMG 材质 Domain 通常设 `User Interface`。\n\n**基础 UMG Material 设置**：\n- Material Domain: `User Interface`。\n- Blend Mode: `Translucent`。\n- Shading Model: `Unlit`。\n- 不写深度（ZWrite Off）。\n- 顶点色 tint：`col * vertexColor`。\n\n**关键节点**：\n- `VertexColor`：per-instance tint（对应 Unity UI 顶点色）。\n- `Texture Sample`：贴图采样。\n- `Time`：时间（流光、动画）。\n- `Absolute UV` / `View Size`：屏幕 UV（全屏特效）。\n\n**Clipping 支持**：\n- UMG 的 Border / Widget Clipping 通过 `SlateBrush` 的 clip rect 传给 shader。\n- 材质里用 `SlateUVs` / `ClipRect` 参数做裁剪。\n\n**和普通 3D 材质区别**：\n- 3D 材质：有光照、PBR、深度、阴影。\n- UMG 材质：Unlit、透明、无深度、顶点色 tint、Slate 合批。\n\n**要点**：\n- UMG 材质要轻量（UI 数量多）。\n- 能用顶点色就别开 MID。\n- 流光/扫描用 `Time` + UV 动画，不分 per-element。\n\n**和 Unity 的对比**：Unity UI Shader 要支持 `unity_GUIZTestMode` + Stencil + `_ClipRect`；UE5 UMG 材质用 `User Interface` Domain，Slate 自动处理 Clip 和 Z-Order。Unity Shader 要手写 Stencil；UE5 不需要（Slate 层处理）。\n\n**面试加分点**：UMG 材质 Domain 选 `User Interface` 自动配 Slate 顶点格式；`VertexColor` 是免费的 per-instance tint；Retainer Box 可对子 Widget 整体应用材质（一次 draw call）；`GetViewportSize` / `ViewSize` 节点做全屏特效；UI 材质要关 Depth Write 避免 3D 深度污染。",
    "tags": ["UMG", "Material", "Slate", "UIShader", "UE5"]
}

part2["ui-030"] = {
    "question": "UMG UI 的描边、阴影、发光怎么做？性能影响？",
    "answer": "**描边（Outline）**：\n- UMG Text Block 没有原生描边组件。\n- 方案一：用富文本或 SDF 字体 + 材质描边（shader 内算，0 顶点增加，质量好）。\n- 方案二：复制 Text Block 4 份偏移（上下左右）—— 顶点数 ×5，性能差，不推荐。\n- 推荐用 SDF 字体材质做描边。\n\n**阴影（Shadow）**：\n- UMG Text Block 有 `Shadow Offset` + `Shadow Color` 属性，内置。\n- 或 SDF 字体材质做阴影（质量好）。\n- Image 阴影：复制一份偏移，或用 Border 做投影。\n\n**发光（Glow）**：\n- UMG 无内置 Bloom。\n- 方案一：Bloom 后处理（UI 参与 Bloom，UI 用 Screen Space + 后处理相机）。\n- 方案二：SDF 字体材质的 Glow（shader 内算）。\n- 方案三：叠加一张发光 sprite（UMG Image + 加色混合）。\n- 方案四：UI 材质的 Emissive + Bloom。\n\n**性能对比**：\n- 复制 Widget 描边/阴影：顶点 ×2-5，大量文字时性能差。\n- SDF 材质：0 顶点增加，shader 计算，性能好。\n- Bloom：全屏后处理，移动端慎用。\n\n**建议**：\n- 文字描边/阴影 → SDF 字体材质或 Text Block 内置 Shadow。\n- 图像发光 → 叠加 sprite 或材质 Emissive。\n- 移动端慎用复制描边（顶点爆）。\n- 关键发光用 Bloom（控制阈值）。\n\n**和 Unity 的对比**：Unity TMP SDF 描边/阴影/Glow；UE5 UMG Text Block 内置 Shadow + SDF 字体材质。Unity Outline 组件顶点 ×5；UE5 复制 Widget 同样问题。\n\n**面试加分点**：UE5 UMG 的 Text Block 内置 `Shadow Offset`/`Shadow Color` 免费阴影；SDF 字体（Canvas Font 转 SDF）材质做高质量描边/发光；`Outline` 属性（部分 Widget 有）控制描边；Bloom 阈值调高避免 UI 糊；移动端用材质模拟 Glow 不用 Bloom。",
    "tags": ["描边", "阴影", "发光", "SDF", "UMG", "UE5"]
}

part2["ui-032"] = {
    "question": "UMG Image 的 Fill Type 怎么用？血条、技能 CD？",
    "answer": "UMG Image 的 Brush 支持填充类型（对应 Unity Filled）。\n\n**UMG Brush 设置**：\n- Image Widget → Appearance → Brush。\n- Tiling：None（Simple）/ Horizontal/Vertical/Both（Tiled）。\n- 对应 Unity Image 的 Simple/Sliced/Tiled/Filled。\n- Fill：UE5 用材质或 ProgressBar Widget 实现进度。\n\n**血条**：\n- 用 UMG 的 ProgressBar Widget（内置进度条，`SetPercent`）。\n- 或用 Image + 材质做进度（材质里用参数控制进度）。\n- 平滑过渡：Lerp + Tick 缓动 `Percent`。\n- 受伤时闪红（叠加一层红色 Image，逐渐淡）。\n\n**技能 CD**：\n- 用材质做径向进度（Radial 360，shader 内算）。\n- 或 ProgressBar + 圆形遮罩材质。\n- 中心放技能图标。\n- CD 期间暗色 overlay。\n- 完成时闪烁提示。\n\n**圆形进度**：\n- 材质做 Radial 360（shader 内 `atan2` 算角度）。\n- 起点可配（顶部、右侧）。\n\n**注意**：\n- 每帧改进度 → Invalidate，控制频率。\n- 血条平滑用 Lerp，不要每帧设（按变化设）。\n- 多个血条用 Retainer Box 隔离（避免互相 Invalidate）。\n\n**替代**：材质内做进度（mask + 时间参数），性能更好。\n\n**和 Unity 的对比**：Unity Image 的 Filled 模式（Fill Method/Amount/Origin）；UE5 用 ProgressBar Widget 或材质做进度。Unity 内置 Filled；UE5 圆形进度要材质。\n\n**面试加分点**：UMG 的 ProgressBar 内置 `SetPercent` + `Fill Color`；圆形进度用材质的 `Time` + `atan2`；Retainer Box 隔离血条 Invalidate；材质做进度比 ProgressBar 性能好（不每帧 Invalidate）；多个 HUD 血条共享一个材质实例 + 顶点色 per-instance。",
    "tags": ["Fill", "血条", "CD", "ProgressBar", "UMG", "UE5"]
}

part2["ui-033"] = {
    "question": "UMG 的 Editable Text 怎么用？移动端虚拟键盘适配？",
    "answer": "**Editable Text / EditableTextBox**：\n- UMG 文本输入 Widget，支持单行/多行、密码模式、字符限制。\n- `EditableTextBox`（带框）/ `EditableText`（无框）。\n- 属性：`Is Password`、`Maximum Length`、`Keyboard Type`（对应 Unity InputField ContentType）。\n\n**移动端虚拟键盘**：\n- 触摸输入框 → 自动弹出系统虚拟键盘。\n- `Keyboard Type`：Default/Number/Email/Password 等。\n- 平台自动适配（iOS/Android）。\n\n**适配注意**：\n\n**1. 键盘遮挡**：\n- 键盘弹出可能盖住输入框。\n- UE5 的 `OnKeyboardVisibilityChanged` 事件。\n- 监听键盘高度，输入框或 UI 上移。\n- `FSlateApplication::Get().GetVirtualKeyboardArea()` 获取键盘区域。\n\n**2. 输入法（IME）**：\n- 中文输入需要 IME。\n- UMG EditableText 支持 IME composition（候选词）。\n- 注意 composition 字符的显示。\n\n**3. 完成/确认**：\n- `OnTextCommitted` 事件（Enter/Done）。\n- 提交输入内容。\n\n**4. 验证**：\n- 输入时验证（`OnTextChanged` + 字符限制、格式）。\n- 错误提示。\n\n**5. 复制粘贴**：\n- 支持系统剪贴板。\n\n**性能**：\n- 输入框多时每输入一个字符 Invalidate。\n- 非活动输入框 `SetIsEnabled(false)`。\n- 中文输入法可能卡（IME 处理）。\n\n**和 Unity 的对比**：Unity `InputField` / `TMP_InputField` + `TouchScreenKeyboard`；UE5 `EditableTextBox` 自动弹虚拟键盘。Unity 手动监听 `TouchScreenKeyboard.area`；UE5 用 `OnKeyboardVisibilityChanged` + `GetVirtualKeyboardArea`。\n\n**面试加分点**：UE5 的 `EditableTextBox` 自动处理 IME；`Keyboard Type` 选 Number/Email 适配；`OnTextCommitted` 区分 Enter/OnFocusLost；移动端键盘遮挡用 `GetVirtualKeyboardArea` 调 UI 位置；多语言 IME 用 `FSlateApplication` 的 IME 相关 API。",
    "tags": ["EditableText", "输入框", "移动端", "UMG", "UE5"]
}

part2["ui-035"] = {
    "question": "UMG 的 Z-Order / Slot Z-Order？怎么控制 UI 层级？",
    "answer": "层级控制（从低到高优先级）：\n\n**1. Widget 树顺序**：\n- 同 Panel 内，后添加的子 Widget 在上。\n- 最简单层级控制。\n\n**2. Slot Z-Order**：\n- UMG Panel 的 Slot 可设 `Z-Order`（Canvas Panel Slot）。\n- Z-Order 大的在上。\n- 同 Panel 内调整 Z-Order 控制层级。\n\n**3. AddToViewport 的 Z-Order**：\n- `AddToViewport(ZOrder)` 设整个 Widget 树的层级。\n- 不同 Widget 树按 Z-Order 排序。\n- 大的在上。\n\n**4. 多 Widget 树管理**：\n- HUD：`AddToViewport(0)`。\n- 弹窗：`AddToViewport(10)`。\n- Loading：`AddToViewport(100)`。\n- Toast：`AddToViewport(200)`。\n\n**策略**：\n- 主 HUD Widget：Z-Order=0。\n- 弹窗 Widget：Z-Order=10。\n- Loading Widget：Z-Order=100。\n- Toast Widget：Z-Order=200。\n\n**注意**：\n- Z-Order 管理要规范，适度。\n- 频繁切换层级用 Z-Order 而非改树顺序。\n- 跨 Widget 树的事件穿透要考虑层级。\n- Z-Order 影响 Slate HitTest 优先级。\n\n**和 Unity 的对比**：Unity SortingLayer + SortingOrder（Canvas 级）；UE5 `AddToViewport(ZOrder)` + Slot Z-Order。Unity 多 Canvas 用 SortingLayer；UE5 多 Widget 树用 AddToViewport Z-Order。\n\n**面试加分点**：UE5 的 `AddToViewport(int32 ZOrder)` 控制整棵 Widget 树层级；Canvas Panel Slot 的 `Z-Order` 控制子 Widget 层级；HitTest 按 Z-Order 从大到小检测；Slate 底层用 `SWidget::GetRenderTransform` + Z 排序；弹窗用独立 Widget 树 + 高 Z-Order 隔离。",
    "tags": ["Z-Order", "层级", "UMG", "UE5"]
}

part2["ui-037"] = {
    "question": "UMG UI 资源的 Pak/Chunk 和 UAssetManager 加载？",
    "answer": "**Pak/Chunk 分包策略**：\n\n**1. 分包**：\n- 按界面分（主菜单、背包、商店各一 Chunk）。\n- 按功能分（HUD、弹窗、通用）。\n- 共享资源（字体、通用图集）独立 Chunk。\n\n**2. 加载方式**：\n- 同步 `LoadObject`（卡，少用）。\n- 异步 `StreamableManager::LoadAsync`（推荐）。\n- `UAssetManager::LoadPrimaryAssets`（推荐，对应 Unity Addressables）。\n\n**3. 依赖管理**：\n- Chunk 间依赖（A 引用 B 的资源）。\n- `UAssetManager` 自动处理依赖。\n- Primary Asset Label 配置依赖。\n\n**4. 卸载**：\n- `UAssetManager::UnloadPrimaryAsset`。\n- 引用计数：所有引用释放后卸载。\n- `Unload` 后资源可被 GC。\n\n**5. 加载时机**：\n- 启动加载：HUD、主菜单（核心）。\n- 按需加载：其他界面进入时加载。\n- 预加载：等待时后台加载即将进入的界面。\n\n**6. 热更新**：\n- Pak 支持热更（下载替换 Pak）。\n- 版本号管理。\n- 增量更新（只下载变化的 Pak）。\n- `FPakFile` / `FPakPlatformFile` API。\n\n**注意**：\n- 重复加载同资源会缓存（不重复加载）。\n- 内存紧张时卸载低优先级 Chunk。\n- `TSoftObjectPtr` 做延迟加载（对应 Unity Late Binding）。\n\n**和 Unity 的对比**：Unity `AssetBundle` / `Addressables`；UE5 `Pak`/`Chunk` + `UAssetManager`。Unity `Unload(true/false)`；UE5 `UnloadPrimaryAsset` + GC。\n\n**面试加分点**：UE5 的 `UAssetManager` 是原生资产管理（对应 Addressables）；`PrimaryAssetLabel` 配置 Chunk 依赖；`TSoftObjectPtr` / `Soft Object Path` 延迟加载；Pak 热更用 `FPatchPlatformFile`；Chunk 的 `PrimaryAssetType` 分类管理；`StreamableManager` 的 async load 完成回调用 lambda。",
    "tags": ["Pak", "Chunk", "UAssetManager", "加载", "UE5"]
}

part2["ui-038"] = {
    "question": "UMG 图集和 Sprite 的引用关系？Soft Object Path / Async Load？",
    "answer": "问题：\n- UI 引用 Sprite / Texture，但图集可能后加载（按需 Chunk）。\n- Sprite 存在但图集没加载 → 显示空白。\n\n**UE5 做法（对应 Unity Late Binding）**：\n\n**1. Soft Object Path（对应 Unity Late Binding）**：\n- 用 `TSoftObjectPtr<UTexture2D>` / `TSoftObjectPtr<UPaper2DSprite>` 引用。\n- 资源不立即加载，按需 `LoadSynchronous` 或 async load。\n- 蓝图用 `Soft Object Reference` 变量。\n\n**2. Async Load（异步加载）**：\n- `StreamableManager::LoadAsync(SoftObjectPath)`。\n- 加载完成回调绑定。\n- UI 加载时图集未加载，显示占位，加载后正常。\n\n**3. 代码示例**：\n```cpp\nTSoftObjectPtr<UTexture2D> AtlasSoftRef;\nFStreamableManager& Streamable = UAssetManager::GetStreamableManager();\nStreamable.RequestAsyncLoad(AtlasSoftRef.ToSoftObjectPath(),\n    FStreamableDelegate::CreateLambda([this]()\n    {\n        UTexture2D* Atlas = AtlasSoftRef.Get();\n        ImageBrush->SetResourceObject(Atlas);\n    }));\n```\n\n**4. 流程**：\n1. UI 引用 Sprite（Soft Object Path）。\n2. UI 加载时图集未加载，Sprite 显示占位。\n3. 图集异步加载完成，回调触发。\n4. Sprite 绑定图集，正常显示。\n\n**注意**：\n- 占位期间 UI 不能交互（避免误操作）。\n- 加载失败要有重试或提示。\n- 多图集按优先级加载（核心先）。\n\n**和 Unity 的对比**：Unity `SpriteAtlasManager.atlasRequested` + Late Binding；UE5 `TSoftObjectPtr` + `StreamableManager::LoadAsync`。Unity 自动绑定；UE5 手动回调绑定（更灵活）。\n\n**面试加分点**：`TSoftObjectPtr` 不立即加载，省内存；`StreamableManager` 的 `LoadAsync` 批量加载；`UAssetManager` 的 `LoadPrimaryAssets` 管理分块；蓝图用 `Soft Object Reference` + `Load Asset` 节点；加载完成用 `On Loaded` 事件更新 UI。",
    "tags": ["SoftObjectPath", "AsyncLoad", "图集", "UAssetManager", "UE5"]
}

part2["ui-040"] = {
    "question": "UMG UI 的 HUD（血条、伤害数字）优化？",
    "answer": "HUD 挑战：数量多、动态创建、跟随 3D。\n\n**优化策略**：\n\n**1. 对象池**：\n- 血条、伤害数字 Widget 池化，复用。\n- 不 CreateWidget/RemoveFromParent。\n\n**2. 单 Widget 树**：\n- 所有 HUD 一个 UMG Widget（合批）。\n- 不每角色一个 Widget 树（draw call 爆）。\n\n**3. 位置更新优化**：\n- 每帧 `ProjectWorldLocationToScreen`（每角色）。\n- 远距离降频（30FPS 更新）。\n- 屏幕外 `Collapsed`（不 Tick 不渲染）。\n\n**4. 血条**：\n- 用 ProgressBar 或材质进度。\n- Lerp 缓动，不每帧设（按变化设）。\n- 多血条用 Retainer Box 隔离（避免互相 Invalidate）。\n\n**5. 伤害数字**：\n- 池化，触发时激活。\n- 上浮 + 淡出动画（UMG Animation 或 Timeline）。\n- 批量伤害合并显示（\"999×3\"）。\n\n**6. 数量控制**：\n- 同屏 HUD 上限（<50）。\n- 远距离隐藏。\n- 死亡立即回收。\n\n**7. 遮挡处理**：\n- 3D 物体被墙挡住时 HUD 隐藏或变暗。\n- 检测：LineTrace 墙或深度缓冲比较。\n\n**8. 性能预算**：\n- HUD 更新 <1ms CPU。\n- HUD 渲染 <0.5ms GPU。\n- 同屏 50 个血条无压力。\n\n**和 Unity 的对比**：Unity `WorldToScreenPoint` + Screen Space Canvas；UE5 `ProjectWorldLocationToScreen` + AddToViewport。Unity World Space Canvas；UE5 Widget Component。\n\n**面试加分点**：UE5 的 `ProjectWorldLocationToScreen` 配合屏幕外检测 `Collapsed`；HUD 池化用 `TArray` + 复用；Retainer Box 隔离血条 Invalidate；遮挡用 LineTrace 检测墙体；伤害数字用 UMG Animation 模板复用；大量 HUD 用材质直接画（不走 UMG，最省）。",
    "tags": ["HUD", "血条", "伤害数字", "UMG", "UE5"]
}

part2["ui-042"] = {
    "question": "UMG UI 的弹窗（Popup）管理？模态/非模态？",
    "answer": "弹窗类型：\n\n**模态（Modal）**：\n- 遮挡背景，阻止背景交互。\n- 背景半透明黑色 overlay（UMG Border + 半透明颜色）。\n- 必须先处理弹窗才能继续。\n- 适合：确认框、设置、重要提示。\n\n**非模态（Non-modal）**：\n- 不遮挡背景，可同时交互。\n- 浮动面板。\n- 适合：信息提示、辅助工具。\n\n**管理**：\n\n**1. 弹窗栈**：\n- 多个弹窗按栈管理（后开在上）。\n- 关闭栈顶弹窗，下面的恢复。\n\n**2. 单例管理器**：\n```cpp\nclass UPopupManager\n{\n    TArray<UPopupBase*> PopupStack;\n    void Show(UPopupBase* Popup)\n    {\n        Popup->AddToViewport(GetNextZOrder());\n        PopupStack.Push(Popup);\n    }\n    void Close(UPopupBase* Popup)\n    {\n        Popup->RemoveFromParent();\n        PopupStack.Remove(Popup);\n    }\n};\n```\n\n**3. 背景遮罩**：\n- 模态弹窗有半透明背景。\n- 点击背景关闭（可选）。\n\n**4. 动画**：\n- 出现：缩放 0→1 + 淡入（UMG Animation，ease OutBack）。\n- 关闭：缩放 1→0.9 + 淡出。\n\n**5. 层级**：\n- 弹窗 Widget 树 `AddToViewport(ZOrder=10)`（除 Toast 外最高）。\n- 多弹窗按栈顺序递增 ZOrder。\n\n**6. 事件**：\n- 弹窗返回结果（确认/取消）。\n- 回调或 Blueprint Async 节点。\n\n**注意**：\n- 避免弹窗套弹窗（复杂）。\n- 关闭时清理事件。\n- 移动端返回键处理（关闭栈顶弹窗）。\n\n**和 Unity 的对比**：Unity 多 Canvas + SortingLayer 管理弹窗；UE5 多 Widget 树 + `AddToViewport(ZOrder)` 管理。Unity `CanvasGroup.blocksRaycasts` 模态；UE5 `SetVisibility` + 背景遮罩。\n\n**面试加分点**：UE5 用 `AddToViewport(ZOrder)` 控制弹窗层级；模态背景用 Border + 半透明 + `SetVisibility(Visible)` 拦截点击；Blueprint Async 节点做弹窗结果回调；弹窗栈用 `TArray` 管理；移动端返回键用 `OnBackPressed` 事件关栈顶弹窗。",
    "tags": ["弹窗", "Popup", "模态", "UMG", "UE5"]
}

part2["ui-046"] = {
    "question": "UMG 材质的 Shader 变体怎么管理？",
    "answer": "问题：UMG 材质加功能（描边、流光、遮罩）容易变体爆炸。\n\n**变体来源**：\n- `Static Switch` 参数（材质静态开关）。\n- `Quality Switch`（平台质量分级）。\n- UE5 内置变体（Feature Level、平台）。\n\n**管理策略**：\n\n**1. Static Switch Parameter**：\n- per-material 静态开关，编译时剥离。\n- 只生成用到的变体。\n- UE5 推荐用 `Static Switch` 而非运行时分支。\n\n**2. 合并开关**：\n- 多个互斥功能用参数 enum 而非多个 toggle。\n- 用 `Static Switch` 的多个分支（互斥）。\n- 3 变体 vs 3 个 toggle 的 8 变体。\n\n**3. 减少运行时分支**：\n- UI 材质通常不需要动态分支。\n- 用 Static Switch 编译时确定。\n\n**4. 变体剥离**：\n- Project Settings → Engine → Materials → 找剥离选项。\n- UI 材质通常变体少，不易爆。\n\n**5. 静态分析**：\n- 材质编辑器 → Statistics 看变体数。\n- 单 UI 材质变体 <10 为佳。\n\n**6. 多材质 vs 单材质多变体**：\n- 功能差异大 → 多材质。\n- 小开关 → 单材质 Static Switch 变体。\n- 权衡：多材质 draw call 可能多，多变体编译慢。\n\n注意：UI 材质通常简单，变体问题不严重，但仍要规范。\n\n**和 Unity 的对比**：Unity `shader_feature` / `multi_compile` / `shader_feature_local`；UE5 `Static Switch Parameter` / `Quality Switch`。Unity 用 Shader Variant Collection；UE5 用 Material 自动编译变体 + Device Profile 剥离。\n\n**面试加分点**：UE5 的 `Static Switch Parameter` 编译时剥离变体（对应 Unity `shader_feature`）；`Quality Switch` 按平台分级（Low/Medium/High）；材质编辑器 Statistics 看变体数；Device Profile 的 `r.MaterialQualityLevel` 切换；UI 材质用 Material Function 复用（流光/描边函数）。",
    "tags": ["Shader变体", "StaticSwitch", "UMG", "材质", "UE5"]
}

part2["ui-047"] = {
    "question": "UMG UI 和后处理的关系？UI 要不要参与 Bloom？",
    "answer": "两种做法：\n\n**1. UI 不参与后处理（默认）**：\n- UI 用 `AddToViewport`，后处理只对 3D 相机。\n- UI 单独渲染到屏幕（Slate 层）。\n- 优点：UI 清晰、性能好、UI 渲染独立。\n- 缺点：UI 不能发光（Bloom 无效）。\n\n**2. UI 参与后处理**：\n- UI 用 Widget Component（World Space），参与场景渲染。\n- 或 UI 渲染到 Render Target，后处理包含 UI。\n- 优点：UI 可发光（Emissive + Bloom）。\n- 缺点：性能贵（UI 也过后处理）、UI 可能糊。\n\n**选择**：\n- 一般 UI（菜单、HUD）→ 不参与（清晰优先）。\n- 特殊发光 UI（技能图标充能、特效 UI）→ 局部参与。\n\n**局部发光方案**：\n- UI 不后处理，但发光元素用材质模拟（亮色 + 模糊 sprite 叠加）。\n- 或发光元素单独一个 Widget Component，单独 Bloom。\n- 或用 SDF 字体材质的 Glow。\n- 或 Retainer Box 把发光 UI 烘到 RT，对 RT 整体 Bloom。\n\n**移动端**：UI 不参与后处理（性能优先），发光用材质模拟。\n\n**PC/主机**：可让 UI 参与 Bloom 增强氛围，但控制强度（UI 糊影响可读性）。\n\n**和 Unity 的对比**：Unity Screen Space Overlay（不参与）/ Screen Space Camera（参与）；UE5 AddToViewport（不参与）/ Widget Component（参与）。Unity UI 单独渲染栈；UE5 Slate 层独立。\n\n**面试加分点**：UE5 的 `AddToViewport` UI 不过后处理（Slate 直接画屏幕）；Widget Component 的 UI 参与场景后处理；Retainer Box 烘 RT 后可对 RT 整体 Bloom；发光 UI 用材质 Emissive + 局部 Bloom；移动端用材质模拟 Glow 避免 Bloom 性能开销。",
    "tags": ["后处理", "Bloom", "UMG", "WidgetComponent", "UE5"]
}

part2["ui-048"] = {
    "question": "UMG UI 的设计规范和美术协作？",
    "answer": "TA 角色：桥接美术和程序，制定规范。\n\n**规范内容**：\n\n**1. 设计规范**：\n- 设计分辨率（如 1920×1080）。\n- 色板（主色、辅色、警示色）。\n- 字体（标题/正文/数字字体、大小阶梯）。\n- 间距系统（4/8/16/24px 栅格）。\n- 圆角、阴影统一。\n\n**2. 资源规范**：\n- 命名（前缀_元素_状态_变体）。\n- 目录结构。\n- 贴图规格（尺寸、压缩、mipmap off）。\n- 图集划分。\n\n**3. 切图规范**：\n- 九宫格 border 设置（Sprite Editor）。\n- icon 尺寸统一（如 64×64）。\n- 透明边距。\n\n**4. 动效规范**：\n- 缓动曲线统一（ease out、ease in out）。\n- 时长规范（0.2s 出现、0.3s 消失）。\n- 交互反馈统一。\n\n**协作流程**：\n- 美术出设计稿（Figma/Sketch/PSD）。\n- TA 检查规范符合度。\n- 切图导出（美术或 TA）。\n- 程序搭建 UMG（或 FGUI 编辑）。\n- TA Review 性能。\n\n**工具**：\n- Figma/Sketch 设计。\n- Photoshop 切图。\n- UE5 Paper2D Sprite Editor 切九宫格。\n- 自研检查工具（命名、尺寸）。\n- Editor Utility Blueprint 批量检查。\n\n**和 Unity 的对比**：流程一致，工具不同。Unity 用 Sprite Editor；UE5 用 Paper2D Sprite Editor。Unity Prefab；UE5 Widget Blueprint。\n\n**面试加分点**：UE5 的 Editor Utility Blueprint 做自动化检查（命名、贴图大小、图集引用）；Widget Blueprint 可版本控制友好（文本资产）；Figma to UE5 插件自动生成 UMG；DPI Scale 规范统一；规范文档在线化（Confluence/Notion）；TA 做性能 Review Checklist。",
    "tags": ["规范", "美术协作", "设计", "UMG", "UE5"]
}

part2["ui-050"] = {
    "question": "UMG UI 的性能预算和指标？",
    "answer": "性能预算：\n\n**CPU**：\n- Slate Tick：<2ms/帧。\n- UMG 事件处理：<0.5ms。\n- UI 加载：<500ms（界面切换）。\n\n**GPU**：\n- UI draw call：<50（移动）/ <100（PC）。\n- UI 渲染：<2ms（移动）/ <4ms（PC）。\n- UI overdraw：≤3-4 层（移动）。\n\n**内存**：\n- UI 资源：<50MB（移动常驻）。\n- 图集：每张 1024 = 1MB（ASTC）。\n- 字体：<5MB。\n- UMG Widget 实例：<1000。\n\n**指标监控**：\n- `stat Slate` / `stat UMG` 定期检查。\n- ProfileGPU 看 UI pass。\n- 真机测试（低端机）。\n- 上线后 telemetry。\n\n**优化目标**：\n- 60FPS 稳定（移动）。\n- 界面切换 <200ms（无感）。\n- 滚动流畅（60FPS）。\n- 长时间运行无内存增长。\n\n**检查清单**：\n- [ ] Widget 树拆分合理\n- [ ] 图集合批\n- [ ] 无 Layout Panel 滥用\n- [ ] Visibility 优化（HitTestInvisible）\n- [ ] 资源按需加载（Pak/Chunk）\n- [ ] 池化复用（ListView）\n- [ ] 多分辨率适配\n\n**和 Unity 的对比**：Unity Rebuild <2ms / draw call <50；UE5 Slate Tick <2ms / draw call <50。指标相近，工具不同。\n\n**面试加分点**：UE5 用 `stat Slate` 看每帧 Slate 时间；`stat UMG` 看 UMG 事件；ProfileGPU 看 UI pass；UMG Widget 实例数用 `DumpUMGWidgets` 命令查；ListView 的 Entry Widget Pool 控制实例数；Retainer Box 控制合批；Device Profile 按设备分级 UI 质量。",
    "tags": ["性能预算", "指标", "UMG", "UE5"]
}

part2["ui-052"] = {
    "question": "UMG UI 的热更新？资源热更 vs 代码热更？",
    "answer": "**资源热更**：\n- UI Widget Blueprint、贴图、图集、字体热更。\n- Pak 包下载替换。\n- 流程：\n  1. 版本对比（本地 vs 服务器）。\n  2. 下载差异 Pak。\n  3. Mount Pak，加载新资源。\n- 工具：`UAssetManager` + Pak、自研热更系统。\n\n**代码热更**：\n- UI 逻辑代码热更（修 bug、改行为）。\n- 方案：\n  - Lua（slua-unreal / UnLua / sluaunreal）：常用，成熟。\n  - Puerts（JS/TS 热更）：腾讯开源。\n  - C++ 热更：重新编译 DLL 替换（PC 方便，移动难）。\n  - Blueprint 热更：把 Blueprint 转 Pak 热更（有限）。\n- 适合：频繁迭代的 UI 逻辑。\n\n**热更策略**：\n- 资源热更：常规更新（新活动、新界面）。\n- 代码热更：紧急 bug 修复、小逻辑调整。\n- 大版本更新：走商店审核。\n\n**UI 热更注意**：\n- Widget Blueprint 引用的脚本要兼容（字段重命名会丢引用）。\n- 数据结构变化要兼容旧存档。\n- 热更包大小控制（增量 Pak）。\n- 热更失败回滚。\n\n**流程**：\n1. 开发环境构建热更 Pak。\n2. 上传 CDN。\n3. 客户端检查版本，下载。\n4. Mount Pak，加载新资源/代码。\n5. 验证完整性。\n\n**和 Unity 的对比**：Unity `AssetBundle` / `Addressables` + ILRuntime / HybridCLR / xLua；UE5 `Pak` + UnLua / Puerts / sluaunreal。Unity ILRuntime 热更 C#；UE5 用 Lua/JS 热更（C++ 热更难）。\n\n**面试加分点**：UE5 的 Pak 热更用 `FPakPlatformFile` Mount；`UAssetManager` 管理热更资源；Lua 热更常用 UnLua（腾讯）/ sluaunreal；Puerts 用 JS/TS 热更；Widget Blueprint 可热更（Pak 打包）；增量 Pak 用 patch pak；版本号 + Manifest 管理热更。",
    "tags": ["热更新", "Pak", "Lua", "UAssetManager", "UE5"]
}

part2["ui-053"] = {
    "question": "UMG UI 的性能 Review 流程？TA 怎么把关 UI 性能？",
    "answer": "Review 流程：\n\n**1. 提交前自检**：\n- 程序/美术在引擎测 UI。\n- 填自检表（draw call、Slate Tick、内存）。\n\n**2. TA Review**：\n- 在引擎实机查看。\n- 检查：\n  - draw call 数（<50 移动）。\n  - Slate Tick 耗时（`stat Slate`）。\n  - overdraw 层数。\n  - 内存占用。\n  - 合批情况（ProfileGPU）。\n  - 适配（多分辨率）。\n  - 交互（按钮反馈、滚动流畅）。\n  - 命名规范、目录。\n\n**3. 性能测试**：\n- 低端机测试。\n- 长时间运行（内存泄漏）。\n- 极端操作（快速切换界面）。\n\n**4. 反馈修改**：\n- TA 给优化建议（拆 Widget 树、合图集、HitTestInvisible）。\n- 修改后复审。\n\n**5. 签收**：\n- 性能 + 视觉达标 → 入库。\n- 记录到 UI 库。\n\n**工具**：\n- Review 场景（预设分辨率切换）。\n- `stat Slate` / `stat UMG` 实时监控。\n- ProfileGPU 看渲染。\n- Slate Insights 精确分析。\n- 自动化检查（Editor Utility Blueprint）。\n- Checklist 文档。\n\n**KPI**：\n- 一次 Review 通过率 >80%。\n- UI 性能达标率 100%。\n- 上线后 UI 相关 bug <5。\n\n**和 Unity 的对比**：Unity Profiler + Frame Debugger；UE5 Profiler + `stat Slate` + ProfileGPU + Slate Insights。Unity 自定义统计用 `Canvas.willRenderCanvases`；UE5 用 `stat Slate`。\n\n**面试加分点**：UE5 的 Slate Insights 是 UI 性能分析利器（Widget 级别耗时）；Editor Utility Blueprint 自动化检查（命名、贴图大小、Visibility）；`stat Slate` 看每帧 Slate 时间；ProfileGPU 看 UI pass draw call；Device Profile 按设备分级 UI 质量；Review Checklist 文档化；CI/CD 集成性能回归。",
    "tags": ["Review", "性能", "流程", "UMG", "Slate", "UE5"]
}

part2["ui-055"] = {
    "question": "从零搭建 UE5 UMG UI 系统要做什么？",
    "answer": "搭建步骤：\n\n**1. 选型**：\n- UMG / FGUI / Slate。\n- 团队熟悉度、项目需求。\n\n**2. 框架**：\n- UI 基类（View/Window/Widget，基于 `UUserWidget` 派生）。\n- 生命周期（`NativeOnInitialized` / `NativeOnActivated` / `NativeOnDeactivated` / `Destruct`）。\n- 事件系统（UE5 Delegate / Gameplay Tag）。\n- 数据绑定（可选 MVVM，UE5 有 FieldNotification）。\n- UI 栈管理（弹窗、界面切换）。\n\n**3. 资源管理**：\n- Pak/Chunk 打包策略。\n- `UAssetManager` 加载/卸载。\n- 引用计数。\n- 热更新支持（Pak 热更）。\n\n**4. 图集系统**：\n- 编辑时打包（Paper2D Sprite Atlas 或手动 Texture2D）。\n- `TSoftObjectPtr` 延迟加载。\n- 图集划分。\n\n**5. 字体系统**：\n- UMG Text Block + SDF 字体。\n- 字符集裁剪。\n- 多语言字体。\n\n**6. 适配系统**：\n- DPI Scale 配置。\n- SafeZone。\n- 多分辨率测试。\n\n**7. 性能工具**：\n- `stat Slate` / `stat UMG` 监控。\n- Slate Insights 分析。\n- 自动化检查（Editor Utility）。\n- Review 流程。\n\n**8. 规范文档**：\n- 设计规范、资源规范、命名规范。\n- 制作流程。\n- 培训材料。\n\n**9. 工具链**：\n- 代码生成、检查工具（Editor Utility Blueprint）。\n- CI/CD 集成。\n\n**10. 持续优化**：\n- 定期性能 review。\n- 更新规范。\n- 优化热点界面。\n\n**和 Unity 的对比**：\n| Unity | UE5 |\n| MonoBehaviour UI | UUserWidget 派生 |\n| Canvas + SortingLayer | AddToViewport + Z-Order |\n| Addressables | UAssetManager + Pak |\n| Sprite Atlas | Paper2D Sprite Atlas |\n| Canvas Scaler | DPI Scale |\n| SafeArea 脚本 | SafeZone Widget |\n\n预算：中型项目 UI 系统搭建 1-2 人月。\n\n**面试加分点**：UE5 的 `UUserWidget` 是 UMG 框架基类（派生做 View/Window/Widget）；`UAssetManager` + Pak 是原生资产管理；FieldNotification 做 MVVM 数据绑定；Editor Utility Blueprint 做自动化工具；Slate Insights 做 UI 性能分析；Device Profile 按设备分级 UI 质量；UE5 的 UMG 系统搭建比 Unity 省心（SafeZone / DPI Scale 内置）。",
    "tags": ["UI系统", "搭建", "UMG", "框架", "UE5"]
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "rewrite_ui_part1.json", "w", encoding="utf-8") as f:
        json.dump(part1, f, ensure_ascii=False, indent=2)
    with open(OUT / "rewrite_ui_part2.json", "w", encoding="utf-8") as f:
        json.dump(part2, f, ensure_ascii=False, indent=2)
    print(f"Part1: {len(part1)} 题")
    print(f"Part2: {len(part2)} 题")
    print(f"Total: {len(part1) + len(part2)} 题")
    # 验证 JSON
    with open(OUT / "rewrite_ui_part1.json", "r", encoding="utf-8") as f:
        json.load(f)
    with open(OUT / "rewrite_ui_part2.json", "r", encoding="utf-8") as f:
        json.load(f)
    print("JSON 格式验证通过")


if __name__ == "__main__":
    main()
