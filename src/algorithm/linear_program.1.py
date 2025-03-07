import pulp  # Python for Mathematical Programming

"""
线性规划问题（最小值）

在如下线性约束条件下：2x+3y≤30；x+2y≥10；x≥y；x≥5；y≥0，目标函数2x+3y的极小值为（ ）。
"""


def solve_linear_programming():
    # 创建最大化问题
    prob = pulp.LpProblem("线性规划问题", pulp.LpMinimize)

    # 创建变量
    x = pulp.LpVariable("x", lowBound=5)  # x≥5
    y = pulp.LpVariable("y", lowBound=0)  # y≥0

    # 目标函数：最大化 2x+3y
    prob += 2 * x + 3 * y

    # 约束条件
    prob += 2 * x + 3 * y <= 30  # 2x+3y≤30
    prob += x + 2 * y >= 10  # x+2y≥10
    prob += x >= y  # x≥y

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
