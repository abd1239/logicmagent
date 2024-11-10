# //////////////   2

from collections import deque
from message import Message
from board import Board
from Node import Node


class Algorithm:
    def __init__(self):
        self.visited_nodes = 0

    @staticmethod
    def bfs(board: Board):
        root = Board(board)
        states = deque([root])
        visited_counter = 0

        while states:
            current = Board(states.popleft())
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

    # ///////

    @staticmethod
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
                                states.append(
                                    result_board
                                )  
