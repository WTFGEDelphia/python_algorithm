import pulp


"""
指派问题(创建生产规划问题)

某企业需要采用甲、乙、丙三种原材料生产I、II两种产品。生产两种产品所需原材料数量、单位产品可获得利润以及企业现有原材料数,
如下表所示，则公司可以获得的最大利润是（1）万元。取得最大利润时，原材料（2）尚有剩余。

| 所需资源            | 产品（吨） |      | 现有原材料（吨） |
| :------------------ | :--------- | :--- | :--------------- |
|                     | I          | II   |                  |
| 甲                  | 1          | 1    | 4                |
| 乙                  | 4          | 3    | 12               |
| 丙                  | 1          | 3    | 6                |
| 单位利润（万元/吨） |            | 9    | 12               |
"""


def solve_production_planning():
    # 创建生产规划问题
    prob = pulp.LpProblem("生产规划问题", pulp.LpMaximize)

    # 创建决策变量（两种产品的生产量）
    x1 = pulp.LpVariable("产品I", lowBound=0)  # 产品I的生产量
    x2 = pulp.LpVariable("产品II", lowBound=0)  # 产品II的生产量

    # 定义原材料消耗系数
    materials = {
        "甲": {"I": 1, "II": 1, "现有量": 4},
        "乙": {"I": 4, "II": 3, "现有量": 12},
        "丙": {"I": 1, "II": 3, "现有量": 6},
    }

    # 定义单位利润（万元/吨）
    profit = {"I": 9, "II": 12}

    # 目标函数：最大化总利润
    prob += profit["I"] * x1 + profit["II"] * x2

    # 约束条件：原材料限制
    prob += (
        materials["甲"]["I"] * x1 + materials["甲"]["II"] * x2
        <= materials["甲"]["现有量"]
    )  # 甲材料约束
    prob += (
        materials["乙"]["I"] * x1 + materials["乙"]["II"] * x2
        <= materials["乙"]["现有量"]
    )  # 乙材料约束
    prob += (
        materials["丙"]["I"] * x1 + materials["丙"]["II"] * x2
        <= materials["丙"]["现有量"]
    )  # 丙材料约束

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        max_profit = pulp.value(prob.objective)
        x1_value = pulp.value(x1)
        x2_value = pulp.value(x2)

        print(f"最大利润：{max_profit}万元")
        print(f"\n生产方案：")
        print(f"产品I生产量：{x1_value:.2f}吨")
        print(f"产品II生产量：{x2_value:.2f}吨")

        print(f"\n原材料使用情况：")
        for material in materials:
            used = (
                materials[material]["I"] * x1_value
                + materials[material]["II"] * x2_value
            )
            remaining = materials[material]["现有量"] - used
            print(f"{material}材料：使用{used:.2f}，剩余{remaining:.2f}")
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_production_planning()
