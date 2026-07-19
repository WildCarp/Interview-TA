"""
修复 2 条字面替换导致的语义错误题目：
1. pipeline_023: 原"Unity Asset Pipeline vs Unreal"对比题，替换后变自比
2. vfx-033: 原"Niagara(UE) vs VFX Graph(Unity)"对比题，替换后变自比

重写为纯 UE5 视角的题目。
"""
import json
from pathlib import Path

PARTS_DIR = Path(r"C:\Users\Administrator\WorkBuddy\2026-07-19-19-08-08\parts")

# pipeline_023 重写：UE5 Asset Pipeline 工作原理
PIPELINE_023 = {
    "id": "pipeline_023",
    "category": "pipeline",
    "difficulty": "中级",
    "question": "UE5 的 Asset Pipeline（UAT / UBT / Cook）是怎么工作的？各模块职责是什么？",
    "answer": """**UE5 Asset Pipeline 三大核心工具**：

**1. UBT（UnrealBuildTool）**：
- 负责 C++ 代码编译，生成 .module/BUILD.cs 规则
- 解析模块依赖（PublicDependencyModuleNames / PrivateDependencyModuleNames）
- 支持 Development/Shipping/Debug/DebugGame 等多种配置
- 增量编译，未改动的模块跳过
- 跨平台编译（Win64/Android/iOS/PS5/XSX 等目标平台）

**2. UAT（UnrealAutomationTool）**：
- 上层编排工具，驱动整个构建流程
- 命令行入口：`UnrealBuildTool BuildCookRun`（旧）或 `ProjectPackagingTool`
- 流程：Build → Cook → Stage → Package → Deploy → Run
- 支持自动化测试（Automation System）
- 可写自定义 BuildTarget（.target.cs）扩展流程

**3. Cook（CookContent）**：
- 把编辑器格式（.uasset）转成平台特定格式
- 剔除未引用资产（基于 Asset Registry 依赖图）
- 贴图压缩格式转换（BC7 → ASTC 等）
- 材质 Shader 编译到目标平台 Shader Format（GLSL/Vulkan/Metal/DXC）
- 输出到 `Saved/Cooked/<Platform>/`

**.uasset / .uexp 格式**：
- `.uasset`：资产头 + 元数据 + Object 数据（二进制包）
- `.uexp`：大体量导出数据（贴图像素、网格顶点）单独存
- 内部存 Object 数据 + 依赖图（Package 引用）
- ImportGuid / ExportGuid 跨包引用

**Asset Registry**：
- 全局资产索引，启动时扫描所有 .uasset 提取元数据
- 支持按 Path/Class/Tag 查询（FAssetRegistryModule）
- Cook 时用它的依赖图做剔除
- 编辑器里 Content Browser 的数据源

**Editor Asset API**：
- `UEditorAssetLibrary::LoadAsset()` / `FindPackageReferencersForAsset()`
- `UAssetManager`：运行时资产加载、Chunk 管理、PrimaryAsset 体系
- `FAssetToolsModule`：批量重命名、迁移、导出
- 比 Unity 的 AssetDatabase 更底层，但功能等价

**和 Unity 管线的关键差异**（面试常问）：
- Unity 用 C# 脚本驱动 AssetDatabase；UE5 用 C++ + UAssetManager
- Unity 的 .meta 是文本 GUID；UE5 的 .uasset 内嵌 GUID
- Unity 构建 AB 需手写 BuildPipeline；UE5 Cook 自动处理
- UE5 的 Shader 编译是异步的（ShaderCompileWorker），第一次 Cook 慢""",
    "tags": ["UAT", "UBT", "Cook", "AssetRegistry", "管线"]
}

# vfx-033 重写：Niagara 核心概念
VFX_033 = {
    "id": "vfx-033",
    "category": "vfx",
    "difficulty": "中级",
    "question": "Niagara 系统的核心概念？System、Emitter、Module 的关系？和 Cascade 的区别？",
    "answer": """**Niagara 三层架构**：

**System（系统）**：
- 顶层容器，一个完整的特效效果（如"火球爆炸"）
- 持有多个 Emitter，控制它们的生命周期、播放顺序
- 支持绑定到 Actor（Attachment），可接收外部参数
- 可嵌套（System 里引用其他 System）
- 支持编辑器内的暴露参数（ExposedParameters）给美术调

**Emitter（发射器）**：
- 一个粒子发射源，对应一种粒子行为（火花/烟/碎片）
- 由 Module Stack 组成，按 Spawn → Init → Update → Output 组织
- 可独立开关、设置 LoopCount、Burst
- 一个 Emitter 只产生一类粒子，但可复用 Module
- 可继承其他 Emitter（Inheritance）做模板

**Module（模块）**：
- 最小功能单元，控制粒子某一行为
- 分组：
  - **Spawn**：Spawn Burst / Spawn Rate / Spawn Burst Instantaneous
  - **Initialization**：Initialize Particle / Initialize Location / Init Color
  - **Update**：Gravity Force / Drag / Velocity / Color Update / Size Scale
  - **Render/Output**：Sprite Renderer / Mesh Renderer / Ribbon Renderer
- 支持自定义 Module（C++ / 蓝图），HLSL 写脚本
- 参数绑定（Parameter Binding）：模块间数据传递（如把 Speed 传给 Gravity）

**Module Stack 执行模型**：
- 每帧按顺序执行所有 Module
- 数据存在 Particle Attributes（Position/Velocity/Color/Life/Age 等）
- 支持事件（Event）：碰撞触发、死亡触发，跨 Emitter 通信
- Data Interface（DI）：读场景数据（骨骼/Collision/Spline/Audio）

**CPU vs GPU 仿真**：
- CPU Emitter：粒子数少（< 10k），支持复杂逻辑和 DI
- GPU Emitter：粒子数多（百万级），用 Compute Shader，DI 受限
- 同一 System 可混用 CPU + GPU Emitter

**Scratch Pad / Scripting**：
- 内置可视化脚本编辑器（节点图）
- 支持写 HLSL 片段直接控制粒子
- 可定义自定义参数（User Variables）
- 调试强：实时预览、参数可视化

**和 Cascade（旧粒子系统）的区别**：
- Cascade 模块固定，扩展要写 C++ 重新编译
- Niagara 模块化、可脚本化，美术能自建 Module
- Niagara 支持 GPU 仿真、Data Interface、Mesh Rendering
- Niagara 调试工具完善（Scratch Pad、Profiler）
- UE5 推荐全用 Niagara，Cascade 只为兼容旧资产保留

**面试加分点**：
- 提 Niagara 的 Module Stack 是数据驱动（Data Driven），比 Cascade 的硬编码灵活
- 提 Niagara 的 Simulation Space（Local/World）选择对运动效果的影响
- 提 Niagara Data Interface（DI）能读骨骼/碰撞/Spline，做交互特效
- 提 Niagara 和 Chaos 物理、Field System 的集成""",
    "tags": ["Niagara", "System", "Emitter", "Module", "粒子"]
}


def main():
    fixes = [
        ("questions_pipeline.json", "pipeline_023", PIPELINE_023),
        ("questions_vfx.json", "vfx-033", VFX_033),
    ]

    for fname, qid, new_q in fixes:
        fpath = PARTS_DIR / fname
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 兼容 list / dict
        if isinstance(data, dict):
            questions = data["questions"]
        else:
            questions = data

        # 找到并替换
        found = False
        for i, q in enumerate(questions):
            if q["id"] == qid:
                questions[i] = new_q
                found = True
                print(f"[OK] {fname} {qid}: 已重写")
                break

        if not found:
            print(f"[ERR] {fname} {qid}: 未找到")
            continue

        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 验证 JSON 合法
        with open(fpath, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"  JSON 验证通过")

    print("\n2 条语义错误已修复")


if __name__ == "__main__":
    main()
