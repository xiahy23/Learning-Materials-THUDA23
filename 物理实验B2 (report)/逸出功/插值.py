from scipy import interpolate

# 原始数据
A_original = [0.500, 0.550, 0.600, 0.650, 0.700, 0.750]
T_original = [1726, 1809, 1901, 1975, 2059, 2136]

# 创建线性插值函数
f = interpolate.interp1d(A_original, T_original, kind='linear')

# 打印表头
print("A\t\tT(K)")

# 生成从0.50到0.75，步长为0.01的A值，并计算对应的T值
for a_value in range(50, 76):  # 从50到75，对应0.50到0.75
    a = a_value / 100.0  # 转换为浮点数
    t = f(a)  # 计算插值
    print(f"{a:.2f}\t\t{t:.1f}")