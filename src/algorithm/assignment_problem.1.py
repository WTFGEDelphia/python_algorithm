import pulp


"""
指派问题

某企业准备将四个工人甲、乙、丙、丁分配在A、B、C、D四个岗位。每个工人由于技术水平不同，在不同岗位上每天完成任务所需的工时见下表。
适当安排岗位，可使四个工人以最短的总工时（ ）全部完成每天的任务。

表格内容如下：

|      | A    | B    | C    | D    |
| :--- | :--- | :--- | :--- | :--- |
| 甲   | 7    | 5    | 2    | 3    |
| 乙   | 9    | 4    | 3    | 7    |
| 丙   | 5    | 4    | 7    | 5    |
| 丁   | 4    | 6    | 5    | 6    |
"""


def solve_assignment():
    # 创建问题
    prob = pulp.LpProblem("工作分配问题", pulp.LpMinimize)

    # 定义工人和岗位
    workers = ["甲", "乙", "丙", "丁"]
    positions = ["A", "B", "C", "D"]

    # 定义完成时间矩阵
    times = {
        "甲": {"A": 7, "B": 5, "C": 2, "D": 3},
        "乙": {"A": 9, "B": 4, "C": 3, "D": 7},
        "丙": {"A": 5, "B": 4, "C": 7, "D": 5},
        "丁": {"A": 4, "B": 6, "C": 5, "D": 6},
    }

    # 创建决策变量
    x = pulp.LpVariable.dicts(
        "assign", ((w, p) for w in workers for p in positions), cat="Binary"
    )

    # 创建最大完成时间变量
    max_time = pulp.LpVariable("max_time")

    # 目标函数：最小化最大完成时间
    prob += max_time

    # 约束条件1：每个工人只能分配一个岗位
    for w in workers:
        prob += pulp.lpSum(x[w, p] for p in positions) == 1

    # 约束条件2：每个岗位只能分配一个工人
    for p in positions:
        prob += pulp.lpSum(x[w, p] for w in workers) == 1

    # 约束条件3：最大完成时间必须大于等于每个分配的完成时间
    for w in workers:
        for p in positions:
            prob += max_time >= times[w][p] * x[w, p]

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        print(f"最短完成时间：{pulp.value(max_time)}小时")
        print("\n分配方案：")
        for w in workers:
            for p in positions:
                if pulp.value(x[w, p]) == 1:
                    print(f"{w}分配到岗位{p}，完成时间：{times[w][p]}小时")
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_assignment()
