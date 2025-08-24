import matplotlib.pyplot as plt
import numpy as np
# 设置字体和负号显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 数据
x = np.array([5.2, 9.8, 15.3, 19.2, 25, 8, 12, 18])  # 月销售额（万元）
y = np.array([5000, 7200, 9300, 11000, 12800, 6300, 8000, 10000])  # 月薪（元）

# 绘制散点图
plt.figure(figsize=(8, 5))
plt.scatter(x, y, color='blue', label='实际数据点')
plt.title('员工月薪关于月销售额的散点图', fontsize=14)
plt.xlabel('月销售额（万元）', fontsize=12)
plt.ylabel('月薪（元）', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.show()