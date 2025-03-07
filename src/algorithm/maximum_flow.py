import pulp

"""
在军事演习中，张司令希望将部队尽快从A地通过公路网（见下图）运送到F地：
复制
A ---13-- B ---8-- F
|       |     |
2       5     4
|       |     |
C ---6-- E ---15-- F
|       |     |
3       4     |
|_______|_____|
      D
图中标出了各路段上的最大运量（单位：千人/小时）。根据该图可以算出，从A地到F地的最大运量是（ ）千人/小时。
"""


def solve_max_flow():
    # 创建最大流问题
    prob = pulp.LpProblem("最大流问题", pulp.LpMaximize)

    # 定义节点集合
    nodes = ["A", "B", "C", "D", "E", "F"]

    # 定义边的初始容量
    capacities = {
        ("A", "B"): 13,
        ("A", "C"): 2,
        ("A", "D"): 3,
        ("B", "F"): 8,
        ("B", "E"): 5,
        ("C", "E"): 2,  # 受A->C=2限制
        ("D", "E"): 3,  # 受A->D=3限制
        ("E", "F"): 14,  # 受B->E=5, C->E=2, D->E=3限制，总和为10
    }

    # 创建流量变量
    flows = pulp.LpVariable.dicts(
        "flow", ((i, j) for i in nodes for j in nodes), lowBound=0
    )

    # 目标函数：最大化到达F的总流量
    prob += pulp.lpSum(flows[j, "F"] for j in nodes if (j, "F") in capacities)

    # 约束条件1：流量不超过容量
    for i, j in capacities:
        prob += flows[i, j] <= capacities[i, j]

    # 约束条件2：节点B的流量分配
    prob += flows["A", "B"] <= 13  # B的输入限制
    prob += flows["B", "F"] + flows["B", "E"] <= flows["A", "B"]  # B的输出不超过输入
    prob += flows["B", "F"] <= 8  # B到F的容量限制
    prob += flows["B", "E"] <= 5  # B到E的容量限制

    # 约束条件3：节点C的流量分配
    prob += flows["A", "C"] <= 2  # C的输入限制
    prob += flows["C", "E"] <= flows["A", "C"]  # C的输出不超过输入

    # 约束条件4：节点D的流量分配
    prob += flows["A", "D"] <= 3  # D的输入限制
    prob += flows["D", "E"] <= flows["A", "D"]  # D的输出不超过输入

    # 约束条件5：节点E的流量分配
    inflow_E = pulp.lpSum(flows[j, "E"] for j in ["B", "C", "D"])
    prob += flows["E", "F"] <= inflow_E  # E的输出不超过总输入
    prob += flows["E", "F"] <= 15  # E到F的容量限制

    # 约束条件6：不存在的边流量为0
    for i in nodes:
        for j in nodes:
            if (i, j) not in capacities:
                prob += flows[i, j] == 0

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        max_flow_value = pulp.value(prob.objective)
        print(f"从A地到F地的最大运量是：{max_flow_value}千人/小时")

        print("\n各路段的流量分配：")
        for i, j in capacities:
            flow_value = pulp.value(flows[i, j])
            if flow_value > 0:
                print(f"{i}->{j}: {flow_value:.1f}千人/小时")
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_max_flow()
