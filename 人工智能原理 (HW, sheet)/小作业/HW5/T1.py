import numpy as np

# 定义激活函数
def cos_activation(z):
    return np.cos(z)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# 初始化网络参数
W1 = np.array([
    [0.1, 0.1, 0.3],
    [0.2, 0.3, 0.2],
    [0.1, 0.2, 0.1],
    [0.3, 0.1, 0.1]
])
W2 = W1.T  # W2 = W1^T
W3 = np.array([0.2, 0.2, 0.4])
b1 = 0.5
b2 = 0.5
b3 = 0.2

# 前向传播计算
def forward(x):
    # 第一层 (输入层 -> 隐藏层)
    z1 = np.dot(W1, x) + b1
    h1 = cos_activation(z1)
    
    # 第二层 (隐藏层 -> 隐藏层)
    z2 = np.dot(W2, h1) + b2
    h2 = cos_activation(z2)
    
    # 第三层 (隐藏层 -> 输出层)
    z3 = np.dot(W3, h2) + b3
    y = sigmoid(z3)
    
    # 保存中间结果用于反向传播
    cache = {
        'x': x, 'z1': z1, 'h1': h1, 
        'z2': z2, 'h2': h2, 'z3': z3, 'y': y
    }
    
    return y, cache

# 反向传播算法
def backpropagation(cache, target):
    y = cache['y']
    h2 = cache['h2']
    
    # 输出层误差
    dL_dy = y - target  # 损失函数对输出的梯度
    dy_dz3 = y * (1 - y)  # sigmoid导数
    delta3 = dL_dy * dy_dz3  # 输出层误差项
    
    # 计算W3的梯度
    dL_dW3 = delta3 * h2
    
    return dL_dW3, 0.5 * (y - target)**2  # 返回梯度和损失值

# 更新参数
def update_parameters(W3, dW3, learning_rate):
    return W3 - learning_rate * dW3

# 主程序
def main():
    # a) 计算输出
    x = np.array([0.05, 0.10, 0.05])
    y, cache = forward(x)
    print(f"a) 输入 x = {x} 时的计算过程:")
    print(f"   z1 = W1·x + b1 = \n{cache['z1']}")
    print(f"   h1 = cos(z1) = \n{cache['h1']}")
    print(f"   z2 = W2·h1 + b2 = \n{cache['z2']}")
    print(f"   h2 = cos(z2) = \n{cache['h2']}")
    print(f"   z3 = W3·h2 + b3 = {cache['z3']}")
    print(f"   y = sigmoid(z3) = {y}")
    
    # b) 计算W3的梯度
    target = 0.95
    dW3, loss = backpropagation(cache, target)
    print(f"\nb) 当目标输出为 {target} 时:")
    print(f"   损失函数值 = {loss}")
    print(f"   W3的梯度 = {dW3}")
    
    # c) 使用梯度下降更新W3
    learning_rate = 0.1
    W3_new = update_parameters(W3, dW3, learning_rate)
    print(f"\nc) 使用学习率 {learning_rate} 更新W3:")
    print(f"   更新前 W3 = {W3}")
    print(f"   更新后 W3 = {W3_new}")

if __name__ == "__main__":
    main()