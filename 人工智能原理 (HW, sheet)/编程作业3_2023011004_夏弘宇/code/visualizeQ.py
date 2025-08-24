import numpy as np
import matplotlib.pyplot as plt
from maze_env import MAZE_H, MAZE_W, INIT_POS, GOAL_POS, TRAP_POS
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
def visualize_q_table(q_table):
    """可视化Q表，显示最优策略和Q值大小"""
    
    # 创建画布
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 绘制网格
    for i in range(MAZE_W+1):
        ax.axvline(i, color='black', lw=1)
    for j in range(MAZE_H+1):
        ax.axhline(j, color='black', lw=1)
    
    # 标记特殊位置
    ax.scatter(INIT_POS[0] + 0.5, INIT_POS[1] + 0.5, color='blue', s=200, marker='o', label='起点')
    ax.scatter(GOAL_POS[0] + 0.5, GOAL_POS[1] + 0.5, color='green', s=200, marker='*', label='火焰杯')
    trap_x = [pos[0] + 0.5 for pos in TRAP_POS]
    trap_y = [pos[1] + 0.5 for pos in TRAP_POS]
    ax.scatter(trap_x, trap_y, color='red', s=200, marker='x', label='陷阱')
    
    # 动作方向映射
    directions = {
        0: (0, -0.3),  # 上
        1: (0, 0.3),   # 下
        2: (0.3, 0),   # 右
        3: (-0.3, 0)   # 左
    }
    arrow_colors = ['blue', 'green', 'red', 'orange']
    
    # 绘制最优动作箭头
    for state in range(q_table.shape[0]):
        if np.all(q_table[state] == 0):  # 跳过未学习的状态
            continue
            
        y = state // MAZE_W
        x = state % MAZE_W
        
        # 所有动作的Q值
        q_values = q_table[state]
        max_q = np.max(q_values)
        
        # 最优动作
        best_action = np.argmax(q_values)
        dx, dy = directions[best_action]
        
        # 显示最优动作的Q值
        ax.text(x+0.5, y+0.2, f"Q={max_q:.1f}", ha='center', va='center', fontsize=9)
        
        # 绘制表示最优动作的箭头
        if max_q > 0:  # 只绘制正向Q值的箭头
            ax.arrow(x+0.5, y+0.5, dx, dy, head_width=0.15, head_length=0.15, 
                    fc=arrow_colors[best_action], ec=arrow_colors[best_action], width=0.05)
    
    # 设置坐标轴
    ax.set_xlim(0, MAZE_W)
    ax.set_ylim(MAZE_H, 0)  # 反转Y轴使(0,0)在左上角
    ax.set_xticks(np.arange(0.5, MAZE_W, 1))
    ax.set_yticks(np.arange(0.5, MAZE_H, 1))
    ax.set_xticklabels(range(MAZE_W))
    ax.set_yticklabels(range(MAZE_H))
    
    ax.set_title('哈利波特的最优策略图', fontsize=16)
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('q_table_visualization.png', dpi=300)
    plt.show()

# 将提供的Q表转换为numpy数组
q_table = np.array([
    [-0.83, -4.08, 40.60, -1.03],
    [-3.76, -2.95, 52.83, 0.38],
    [-2.40, -2.71, 64.73, 1.24],
    [10.88, 76.25, -0.74, 2.99],
    [-0.50, -0.54, -0.50, -0.42],
    
    [-0.43, -3.32, -3.31, -3.40],
    [4.97, -3.44, -3.44, -3.01],
    [0.00, 0.00, 0.00, 0.00],
    [5.72, 87.78, -0.20, -1.00],
    [-0.22, -0.38, -0.50, -0.14],
    
    [-2.81, -2.80, -2.71, -2.93],
    [0.00, 0.00, 0.00, 0.00],
    [0.00, 0.00, 0.00, 0.00],
    [-0.08, 5.68, 0.28, 99.98],
    [-0.22, -0.40, 0.00, 14.02],
    
    [-2.30, -2.23, -2.71, -2.42],
    [0.00, 0.00, 0.00, 0.00],
    [0.00, -0.22, -0.14, -1.00],
    [34.61, 0.00, -0.32, 0.00],
    [-0.20, -0.20, -0.50, 4.07],
    
    [-1.78, -1.97, -1.73, -2.33],
    [-1.90, -1.44, -1.03, -1.15],
    [-0.54, -0.50, -0.54, -0.44],
    [0.40, -0.50, -0.20, -0.20],
    [-0.20, -0.50, -0.50, -0.20]
])

def visualize_q_heatmap(q_table):
    """使用热力图可视化Q表的最大值"""
    
    # 提取每个状态的最大Q值
    max_q_values = np.max(q_table, axis=1).reshape(MAZE_H, MAZE_W)
    
    plt.figure(figsize=(10, 8))
    
    # 绘制热力图
    im = plt.imshow(max_q_values, cmap='YlOrRd')
    cbar = plt.colorbar(im)
    cbar.set_label('最大Q值')
    
    # 添加标记
    for i in range(MAZE_H):
        for j in range(MAZE_W):
            state_idx = i * MAZE_W + j
            max_q = np.max(q_table[state_idx])
            best_action = np.argmax(q_table[state_idx])
            action_symbols = ['↑', '↓', '→', '←']
            
            if (i, j) == tuple(INIT_POS):
                plt.scatter(i, j, color='blue', s=100, marker='o')
                text = f"S\n{action_symbols[best_action]} {max_q:.1f}"
            elif (i, j) == tuple(GOAL_POS):
                plt.scatter(i, j, color='green', s=100, marker='*')
                text = f"G\n{action_symbols[best_action]} {max_q:.1f}"
            elif [i, j] in TRAP_POS:
                plt.scatter(i, j, color='red', s=100, marker='x')
                text = f"T\n{action_symbols[best_action]} {max_q:.1f}"
            else:
                text = f"{action_symbols[best_action]} {max_q:.1f}"
                
            plt.text(j, i, text, ha='center', va='center', 
                     bbox=dict(facecolor='white', alpha=0.5))
    
    plt.title('Q值热力图与最优动作', fontsize=16)
    plt.xticks(range(MAZE_W))
    plt.yticks(range(MAZE_H))
    plt.grid(True, color='white', linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('q_heatmap.png', dpi=300)
    plt.show()

visualize_q_heatmap(q_table)