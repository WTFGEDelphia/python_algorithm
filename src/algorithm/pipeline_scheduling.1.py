import pulp

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

"""


def solve_flow_shop():
    # 创建流水线调度问题
    prob = pulp.LpProblem("流水线调度问题", pulp.LpMinimize)

    # 定义数据
    products = ["甲", "乙", "丙", "丁"]
    times = {
        "甲": {"design": 13, "manufacture": 15, "inspect": 20},
        "乙": {"design": 10, "manufacture": 20, "inspect": 18},
        "丙": {"design": 20, "manufacture": 16, "inspect": 10},
        "丁": {"design": 8, "manufacture": 10, "inspect": 15},
    }

    # 决策变量：每个产品的开始时间
    design_start = pulp.LpVariable.dicts("design_start", products, lowBound=0)
    manufacture_start = pulp.LpVariable.dicts("manufacture_start", products, lowBound=0)
    inspect_start = pulp.LpVariable.dicts("inspect_start", products, lowBound=0)

    # 决策变量：产品顺序（二进制变量）
    sequence = pulp.LpVariable.dicts(
        "seq", ((i, j) for i in products for j in range(len(products))), cat="Binary"
    )

    # 目标函数：最小化最后一个产品的完成时间
    makespan = pulp.LpVariable("makespan", lowBound=0)
    prob += makespan

    # 约束条件
    M = 1000  # 大数

    # 1. 每个位置只能安排一个产品
    for j in range(len(products)):
        prob += pulp.lpSum(sequence[i, j] for i in products) == 1

    # 2. 每个产品只能安排一次
    for i in products:
        prob += pulp.lpSum(sequence[i, j] for j in range(len(products))) == 1

    # 3. 工序顺序约束
    for i in products:
        # 制造必须在设计完成后开始
        prob += manufacture_start[i] >= design_start[i] + times[i]["design"]
        # 检验必须在制造完成后开始
        prob += inspect_start[i] >= manufacture_start[i] + times[i]["manufacture"]
        # 完工时间约束
        prob += makespan >= inspect_start[i] + times[i]["inspect"]

    # 4. 相邻产品的同步等待约束
    for i in products:
        for k in products:
            if i != k:
                for j in range(len(products) - 1):
                    # 如果产品i在位置j，产品k在位置j+1
                    # 设计部门约束 后一个产品必须等前一个产品设计完成
                    prob += design_start[k] >= (
                        design_start[i]
                        + times[i]["design"]
                        - M * (2 - sequence[i, j] - sequence[k, j + 1])
                    )
                    # 制造部门约束 后一个产品必须等前一个产品制造完成
                    prob += manufacture_start[k] >= (
                        manufacture_start[i]
                        + times[i]["manufacture"]
                        - M * (2 - sequence[i, j] - sequence[k, j + 1])
                    )
                    # 检验部门约束 后一个产品必须等前一个产品检验完成
                    prob += inspect_start[k] >= (
                        inspect_start[i]
                        + times[i]["inspect"]
                        - M * (2 - sequence[i, j] - sequence[k, j + 1])
                    )

    # 求解
    prob.solve()

    # 输出结果
    if pulp.LpStatus[prob.status] == "Optimal":
        # 获取最优序列
        optimal_sequence = []
        for j in range(len(products)):
            for i in products:
                if pulp.value(sequence[i, j]) == 1:
                    optimal_sequence.append(i)

        print(f"最优生产顺序：{'->'.join(optimal_sequence)}")
        print(f"最短完成时间：{int(pulp.value(makespan))}天")

        # 输出详细时间安排
        print("\n详细时间安排：")
        for i in products:
            print(f"\n{i}产品：")
            print(f"设计开始时间：{int(pulp.value(design_start[i]))}天")
            print(f"制造开始时间：{int(pulp.value(manufacture_start[i]))}天")
            print(f"检验开始时间：{int(pulp.value(inspect_start[i]))}天")
    else:
        print("问题无解")


if __name__ == "__main__":
    solve_flow_shop()
