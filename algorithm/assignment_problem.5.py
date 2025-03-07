import pulp


"""
指派问题(商品分配问题)

某批发站准备向甲、乙、丙、丁四家小商店供应5箱商品。批发站能取得的利润（单位：百元）与分配的箱数有关（见下表）。

表格内容如下：

| 利润 | 甲   | 乙   | 丙   | 丁   |
| :--- | :--- | :--- | :--- | :--- |
| A:1箱  | 4    | 2    | 3    | 4    |
| B:2箱  | 6    | 4    | 6    | 5    |
| C:3箱  | 7    | 6    | 7    | 6    |
| D:4箱  | 7    | 8    | 8    | 6    |
| E:5箱  | 7    | 9    | 8    | 6    |

批发站为取得最大总利润，应分配（ ）。

解题思路：

指派问题
  批发站采用五中批发策略 A:1箱、B:2箱、C:3箱、D:4箱、E:5箱，四家商店要么供应，要么不供应。
"""


def solve_assignment():
    # 创建最大化问题
    prob = pulp.LpProblem("商品分配问题", pulp.LpMaximize)

    # 定义商店和分配策略
    stores = ["甲", "乙", "丙", "丁"]
    strategies = {
        "A": 1,  # 1箱
        "B": 2,  # 2箱
        "C": 3,  # 3箱
        "D": 4,  # 4箱
        "E": 5,  # 5箱
    }

    # 定义利润矩阵（百元）
    profits = {
        "甲": {"A": 4, "B": 6, "C": 7, "D": 7, "E": 7},
        "乙": {"A": 2, "B": 4, "C": 6, "D": 8, "E": 9},
        "丙": {"A": 3, "B": 6, "C": 7, "D": 8, "E": 8},
        "丁": {"A": 4, "B": 5, "C": 6, "D": 6, "E": 6},
    }

    # 创建决策变量（商店s是否采用策略t）
    x = pulp.LpVariable.dicts(
        "assign", ((s, t) for s in stores for t in strategies), cat="Binary"
    )

    # 目标函数：最大化总利润
    prob += pulp.lpSum(profits[s][t] * x[s, t] for s in stores for t in strategies)

    # 约束条件1：每个商店最多只能选择一种策略
    for s in stores:
        prob += pulp.lpSum(x[s, t] for t in strategies) <= 1

    # 约束条件2：所有分配的箱数之和必须等于5
    prob += pulp.lpSum(strategies[t] * x[s, t] for s in stores for t in strategies) == 5

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        total_profit = pulp.value(prob.objective)
        print(f"最大总利润：{total_profit}百元")

        print("\n分配方案：")
        for s in stores:
            for t in strategies:
                if pulp.value(x[s, t]) > 0:
                    print(
                        f"商店{s}分配{strategies[t]}箱（策略{t}），利润{profits[s][t]}百元"
                    )
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_assignment()
