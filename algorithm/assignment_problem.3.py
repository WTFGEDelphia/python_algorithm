import pulp


"""
指派问题(创建投资组合优化问题)

某公司现有4百万元用于投资甲、乙、丙三个项目，投资额以百万元为单位，已知甲、乙、丙三项投资的可能方案及相应获得的收益如下表所示：

| 项目\收益\投资额 |  1  |  2  |  3  |  4  |
| :----------- - | :-- | :-- | :-- | :-- |
|       甲       |  4  |  6  |   9  |  10 |
|       乙       |  3  |  9  |  10  |  11 |
|       丙       |  5  |  8  |  11  |  15 |


则该公司能够获得的最大收益值是（ ）百万元。
"""


def solve_investment():
    # 创建投资组合优化问题
    prob = pulp.LpProblem("投资组合优化", pulp.LpMaximize)

    # 定义项目和投资额选项
    projects = ["甲", "乙", "丙"]
    investments = [1, 2, 3, 4]  # 投资额（百万元）

    # 定义收益矩阵
    returns = {
        "甲": {1: 4, 2: 6, 3: 9, 4: 10},
        "乙": {1: 3, 2: 9, 3: 10, 4: 11},
        "丙": {1: 5, 2: 8, 3: 11, 4: 15},
    }

    # 创建决策变量（是否选择某个项目的某个投资额）
    x = pulp.LpVariable.dicts(
        "invest", ((p, i) for p in projects for i in investments), cat="Binary"
    )

    # 目标函数：最大化总收益
    prob += pulp.lpSum(returns[p][i] * x[p, i] for p in projects for i in investments)

    # 约束条件1：总投资额不超过4
    prob += pulp.lpSum(i * x[p, i] for p in projects for i in investments) <= 4

    # 约束条件2：每个项目只能选择一个投资额
    for p in projects:
        prob += pulp.lpSum(x[p, i] for i in investments) <= 1

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        total_return = pulp.value(prob.objective)
        print(f"最大收益：{total_return}百万元")

        print("\n投资方案：")
        for p in projects:
            for i in investments:
                if pulp.value(x[p, i]) > 0:
                    print(f"项目{p}投资{i}百万元，收益{returns[p][i]}百万元")

        print(
            f"\n总投资额：{sum(i * pulp.value(x[p, i]) for p in projects for i in investments)}百万元"
        )
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_investment()
