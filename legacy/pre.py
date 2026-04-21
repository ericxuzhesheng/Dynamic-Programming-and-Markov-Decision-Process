import numpy as np

# 定义参数
gamma = 0.9  # 折扣因子
max_iterations = 100  # 最大迭代次数
epsilon = 1e-6  # 收敛阈值

# 奖励函数 R(s,a)
# (状态，动作) -> 奖励值
# 状态: 0=上涨(s1), 1=下跌(s2)
# 动作: 0=买入(a1), 1=卖出(a2)
R = {
    (0, 0): 10,  # 上涨时买入
    (0, 1): -5,  # 上涨时卖出
    (1, 0): -10,  # 下跌时买入
    (1, 1): 5,  # 下跌时卖出
}

# 转移概率 P(s'|s,a)
# (状态，动作) -> [转移到s1的概率, 转移到s2的概率]
P = {
    (0, 0): np.array([0.7, 0.3]),  # 上涨时买入 -> [0.7概率仍上涨, 0.3概率变下跌]
    (0, 1): np.array([0.3, 0.7]),  # 上涨时卖出 -> [0.3概率仍上涨, 0.7概率变下跌]
    (1, 0): np.array([0.3, 0.7]),  # 下跌时买入 -> [0.3概率变上涨, 0.7概率仍下跌]
    (1, 1): np.array([0.7, 0.3]),  # 下跌时卖出 -> [0.7概率变上涨, 0.3概率仍下跌]
}

# 初始化策略 π(a|s)
# pi[s, a] 表示在状态s下选择动作a的概率
pi = np.zeros((2, 2))
pi[0, 0] = 1.0  # 初始策略：上涨状态(s1)选择买入(a1)
pi[1, 0] = 1.0  # 初始策略：下跌状态(s2)选择买入(a1)

# 策略迭代主循环
iteration = 0
while iteration < max_iterations:
    iteration += 1
    print(f"\n第{iteration}轮策略迭代:")

    # 步骤1: 策略评估 - 计算当前策略下的状态值函数V(s)
    print("策略评估 - 计算当前策略下的值函数")
    V = np.zeros(2)  # 初始化值函数
    eval_iteration = 0

    while True:
        eval_iteration += 1
        V_new = np.zeros(2)

        for s in range(2):
            # 根据当前策略计算状态s的值
            for a in range(2):
                # V(s) += π(a|s) * [R(s,a) + γ * Σ P(s'|s,a) * V(s')]
                V_new[s] += pi[s, a] * (R[(s, a)] + gamma * np.dot(P[(s, a)], V))

        # 检查值函数是否收敛
        delta = np.max(np.abs(V_new - V))
        V = V_new  # 更新值函数

        if delta < epsilon:
            print(
                f"  值函数在{eval_iteration}次迭代后收敛: V(s1)={V[0]:.4f}, V(s2)={V[1]:.4f}"
            )
            break

        if eval_iteration > max_iterations:
            print("  值函数评估达到最大迭代次数")
            break

    # 步骤2: 策略改进 - 基于当前值函数V选择最优动作
    print("策略改进 - 更新策略")
    policy_stable = True
    new_pi = np.zeros((2, 2))

    for s in range(2):
        old_action = np.argmax(pi[s])

        # 计算每个动作的行动值函数Q(s,a)
        q_values = np.zeros(2)
        for a in range(2):
            # Q(s,a) = R(s,a) + γ * Σ P(s'|s,a) * V(s')
            q_values[a] = R[(s, a)] + gamma * np.dot(P[(s, a)], V)

        # 选择Q值最大的动作
        best_a = np.argmax(q_values)
        new_pi[s, best_a] = 1.0

        # 检查策略是否变化
        if old_action != best_a:
            policy_stable = False
            print(f"  状态s{s+1}的策略从a{old_action+1}变为a{best_a+1}")

    # 更新策略
    pi = new_pi

    # 如果策略稳定，结束迭代
    if policy_stable:
        print("策略已稳定，停止迭代")
        break

# 输出最终结果
print("\n最优策略：")
for s in range(2):
    action_desc = "买入(a1)" if np.argmax(pi[s]) == 0 else "卖出(a2)"
    state_desc = "上涨(s1)" if s == 0 else "下跌(s2)"
    print(f"状态 {state_desc}：动作 {action_desc}")

print(f"对应状态值函数：V(s1) = {V[0]:.4f}, V(s2) = {V[1]:.4f}")

# 计算最优策略下的Q值
print("\n最优策略下的行动值函数Q(s,a)：")
for s in range(2):
    for a in range(2):
        q_value = R[(s, a)] + gamma * np.dot(P[(s, a)], V)
        state_desc = "上涨(s1)" if s == 0 else "下跌(s2)"
        action_desc = "买入(a1)" if a == 0 else "卖出(a2)"
        print(f"Q({state_desc}, {action_desc}) = {q_value:.4f}")
