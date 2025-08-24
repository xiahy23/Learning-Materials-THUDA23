#include <iostream>
#include <vector>
#include <queue>
#include <unordered_set>
#include <algorithm>
#include <chrono>
#include <fstream>
#include <string>
#include <functional>

// 定义状态类型
using State = std::vector<std::vector<int>>;

// 状态哈希函数，用于在集合中比较状态
struct StateHash {
    std::size_t operator()(const State& state) const {
        std::size_t seed = 0;
        for (const auto& row : state) {
            for (int val : row) {
                seed ^= std::hash<int>{}(val) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
            }
        }
        return seed;
    }
};

// 状态相等比较函数
struct StateEqual {
    bool operator()(const State& a, const State& b) const {
        return a == b;
    }
};

// 曼哈顿距离计算
int manhattanDistance(const std::vector<int>& pos1, const std::vector<int>& pos2) {
    return std::abs(pos1[0] - pos2[0]) + std::abs(pos1[1] - pos2[1]);
}

// 获取特定数字在状态中的位置
std::vector<int> getPosition(const State& state, int number) {
    for (int i = 0; i < state.size(); ++i) {
        for (int j = 0; j < state[i].size(); ++j) {
            if (state[i][j] == number) {
                return {i, j};
            }
        }
    }
    return {-1, -1}; // 不应该到达这里
}

// 启发函数
int h_function_null(const State& state, const State& goal_state) {
    return 0;
}

int h0_function(const State& state, const State& goal_state) {
    return 0;
}

int h1_function(const State& state, const State& goal_state) {
    int misplaced = 0;
    for (int num = 2; num <= 6; ++num) {
        auto state_pos = getPosition(state, num);
        auto goal_pos = getPosition(goal_state, num);
        misplaced += (state_pos != goal_pos);
    }
    return misplaced;
}

int h2_function(const State& state, const State& goal_state) {
    int distance = 0;
    
    // 对数字2, 3, 4, 6使用曼哈顿距离
    for (int num : {2, 3, 4, 6}) {
        auto state_pos = getPosition(state, num);
        auto goal_pos = getPosition(goal_state, num);
        distance += manhattanDistance(state_pos, goal_pos);
    }
    
    // 对数字5只使用是否错位判断
    auto s5_pos = getPosition(state, 5);
    auto g5_pos = getPosition(goal_state, 5);
    distance += (s5_pos != g5_pos);
    
    return distance;
}

// 节点类
class Node {
public:
    State state;
    Node* parent;
    std::vector<int> action;
    double path_cost;
    int depth;

    Node(const State& s, Node* p = nullptr, 
         const std::vector<int>& a = {}, double cost = 0.0)
        : state(s), parent(p), action(a), path_cost(cost), depth(0) {
        if (parent) {
            depth = parent->depth + 1;
        }
    }

    // 获取路径
    std::vector<Node*> path() const {
        std::vector<Node*> path_back;
        const Node* current = this;
        while (current) {
            path_back.push_back(const_cast<Node*>(current));
            current = current->parent;
        }
        std::reverse(path_back.begin(), path_back.end());
        return path_back;
    }

    // 打印状态
    std::string toString() const {
        std::string result = "#########\n";
        for (const auto& row : state) {
            result += "#";
            for (int val : row) {
                result += " " + std::to_string(val);
            }
            result += " #\n";
        }
        result += "#########";
        return result;
    }

    bool operator<(const Node& other) const {
        return path_cost > other.path_cost; // 优先队列是大顶堆，所以反过来
    }
};

// 问题基类
class Problem {
public:
    State init_state;
    State goal_state;
    std::function<int(const State&, const State&)> h;

    Problem(const State& init, const State& goal, 
            std::function<int(const State&, const State&)> h_func = h_function_null)
        : init_state(init), goal_state(goal), h(h_func) {}
    
    virtual ~Problem() {}

    virtual std::vector<std::vector<int>> actions(const State& state) = 0;
    virtual State move(const State& state, const std::vector<int>& action) = 0;
    virtual bool is_goal(const State& state) = 0;
    
    virtual double g(int cost, const State&, const std::vector<int>&, const State&) {
        return cost + 1;
    }

    // 生成子节点
    std::vector<Node*> expand(Node* node) {
        std::vector<Node*> children;
        auto valid_actions = actions(node->state);
        
        for (const auto& action : valid_actions) {
            State new_state = move(node->state, action);
            double new_cost = node->path_cost - h(node->state, goal_state) + 
                              g(node->depth, node->state, action, new_state) + 
                              h(new_state, goal_state);
            
            Node* child = new Node(new_state, node, action, new_cost);
            children.push_back(child);
        }
        
        return children;
    }
};

// 网格问题类
class GridsProblem : public Problem {
public:
    int n;

    GridsProblem(int grid_size = 4,
                const State& init = {{1, 3, 1, 1}, {1, 1, 0, 1}, {1, 2, 1, 1}, {4, 1, 5, 6}},
                const State& goal = {{1, 1, 1, 1}, {2, 1, 1, 1}, {3, 5, 1, 1}, {4, 6, 1, 0}},
                std::function<int(const State&, const State&)> h_func = h_function_null)
        : Problem(init, goal, h_func), n(grid_size) {}

    bool is_valid(const std::vector<int>& loc) const {
        return loc[0] >= 0 && loc[0] < n && loc[1] >= 0 && loc[1] < n;
    }

    std::vector<std::vector<int>> actions(const State& state) override {
        // 找到空格位置
        auto empty_pos = getPosition(state, 0);
        int empty_row = empty_pos[0];
        int empty_col = empty_pos[1];

        // 可能的移动方向
        std::vector<std::vector<int>> candidates = {
            {empty_row - 1, empty_col}, {empty_row + 1, empty_col},
            {empty_row, empty_col - 1}, {empty_row, empty_col + 1}
        };

        // 过滤有效移动
        std::vector<std::vector<int>> valid_candidates;
        for (const auto& pos : candidates) {
            if (is_valid(pos)) {
                valid_candidates.push_back(pos);
            }
        }

        // 特殊规则1: 数字5总是可以移动
        auto ab_pos = getPosition(state, 5);
        bool ab_in_candidates = false;
        for (const auto& pos : valid_candidates) {
            if (pos == ab_pos) {
                ab_in_candidates = true;
                break;
            }
        }
        if (!ab_in_candidates) {
            valid_candidates.push_back(ab_pos);
        }

        // 特殊规则2: 数字3和4距离限制
        auto nz1_pos = getPosition(state, 3);
        auto nz2_pos = getPosition(state, 4);
        
        for (auto it = valid_candidates.begin(); it != valid_candidates.end();) {
            if (*it == nz1_pos && manhattanDistance(empty_pos, nz2_pos) > 4) {
                it = valid_candidates.erase(it);
            } else if (*it == nz2_pos && manhattanDistance(empty_pos, nz1_pos) > 4) {
                it = valid_candidates.erase(it);
            } else {
                ++it;
            }
        }

        return valid_candidates;
    }

    State move(const State& state, const std::vector<int>& action) override {
        auto empty_pos = getPosition(state, 0);
        
        // 创建新状态
        State new_state = state;
        new_state[empty_pos[0]][empty_pos[1]] = state[action[0]][action[1]];
        new_state[action[0]][action[1]] = 0;
        
        return new_state;
    }

    bool is_goal(const State& state) override {
        return state == goal_state;
    }
};

// 有信息搜索 (A*)

// 有信息搜索 (A*)
void search_with_info(GridsProblem& problem) {
    std::cout << "有信息搜索" << std::endl;
    auto start_time = std::chrono::high_resolution_clock::now();
    
    std::priority_queue<Node> open;
    open.push(Node(problem.init_state, nullptr, {}, problem.h(problem.init_state, problem.goal_state)));
    
    std::unordered_set<State, StateHash, StateEqual> closed_open;
    closed_open.insert(problem.init_state);
    
    int nodes_explored = 0;
    
    while (!open.empty()) {
        Node node = open.top();
        open.pop();
        
        if (problem.is_goal(node.state)) {
            std::cout << "搜索成功" << std::endl;
            std::cout << "路径为：" << std::endl;
            
            auto path = node.path();
            int steps = 0;
            
            for (auto* n : path) {
                std::cout << n->toString() << std::endl;
                steps++;
                
                // 内存管理：如果不是当前节点，释放内存
                if (n != &node && n != path[0]) {
                    delete n;
                }
            }
            
            std::cout << "方案步数为" << steps << std::endl;
            auto end_time = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count() / 1000.0;
            std::cout << "搜索时间为" << duration << "s, 搜索节点数为" << nodes_explored << "个" << std::endl;
            return;
        }
        
        std::vector<Node*> children = problem.expand(&node);
        for (auto* child : children) {
            if (closed_open.find(child->state) == closed_open.end()) {
                open.push(*child);
                closed_open.insert(child->state);
                nodes_explored++;
            } else {
                delete child;  // 释放不需要的节点
            }
        }
    }
    
    std::cout << "搜索失败" << std::endl;
}

// 无信息搜索 (BFS)
void search_without_info(GridsProblem& problem) {
    std::cout << "无信息搜索" << std::endl;
    auto start_time = std::chrono::high_resolution_clock::now();
    
    std::deque<Node> open;
    open.push_back(Node(problem.init_state));
    
    std::unordered_set<State, StateHash, StateEqual> closed_open;
    closed_open.insert(problem.init_state);
    
    int nodes_explored = 0;
    
    while (!open.empty()) {
        Node node = open.front();
        open.pop_front();
        
        if (problem.is_goal(node.state)) {
            std::cout << "搜索成功" << std::endl;
            std::cout << "路径为：" << std::endl;
            
            auto path = node.path();
            int steps = 0;
            
            for (auto* n : path) {
                std::cout << n->toString() << std::endl;
                steps++;
                
                // 内存管理
                if (n != &node && n != path[0]) {
                    delete n;
                }
            }
            
            std::cout << "方案步数为" << steps << std::endl;
            auto end_time = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count() / 1000.0;
            std::cout << "搜索时间为" << duration << "s, 搜索节点数为" << nodes_explored << "个" << std::endl;
            return;
        }
        
        std::vector<Node*> children = problem.expand(&node);
        for (auto* child : children) {
            if (closed_open.find(child->state) == closed_open.end()) {
                open.push_back(*child);
                closed_open.insert(child->state);
                nodes_explored++;
            } else {
                delete child;  // 释放不需要的节点
            }
        }
    }
    
    std::cout << "搜索失败" << std::endl;
}

int main() {
    // 创建输出文件
    std::ofstream output_file("search_results.txt");
    
    // 保存原始输出流
    auto original_cout_buf = std::cout.rdbuf();
    
    // 重定向输出到文件
    std::cout.rdbuf(output_file.rdbuf());
    
    // 无信息搜索
    GridsProblem problem_bfs(4);
    search_without_info(problem_bfs);
    
    // A*搜索算法，使用不同的启发函数
    GridsProblem problem_h0(4, 
                          {{1, 3, 1, 1}, {1, 1, 0, 1}, {1, 2, 1, 1}, {4, 1, 5, 6}},
                          {{1, 1, 1, 1}, {2, 1, 1, 1}, {3, 5, 1, 1}, {4, 6, 1, 0}},
                          h0_function);
    search_with_info(problem_h0);
    
    GridsProblem problem_h1(4, 
                          {{1, 3, 1, 1}, {1, 1, 0, 1}, {1, 2, 1, 1}, {4, 1, 5, 6}},
                          {{1, 1, 1, 1}, {2, 1, 1, 1}, {3, 5, 1, 1}, {4, 6, 1, 0}},
                          h1_function);
    search_with_info(problem_h1);
    
    GridsProblem problem_h2(4, 
                          {{1, 3, 1, 1}, {1, 1, 0, 1}, {1, 2, 1, 1}, {4, 1, 5, 6}},
                          {{1, 1, 1, 1}, {2, 1, 1, 1}, {3, 5, 1, 1}, {4, 6, 1, 0}},
                          h2_function);
    search_with_info(problem_h2);
    
    // 恢复原始输出
    std::cout.rdbuf(original_cout_buf);
    output_file.close();
    
    std::cout << "搜索结果已保存到 search_results.txt" << std::endl;
    
    return 0;
}