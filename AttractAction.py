# //////  2
# استيراد مكتبة queue لتعامل مع الكائنات المتحركة
from queue import Queue
from board import Board
from message import Message  # يفترض وجود هذا الملف للكلاس Message
from stone import Stone, StoneType


class AttractAction(Board):
    def move_attract(self, stone):
        while True:
            row = int(input("Enter the desired cell row target: "))
            col = int(input("Enter the desired cell column target: "))

            if not self.check_valid_move(row, col):
                Message.message("Invalid Move")
            else:
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
        right_side = Queue()
        for col in range(column, self.cols):
            if col + 1 >= self.cols:
                break
            next_stone = self.board[row][col + 1]
            self.push_acceptable_stones(right_side, next_stone)

        while not right_side.empty() and right_side.queue[0].type != "OBSTACLE":
            stone = right_side.get()
            old_row, old_col = stone.position
            new_row = old_row
            new_col = old_col - 1
            if new_col >= self.cols:
                break
            self.movement_replacing(old_row, old_col, new_row, new_col)

    def handle_attract_reflection_left(self, row, column):
        left_side = Queue()
        for col in range(column, -1, -1):
            if col - 1 < 0:
                break
            next_stone = self.board[row][col - 1]
            self.push_acceptable_stones(left_side, next_stone)

        while not left_side.empty() and left_side.queue[0].type != "OBSTACLE":
            stone = left_side.get()
            old_row, old_col = stone.position
            new_row = old_row
            new_col = old_col + 1
            if new_col < 0:
                break
            self.movement_replacing(old_row, old_col, new_row, new_col)

    def handle_attract_reflection_up(self, row, column):
        up_side = Queue()
        for r in range(row, -1, -1):
            if r - 1 < 0:
                break
            next_stone = self.board[r - 1][column]
            self.push_acceptable_stones(up_side, next_stone)

        while not up_side.empty() and up_side.queue[0].type != "OBSTACLE":
            stone = up_side.get()
            old_row, old_col = stone.position
            new_row = old_row + 1
            new_col = old_col
            if new_row < 0:
                break
            self.movement_replacing(old_row, old_col, new_row, new_col)

    def handle_attract_reflection_down(self, row, column):
        down_side = Queue()
        for r in range(row, self.rows):
            if r + 1 >= self.rows:
                break
            next_stone = self.board[r + 1][column]
            self.push_acceptable_stones(down_side, next_stone)

        while not down_side.empty() and down_side.queue[0].type != "OBSTACLE":
            stone = down_side.get()
            old_row, old_col = stone.position
            new_row = old_row - 1
            new_col = old_col
            if new_row >= self.rows:
                break
            self.movement_replacing(old_row, old_col, new_row, new_col)

    def push_acceptable_stones(self, queue, stone):
        if stone.type == "STONE" or stone.type == "IRON":
            queue.put(stone)


def movement_replacing(self, old_row, old_col, new_row, new_col):
    next_cell = self.board[new_row][new_col]
    current_cell = self.board[old_row][old_col]

    if next_cell.type == "EMPTY" and current_cell.type == "STONE":
        next_cell.stone((new_row, new_col))
        current_cell.empty((old_row, old_col))

    elif next_cell.type == "GOAL" and current_cell.type == "STONE":
        next_cell.stone_and_goal((new_row, new_col))
        current_cell.empty((old_row, old_col))

    elif current_cell.type == "STONEANDGOAL" and next_cell.type == "EMPTY":
        next_cell.stone((new_row, new_col))
        current_cell.goal((old_row, old_col))

    elif current_cell.type == "STONEANDGOAL" and next_cell.type == "GOAL":
        next_cell.stone_and_goal((new_row, new_col))
        current_cell.goal((old_row, old_col))

    elif next_cell.type == "EMPTY" and current_cell.type == "REPEL":
        next_cell.repel((new_row, new_col))
        current_cell.empty((old_row, old_col))

    elif next_cell.type == "EMPTY" and current_cell.type == "REPELANDGOAL":
        next_cell.repel((new_row, new_col))
        current_cell.goal((old_row, old_col))

    elif next_cell.type == "GOAL" and current_cell.type == "REPEL":
        next_cell.repel_and_goal((new_row, new_col))
        current_cell.empty((old_row, old_col))

    elif next_cell.type == "GOAL" and current_cell.type == "REPELANDGOAL":
        next_cell.repel_and_goal((new_row, new_col))
        current_cell.goal((old_row, old_col))

    elif next_cell.type == "EMPTY" and current_cell.type == "ATTRACT":
        next_cell.attract((new_row, new_col))
        current_cell.empty((old_row, old_col))

    elif next_cell.type == "EMPTY" and current_cell.type == "ATTRACTANDGOAL":
        next_cell.attract((new_row, new_col))
        current_cell.goal((old_row, old_col))

    elif next_cell.type == "GOAL" and current_cell.type == "ATTRACT":
        next_cell.attract_and_goal((new_row, new_col))
        current_cell.empty((old_row, old_col))

    elif next_cell.type == "GOAL" and current_cell.type == "ATTRACTANDGOAL":
        next_cell.attract_and_goal((new_row, new_col))
        current_cell.goal((old_row, old_col))
