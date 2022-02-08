# Creating an 8 puzzle
# input an array of numbers 1 - 8,
# matrix 3 x 3
# empty space = None
# [0,0] [0,1] [0,2] | 1 2 3
# [1,0] [1,1] [1,2] | 4 5 6
# [2,0] [2,1] [2,2] | 7 8 9

import math, copy
from pickle import TRUE



class Node:
    def __init__(self, value):
        self.value = value
        self.hval= None
        self.child = []

class Puzzle:
    queue = []
    
    def __init__(self, board):
        self._hval = 0
        self._depth = 0
        self.board = board

    def successor(self):
        current = self.board
        subNode = []
        if self.move_up(current) is not None:
            subNode.append(self.move_up(current))
        if self.move_down(current) is not None:
            subNode.append(self.move_down(current))
        if self.move_right(current) is not None:
            subNode.append(self.move_right(current))
        if self.move_left(current) is not None:
            subNode.append(self.move_left(current))
        return subNode

    def goalstate(self):
        self.goal = self.board.copy()
        self.goal.sort()
        return self.goal
    
    def coordinate(self, value, current):
        # arr[x,y]
        # [0, 0] = index is 0
        # [0, 1] = index is 1
        # [1, 0] = index is 3
        # [2, 2] = index is 8
        # index = size_of_board * x + y
        value_index = current.index(value)
        x = math.floor(value_index/self.size_of_board())
        y = math.floor(value_index - x * self.size_of_board())
        coor = [x, y]
        return coor
        
    def coor_to_index(self, arr):
        if len(arr) > 2:
            return
        if (arr[0] > (self.size_of_board()-1) or arr[1] > (self.size_of_board()-1)):
            return
        return int(self.size_of_board() * arr[0] + arr[1])

    def size_of_board(self):
        return math.sqrt(len(self.board))

    def h_manhattan(self): 
        #find a legal move that makes it closer to the goal state
        #get the hval of the item that was also being moved
        #For example:
        # [0,0] [0,1] [0,2] | 1 2 3
        # [1,0] [1,1] [1,2] | 4 5 6
        # [2,0] [2,1] [2,2] | 7 0 8
        # move right:
        # [0,0] [0,1] [0,2] | 1 2 3
        # [1,0] [1,1] [1,2] | 4 5 6
        # [2,0] [2,1] [2,2] | 0 7 8
        # calculate the manhattan value for 7, the lower the value, the closer we are to the solution
        # To find the value for a given tile, since we have it in a list ([1, 2, 3, 4, 5, 6, 7, 0, 8]) we find the distance from
        # the current board and the goal state, (y-axis) + (x-axis)
        # [0,0] [0,1] [0,2] | 1 2 3
        # [1,0] [1,1] [1,2] | 4 5 6
        # [2,0] [2,1] [2,2] | 0 7 8
        # hval is |goal_y - curr_y| + |goal_x - curr_y| 
        h_val = 0
        current = self.board
        goal = self.goalstate()
        for i in current:
        #    print("curr", i, self.coordinate(i, current))
        #    print("goal", i, self.coordinate(i, goal))
            h_val += abs(self.coordinate(i,goal)[0] - self.coordinate(i,current)[0]) + abs(self.coordinate(i,goal)[1] - abs(self.coordinate(i,current)[1]))
        #print(h_val)
        return h_val

    #actions

    def swapping_indexes(self, value, null_space, current):
        #print(current)
        #print(value)
        x = current.copy()
        temp = x[value]
        x[value] = x[null_space]
        x[null_space] = temp
        return x

    # moving the tile down to the empty space
    def move_up(self,current):
        if current is not None:
            coor = self.coordinate(0,current)
            if(coor[0] > 0):
                # print("up")
                above = [coor[0] - 1, coor[1]]
                return self.swapping_indexes(self.coor_to_index(above), current.index(0), current)
            else:
                return
        return
    # moving the tile up to the empty space
    def move_down(self,current):
        if current is not None:
            coor = self.coordinate(0,current)
            if(coor[0] < self.size_of_board()-1):
                # print("down")
                below = [coor[0] + 1, coor[1]]
                return self.swapping_indexes(self.coor_to_index(below), current.index(0), current)
            else:
                return
        return
    # moving the tile left to the empty space
    def move_right(self,current):
        if current is not None:
            coor = self.coordinate(0,current)
            if(coor[1] < self.size_of_board()-1):
                # print("right")
                right = [coor[0], coor[1] + 1]
                return self.swapping_indexes(self.coor_to_index(right), current.index(0),current)        
            else:
                return
        return
    # moving the tile right to the empty space
    def move_left(self,current):
        if current is not None:
            coor = self.coordinate(0,current)
            if(coor[1] > 0):
                # print("left")
                left = [coor[0], coor[1] - 1]
                return self.swapping_indexes(self.coor_to_index(left), current.index(0),current)
            else:
                return
        return

class Solution:
    #creating boards
    BOARD_0 =[0, 1, 2, 3, 4, 5, 6, 7, 8]
    BOARD_1 = [1, 0, 2, 
        3, 4, 5, 
        6, 7, 8]
    BOARD_2 = [8, 2, 6, 
        4, 1, 5, 
        0, 7, 3]
    BOARD_3 = [1, 2, 3, 4, 
        5, 6, 7, 8, 
        9, 10, 0, 15, 
        13, 12, 11, 14]
    visited = []
    queue = []
    def __init__(self):
        self.root = Node(self.BOARD_2)

    def Garbage_Solution(self):
        # Brute force approach (DFS). Create a child node everytime there is a possible node. Continue until the
        # the state is repeated or found the solution.
        self.visited.append(self.root)
        #print(Puzzle(self.BOARD_1).goalstate())
        for n in Puzzle(self.root).successor():
            temp = Node(n)
            if n not in self.visited:
                self.root.child.append(n)
            self._setChild(temp)
        print(self.visited)

    def _setChild(self, current):
        print(current.value)
        if current.value == Puzzle(self.root.value).goalstate():
            return
        if current.value in self.visited:
            return
        self.visited.append(current.value)
        for i in Puzzle(current.value).successor():  
            temp = Node(i)   
            if current.value not in self.visited:
                self.visited.append(i)
                current.child.append(i)
            self._setChild(temp)
        #print(current.child)
    
    def BFS(self):
        # Breadth First search solution
        queue = []
        current = self.root.value
        queue.append(current)
        while queue:
            for i in Puzzle(queue.pop(0)).successor():
                print(i)
                if i == Puzzle(i).goalstate():
                    return
                if i not in self.visited:
                    self.visited.append(i)
                    queue.append(i)
                    #print(i is Puzzle(i).goalstate())
                    #print(self.visited)

    def h_manhattan(self):
        # find all the successor of the of the current
        # choose the tree to go down
        # Use the priority queue to remove the go down the smallest manhattan value
        current = self.root
        current.hval = Puzzle(current.value).h_manhattan()
        print(current.hval)
        self.visited.append(current.value)
        self.queue.append(current)
        while self.queue:
            for i in Puzzle(self.delete()).successor():
                print(i)
                temp = Node(i)
                temp.hval = Puzzle(i).h_manhattan()
                if i == Puzzle(i).goalstate():
                    return
                if i not in self.visited:
                    self.visited.append(i)
                    self.queue.append(temp)

    # delete function
    # input: None
    # Output: the Deleted queue
    # Piority Queue, delete the smallest mannhattan at the given current state
    # Find the smallest manhattan value and remove it from the queue.
    def delete(self):
        min = 0
        for i in range(len(self.queue)):
            if self.queue[i].hval < self.queue[min].hval:
                min = i
        item = self.queue[min].value
        del self.queue[min]
        return item
t = Solution()
t.h_manhattan()

