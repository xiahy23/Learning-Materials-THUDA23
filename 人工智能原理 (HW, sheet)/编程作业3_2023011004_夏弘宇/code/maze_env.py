import numpy as np
import pandas as pd
import time
import sys
import tkinter as tk
from tkinter import PhotoImage


UNIT = 100   # 迷宫中每个格子的像素大小
MAZE_H = 5  # 迷宫的高度（格子数）
MAZE_W = 5  # 迷宫的宽度（格子数）
INIT_POS = [0, 0]  # 哈利波特的起始位置
GOAL_POS = [2, 2]  # 火焰杯的位置
TRAP_POS = [[1, 2], [2, 1], [1, 3]]  # 陷阱的位置


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']  # 决策空间
        self.n_actions = len(self.action_space)
        self.title('Q-learning')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        """
        迷宫初始化
        """
        self.canvas = tk.Canvas(self, bg='white',
                                height=MAZE_H * UNIT,
                                width=MAZE_W * UNIT)

        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1, fill="black")
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1, fill="black")

        origin = np.array([UNIT/2, UNIT/2])

        self.bm_trap = PhotoImage(file="trap.png")
        self.trap_list = []
        for i in range(len(TRAP_POS)):
            self.trap_list.append(self.canvas.create_image(
                origin[0]+UNIT * TRAP_POS[i][0], origin[1]+UNIT * TRAP_POS[i][1], image=self.bm_trap))

        self.bm_potter = PhotoImage(file="potter.png")
        self.potter = self.canvas.create_image(
            origin[0]+INIT_POS[0]*UNIT, origin[1]+INIT_POS[1]*UNIT, image=self.bm_potter)

        self.bm_goal = PhotoImage(file="cup.png")
        self.goal = self.canvas.create_image(
            origin[0]+GOAL_POS[0]*UNIT, origin[1]+GOAL_POS[1]*UNIT, image=self.bm_goal)

        self.canvas.pack()

    def reset(self):
        self.update()  # tk.Tk().update 强制画面更新
        time.sleep(0.5)
        self.canvas.delete(self.potter)
        origin = np.array([UNIT/2, UNIT/2])

        self.potter = self.canvas.create_image(
            origin[0], origin[1], image=self.bm_potter)
        self.update()
        # 返回当前potter所在的位置
        return self.canvas.coords(self.potter)

    def step(self, action):
        s = self.canvas.coords(self.potter)
        base_action = np.array([0, 0])
        if action == 0:   # 向上移动
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # 向下移动
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # 向右移动
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # 向左移动
            if s[0] > UNIT:
                base_action[0] -= UNIT

        
        hit_wall = base_action[0] == 0 and base_action[1] == 0
        self.canvas.move(
            self.potter, base_action[0], base_action[1])
        s_ = self.canvas.coords(self.potter)

        # 回报函数
        if s_ == self.canvas.coords(self.goal):
            reward = 100
            done = True
            s_ = 'terminal'
        elif s_ in [self.canvas.coords(a_trap) for a_trap in self.trap_list]:
            reward = -10
            done = True
            s_ = 'terminal'
        elif hit_wall:
            reward = -5
            done = False
        else:
            reward = -2
            done = False
        return s_, reward, done

    def render(self):
        time.sleep(0.05)
        self.update()



def update():
    # 更新图形化界面
    for t in range(30):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break


if __name__ == '__main__':
    env = Maze()
    env.after(100, update)
    env.mainloop()
