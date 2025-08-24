import numpy as np

# 输入数据
xt = np.array([1])
ht_1 = np.array([0])
Ct_1 = np.array([0])

# 权重参数
Wf = np.array([0.5, 0.5])  # 遗忘门
Wi = np.array([0.4, 0.4])  # 输入门
Wc = np.array([0.4, 0.4])  # 候选记忆
Wo = np.array([0.5, 0.5])  # 输出门

# 拼接输入
concat = np.concatenate((ht_1, xt))

# 计算各门控
ft = 1 / (1 + np.exp(-np.dot(Wf, concat)))  # 遗忘门
it = 1 / (1 + np.exp(-np.dot(Wi, concat)))  # 输入门
C_tilde = np.tanh(np.dot(Wc, concat))       # 候选记忆
ot = 1 / (1 + np.exp(-np.dot(Wo, concat)))  # 输出门

# 更新记忆和输出
Ct = ft * Ct_1 + it * C_tilde
ht = ot * np.tanh(Ct)

print(f"遗忘门 ft: {ft:.4f}")
print(f"输入门 it: {it:.4f}")
print(f"候选记忆 C̃t: {C_tilde:.4f}")
print(f"输出门 ot: {ot:.4f}")
print(f"记忆状态 Ct: {Ct[0]:.4f}")
print(f"输出值 ht: {ht[0]:.4f}")

# 理论输出
d = 0.6

# 前向传播结果
ht = 0.1393
Ct = 0.2274
ot = 0.6225
concat = np.array([0, 1])  # [ht_1, xt]

# 计算梯度
dL_dy = ht - d

# 输出门相关导数
dht_dot = np.tanh(Ct)
dot_dzo = ot * (1 - ot)

# W_o梯度
dL_dWo = dL_dy * dht_dot * dot_dzo * concat

# 权重更新
learning_rate = 0.1
Wo_new = Wo - learning_rate * dL_dWo

print(f"损失函数梯度: {dL_dy:.4f}")
print(f"ht对ot的梯度: {dht_dot:.4f}")
print(f"ot对zo的梯度: {dot_dzo:.4f}")
print(f"Wo的梯度: {dL_dWo}")
print(f"更新后的Wo: {Wo_new}")