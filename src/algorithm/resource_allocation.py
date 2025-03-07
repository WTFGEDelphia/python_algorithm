import pulp

"""
资源分配问题

某公司需要将4吨贵金属材料分配给下属的甲、乙、丙三个子公司（单位：吨）。
据测算，各子公司得到这些材料后所能获得的利润（单位：万元）见下表：

| 子公司 | 材料 | 1吨  | 2吨  | 3吨  | 4吨  |
| :----- | :--- | :--- | :--- | :--- | :--- |
| 甲     |      | 4    | 7    | 10   | 13   |
| 乙     |      | 5    | 9    | 11   | 13   |
| 丙     |      | 4    | 6    | 11   | 14   |

根据此表，只要材料分配适当，该公司最多可以获得利润（ ）万元。
"""


def solve_material_allocation():
    # 创建资源分配问题
    prob = pulp.LpProblem("资源分配问题", pulp.LpMaximize)

    # 定义数据
    companies = ["甲", "乙", "丙"]
    tons = range(5)  # 0-4吨
    profits = {
        "甲": {0: 0, 1: 4, 2: 7, 3: 10, 4: 13},
        "乙": {0: 0, 1: 5, 2: 9, 3: 11, 4: 13},
        "丙": {0: 0, 1: 4, 2: 6, 3: 11, 4: 14},
    }

    # 决策变量：x[i][j] = 1 表示公司i分配j吨材料
    x = pulp.LpVariable.dicts(
        "x", ((i, j) for i in companies for j in tons), cat="Binary"
    )

    # 目标函数：最大化总利润
    prob += pulp.lpSum(profits[i][j] * x[i, j] for i in companies for j in tons)

    # 约束条件1：每个公司只能分配一个数量
    for i in companies:
        prob += pulp.lpSum(x[i, j] for j in tons) == 1

    # 约束条件2：总分配量必须等于4吨
    prob += pulp.lpSum(j * x[i, j] for i in companies for j in tons) == 4

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        total_profit = pulp.value(prob.objective)
        print(f"最大利润：{total_profit}万元")
        print("\n具体分配方案：")
        for i in companies:
            for j in tons:
                if pulp.value(x[i, j]) == 1:
                    print(f"{i}公司分配{j}吨材料，获得利润{profits[i][j]}万元")
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_material_allocation()
