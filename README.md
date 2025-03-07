# Python 算法项目

## 项目结构

```
.
├── LICENSE           # 项目许可证文件
├── README.md        # 项目说明文档
├── requirements.txt  # 项目依赖文件
├── src/             # 源代码目录
│   └── algorithm/   # 算法实现目录
│       ├── assignment_problem.py      # 分配问题算法
│       ├── decision_tree.py          # 决策树算法
│       ├── geometric_probability.py   # 几何概率算法
│       ├── linear_program.py         # 线性规划算法
│       ├── maximum_flow.py           # 最大流算法
│       ├── pipeline_scheduling.py     # 流水线调度算法
│       └── resource_allocation.py     # 资源分配算法
└── tests/           # 测试目录
```

## 算法模块说明

- **分配问题 (Assignment Problem)**: 解决资源分配的优化问题，如工作分配、任务调度等
- **决策树 (Decision Tree)**: 实现决策树算法，用于分类和回归问题
- **几何概率 (Geometric Probability)**: 处理与几何相关的概率问题
- **线性规划 (Linear Programming)**: 求解线性规划问题，优化线性目标函数
- **最大流 (Maximum Flow)**: 解决网络流问题，计算网络中的最大流量
- **流水线调度 (Pipeline Scheduling)**: 处理流水线作业调度优化问题
- **资源分配 (Resource Allocation)**: 优化资源分配策略

## 依赖管理

### 导出当前 Python 环境中安装的所有包及其版本号
```bash
pip freeze > requirements.txt
 ```
具体解释：

1. pip freeze 会列出当前环境中安装的所有 Python 包及其精确版本号
2. `>` 是重定向符号，将命令的输出重定向到指定文件
3. requirements.txt 是保存依赖列表的文件名（这是 Python 项目的一个常见约定）
例如，如果你的环境中安装了以下包：

- numpy==1.21.0
- pandas==1.3.0
- requests==2.26.0
执行 pip freeze > requirements.txt 后，会在当前目录创建一个 requirements.txt 文件，内容如下：

```plaintext
numpy==1.21.0
pandas==1.3.0
requests==2.26.0
 ```

这个文件的主要用途是：

1. 记录项目的依赖关系
2. 方便在其他环境中重现相同的开发环境
3. 确保团队成员使用相同版本的依赖包
### 安装依赖
当其他开发者拿到这个项目时，可以通过以下命令安装相同版本的依赖：

```bash
pip install -r requirements.txt
 ```

这样就能确保所有人使用相同版本的包，避免版本不一致导致的问题。