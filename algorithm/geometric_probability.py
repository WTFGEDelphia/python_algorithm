"""
1路和2路公交车都将在10分钟内均匀随机地到达同一车站，则它们相隔4分钟内到达该站的概率为（   ）。
"""

import random
import numpy as np


# 蒙特卡洛模拟方法
def monte_carlo_simulation(n_trials=1000000):
    count = 0
    for _ in range(n_trials):
        t1 = random.uniform(0, 10)  # 第一辆车到达时间
        t2 = random.uniform(0, 10)  # 第二辆车到达时间
        if abs(t1 - t2) <= 4:
            count += 1
    return count / n_trials


# 几何概率方法
def geometric_probability():
    # 总面积
    total_area = 10 * 10

    # |t1-t2| <= 4 的区域面积
    # 这是一个宽度为4的带状区域
    favorable_area = 10 * 8 - 16  # 总带宽区域减去超出正方形的部分

    probability = favorable_area / total_area
    return probability


if __name__ == "__main__":
    probability = monte_carlo_simulation()
    print(f"两辆公交车在4分钟内到达的概率为：{probability:.3f}")
    probability = geometric_probability()
    print(f"两辆公交车在4分钟内到达的概率为：{probability:.3f}")
