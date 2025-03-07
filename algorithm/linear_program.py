import pulp  # Python for Mathematical Programming

"""
线性规划问题

某服装店有甲、乙、丙、丁四个缝制小组。甲组每天能缝制5件上衣或6条裤子；乙组每天能缝制6件上衣或7条裤子；丙组每天
能缝制7件上衣或8条裤子；丁组每天能缝制8件上衣或9条裤子。每组每天要么缝制上衣，要么缝制裤子，不能弄混。订单要求
上衣和裤子必须配套（每套衣服包括一件上衣和一条裤子）。只要做好合理安排，该服装店15天最多能缝制（ ）套衣服。
"""


def solve_clothing_problem():
    # 创建线性规划问题
    prob = pulp.LpProblem("服装生产规划", pulp.LpMaximize)

    # 决策变量：每个组做上衣或裤子的天数
    xa = pulp.LpVariable("xa", 0, 15, pulp.LpInteger)  # 甲组做上衣的天数
    xb = pulp.LpVariable("xb", 0, 15, pulp.LpInteger)  # 乙组做上衣的天数
    xc = pulp.LpVariable("xc", 0, 15, pulp.LpInteger)  # 丙组做上衣的天数
    xd = pulp.LpVariable("xd", 0, 15, pulp.LpInteger)  # 丁组做上衣的天数

    ya = pulp.LpVariable("ya", 0, 15, pulp.LpInteger)  # 甲组做裤子的天数
    yb = pulp.LpVariable("yb", 0, 15, pulp.LpInteger)  # 乙组做裤子的天数
    yc = pulp.LpVariable("yc", 0, 15, pulp.LpInteger)  # 丙组做裤子的天数
    yd = pulp.LpVariable("yd", 0, 15, pulp.LpInteger)  # 丁组做裤子的天数

    # 产品数量约束
    upper = 5 * xa + 6 * xb + 7 * xc + 8 * xd  # 上衣总数
    lower = 6 * ya + 7 * yb + 8 * yc + 9 * yd  # 裤子总数
    prob += upper  # # 最大化套装数量，上衣和裤子数量相等

    # 工作天数约束
    prob += upper == lower  # 上衣和裤子数量相等
    prob += xa + ya == 15  # 甲组总工作天数为15
    prob += xb + yb == 15  # 乙组总工作天数为15
    prob += xc + yc == 15  # 丙组总工作天数为15
    prob += xd + yd == 15  # 丁组总工作天数为15

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        total_suits = pulp.value(upper)  # 由于上衣和裤子数量相等，用任意一个都可以
        print(f"最多可以生产 {int(total_suits)} 套衣服")
        print("\n具体安排：")
        print(f"甲组：做上衣 {int(xa.value())} 天，做裤子 {int(ya.value())} 天")
        print(f"乙组：做上衣 {int(xb.value())} 天，做裤子 {int(yb.value())} 天")
        print(f"丙组：做上衣 {int(xc.value())} 天，做裤子 {int(yc.value())} 天")
        print(f"丁组：做上衣 {int(xd.value())} 天，做裤子 {int(yd.value())} 天")
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_clothing_problem()
