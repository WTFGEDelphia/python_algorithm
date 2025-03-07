import pulp

"""
决策树问题

生产某种产品有两个建厂方案：
（1）建大厂，需要初期投资500万元。如果产品销路好，每年可以获利200万元；如果销路不好，每年会亏损20万元。
（2）建小厂，需要初期投资200万元。如果产品销路好，每年可以获利100万元；如果销路不好，每年只能获利20万元。
市场调研表明，未来2年这种产品销路好的概率为70%。如果这2年销路好，则后续5年销路好的概率上升为80%；
如果这2年销路不好，则后续5年销路好的概率仅为10%。为取得7年最大总收益，决策者应（ ）。
"""


def calculate_expected_value():
    # 初始投资
    large_investment = 500  # 大厂投资500万
    small_investment = 200  # 小厂投资200万

    # 未来2年的销路概率
    initial_success_rate = 0.7  # 70%概率好
    initial_failure_rate = 0.3  # 30%概率差

    # 后续5年的销路概率
    success_after_success = 0.8  # 如果前2年好，后5年80%概率好
    success_after_failure = 0.1  # 如果前2年差，后5年10%概率好

    def calculate_large_factory():
        # 大厂方案
        # 前2年
        success_2y = 200 * 2  # 好的情况每年赚200
        failure_2y = -20 * 2  # 差的情况每年亏20

        # 后5年
        success_5y = 200 * 5  # 好的情况每年赚200
        failure_5y = -20 * 5  # 差的情况每年亏20

        # 计算期望值
        expected_value = -large_investment  # 先减去投资

        # 前2年好的情况 (70%概率)
        good_path = initial_success_rate * (
            success_2y  # 前2年的收益
            + (
                success_after_success * success_5y  # 后5年好的情况
                + (1 - success_after_success) * failure_5y
            )  # 后5年差的情况
        )

        # 前2年差的情况 (30%概率)
        bad_path = initial_failure_rate * (
            failure_2y  # 前2年的收益
            + (
                success_after_failure * success_5y  # 后5年好的情况
                + (1 - success_after_failure) * failure_5y
            )  # 后5年差的情况
        )

        return expected_value + good_path + bad_path

    def calculate_small_factory():
        # 小厂方案
        # 前2年
        success_2y = 100 * 2  # 好的情况每年赚100
        failure_2y = 20 * 2  # 差的情况每年赚20

        # 后5年
        success_5y = 100 * 5  # 好的情况每年赚100
        failure_5y = 20 * 5  # 差的情况每年赚20

        # 计算期望值
        expected_value = -small_investment  # 先减去投资

        # 前2年好的情况 (70%概率)
        good_path = initial_success_rate * (
            success_2y  # 前2年的收益
            + (
                success_after_success * success_5y  # 后5年好的情况
                + (1 - success_after_success) * failure_5y
            )  # 后5年差的情况
        )

        # 前2年差的情况 (30%概率)
        bad_path = initial_failure_rate * (
            failure_2y  # 前2年的收益
            + (
                success_after_failure * success_5y  # 后5年好的情况
                + (1 - success_after_failure) * failure_5y
            )  # 后5年差的情况
        )

        return expected_value + good_path + bad_path

    # 计算两种方案的期望值
    large_factory_value = calculate_large_factory()
    small_factory_value = calculate_small_factory()

    print(f"建大厂的期望收益：{large_factory_value:.2f}万元")
    print(f"建小厂的期望收益：{small_factory_value:.2f}万元")

    if large_factory_value > small_factory_value:
        print("\n建议选择：建大厂")
    else:
        print("\n建议选择：建小厂")


if __name__ == "__main__":
    calculate_expected_value()
