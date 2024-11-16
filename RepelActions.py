# ///////////

from collections import deque
from message import Message
from stone import Stone, StoneType


class Board:
    def __init__(self, rows=1, cols=1, allowed_moves=2):
        self.rows = rows
        self.cols = cols
        self.allowed_moves = allowed_moves
        self.moves = 0
        self.cost = 0
        self.movables = []
        self.board = [
            [Stone(StoneType.EMPTY, True, (i - 1, j - 1)) for j in range(self.cols)]
            for i in range(self.rows)
        ]

    def __lt__(self, other):
        return self.cost < other.cost  # مقارنة التكلفة

    def init_movables(self):
        print(f"Updating movables for board: {self.board}")
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
                    print(f"Added movable: {current.name}")

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

    def print_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print("+---", end="")
            print("+")
            for j in range(self.cols):
                print(f"|{self.board[i][j].name}", end="")
            print("|")
        for j in range(self.cols):
            print("+---", end="")
        print("+")
        print("----------------------!!!!!----------------------")

        print(type(self.rows))  # يجب أن تكون <class 'int'>
        print(self.rows)  # يجب أن تكون قيمة صحيحة

    def check_valid_move(self, row, col):
        if row > self.rows - 1 or col > self.cols - 1:
            return False
        target_type = self.board[row][col].type
        if target_type in {
            StoneType.STONE,
            StoneType.OBSTACLE,
            StoneType.STONEANDGOAL,
            StoneType.REPELANDGOAL,
            StoneType.ATTRACTANDGOAL,
        }:
            print("valid")
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
        print("All goals are achieved!")
        return True

    def move_repel(self, stone):
        while True:
            Message.message("Enter the desired cell row target:")
            target_row = int(input())
            Message.message("Enter the desired cell column target:")
            target_col = int(input())

            # التحقق من صلاحية الحركة إلى الهدف
            if self.check_valid_move(target_row, target_col):
                # الحصول على الخلايا الحالية والهدف
                current_cell = self.board[stone.position[0]][stone.position[1]]
                target_cell = self.board[target_row][target_col]

                # تنفيذ حركة التنافر بناءً على نوع الخلية الهدف
                if (
                    target_cell.type == StoneType.EMPTY
                    and current_cell.type == StoneType.REPEL
                ):
                    current_cell.empty(stone.position)
                    target_cell.repel((target_row, target_col))
                elif (
                    target_cell.type == StoneType.EMPTY
                    and current_cell.type == StoneType.REPELANDGOAL
                ):
                    current_cell.empty(stone.position)
                    target_cell.repel_and_goal((target_row, target_col))
                elif (
                    target_cell.type == StoneType.GOAL
                    and current_cell.type == StoneType.REPEL
                ):
                    current_cell.empty(stone.position)
                    target_cell.repel_and_goal((target_row, target_col))
                elif (
                    current_cell.type == StoneType.REPELANDGOAL
                    and target_cell.type == StoneType.GOAL
                ):
                    current_cell.goal(stone.position)
                    target_cell.repel_and_goal((target_row, target_col))
                else:
                    self.allowed_moves += 1
                    Message.message("Invalid Move")
                    continue

                # التعامل مع الانعكاسات بعد حركة التنافر
                self.handle_repel_reflection(target_row, target_col)
                self.print_board()  # طباعة اللوحة بعد الحركة

                return target_cell
            else:
                Message.message("Invalid target cell. Please try again.")

    def handle_repel_reflection(self, current_row, current_col):
        self.handle_repel_reflection_right(current_row, current_col)
        self.handle_repel_reflection_left(current_row, current_col)
        self.handle_repel_reflection_down(current_row, current_col)
        self.handle_repel_reflection_up(current_row, current_col)

    def handle_repel_reflection_right(self, row, column):
        right_side = deque()
        for col in range(column, self.cols):
            if col + 1 >= self.cols:
                break
            next_stone = self.board[row][col + 1]
            if next_stone.type in {
                StoneType.STONE,
                StoneType.STONEANDGOAL,
                StoneType.REPEL,
                StoneType.REPELANDGOAL,
                StoneType.ATTRACT,
                StoneType.ATTRACTANDGOAL,
            }:
                right_side.append(next_stone)
            else:
                break
        while right_side and right_side[-1].type != StoneType.OBSTACLE:
            stone = right_side.pop()
            old_row, old_col = stone.position
            new_row = old_row
            new_col = old_col + 1
            if new_col >= self.cols:
                break
            self.movement_replacing(old_row, old_col, new_row, new_col)

    def handle_repel_reflection_left(self, row, column):
        left_side = deque()
        for col in range(column, -1, -1):
            if col - 1 < 0:
                break
            next_stone = self.board[row][col - 1]
            if next_stone.type in {
                StoneType.STONE,
                StoneType.STONEANDGOAL,
                StoneType.REPEL,
                StoneType.REPELANDGOAL,
                StoneType.ATTRACT,
                StoneType.ATTRACTANDGOAL,
                StoneType.GOAL,
            }:
                if next_stone.type != StoneType.GOAL:
                    left_side.append(next_stone)
            else:
                break

        while left_side and left_side[-1].type != StoneType.OBSTACLE:
            stone = left_side.pop()
            old_row, old_col = stone.position
            new_row = old_row
            new_col = old_col - 1  # Move to the left
            if new_col < 0:
                break
            self.movement_replacing(old_row, old_col, new_row, new_col)

    def handle_repel_reflection_up(self, row, column):
        up_side = []
        for r in range(row, -1, -1):  # Iterate upwards
            if r - 1 < 0:
                break
            next_stone = self.board[r - 1][column]
            if next_stone.type in {
                StoneType.STONE,
                StoneType.STONEANDGOAL,
                StoneType.REPEL,
                StoneType.REPELANDGOAL,
                StoneType.ATTRACT,
                StoneType.ATTRACTANDGOAL,
            }:
                up_side.append(next_stone)
            else:
                break

        while up_side and up_side[-1].type != StoneType.OBSTACLE:
            stone = up_side.pop()
            old_row, old_col = stone.position
            new_row = old_row - 1  # Move up
            new_col = old_col
            if new_row < 0:
                break
            self.movement_replacing(old_row, old_col, new_row, new_col)

    def handle_repel_reflection_down(self, row, column):
        down_side = []
        for r in range(row, self.rows):  # Iterate downwards
            if r + 1 >= self.rows:
                break
            next_stone = self.board[r + 1][column]
            if next_stone.type in {
                StoneType.STONE,
                StoneType.STONEANDGOAL,
                StoneType.REPEL,
                StoneType.REPELANDGOAL,
                StoneType.ATTRACT,
                StoneType.ATTRACTANDGOAL,
            }:
                down_side.append(next_stone)
            else:
                break

        while down_side and down_side[-1].type != StoneType.OBSTACLE:
            stone = down_side.pop()
            old_row, old_col = stone.position
            new_row = old_row + 1  # Move down
            new_col = old_col
            if new_row >= self.rows:
                break
            self.movement_replacing(old_row, old_col, new_row, new_col)

    def movement_replacing(self, old_row, old_col, new_row, new_col):
        next_cell = self.board[new_row][new_col]
        current_cell = self.board[old_row][old_col]

        if next_cell.type == StoneType.EMPTY and current_cell.type == StoneType.STONE:
            next_cell.stone((new_row, new_col))
            current_cell.empty((old_row, old_col))
        elif next_cell.type == StoneType.GOAL and current_cell.type == StoneType.STONE:
            next_cell.stone_and_goal((new_row, new_col))
            current_cell.empty((old_row, old_col))
        elif (
            current_cell.type == StoneType.STONEANDGOAL
            and next_cell.type == StoneType.EMPTY
        ):
            next_cell.stone((new_row, new_col))
            current_cell.goal((old_row, old_col))
        elif (
            current_cell.type == StoneType.STONEANDGOAL
            and next_cell.type == StoneType.GOAL
        ):
            next_cell.stone_and_goal((new_row, new_col))
            current_cell.goal((old_row, old_col))
        elif next_cell.type == StoneType.EMPTY and current_cell.type == StoneType.REPEL:
            next_cell.repel((new_row, new_col))
            current_cell.empty((old_row, old_col))
        elif (
            next_cell.type == StoneType.EMPTY
            and current_cell.type == StoneType.REPELANDGOAL
        ):
            next_cell.repel((new_row, new_col))
            current_cell.goal((old_row, old_col))
        elif next_cell.type == StoneType.GOAL and current_cell.type == StoneType.REPEL:
            next_cell.repel_and_goal((new_row, new_col))
            current_cell.empty((old_row, old_col))
        elif (
            next_cell.type == StoneType.GOAL
            and current_cell.type == StoneType.REPELANDGOAL
        ):
            next_cell.repel_and_goal((new_row, new_col))
            current_cell.goal((old_row, old_col))
        elif (
            next_cell.type == StoneType.EMPTY and current_cell.type == StoneType.ATTRACT
        ):
            next_cell.attract((new_row, new_col))
            current_cell.empty((old_row, old_col))
        elif (
            next_cell.type == StoneType.EMPTY
            and current_cell.type == StoneType.ATTRACTANDGOAL
        ):
            next_cell.attract((new_row, new_col))
            current_cell.goal((old_row, old_col))
        elif (
            next_cell.type == StoneType.GOAL and current_cell.type == StoneType.ATTRACT
        ):
            next_cell.attractAndGoal((new_row, new_col))
            current_cell.empty((old_row, old_col))
        elif (
            next_cell.type == StoneType.GOAL
            and current_cell.type == StoneType.ATTRACTANDGOAL
        ):
            next_cell.attractAndGoal((new_row, new_col))
            current_cell.goal((old_row, old_col))

    def move_attract(self, stone):
        row, col = -1, -1

        while True:
            Message.message("Enter the desired cell row target :")
            row = int(input())
            Message.message("Enter the desired cell column target :")
            col = int(input())

            if not self.check_valid_move(row, col):
                Message.message("invalid Move")
                continue

            break

        current_cell = self.board[stone.position.row][stone.position.col]
        target_cell = self.board[row][col]

        if (
            target_cell.type == StoneType.EMPTY
            and current_cell.type == StoneType.ATTRACT
        ):
            current_cell.empty(stone.position)
            target_cell.attract((row, col))

        elif (
            target_cell.type == StoneType.EMPTY
            and current_cell.type == StoneType.ATTRACTANDGOAL
        ):
            current_cell.goal(stone.position)
            target_cell.attract((row, col))

        elif (
            target_cell.type == StoneType.GOAL
            and current_cell.type == StoneType.ATTRACT
        ):
            current_cell.empty(stone.position)
            target_cell.attract_and_goal((row, col))

        elif (
            current_cell.type == StoneType.ATTRACTANDGOAL
            and target_cell.type == StoneType.GOAL
        ):
            current_cell.goal(stone.position)
            target_cell.attract_and_goal((row, col))

        else:
            self.allowed_moves += 1
            Message.message("Invalid Move")

        self.handle_attract_reflection(row, col)
        self.print_board()
        if self.check_win():
            print("<<<------- You Win ------->>>")
            return current_cell

        return target_cell

    def handle_attract_reflection(self, current_row, current_col):
        self.handle_attract_reflection_right(current_row, current_col)
        self.handle_attract_reflection_left(current_row, current_col)
        self.handle_attract_reflection_up(current_row, current_col)
        self.handle_attract_reflection_down(current_row, current_col)

    def handle_attract_reflection_right(self, row, column):
        right_side = deque()
        for col in range(column, self.cols):
            if col + 1 >= self.cols:
                break
            next_stone = self.board[row][col + 1]
            Board.push_acceptable_stones(right_side, next_stone)

        while right_side and right_side[0].type != StoneType.OBSTACLE:
            stone = right_side.popleft()
            old_row, old_col = stone.position
            new_row = old_row
            new_col = old_col - 1
            if new_col >= self.cols:
                break
            self.movement_replacing(old_row, old_col, new_row, new_col)

    def handle_attract_reflection_left(self, row, column):
        left_side = deque()
        for col in range(column, -1, -1):
            if col - 1 < 0:
                break
            next_stone = self.board[row][col - 1]
            Board.push_acceptable_stones(left_side, next_stone)

        while left_side and left_side[0].type != StoneType.OBSTACLE:
            stone = left_side.popleft()
            old_row, old_col = stone.position
            new_row = old_row
            new_col = old_col + 1
            if new_col < self.cols:
                self.movement_replacing(old_row, old_col, new_row, new_col)
            else:
                break

    def handle_attract_reflection_up(self, row, column):
        up_side = deque()
        for r in range(row, -1, -1):
            if r - 1 < 0:
                break
            next_stone = self.board[r - 1][column]
            self.push_acceptable_stones(up_side, next_stone)

        while up_side and up_side[0].type != StoneType.OBSTACLE:
            stone = up_side.popleft()
            old_row, old_col = stone.position
            new_row = old_row + 1
            new_col = old_col
            if new_row < self.rows:
                self.movement_replacing(old_row, old_col, new_row, new_col)
            else:
                break

    def handle_attract_reflection_down(self, row, column):
        down_side = deque()
        for r in range(row, self.rows):
            if r + 1 >= self.rows:
                break
            next_stone = self.board[r + 1][column]
            self.push_acceptable_stones(down_side, next_stone)

        while down_side and down_side[0].type != StoneType.OBSTACLE:
            stone = down_side.popleft()
            old_row, old_col = stone.position
            new_row = old_row - 1
            new_col = old_col
            if new_row >= 0:
                self.movement_replacing(old_row, old_col, new_row, new_col)
            else:
                break

    def push_acceptable_stones(self, queue, next_stone):
        if next_stone.type in {
            StoneType.STONE,
            StoneType.STONEANDGOAL,
            StoneType.REPEL,
            StoneType.REPELANDGOAL,
            StoneType.ATTRACT,
            StoneType.ATTRACTANDGOAL,
        }:
            queue.append(next_stone)
