# /////////////////////
import copy
from queue import Queue
from RepelActions import Board
from message import Message
from stone import StoneType
import heapq


class Algorithm:
    def __init__(self):
        self.visitedNodes = 0

    @staticmethod
    def move(board, selectedStone, row, col):
        new_board = copy.deepcopy(board)  # إنشاء نسخة جديدة من اللوحة
        currentCell = new_board.board[selectedStone.position[0]][
            selectedStone.position[1]
        ]
        targetCell = new_board.board[row][col]
        new_board.dirty = False

        result = handleMovable(selectedStone, row, col, currentCell, targetCell)

        if result:
            new_board.dirty = True
            if (
                selectedStone.type == StoneType.REPEL
                or selectedStone.type == StoneType.REPELANDGOAL
            ):
                new_board.handle_repel_reflection(row, col)
        elif (
            selectedStone.type == StoneType.ATTRACTANDGOAL
            or selectedStone.type == StoneType.ATTRACT
        ):
            new_board.handle_repel_reflection(row, col)

        return new_board

    # ///////BFS

    def bfs(self, board):
        root = Board(board.rows, board.cols, board.allowed_moves)
        root.board = board.board
        states = Queue()
        states.put(root)
        visited_states = set()
        visited_counter = 0

        while not states.empty():
            current = states.get()

            # تحقق من حالة الفوز في الحالة الحالية
            if current.check_win():
                Message.message("The Win State")
                current.print_board()
                print(f"Total Visited Nodes: {visited_counter}")
                # return
                break

            state_tuple = tuple(
                tuple(stone.type for stone in row) for row in current.board
            )
            if state_tuple in visited_states:
                continue

            visited_states.add(state_tuple)
            visited_counter += 1
            # print("aaammkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")

            current.init_movables()
            # print(f"Current Board: {current.board}")
            # print(f"Current Movables: {[m.name for m in current.movables]}")

            for movable in current.movables:
                for row in range(current.rows):
                    for col in range(current.cols):
                        if current.check_valid_move(row, col):
                            new_board = Algorithm.move(current, movable, row, col)
                            # print(f"New Board after move: {new_board.board}")
                            print(f"New Board after move: {current.print_board()}")

                            new_state_tuple = tuple(
                                tuple(stone.type for stone in new_board.board[r])
                                for r in range(new_board.rows)
                            )

                            if new_state_tuple not in visited_states:
                                states.put(new_board)

        # print(f"Total Visited Nodes: {visited_counter}")
        # print(f"New Board after move: {[[(stone.type) for stone in row] for row in new_board.board]}")

    def dfs(board: Board):
        root = Board(board)
        states = [root]
        visited_counter = 0

        while states:
            current = Board(states.pop())
            current.init_movables()
            win, out_of_moves = False, False

            for row in range(current.rows):
                if win or out_of_moves:
                    break

                for col in range(current.cols):
                    if win or out_of_moves:
                        break

                    current.init_movables()

                    while current.movables:
                        movable = current.movables.pop()
                        if current.check_valid_move(row, col):
                            result_board = Board(
                                Algorithm.move(current, movable, row, col)
                            )
                            result_board.father = current

                            if result_board.dirty:
                                result_board.print_board()
                                visited_counter += 1

                                if result_board.check_win():
                                    win = True
                                    states.clear()
                                    Message.message("The Win State")
                                    result_board.print_board()
                                    print(
                                        "The Solution Depth Is:",
                                        result_board.allowed_moves,
                                    )
                                    print(
                                        "The Count Of Visited Nodes Is:",
                                        visited_counter,
                                    )
                                    Algorithm.ask_for_solution_path(result_board)
                                    break

                                if result_board.allowed_moves <= 0:
                                    out_of_moves = True
                                    break

                                result_board.allowed_moves -= 1
                                states.append(result_board)

    # //////////UCS

    def ucs(self, board):
        root = Board(board.rows, board.cols, board.allowed_moves)

        root.board = [row[:] for row in board.board]
        root.cost = 0
        states = []
        visited_states = set()
        heapq.heappush(states, (root.cost, root))

        visited_counter = 0

        while states:
            current_cost, current = heapq.heappop(states)
            print(f"Popped state with cost: {current_cost}")
            current.init_movables()

            current_board_state = tuple(
                tuple(stone.type for stone in row) for row in current.board
            )
            if current_board_state in visited_states:
                continue
            visited_states.add(current_board_state)
            visited_counter += 1

            if current.check_win():
                print("Win state found!")
                current.print_board()
                print(f"Total Visited Nodes: {visited_counter}")
                break

            for movable in current.movables:
                for row in range(current.rows):
                    for col in range(current.cols):
                        if current.check_valid_move(row, col):
                            result_board = Algorithm.move(current, movable, row, col)
                            result_board.father = current

                            if result_board.dirty:
                                print(f"Current board after move: {result_board.board}")
                                result_board.cost = current.cost + (
                                    1
                                    if movable.type
                                    in (StoneType.REPEL, StoneType.REPELANDGOAL)
                                    else 2
                                )
                                # visited_counter += 1

                                new_state_tuple = tuple(
                                    tuple(stone.type for stone in result_board.board[r])
                                    for r in range(result_board.rows)
                                )
                                if new_state_tuple not in visited_states:
                                    # visited_states.add(new_state_tuple)
                                    heapq.heappush(
                                        states, (result_board.cost, result_board)
                                    )
                                    print(
                                        f"Added new state with cost: {result_board.cost}"
                                    )

        # print(f"Total Visited Nodes: {visited_counter}")


@staticmethod
def handleMovable(stone, row, col, currentCell, targetCell):
    # attract moves
    if targetCell.type == StoneType.EMPTY and currentCell.type == StoneType.ATTRACT:
        currentCell.empty(stone.position)
        targetCell.attract((row, col))
        return True
    elif (
        targetCell.type == StoneType.EMPTY
        and currentCell.type == StoneType.ATTRACTANDGOAL
    ):
        currentCell.goal(stone.position)
        targetCell.attract((row, col))
        return True
    elif targetCell.type == StoneType.GOAL and currentCell.type == StoneType.ATTRACT:
        currentCell.empty(stone.position)
        targetCell.attract_and_goal((row, col))
        return True
    elif (
        currentCell.type == StoneType.ATTRACTANDGOAL
        and targetCell.type == StoneType.GOAL
    ):
        currentCell.goal(stone.position)
        targetCell.attract_and_goal((row, col))
        return True

    # repel moves
    elif targetCell.type == StoneType.EMPTY and currentCell.type == StoneType.REPEL:
        currentCell.empty(stone.position)
        targetCell.repel((row, col))
        return True
    elif (
        targetCell.type == StoneType.EMPTY
        and currentCell.type == StoneType.REPELANDGOAL
    ):
        currentCell.goal(stone.position)
        targetCell.repel((row, col))
        return True
    elif targetCell.type == StoneType.GOAL and currentCell.type == StoneType.REPEL:
        currentCell.empty(stone.position)
        targetCell.repel_and_goal((row, col))
        return True
    elif (
        currentCell.type == StoneType.REPELANDGOAL and targetCell.type == StoneType.GOAL
    ):
        currentCell.goal(stone.position)
        targetCell.repel_and_goal((row, col))
        return True
    else:
        return False

    # ///////
