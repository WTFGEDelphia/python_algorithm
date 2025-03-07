from itertools import permutations

"""
流水线调度问题

某企业拟生产甲、乙、丙、丁四个产品。每个产品必须依次由设计部门、制造部门和检验部门进行设计、制造和检验，每个部门生产产品的顺序是相同的。各产品各工序所需的时间如下表所示：

| 项目 | 设计（天） | 制造（天） | 检验（天） |
| :--- | :--------- | :--------- | :--------- |
| 甲   | 13         | 15         | 20         |
| 乙   | 10         | 20         | 18         |
| 丙   | 20         | 16         | 10         |
| 丁   | 8          | 10         | 15         |

只要适当安排好项目实施顺序，企业最快可以在（ ）天全部完成这四个项目。

解题思路：
本题的关键是要找到一个最优的流水线调度顺序。
做这类题，有一个基本的原则：把多个任务中，第1步耗时最短的安排在最开始执行，再把最后1步耗时最短的安排在最后完成。所以在本题中最先应执行的是丁项目，最后执行的是丙项目。这样所有的安排方案只有两个：
1、丁甲乙丙
2、丁乙甲丙

通过画时空图可知丁甲乙丙执行时间如图所示，总执行时间为84天，而丁乙甲丙执行时间如图所示，总执行时间为90天。

时间（天）:  0  8  10 13 15 20 36 56 74 84
-------------------------------------------------
设计        |丁  |甲  |乙  |丙
-------------------------------------------------
制造        |    |丁  |甲  |乙  |丙
-------------------------------------------------
检验        |    |    |丁  |甲  |乙  |丙
"""


def calculate_completion_time(sequence, times):
    """计算给定顺序的完成时间"""
    n = len(sequence)
    # 初始化每个部门的完成时间
    design_end = [0] * n  # 设计部门完成时间
    manufacture_end = [0] * n  # 制造部门完成时间
    inspect_end = [0] * n  # 检验部门完成时间

    # 计算第一个项目的各阶段完成时间
    design_end[0] = times[sequence[0]]["design"]
    manufacture_end[0] = design_end[0] + times[sequence[0]]["manufacture"]
    inspect_end[0] = manufacture_end[0] + times[sequence[0]]["inspect"]

    # 计算后续项目的完成时间
    for i in range(1, n):
        # 设计阶段：必须等前一个项目的设计完成
        design_end[i] = design_end[i - 1] + times[sequence[i]]["design"]

        # 制造阶段：必须等当前项目设计完成且前一个项目制造完成
        manufacture_end[i] = (
            max(design_end[i], manufacture_end[i - 1])
            + times[sequence[i]]["manufacture"]
        )

        # 检验阶段：必须等当前项目制造完成且前一个项目检验完成
        inspect_end[i] = (
            max(manufacture_end[i], inspect_end[i - 1]) + times[sequence[i]]["inspect"]
        )

    # 返回最后一个项目的检验完成时间
    return inspect_end[-1]


def find_optimal_sequence():
    # 定义各项目各阶段所需时间
    times = {
        "甲": {"design": 13, "manufacture": 15, "inspect": 20},
        "乙": {"design": 10, "manufacture": 20, "inspect": 18},
        "丙": {"design": 20, "manufacture": 16, "inspect": 10},
        "丁": {"design": 8, "manufacture": 10, "inspect": 15},
    }

    # 所有可能的项目顺序
    projects = ["甲", "乙", "丙", "丁"]
    all_sequences = list(permutations(projects))

    # 找出最优顺序
    min_time = float("inf")  # 初始化最小完成时间为无穷大
    optimal_sequence = None  # 初始化最优顺序为None

    for sequence in all_sequences:
        time = calculate_completion_time(sequence, times)
        if time < min_time:
            min_time = time
            optimal_sequence = sequence

    return optimal_sequence, min_time


def main():
    sequence, total_time = find_optimal_sequence()
    print(f"最优项目顺序：{'->'.join(sequence)}")
    print(f"最短完成时间：{total_time}天")


if __name__ == "__main__":
    main()
