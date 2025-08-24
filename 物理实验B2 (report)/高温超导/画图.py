import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

# 直接使用提供的数据创建DataFrame
# 升温数据
heating_ut = [36.08, 35.17, 34.35, 33.82, 33.76, 33.69, 33.63, 33.58, 33.51, 33.48, 33.45, 33.44, 33.39, 33.32, 32.34, 31.47, 30.67, 29.85, 29, 28.17, 27.37, 26.56, 26.15, 25.83, 25.4, 24.88, 24.22]
heating_usuper = [0.105, 0.103, 0.102, 0.099, 0.099, 0.098, 0.096, 0.073, 0.059, 0.046, 0.046, 0.026, 0.02, 0.019, 0.018, 0.018, 0.019, 0.019, 0.019, 0.019, 0.019, 0.019, 0.019, 0.02, 0.019, 0.02, 0.02]
heating_um = [23.36, 23.4, 23.44, 23.47, 23.52, 23.48, 23.48, 23.48, 23.48, 23.49, 23.49, 23.49, 23.49, 23.5, 23.54, 23.58, 23.62, 23.66, 23.7, 23.72, 23.76, 23.32, 21.21, 19.42, 17.97, 16.41, 15.22]

# 降温数据
cooling_ut = [20.89, 21.57, 22.46, 23.24, 24.8, 24.91, 25.72, 26.52, 27.37, 28.2, 29, 29.86, 30.24, 30.67, 31.08, 31.47, 31.93, 32.33, 32.72, 32.89, 32.95, 32.98, 33.06, 33.12, 33.11, 33.17, 33.23, 33.26, 33.41, 33.54, 34.36, 35.16, 35.99, 36.81, 37.56]
cooling_usuper = [0.021, 0.022, 0.022, 0.022, 0.021, 0.021, 0.02, 0.02, 0.02, 0.019, 0.019, 0.019, 0.018, 0.019, 0.018, 0.018, 0.018, 0.018, 0.018, 0.019, 0.024, 0.035, 0.045, 0.049, 0.059, 0.067, 0.075, 0.083, 0.096, 0.099, 0.102, 0.104, 0.106, 0.107, 0.109]
cooling_um = [13.56, 13.57, 13.59, 13.62, 13.62, 13.68, 13.76, 13.91, 14.12, 14.47, 14.9, 15.82, 16.14, 17.03, 18.08, 18.89, 20.54, 23.14, 23.79, 23.8, 23.8, 23.8, 23.8, 23.8, 23.8, 23.8, 23.79, 23.79, 23.78, 23.78, 23.73, 23.69, 23.65, 23.6, 23.55]

# 创建DataFrame
cooling_data = pd.DataFrame({
    'Ut': cooling_ut,
    'U_meas': cooling_usuper,
    'U_spur': 0.021,
    'Um': cooling_um
})

heating_data = pd.DataFrame({
    'Ut': heating_ut,
    'U_meas': heating_usuper,
    'U_spur': 0.021,
    'Um': heating_um
})

# 铂电阻温度计算函数
def calculate_temperature(Ut):
    """
    根据铂电阻电压计算温度
    使用简化公式直接计算温度 (假设线性关系)
    """
    # 简化处理：利用Ut与温度的近似计算公式计算
    # 这里使用线性公式进行粗略计算
    # 铂电阻温度计算公式
    A = 3.9083e-3  # °C⁻¹
    B = -5.775e-7  # °C⁻²
    
    # 假设Ut直接对应Rt
    Rt = Ut
    
    # 使用公式: t = (-A + sqrt(A² - 4B(1-0.01Rt)))/(2B)
    discriminant = A**2 - 4*B*(1-0.01*Rt)
    t = (-A + np.sqrt(discriminant)) / (2*B)
    return t

# 数据预处理
def process_data(df):
    """处理单次实验数据"""
    # 计算温度
    df['Temp'] = calculate_temperature(df['Ut'])
    
    # 计算超导样品电阻（考虑乱真电势修正）
    df['U_super'] = df['U_meas'] - df['U_spur'] # 简化：直接使用U_meas1作为样品电压
    df['R_super'] = df['U_super']  # 电流为1mA，电压单位是mV，电阻单位是Ω
    
    # 根据温度从小到大排序
    df = df.sort_values('Temp')
    return df

# 处理降温和升温数据
cooling = process_data(cooling_data)
heating = process_data(heating_data)

# 确定转变温度范围
def find_transition(data):
    """确定超导转变参数"""
    # 首先排序以确保找到正确的转变点
    data = data.sort_values('Temp')
    R_max = data['R_super'].max()
    R_min = data['R_super'].min()
    
    # 寻找特征点
    T_onset = data[data['R_super'] >= 0.9*R_max]['Temp'].iloc[0]
    
    # 查找最后一个电阻值小于0.1*R_max的点
    low_R_data = data[data['R_super'] <= 0.1*R_max]
    if len(low_R_data) > 0:
        T_end = low_R_data['Temp'].iloc[-1]
    else:
        T_end = data['Temp'].min()  # 如果没有找到，使用最低温度
    
    # 查找第一个电阻值小于0.5*R_max的点
    mid_R_data = data[data['R_super'] <= 0.5*R_max]
    if len(mid_R_data) > 0:
        T_middle = mid_R_data['Temp'].iloc[-1]
    else:
        T_middle = (T_onset + T_end) / 2  # 如果没有找到，取中点
    
    return T_onset, T_end, T_middle

# 绘图设置
plt.rcParams.update({
    'font.family': 'SimHei',
    'axes.unicode_minus': False,
    'font.size': 12
})

# 绘制电阻-温度曲线
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

# 降温过程
# 获取升温过程的转变参数
T_onset, T_end, T_middle = find_transition(cooling)
delta_T = T_onset - T_end
ax1.plot(cooling['Temp'], cooling['R_super'], 'b-', label='降温过程')
ax1.scatter(cooling['Temp'], cooling['R_super'], marker='x', color='b', s=30)
ax1.axvline(T_middle, color='k', linestyle='--', label=f'Tc={T_middle:.2f}℃')
ax1.axvspan(T_end, T_onset, alpha=0.2, color='gray', label=f'ΔT={delta_T:.2f}℃')
ax1.set(xlabel='温度 (℃)', ylabel='样品电阻 (Ω)', 
    title='超导样品电阻-温度特性曲线')
ax1.legend()
print(f"""
超导转变参数（降温过程）:
中点转变温度 Tc = {T_middle:.2f} ℃
转变宽度 ΔTc = {delta_T:.2f} ℃
""")

# 升温过程
# 获取升温过程的转变参数
T_onset, T_end, T_middle = find_transition(heating)
delta_T = T_onset - T_end
ax2.plot(heating['Temp'], heating['R_super'], 'r-', label='升温过程')
ax2.scatter(heating['Temp'], heating['R_super'], marker='x', color='r', s=30)
ax2.axvline(T_middle, color='k', linestyle='--', label=f'Tc={T_middle:.2f}℃')
ax2.axvspan(T_end, T_onset, alpha=0.2, color='gray', label=f'ΔT={delta_T:.2f}℃')
ax2.set(xlabel='温度 (℃)', ylabel='样品电阻 (Ω)')
ax2.legend()
print(f"""
超导转变参数（升温过程）:
中点转变温度 Tc = {T_middle:.2f} ℃
转变宽度 ΔTc = {delta_T:.2f} ℃
""")

# 绘制感应电压-温度曲线
# 绘制感应电压-温度曲线（分为升温和降温两个子图）
fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(10, 12))

# 降温过程
ax3.plot(cooling['Temp'], cooling['Um'], 'b-', label='降温过程')
ax3.scatter(cooling['Temp'], cooling['Um'], marker='x', color='b', s=30)
ax3.set(xlabel='温度 (℃)', ylabel='感应电压 (mV)', 
    title='感应电压-温度特性曲线')
ax3.legend()

# 升温过程
ax4.plot(heating['Temp'], heating['Um'], 'r-', label='升温过程')
ax4.scatter(heating['Temp'], heating['Um'], marker='x', color='r', s=30)
ax4.set(xlabel='温度 (℃)', ylabel='感应电压 (mV)')
ax4.legend()

plt.tight_layout()
plt.show()

# 输出关键参数
print(f"""
超导转变参数（升温过程）:
中点转变温度 Tc = {T_middle:.2f} ℃
转变宽度 ΔTc = {delta_T:.2f} ℃
""")

# 在现有代码最后添加以下内容（在plt.show()之后）

# 创建数据表格并保存
def create_data_tables(heating_df, cooling_df):
    """创建包含铂电阻阻值和超导样品电阻的数据表格"""
    # 选择需要的列并准备数据
    heating_table = heating_df[['Ut', 'Temp', 'R_super']].copy()
    cooling_table = cooling_df[['Ut', 'Temp', 'R_super']].copy()
    
    # 重命名列以便更清晰
    columns = ['铂电阻阻值(Rt)/mV', '温度(T)/℃', '超导样品电阻(R_super)/Ω']
    heating_table.columns = columns
    cooling_table.columns = columns
    
    # 保存到CSV文件
    heating_file = 'heating_data_table.csv'
    cooling_file = 'cooling_data_table.csv'
    heating_table.to_csv(heating_file, index=False, encoding='utf-8-sig')
    cooling_table.to_csv(cooling_file, index=False, encoding='utf-8-sig')
    
    # 为控制台显示选择适当数量的行
    if len(heating_table) > 8:
        step = max(1, len(heating_table) // 8)
        display_heating = heating_table.iloc[::step].head(8).round(4)
    else:
        display_heating = heating_table.round(4)
    
    if len(cooling_table) > 8:
        step = max(1, len(cooling_table) // 8)
        display_cooling = cooling_table.iloc[::step].head(8).round(4)
    else:
        display_cooling = cooling_table.round(4)
    
    print("\n升温过程数据表（样本）：")
    print(display_heating.to_string(index=False))
    print(f"\n完整数据已保存至: {heating_file}（共{len(heating_table)}行）")
    
    print("\n降温过程数据表（样本）：")
    print(display_cooling.to_string(index=False))
    print(f"\n完整数据已保存至: {cooling_file}（共{len(cooling_table)}行）")
    
    return heating_table, cooling_table

# 输出关键参数
print(f"""
超导转变参数（升温过程）:
中点转变温度 Tc = {T_middle:.2f} ℃
转变宽度 ΔTc = {delta_T:.2f} ℃
""")

# 创建并显示数据表格
heating_table, cooling_table = create_data_tables(heating, cooling)