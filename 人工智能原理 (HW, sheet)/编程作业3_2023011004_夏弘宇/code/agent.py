import numpy as np
import random

class QLearningAgent:
    def __init__(self, maze_size, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.maze_width = maze_size[1]
        self.maze_height = maze_size[0]
        self.n_states = maze_size[0] * maze_size[1]
        self.n_actions = 4  # 上、下、左、右四个动作
        self.q_table = np.zeros((self.n_states, self.n_actions))
        self.alpha = alpha  # 学习率
        self.gamma = gamma  # 折扣因子
        self.epsilon = epsilon  # 探索率
        
    def _coords_to_state(self, coords):
        """将坐标转换为状态索引"""
        if coords == 'terminal':
            return -1
            
        x = int((coords[0] - 50) / 100)
        y = int((coords[1] - 50) / 100)
        return y * self.maze_width + x
        
    def choose_action(self, coords):
        """使用epsilon-greedy策略选择动作"""
        # 如果是终端状态，因为没法再执行了，所以随便返回一个0就行
        if coords == 'terminal':
            return 0
            
        state = self._coords_to_state(coords)
        
        # 探索：以epsilon的概率随机选择动作
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        
        # 利用：选择当前状态下Q值最大的动作
        # 处理可能的并列情况
        max_actions = np.where(self.q_table[state] == np.max(self.q_table[state]))[0]
        return np.random.choice(max_actions)
        
    def learn(self, s, a, r, s_):
        """Q-learning更新规则"""
        # 如果起始状态就是终端，不进行学习
        if s == 'terminal':
            return
            
        state = self._coords_to_state(s)
        
        # 如果下一状态是终端状态，没有未来奖励
        if s_ == 'terminal':
            q_target = r
        else:
            next_state = self._coords_to_state(s_)
            q_target = r + self.gamma * np.max(self.q_table[next_state])
            
        # 更新Q值
        self.q_table[state, a] += self.alpha * (q_target - self.q_table[state, a])