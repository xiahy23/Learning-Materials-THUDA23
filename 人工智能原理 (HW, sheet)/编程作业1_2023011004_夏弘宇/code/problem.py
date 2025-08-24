import numpy as np
import random
from copy import deepcopy
from utils import *
import time
import sys


def h_function_null(state, goal_state):
    return 0

def h1_function(state, goal_state):
    s2_pos = [np.where(np.array(state) == 2)[0][0], np.where(np.array(state) == 2)[1][0]]
    g2_pos = [np.where(np.array(goal_state) == 2)[0][0], np.where(np.array(goal_state) == 2)[1][0]]
    s3_pos = [np.where(np.array(state) == 3)[0][0], np.where(np.array(state) == 3)[1][0]]
    g3_pos = [np.where(np.array(goal_state) == 3)[0][0], np.where(np.array(goal_state) == 3)[1][0]]
    s4_pos = [np.where(np.array(state) == 4)[0][0], np.where(np.array(state) == 4)[1][0]]
    g4_pos = [np.where(np.array(goal_state) == 4)[0][0], np.where(np.array(goal_state) == 4)[1][0]]
    s5_pos = [np.where(np.array(state) == 5)[0][0], np.where(np.array(state) == 5)[1][0]]
    g5_pos = [np.where(np.array(goal_state) == 5)[0][0], np.where(np.array(goal_state) == 5)[1][0]]
    s6_pos = [np.where(np.array(state) == 6)[0][0], np.where(np.array(state) == 6)[1][0]]
    g6_pos = [np.where(np.array(goal_state) == 6)[0][0], np.where(np.array(goal_state) == 6)[1][0]]
    return  (s2_pos != g2_pos) + (s3_pos != g3_pos) + (s4_pos != g4_pos) + (s5_pos != g5_pos) + (s6_pos != g6_pos)

def h2_function(state, goal_state):
    s2_pos = [np.where(np.array(state) == 2)[0][0], np.where(np.array(state) == 2)[1][0]]
    g2_pos = [np.where(np.array(goal_state) == 2)[0][0], np.where(np.array(goal_state) == 2)[1][0]]
    s3_pos = [np.where(np.array(state) == 3)[0][0], np.where(np.array(state) == 3)[1][0]]
    g3_pos = [np.where(np.array(goal_state) == 3)[0][0], np.where(np.array(goal_state) == 3)[1][0]]
    s4_pos = [np.where(np.array(state) == 4)[0][0], np.where(np.array(state) == 4)[1][0]]
    g4_pos = [np.where(np.array(goal_state) == 4)[0][0], np.where(np.array(goal_state) == 4)[1][0]]
    s5_pos = [np.where(np.array(state) == 5)[0][0], np.where(np.array(state) == 5)[1][0]]
    g5_pos = [np.where(np.array(goal_state) == 5)[0][0], np.where(np.array(goal_state) == 5)[1][0]]
    s6_pos = [np.where(np.array(state) == 6)[0][0], np.where(np.array(state) == 6)[1][0]]
    g6_pos = [np.where(np.array(goal_state) == 6)[0][0], np.where(np.array(goal_state) == 6)[1][0]]
    return Mannhattan_distance(s2_pos, g2_pos) + Mannhattan_distance(s3_pos, g3_pos) + Mannhattan_distance(s4_pos, g4_pos) + (s5_pos != g5_pos) + Mannhattan_distance(s6_pos, g6_pos)

def h0_function(state, goal_state):
    return 0


def Mannhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class Node(object):  # Represents a node in a search tree
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def child_node(self, problem, action):
        next_state = problem.move(self.state, action)
        next_node = Node(next_state, self, action,
                         problem.g(self.depth, self.state, action, next_state) + 
                         problem.h(next_state, problem.goal_state.state),)
        return next_node

    def path(self):
        """
        Returns list of nodes from this node to the root node
        """
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __repr__(self):
        return f"#########\n#{self.state[0][0]} {self.state[0][1]} {self.state[0][2]} {self.state[0][3]}#\n#{self.state[1][0]} {self.state[1][1]} {self.state[1][2]} {self.state[1][3]}#\n#{self.state[2][0]} {self.state[2][1]} {self.state[2][2]} {self.state[2][3]}#\n#{self.state[3][0]} {self.state[3][1]} {self.state[3][2]} {self.state[3][3]}#\n#########"


    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def __eq__(self, other):
        return self.state == other.state


class Problem(object):
    def __init__(self, init_state=None, goal_state=None, h_function=None):
        self.init_state = Node(init_state)
        self.goal_state = Node(goal_state)
        self.h = h_function

    def actions(self, state):
        """
        Given the current state, return valid actions.
        :param state:
        :return: valid actions
        """
        pass

    def move(self, state, action):
        pass

    def is_goal(self, state):
        pass

    def g(self, cost, from_state, action, to_state):
        return cost + 1

    def solution(self, goal):
        """
        Returns actions from this node to the root node
        """
        if goal.state is None:
            return None
        return [node.action for node in goal.path()[1:]]

    def expand(self, node):  # Returns a list of child nodes
        return [node.child_node(self, action) for action in self.actions(node.state)]
    

class GridsProblem(Problem):
    def __init__(self,
                 n=4,
                 init_state=[[1, 3, 1, 1], 
                             [1, 1, 0, 1], 
                             [1, 2, 1, 1], 
                             [4, 1, 5, 6]],
                 goal_state=[[1, 1, 1, 1], 
                             [2, 1, 1, 1], 
                             [3, 5, 1, 1], 
                             [4, 6, 1, 0]],
                 h_function=h_function_null):
        super().__init__(init_state, goal_state, h_function)
        self.n = n

    def is_valid(self, loc):
        return -1 < loc[0] < self.n and -1 < loc[1] < self.n

    def actions(self, state):#返回所有合法的动作，以空格的去向表示
        empty_row, empty_col = np.where(np.array(state) == 0)[0][0], np.where(np.array(state) == 0)[1][0] #找到空格的位置
        candidates = [[empty_row-1, empty_col], [empty_row+1, empty_col],
                      [empty_row, empty_col-1], [empty_row, empty_col+1],]                                #基本规则：可以上下左右移动
        valid_candidates = [item for item in candidates if self.is_valid(item)]                           #判断是否越界
        
        ab_pos = [np.where(np.array(state) == 5)[0][0], np.where(np.array(state) == 5)[1][0]]             #敖丙技能实现
        if ab_pos not in valid_candidates:
            valid_candidates.append(ab_pos)
        
        nz1_pos = [np.where(np.array(state) == 3)[0][0], np.where(np.array(state) == 3)[1][0]]            #哪吒约束实现
        nz2_pos = [np.where(np.array(state) == 4)[0][0], np.where(np.array(state) == 4)[1][0]]
        if nz1_pos in valid_candidates:
            if Mannhattan_distance([empty_row, empty_col], nz2_pos) > 4:
                valid_candidates.remove(nz1_pos)
        if nz2_pos in valid_candidates:
            if Mannhattan_distance([empty_row, empty_col], nz1_pos) > 4:
                valid_candidates.remove(nz2_pos)
        return valid_candidates

    def move(self, state, action):
        empty_row, empty_col = np.where(np.array(state) == 0)[0][0], np.where(np.array(state) == 0)[1][0]
        new_state = deepcopy(state)
        new_state[empty_row][empty_col] = state[action[0]][action[1]]
        new_state[action[0]][action[1]] = 0
        return new_state

    def is_goal(self, state):
        return state == self.goal_state.state

    def g(self, cost, from_state, action, to_state):
        return cost + 1
    
    
def search_with_info(problem: GridsProblem):
    # A*
    print("有信息搜索")
    start_time = time.time()
    open = PriorityQueue(problem.init_state)
    closed_open = set()
    while not open.empty():
        node = open.pop()
        if problem.is_goal(node.state):
            print("搜索成功")
            print("路径为：")
            cnt = 0
            for nodes in node.path():
                print(nodes)
                cnt += 1
            print(f"方案步数为{cnt}")
            print(f"搜索时间为{time.time() - start_time:.2f}s, 搜索节点数为{len(closed_open)}个")
            return
        for child in problem.expand(node):
            if tuple(map(tuple, child.state)) not in closed_open:
                open.push(child)
                closed_open.add(tuple(map(tuple, child.state)))

def search_without_info(problem: GridsProblem):
    print("无信息搜索")
    #BFS具有完备性和最优性，可以作为无信息搜索的基准
    start_time = time.time()
    open = Queue()
    open.push(problem.init_state)
    closed_open = set()
    while not open.empty():
        node = open.pop()
        if problem.is_goal(node.state):
            print("搜索成功")
            print("路径为：")
            cnt = 0
            for nodes in node.path():
                print(nodes)
                cnt += 1
            print(f"方案步数为{cnt}")
            print(f"搜索时间为{time.time() - start_time:.2f}s, 搜索节点数为{len(closed_open)}个")
            return
        for child in problem.expand(node):
            if tuple(map(tuple, child.state)) not in closed_open:
                open.push(child)
                closed_open.add(tuple(map(tuple, child.state)))


if __name__ == "__main__":
    # 无信息搜索
    with open("search_results.txt", "w") as f:
        # 保存原始stdout
        original_stdout = sys.stdout
        # 重定向stdout到文件
        sys.stdout = f
        problem = GridsProblem(h_function=h_function_null)
        search_without_info(problem)

        # A*搜索算法
        # 以0作为启发式函数，比无信息搜索在复杂度上多一个log
        problem = GridsProblem(h_function=h0_function)
        search_with_info(problem)

        problem = GridsProblem(h_function=h1_function)
        search_with_info(problem)

        problem = GridsProblem(h_function=h2_function)
        search_with_info(problem)
        
        sys.stdout = original_stdout