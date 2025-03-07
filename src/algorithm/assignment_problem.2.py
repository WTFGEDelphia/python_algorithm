import pulp


"""
指派问题（运输优化问题）

设三个煤场A、B、C分别能供应煤12、14、10万吨，三个工厂X、Y、Z分别需要煤11、12、13万吨，从各煤场到各工厂运煤的单价（百元/吨）见下表方框内的数字。只要选择最优的运输方案，总的运输成本就能降到（ ）百万元。

表格内容如下：

|                | 工厂X | 工厂Y | 工厂Z | 供应量（万吨） |
| :------------- | :---- | :---- | :---- | :------------- |
| 煤场A          | 5     | 1     | 6     | 12             |
| 煤场B          | 2     | 4     | 3     | 14             |
| 煤场C          | 3     | 6     | 7     | 10             |
| 需求量（万吨） | 11    | 12     | 13     | 36             |
"""


def solve_transportation():
    # 创建运输优化问题
    prob = pulp.LpProblem("运输优化问题", pulp.LpMinimize)

    # 定义供应点和需求点
    supply_points = ["煤场A", "煤场B", "煤场C"]
    demand_points = ["工厂X", "工厂Y", "工厂Z"]

    # 定义供应量（万吨）
    supply = {"煤场A": 12, "煤场B": 14, "煤场C": 10}

    # 定义需求量（万吨）
    demand = {"工厂X": 11, "工厂Y": 12, "工厂Z": 13}

    # 定义运输成本（元/吨）
    costs = {
        ("煤场A", "工厂X"): 8,
        ("煤场A", "工厂Y"): 1,
        ("煤场A", "工厂Z"): 6,
        ("煤场B", "工厂X"): 2,
        ("煤场B", "工厂Y"): 4,
        ("煤场B", "工厂Z"): 3,
        ("煤场C", "工厂X"): 3,
        ("煤场C", "工厂Y"): 8,
        ("煤场C", "工厂Z"): 7,
    }

    # 创建决策变量（运输量）
    x = pulp.LpVariable.dicts(
        "transport", ((s, d) for s in supply_points for d in demand_points), lowBound=0
    )

    # 目标函数：最小化总运输成本
    prob += pulp.lpSum(
        x[s, d] * costs[s, d] for s in supply_points for d in demand_points
    )

    # 约束条件1：供应点的供应量约束
    for s in supply_points:
        prob += pulp.lpSum(x[s, d] for d in demand_points) == supply[s]

    # 约束条件2：需求点的需求量约束
    for d in demand_points:
        prob += pulp.lpSum(x[s, d] for s in supply_points) == demand[d]

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        total_cost = pulp.value(prob.objective)
        print(f"最小运输成本：{total_cost}万元")
        print("\n运输方案：")
        for s in supply_points:
            for d in demand_points:
                if pulp.value(x[s, d]) > 0:
                    print(
                        f"从{s}运输到{d}：{pulp.value(x[s, d])}万吨，成本：{pulp.value(x[s, d]) * costs[s, d]}万元"
                    )
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_transportation()
