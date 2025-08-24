import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import math
import sys

# 设置全局字体为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决坐标轴负号显示问题
plt.rcParams['axes.unicode_minus'] = False
class OutputRedirector:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.file = open(filename, 'w', encoding='utf-8')
    
    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)
    
    def flush(self):
        self.terminal.flush()
        self.file.flush()
        
    def close(self):
        self.file.close()

# 设置输出重定向
sys.stdout = OutputRedirector('实验结果.txt')

# 实验数据
data = {
    # If(A), T(K), 采样电阻(Ω), [Ua1...Ua8](V), [Ue'1...Ue'8](mV)
    0.50: {"T": 1726, "R": 2700, "Ua": [23.73, 33.72, 43.7, 53.7, 63.69, 73.69, 83.68, 93.68], 
           "Ue": [2.84, 2.89, 2.94, 2.97, 3.04, 3.08, 3.09, 3.12]},
    0.54: {"T": 1792.4, "R": 2700, "Ua": [23.55, 33.57, 43.54, 53.54, 63.53, 73.58, 83.51, 93.52], 
           "Ue": [10.25, 10.45, 10.6, 10.74, 10.89, 11.02, 11.14, 11.25]},
    0.58: {"T": 1864.2, "R": 2700, "Ua": [23.37, 33.36, 43.33, 53.33, 63.33, 73.33, 83.32, 93.31], 
           "Ue": [32.28, 32.95, 33.46, 33.89, 34.28, 34.65, 35, 35.34]},
    0.62: {"T": 1930.6, "R": 2700, "Ua": [23.18, 33.16, 43.16, 53.15, 63.15, 73.14, 83.13, 93.13], 
           "Ue": [92.24, 93.84, 95.19, 96.28, 97.38, 98.45, 99.47, 100.16]},
    0.66: {"T": 1991.8, "R": 270, "Ua": [22.96, 32.95, 42.93, 52.92, 62.92, 72.91, 82.91, 92.91], 
           "Ue": [24.24, 24.67, 24.95, 25.38, 25.46, 25.73, 25.98, 26.19]},
    0.70: {"T": 2059, "R": 270, "Ua": [22.75, 32.75, 42.73, 52.73, 62.71, 72.71, 82.7, 92.7], 
           "Ue": [58.35, 59.34, 60.14, 60.88, 61.47, 62.11, 62.64, 63.11]}
}

# 第一步: 创建图1: lg(I'e) ~ sqrt(Ua) 
plt.figure(figsize=(10, 6))
colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown']
markers = ['o', 's', '^', 'D', 'x', '*']

# 记录每个温度下拟合得到的截距(即lg(I_e))
I_e_data = {}  # 将存储温度T和对应的I_e值

# 创建结果保存表格

for i, (If, values) in enumerate(data.items()):
    T = values["T"]
    
    # 计算I'e (mA)
    I_e = [ue / values["R"] for ue in values["Ue"]]  # 单位为A
    I_e = [ie * 1000 for ie in I_e]  # 转换为mA
    
    # 计算sqrt(Ua)和lg(I'e)
    sqrt_Ua = [math.sqrt(ua) for ua in values["Ua"]]
    lg_Ie = [math.log10(ie) for ie in I_e]
    
    # 线性拟合
    slope, intercept = np.polyfit(sqrt_Ua, lg_Ie, 1)
    r = np.corrcoef(sqrt_Ua, lg_Ie)[0, 1]
    
    # 保存截距值，这是lg(I_e)
    I_e_data[T] = intercept
    
    # 计算拟合线
    fit_line = [slope * x + intercept for x in sqrt_Ua]
    
    # 绘制散点和拟合线
    plt.scatter(sqrt_Ua, lg_Ie, marker=markers[i], color=colors[i], s=50)
    plt.plot(sqrt_Ua, fit_line, color=colors[i], 
             label=f'If={If}A, T={T}K, y={slope:.3f}x+{intercept:.5f}, r={r:.3f}')

plt.xlabel('$\sqrt{U_a} (V^{1/2})$', fontsize=12)
plt.ylabel('$lg(I\'_e) (lg(mA))$', fontsize=12)
plt.title('l$g(I\'_e) \sim \sqrt{U_a}$线性拟合', fontsize=14)
plt.grid(True)
plt.legend(loc='best', fontsize=9)
plt.tight_layout()
plt.savefig('lg_Ie_vs_sqrt_Ua_fitted.png', dpi=300)

# 第二步: 根据Richardson-Dushman方程拟合 lg(I_e/T^2) vs 1/T
plt.figure(figsize=(10, 6))

# 处理之前得到的截距(lg(I_e))数据
temps = list(I_e_data.keys())
lg_I_es = list(I_e_data.values())

# 计算lg(I_e/T^2)和1/T
x_data = [1/T for T in temps]  # 1/T
y_data = [lg_I_e - 2*math.log10(T) for lg_I_e, T in zip(lg_I_es, temps)]  # lg(I_e/T^2) = lg(I_e) - lg(T^2)

# 线性拟合
slope, intercept = np.polyfit(x_data, y_data, 1)
r = np.corrcoef(x_data, y_data)[0, 1]

# 计算拟合线
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = [slope * x + intercept for x in x_fit]

# 绘制散点和拟合线
plt.scatter(x_data, y_data, marker='o', s=60, color='blue')
plt.plot(x_fit, y_fit, '--', color='red', 
         label=f'拟合线: y={slope:.5e}x+{intercept:.2f}, r={r:.4f}')

plt.xlabel('$1/T ~~ (K^{-1})$', fontsize=12)
plt.ylabel('$lg\\frac{I_e}{T^2} ~~ (lg(mA/K^2))$', fontsize=12)
plt.title('$lg\\frac{I_e}{T^2} \sim \\frac{1}{T}$', fontsize=14)
plt.grid(True)
plt.legend(loc='best', fontsize=10)
plt.tight_layout()
plt.savefig('Richardson_Dushman_fit.png', dpi=300)

# 计算物理量：逸出功
# 根据Richardson-Dushman方程：ln(I_e/T^2) = ln(A) - eφ/(kT)
# 斜率 = -eφ/(k*ln(10))
k = 1.380649e-23  # 玻尔兹曼常数 J/K
e = 1.602176634e-19  # 电子电荷 C

# 逸出功计算: φ = -k*slope/e * ln(10)
phi = -k * slope / e * math.log(10)

plt.show()

# 打印逸出功结果到一个表格
print("\n========== 实验结果总结 ==========")
print("零场发射电流I_e值:")
for T, lg_I_e in I_e_data.items():
    I_e = 10**lg_I_e  # 单位为mA
    print(f"T = {T}K: lg(I_e) = {lg_I_e:.4f}, I_e = {I_e:.4e} mA")

print(f"\n斜率 = {slope:.4e}")
print(f"截距 = {intercept:.4f}")
print(f"相关系数 r = {r:.4f}")
print(f"逸出功 φ = {phi:.4f} eV")

sys.stdout.close()
# 恢复标准输出
sys.stdout = sys.__stdout__