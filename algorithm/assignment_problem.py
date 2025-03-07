import pulp

"""
指派问题

甲、乙、丙、丁4人加工A、B、C、D四种工件所需工时如下表所示。
指派每人加工一种工件，四人加工四种工件其总工时最短的最优方案中，工件B应由（ ）加工。
|      | A    | B    | C    | D    |
| :--- | :--- | :--- | :--- | :--- |
| 甲   | 14   | 9    | 4    | 15   |
| 乙   | 11   | 7    | 7    | 10   |
| 丙   | 13   | 2    | 10   | 5    |
| 丁   | 17   | 9    | 15   | 13   |

解题思路：
先将矩阵进行化简，化简的方法是每行的元素减去这一行的最小值，然后每列的元素减去这一列的最小值，确保每行，每列都有0。得到：
1.每行的元素减去这一行的最小值:
|      | A    | B    | C    | D    |
| :--- | :--- | :--- | :--- | :--- |
| 甲   | 10   | 5    | 0    | 11   |
| 乙   | 4    | 0    | 0    | 3    |
| 丙   | 11   | 0    | 8    | 3    |
| 丁   | 8    | 0    | 6    | 4    |
2.每列的元素减去这一列的最小值
|      | A    | B    | C    | D    |
| :--- | :--- | :--- | :--- | :--- |
| 甲   | 6    | 5    | 0    | 8    |
| 乙   | 0    | 0    | 0    | 0    |
| 丙   | 7    | 0    | 8    | 0    |
| 丁   | 4    | 0    | 6    | 1    |
然后找出一种方案，方案组成元素都是0，而这些元素不同行，也不同列。即为解决方案。如下：甲->C,乙->A,丙->D,丁->B, 总工时为29。
|      | A    | B    | C    | D    |
| :--- | :--- | :--- | :--- | :--- |
| 甲   | 6    | 5    | 0    | 8    |
| 乙   | 0    | 0    | 0    | 0    |
| 丙   | 7    | 0    | 8    | 0    |
| 丁   | 4    | 0    | 6    | 1    |
"""


def solve_assignment_problem():
    # 创建指派问题
    prob = pulp.LpProblem("工件分配问题", pulp.LpMinimize)

    # 工人和工件
    workers = ["甲", "乙", "丙", "丁"]
    tasks = ["A", "B", "C", "D"]

    # 加工时间矩阵
    times = {
        "甲": {"A": 14, "B": 9, "C": 4, "D": 15},
        "乙": {"A": 11, "B": 7, "C": 7, "D": 10},
        "丙": {"A": 13, "B": 2, "C": 10, "D": 5},
        "丁": {"A": 17, "B": 9, "C": 15, "D": 13},
    }

    # 决策变量：x[i][j] = 1 表示工人i分配给工件j
    x = pulp.LpVariable.dicts(
        "x", ((i, j) for i in workers for j in tasks), cat="Binary"
    )

    # 目标函数：最小化总加工时间
    prob += pulp.lpSum(times[i][j] * x[i, j] for i in workers for j in tasks)

    # 约束条件：每个工人只能分配一个工件
    for i in workers:
        prob += pulp.lpSum(x[i, j] for j in tasks) == 1

    # 约束条件：每个工件只能分配给一个工人
    for j in tasks:
        prob += pulp.lpSum(x[i, j] for i in workers) == 1

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        print("最优分配方案：")
        total_time = 0
        for i in workers:
            for j in tasks:
                if x[i, j].value() == 1:
                    print(f"{i}工人 -> {j}工件，加工时间：{times[i][j]}")
                    total_time += times[i][j]
        print(f"\n总加工时间：{total_time}")
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_assignment_problem()
