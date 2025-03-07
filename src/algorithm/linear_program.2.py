import pulp  # Python for Mathematical Programming

"""
线性规划问题（最大值）

非负整数变量x和y，在x≤4，y≤3和x+2y≤8的约束条件下，目标函数2x+3y的最大值为（    ）。
"""


def solve_linear_programming():
    # 创建最大化问题
    prob = pulp.LpProblem("线性规划问题", pulp.LpMaximize)

    # 创建变量
    x = pulp.LpVariable("x", upBound=4)  # x≤4
    y = pulp.LpVariable("y", upBound=3)  # y≤3

    # 目标函数：最大化 2x+3y
    prob += 2 * x + 3 * y

    # 约束条件
    prob += x + 2 * y <= 8  # x+2y≤8

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        x_value = pulp.value(x)
        y_value = pulp.value(y)
        objective_value = pulp.value(prob.objective)
        print(f"最优解：")
        print(f"x = {x_value}")
        print(f"y = {y_value}")
        print(f"目标函数最大值 2x+3y = {objective_value}")
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_linear_programming()
