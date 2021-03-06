import os
import sys
from itertools import chain
from collections import deque
import heapq

# A* Search using Misplaced Tiles heuristics

class Node:
    def __init__(self, state, empty_pos = None, depth = 0, node_str = None):
        self.state = state
        self.depth = depth
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

        if empty_pos is not None:
            self.node_str = node_str
            self.empty_pos = empty_pos
        else:
            self.node_str = str(state)
            self.empty_pos = self.find_empty_pos(self.state)
 
    def find_empty_pos(self, state):
        for x in range(n):
            for y in range(n):
                if state[x][y] == 0:
                    return (x, y)

    def est_cost(self, state):
        return self.misplaced_tiles(state) + self.depth + 1

    def misplaced_tiles(self, state):
        misplaced = 0

        for x in range(n):
            for y in range(n):
                correct_tile = x * n + y + 1
                current_tile = state[x][y]

                if current_tile != 0 and current_tile != correct_tile:
                    misplaced += 1

        return misplaced

    def do_move(self, move):
        if move == "UP":
            return self.up()
        if move == "DOWN":
            return self.down()
        if move == "LEFT":
            return self.left()
        if move == "RIGHT":
            return self.right()

    def down(self):
        empty = self.empty_pos
        x = empty[0]
        y = empty[1]

        if (x != 0):
            t = [row[:] for row in self.state]
            t[x][y], t[x - 1][y] = t[x - 1][y], t[x][y]
            return t, (x - 1, y)
        else:
            return self.state, empty

    def up(self):
        empty = self.empty_pos
        x = empty[0]
        y = empty[1]

        if (x != n - 1):
            t = [row[:] for row in self.state]
            t[x][y], t[x + 1][y] = t[x + 1][y], t[x][y]
            return t, (x + 1, y)
        else:
            return self.state, empty

    def right(self):
        empty = self.empty_pos
        x = empty[0]
        y = empty[1]

        if (y != 0):
            t = [row[:] for row in self.state]
            t[x][y], t[x][y - 1] = t[x][y - 1], t[x][y]
            return t, (x, y - 1)
        else:
            return self.state, empty

    def left(self):
        empty = self.empty_pos
        x = empty[0]
        y = empty[1]

        if (y != n - 1):
            t = [row[:] for row in self.state]
            t[x][y], t[x][y + 1] = t[x][y + 1], t[x][y]
            return t, (x, y + 1)
        else:
            return self.state, empty

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        global n 
        global max_num
        n = len(init_state[0])
        max_num = n ** 2 - 1
        self.init_state = init_state
        self.state = init_state
        self.goal_state = goal_state
        self.visited = set()
        self.frontier_node = []
        self.frontier_dict = {}
        self.move_dict = {}
        self.total_nodes = 1
        self.total_visited = 0
        self.max_frontier = 0
        self.depth = 0
 
    def is_goal_state(self, node):
        return node.state == self.goal_state

    def is_solvable(self):
        flat_list = list(chain.from_iterable(self.init_state))
        num_inversions = 0

        for i in range(max_num):
            current = flat_list[i]

            for j in range(i + 1, max_num + 1):
                next = flat_list[j]

                if current > next and next != 0:
                    num_inversions += 1

        if n % 2 != 0 and num_inversions % 2 == 0:
            return True
        elif n % 2 == 0:
            row_with_blank = n - flat_list.index(0) // n

            return (row_with_blank % 2 == 0) == (num_inversions % 2 != 0)
        else:
            return False

    def succ(self, node, frontier):
        node_str = node.node_str
        self.visited.add(node_str)
        self.total_visited += 1
        frontier -= 1

        for m in node.actions:
            transition, t_empty = node.do_move(m)

            if t_empty != node.empty_pos:
                self.total_nodes += 1
                transition_depth = node.depth + 1
                transition_str = str(transition)
                transition_cost = node.est_cost(transition)

                if (transition_str not in self.frontier_dict or transition_cost < self.frontier_dict[transition_str]) and transition_str not in self.visited:
                    heapq.heappush(self.frontier_node, (transition_cost, Node(transition, t_empty, transition_depth, transition_str)))
                    self.frontier_dict[transition_str] = transition_cost
                    self.move_dict[transition_str] = (node_str, m)
                    frontier += 1

        return frontier

    def a_star(self, node, frontier):
        while True:
            if self.is_goal_state(node):
                return node

            frontier = self.succ(node, frontier)
            self.max_frontier = max(self.max_frontier, frontier)
            cost, node = heapq.heappop(self.frontier_node)

            if node.node_str in self.frontier_dict:
                self.frontier_dict.pop(node.node_str)

    def solve(self):
        if not self.is_solvable():
            return ["UNSOLVABLE"]

        init_node = Node(self.init_state)
        goal_node = self.a_star(init_node, 1)
       
        print "Total number of nodes generated: " + str(self.total_nodes)
        print "Total number of nodes explored: " + str(self.total_visited)
        print "Maximum number of nodes in frontier: " + str(self.max_frontier)
        print "Solution depth: " + str(goal_node.depth)
        
        solution = deque()
        init_str = init_node.node_str
        current_str = goal_node.node_str

        while current_str != init_str:
            current_str, move = self.move_dict[current_str]
            solution.appendleft(move)

        return solution

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







