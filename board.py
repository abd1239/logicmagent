# ///////////////////////////2

from collections import deque
from stone import Stone, StoneType 

class Board:
    def __init__(self, rows=1, cols=1, allowed_moves=2):
        self.rows = rows
        self.cols = cols
        self.allowed_moves = allowed_moves
        self.moves = 0
        self.cost = 0
        self.board = [
            [Stone(StoneType.EMPTY, True, (i - 1, j - 1)) for j in range(cols)]
            for i in range(rows)
        ]
        self.movables = deque()
        self.goals = deque()
        self.stones = deque()
        self.dirty = False
        self.father = None

    def init_movables(self):
        self.movables.clear()
        for row in range(self.rows):
            for col in range(self.cols):
                current = self.board[row][col]
                if current.type in {
                    StoneType.REPELANDGOAL,
                    StoneType.REPEL,
                    StoneType.ATTRACTANDGOAL,
                    StoneType.ATTRACT,
                }:
                    self.movables.append(current)

    def init_goals(self):
        self.goals.clear()
        for row in range(self.rows):
            for col in range(self.cols):
                current = self.board[row][col]
                if current.type in {
                    StoneType.REPELANDGOAL,
                    StoneType.STONEANDGOAL,
                    StoneType.ATTRACTANDGOAL,
                    StoneType.GOAL,
                }:
                    self.goals.append(current)

    def init_stones(self):
        self.goals.clear()
        self.movables.clear()
        self.stones.clear()
        for row in range(self.rows):
            for col in range(self.cols):
                current = self.board[row][col]

                if current.type in {StoneType.STONE, StoneType.STONEANDGOAL}:
                    self.stones.append(current)

                if current.type in {
                    StoneType.REPELANDGOAL,
                    StoneType.STONEANDGOAL,
                    StoneType.ATTRACTANDGOAL,
                    StoneType.GOAL,
                }:
                    self.goals.append(current)

                if current.type in {
                    StoneType.REPELANDGOAL,
                    StoneType.REPEL,
                    StoneType.ATTRACTANDGOAL,
                    StoneType.ATTRACT,
                }:
                    self.movables.append(current)

    def destroy(self):
        self.board = None

    def print_board(self):
        for i in range(self.rows):
            print("+---" * self.cols + "+")
            for j in range(self.cols):
                print(f"|{self.board[i][j].name}", end="")
            print("|")
        print("+---" * self.cols + "+")
        print("----------------------!!!!!---------------------- \n")

    def check_valid_move(self, row, col):
        if row >= self.board.rows - 1 or col >= self.board.cols - 1:
            return False
        target_type = self.board.board[row][col].type
        if target_type in {
            StoneType.STONE,
            StoneType.OBSTACLE,
            StoneType.STONEANDGOAL,
            StoneType.REPELANDGOAL,
            StoneType.ATTRACTANDGOAL,
        }:
            return False
        return True

    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                current_cell_type = self.board[row][col].type
                if current_cell_type in {
                    StoneType.REPEL,
                    StoneType.STONE,
                    StoneType.ATTRACT,
                    StoneType.GOAL,
                }:
                    return False
        return True
