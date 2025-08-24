import numpy as np
import matplotlib.pyplot as plt
import time
import os
from maze_env import Maze, MAZE_H, MAZE_W, INIT_POS, GOAL_POS, TRAP_POS, UNIT
from agent import QLearningAgent

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def visualize_path(episode, path, success):
    """
    可视化并保存一个回合的路径
    
    绘制5×5迷宫网格
    标记起点、终点和陷阱位置
    处理智能体路径坐标，包括将像素坐标转换为网格坐标
    处理终端状态，根据成功/失败推断最后一步位置
    绘制探索路径并用数字标记每一步
    设置坐标范围、标题和图例
    创建目录并保存路径可视化图像
    """
    plt.figure(figsize=(7, 7))
    
    for c in range(MAZE_W + 1):
        plt.axvline(c, color='black', linestyle='-', alpha=0.2)
    for r in range(MAZE_H + 1):
        plt.axhline(r, color='black', linestyle='-', alpha=0.2)
    
    plt.scatter(INIT_POS[0] + 0.5, INIT_POS[1] + 0.5, color='blue', s=100, marker='o', label='起点')
    plt.scatter(GOAL_POS[0] + 0.5, GOAL_POS[1] + 0.5, color='green', s=100, marker='*', label='火焰杯')
    trap_x = [pos[0] + 0.5 for pos in TRAP_POS]
    trap_y = [pos[1] + 0.5 for pos in TRAP_POS]
    plt.scatter(trap_x, trap_y, color='red', s=100, marker='x', label='陷阱')
    
    processed_path = []
    terminal_found = False
    
    for i, coord in enumerate(path):
        if coord == 'terminal':
            terminal_found = True
            if i > 0 and success:
                processed_path.append((GOAL_POS[0] + 0.5, GOAL_POS[1] + 0.5))
            elif i > 0:
                prev_x, prev_y = processed_path[-1]
                min_dist = float('inf')
                closest_trap = None
                
                for trap in TRAP_POS:
                    trap_x, trap_y = trap[0] + 0.5, trap[1] + 0.5
                    dist = ((prev_x - trap_x)**2 + (prev_y - trap_y)**2)**0.5
                    if dist < min_dist:
                        min_dist = dist
                        closest_trap = (trap_x, trap_y)
                
                if closest_trap:
                    processed_path.append(closest_trap)
            break
        else:
            x = (coord[0] - UNIT/2) / UNIT + 0.5
            y = (coord[1] - UNIT/2) / UNIT + 0.5
            processed_path.append((x, y))
    
    for i, (x, y) in enumerate(processed_path):
        plt.text(x, y, str(i), 
                fontsize=12, ha='center', va='center',
                bbox=dict(facecolor='white', alpha=0.7))
        
        if i > 0:
            plt.plot([processed_path[i-1][0], x], [processed_path[i-1][1], y], 'b-', alpha=0.5)
    
    plt.title(f'第{episode}回合探索路径: {"成功" if success else "失败"}')
    plt.legend(loc='upper left')
    plt.grid(True)
    
    plt.xlim(0, MAZE_W)
    plt.ylim(MAZE_H, 0)
    plt.xticks(range(MAZE_W))
    plt.yticks(range(MAZE_H))
    
    plt.tight_layout()
    
    os.makedirs('path_visualizations', exist_ok=True)
    plt.savefig(f'path_visualizations/episode_{episode}_path.png')
    plt.close()

def train():
    """
    执行Q-learning算法训练过程
    
    初始化迷宫环境和Q-learning智能体
    设置训练参数(学习率、折扣因子、探索率)
    执行训练循环，包括：
      重置环境获取初始状态
      记录智能体路径和奖励
      智能体选择动作并执行
      环境返回下一状态、奖励和是否终止
      智能体学习更新Q表
      判断是否成功找到火焰杯
      动态调整探索率
    定期生成路径可视化和输出训练状态
    训练结束后绘制奖励和成功率曲线
    返回训练好的智能体
    """
    env = Maze()
    agent = QLearningAgent(
        maze_size=(MAZE_H, MAZE_W),
        alpha=0.1,
        gamma=0.9,
        epsilon=0.1
    )
    
    n_episodes = 100
    max_steps = 100
    rewards_list = []
    success_list = []
    
    for episode in range(n_episodes):
        observation = env.reset()
        total_reward = 0
        path = [observation]
        success = False
        last_reward = 0
        
        for step in range(max_steps):
            action = agent.choose_action(observation)
            
            observation_, reward, done = env.step(action)
            path.append(observation_)
            last_reward = reward
            
            agent.learn(observation, action, reward, observation_)
            
            observation = observation_
            total_reward += reward
            env.render()
            if done:
                success = reward > 0
                success_list.append(1 if success else 0)
                break
                
            if step == max_steps - 1:
                success_list.append(0)
        
        rewards_list.append(total_reward)
        
        if (episode + 1) % 10 == 0:
            visualize_path(episode + 1, path, success)
            print(f"已保存第{episode + 1}回合的路径可视化")
            
        if (episode + 1) % 10 == 0:
            print(f'回合: {episode + 1}/{n_episodes}, 奖励: {total_reward:.1f}, 探索率: {agent.epsilon:.3f}')
            recent_success = np.mean(success_list[-10:]) if len(success_list) >= 10 else np.mean(success_list)
            print(f'最近成功率: {recent_success:.2%}')
            
        agent.epsilon = max(0.01, agent.epsilon * 0.995)
    
    plot_results(rewards_list, success_list)
    
    return agent


def plot_results(rewards, success_rates):
    """
    绘制训练结果
    
    创建奖励和成功率的可视化图表
    使用移动平均平滑曲线使趋势更清晰
    设置图表标题、坐标轴标签
    保存训练结果图像并展示
    """
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    window = min(20, len(rewards))
    rewards_smoothed = [np.mean(rewards[max(0, i-window):i+1]) for i in range(len(rewards))]
    plt.plot(rewards_smoothed)
    plt.title('训练过程中的奖励变化')
    plt.xlabel('回合')
    plt.ylabel('平均奖励')
    
    plt.subplot(1, 2, 2)
    window = min(20, len(success_rates))
    success_smoothed = [np.mean(success_rates[max(0, i-window):i+1]) for i in range(len(success_rates))]
    plt.plot(success_smoothed)
    plt.title('训练过程中的成功率变化')
    plt.xlabel('回合')
    plt.ylabel('成功率')
    
    plt.tight_layout()
    plt.savefig('training_results.png')
    plt.show()


if __name__ == "__main__":
    """
    执行Q-learning训练过程
    打印最终学习到的Q表
    """
    agent = train()
    
    print("\n最终学习到的Q表:")
    print(agent.q_table.round(2))