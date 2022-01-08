# Creating an 8 puzzle
# input an array of numbers 1 - 8,
# matrix 3 x 3
# empty space = None
# [0,0] [0,1] [0,2] | 1 2 3
# [1,0] [1,1] [1,2] | 4 5 6
# [2,0] [2,1] [2,2] | 7 8 9

import math, copy



class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
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
    
    def coordinate(self, value):
        current = self.board
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
    BOARD_1 = [1, 2, 3, 
        4, 8, 5, 
        0, 7, 6]
    BOARD_2 = [8, 2, 6, 
        4, 1, 5, 
        0, 7, 3]
    BOARD_3 = [1, 2, 3, 4, 
        5, 6, 7, 8, 
        9, 10, 0, 15, 
        13, 12, 11, 14]
    visited = []
    def __init__(self):
        self.root = Node(self.BOARD_1)
    def Garbage_Solution(self):
        self.visited.append(self.BOARD_1)
        #print(Puzzle(self.BOARD_1).goalstate())
        for n in Puzzle(self.BOARD_1).successor():
            temp = Node(n)
            if n not in self.visited:
                self.root.child.append(n)
            self._setChild(temp)
        print(self.visited)

    def _setChild(self, current):
        print(current.value)
        if current.value is Puzzle(self.BOARD_1).goalstate():
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
    
    def h_manhattan(self):
        for i in self.BOARD_1:
            print(abs(Puzzle(self.BOARD_1).goalstate().index(i) - self.BOARD_1.index(i)))  
                

t = Solution()
t.h_manhattan()

