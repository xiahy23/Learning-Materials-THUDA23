import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False

# 输入数据
wavelengths = np.array([447.1, 471.3, 492.2, 501.6, 587.6, 667.8, 706.6])  # 波长（nm）
n_values = np.array([1.6703**2, 1.6652**2, 1.6616**2, 1.6592**2, 1.6486**2, 1.6423**2, 1.6401**2])

# 构建特征矩阵X
X = np.column_stack([
    np.ones_like(wavelengths),      # A0项
    wavelengths**2,                 # A1项
    wavelengths**(-2),              # A2项
    wavelengths**(-4),              # A3项
    wavelengths**(-6),              # A4项
    wavelengths**(-8)               # A5项
])

# 使用LinearRegression进行拟合
model = LinearRegression()
model.fit(X, n_values)

# 获取拟合系数
coefficients = model.coef_
A0 = model.intercept_
_, A1, A2, A3, A4, A5 = coefficients

# 计算R²
r2 = model.score(X, n_values)

# 打印拟合结果
print("拟合系数：")
print(f"A0 = {A0:.6e}")
print(f"A1 = {A1:.6e}")
print(f"A2 = {A2:.6e}")
print(f"A3 = {A3:.6e}")
print(f"A4 = {A4:.6e}")
print(f"A5 = {A5:.6e}")
print(f"R² = {r2:.6f}")

# 绘制拟合结果
plt.figure(figsize=(10, 6))
plt.scatter(wavelengths, n_values, color='red', label='实验数据')

# 生成更多点以绘制平滑曲线
wavelengths_fine = np.linspace(np.min(wavelengths), np.max(wavelengths), 100)
X_fine = np.column_stack([
    np.ones_like(wavelengths_fine),
    wavelengths_fine**2,
    wavelengths_fine**(-2),
    wavelengths_fine**(-4),
    wavelengths_fine**(-6),
    wavelengths_fine**(-8)
])
n_predicted = model.predict(X_fine)

def cauchy(lam, A, B, C, D, E, F):
    return A + B * lam**2 + C * lam**(-2) + D * lam**(-4) + E * lam**(-6) + F * lam**(-8)

print(np.sqrt(cauchy(656.3, A0, A1, A2, A3, A4, A5)))
print(np.sqrt(cauchy(589.3, A0, A1, A2, A3, A4, A5)))
print(np.sqrt(cauchy(486.1, A0, A1, A2, A3, A4, A5)))