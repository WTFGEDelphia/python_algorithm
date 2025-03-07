import pulp


"""
指派问题(商品分配问题)

甲、乙、丙、丁四个任务分配在A、B、C、D四台机器上执行，每台机器执行一个任务，所需的成本（单位：百元）如下表所示。适当分配使总成本最低的最优方案中，任务乙应由机器（ ）执行。

表格内容如下：

|      | A    | B    | C    | D    |
| :--- | :--- | :--- | :--- | :--- |
| 甲   | 1    | 4    | 6    | 3    |
| 乙   | 9    | 7    | 10   | 9    |
| 丙   | 4    | 5    | 11   | 7    |
| 丁   | 8    | 7    | 8    | 5    |

解题思路：

根据任一行，任一列各元素都减或加一常数后，并不会影响最优解的位置，只是目标值（分配方案的各项和）也减或加了这一常数这一性质。

首先，用每一行的值减去该行的最小值得到如下图结果：
|      | A    | B    | C    | D    |
| :--- | :--- | :--- | :--- | :--- |
| 甲   | 0    | 3    | 5    | 2    |
| 乙   | 2    | 0    | 3    | 2    |
| 丙   | 0    | 1    | 7    | 3    |
| 丁   | 3    | 2    | 3    | 0    |

此时第3列仍没有出现0元素，所以第三列列的数值，减去第三列的最小值得到如下图结果：
|      | A    | B    | C    | D    |
| :--- | :--- | :--- | :--- | :--- |
| 甲   | 0    | 3    | 2    | 2    |
| 乙   | 2    | 0    | 0    | 2    |
| 丙   | 0    | 1    | 4    | 3    |
| 丁   | 3    | 2    | 0    | 0    |

可以看出不存在全0分配，所以我们来看总和是不是有1的。显然存在总和为1的分配，如图所示：
|      | A     | B     | C     | D     |
| :--- | :---- | :---- | :---- | :---- |
| 甲   | **0** | 3     | 2     | 2     |
| 乙   | 2     | 0     | **0** | 2     |
| 丙   | 0     | **1** | 4     | 3     |
| 丁   | 3     | 2     | 0     | **0** |

所以把甲任务分配给A机器，乙任务分配给C机器，丙任务分配给B机器，丁任务分配给D机器时等达到最低成本为1+10+5+5=21。
"""


def solve_assignment():
    # 创建任务分配问题最小化问题
    prob = pulp.LpProblem("任务分配问题", pulp.LpMinimize)

    # 定义人员和机器
    people = ["甲", "乙", "丙", "丁"]
    machines = ["A", "B", "C", "D"]

    # 定义成本矩阵（百元）
    costs = {
        "甲": {"A": 1, "B": 4, "C": 6, "D": 3},
        "乙": {"A": 9, "B": 7, "C": 10, "D": 9},
        "丙": {"A": 4, "B": 5, "C": 11, "D": 7},
        "丁": {"A": 8, "B": 7, "C": 8, "D": 5},
    }

    # 创建决策变量（是否分配某人到某机器）
    x = pulp.LpVariable.dicts(
        "assign", ((p, m) for p in people for m in machines), cat="Binary"
    )

    # 目标函数：最小化总成本
    prob += pulp.lpSum(costs[p][m] * x[p, m] for p in people for m in machines)

    # 约束条件1：每个人只能分配一个机器
    for p in people:
        prob += pulp.lpSum(x[p, m] for m in machines) == 1

    # 约束条件2：每个机器只能分配给一个人
    for m in machines:
        prob += pulp.lpSum(x[p, m] for p in people) == 1

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        total_cost = pulp.value(prob.objective)
        print(f"最小总成本：{total_cost}百元")

        print("\n分配方案：")
        for p in people:
            for m in machines:
                if pulp.value(x[p, m]) > 0:
                    print(f"{p}分配到机器{m}，成本{costs[p][m]}百元")
                    if p == "乙":  # 特别输出乙的分配
                        print(f"  乙应由机器{m}执行   ")
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_assignment()
