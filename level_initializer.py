# /////////
from message import Message
from Algorithm import Algorithm
from RepelActions import Board
from stone import StoneType
from Node import Node
import time


def show_node_path(child):
    child.board.print_board()
    if child.parent is None:
        return
    show_node_path(child.parent)


class LevelInitializer:
    def __init__(self):
        self.board = Board()

    def play(self):
        for _ in range(self.board.allowed_moves):
            valid_movable = True

            while True:
                movable_row = int(input("Select Movable row: "))
                movable_col = int(input("Select Movable Column: "))

                selected_movable = self.board.board[movable_row][movable_col]

                if selected_movable.type in [StoneType.REPEL, StoneType.REPELANDGOAL]:
                    self.board.move_repel(selected_movable)
                    self.board.print_board()
                elif selected_movable.type in [
                    StoneType.ATTRACT,
                    StoneType.ATTRACTANDGOAL,
                ]:
                    self.board.move_attract(selected_movable)
                    self.board.print_board()
                else:
                    Message.message("Error: Select A Valid Movable Stone")
                    valid_movable = False

                if self.board.check_win():
                    Message.message("You Win")
                    return

                if valid_movable:
                    break

    def handler(self):
        level_number = int(input("Select A Level Number: From (1) To (12) "))

        if level_number == 1:
            self.level1().handle_choices()
        elif level_number == 2:
            self.level2().handle_choices()
        elif level_number == 3:
            self.level3().handle_choices()
        elif level_number == 4:
            self.level4().handle_choices()
        elif level_number == 5:
            self.level5().handle_choices()
        elif level_number == 6:
            self.level6().handle_choices()
        elif level_number == 7:
            self.level7().handle_choices()
        elif level_number == 8:
            self.level8().handle_choices()
        elif level_number == 9:
            self.level9().handle_choices()
        elif level_number == 10:
            self.level10().handle_choices()
        elif level_number == 11:
            self.level11().handle_choices()
        elif level_number == 12:
            self.level12().handle_choices()
        elif level_number == 21:
            self.level21().handle_choices()
        else:
            self.level1().handle_choices()

    def handle_choices(self):
        valid_selection = True
        choice = 0

        while True:
            self.board.print_board()
            Message.message("If You Want To Play Press (1)")
            Message.message("If You Want To Solve It With BFS Algorithm Press (2)")
            Message.message("If You Want To Solve It With UCS Algorithm Press (3)")
            Message.message(
                "If You Want To Solve It With Hill Climbing Algorithm Press (4)"
            )

            choice = int(input())

            if choice == 1:
                self.play()
                return
            elif choice == 2:
                LevelInitializer.apply_algorithm(self.board, Algorithm.bfs)
                return

            if choice == 3:
                LevelInitializer.apply_algorithm(self.board, Algorithm.ucs)
                return
            elif choice == 4:
                root = Node.create_node(self.board)
                root.depth = self.board.allowed_moves
                self.board.print_board()

                start_time = time.perf_counter()

                algorithm = Algorithm()
                algorithm.hill_climbing(root)
                end_time = time.perf_counter()
                duration = (
                    end_time - start_time
                ) * 1_000_000  # Convert to microseconds
                show_node_path(root)

                print("-------------------------------------------------------------")
                print(
                    f"Execution Time In Micro Seconds Ss : {duration:.0f} Micro Second"
                )
                print("-------------------------------------------------------------")

                print("-------------------------------------------------------------")
                print(f"Visited Nodes Count is : {algorithm.visited_nodes}")
                print("-------------------------------------------------------------")

                return
            else:
                Message.message("Invalid Selection Try Again")
                valid_selection = False

    @staticmethod

    def apply_algorithm(board, algorithm):
        print("dddddddddddddddd")
        algorithm_instance = Algorithm()
        print("eeeeeeeeeeeeeeee")
        start_time = time.perf_counter()
        if algorithm == Algorithm.bfs:
            algorithm_instance.bfs(board)
        elif algorithm == Algorithm.ucs:
            algorithm_instance.ucs(board)
        else:
            print("Invalid algorithm selected.")
        print("aaaaaaaaaaaaaaaa")
        end_time = time.perf_counter()
        duration = (end_time - start_time) * 1_000_000  # Convert to microseconds
        print("-------------------------------------------------------------")
        print(f"Execution Time In Micro Seconds Ss : {duration:.0f} Micro Second")
        print("-------------------------------------------------------------")

    def level1(self):
        self.board = Board(3, 4, 2)
        self.board.board[2][0].repel((2, 0))
        self.board.board[1][2].stone((1, 2))
        self.board.board[1][1].goal((1, 1))
        self.board.board[1][3].goal((1, 3))
        self.board.init_movables()
        return self

    def level2(self):
        self.board = Board(5, 5, 5)
        self.board.board[4][0].repel((4, 0))
        self.board.board[0][2].goal((0, 2))
        self.board.board[2][0].goal((2, 0))
        self.board.board[2][2].goal((2, 2))
        self.board.board[2][4].goal((2, 4))
        self.board.board[4][2].goal((4, 2))
        self.board.board[1][2].stone((1, 2))
        self.board.board[2][1].stone((2, 1))
        self.board.board[2][3].stone((2, 3))
        self.board.board[3][2].stone((3, 2))

        return self

    def level3(self):
        self.board = Board(3, 4, 5)
        self.board.board[2][0].repel((2, 0))
        self.board.board[1][2].stone((1, 2))
        self.board.board[0][3].goal((0, 3))
        self.board.board[2][3].goal((2, 3))
        self.board.board[0][0].obstacle((0, 0))
        self.board.board[0][1].obstacle((0, 1))
        self.board.board[0][2].obstacle((0, 2))

        return self

    def level4(self):
        self.board = Board(5, 3, 5)
        self.board.board[2][0].repel((2, 0))
        self.board.board[1][1].stone((1, 1))
        self.board.board[3][1].stone((3, 1))
        self.board.board[0][0].goal((0, 0))
        self.board.board[0][2].goal((0, 2))
        self.board.board[4][1].goal((4, 1))
        self.board.board[1][0].obstacle((1, 0))
        self.board.board[3][0].obstacle((3, 0))

        return self

    def level5(self):
        self.board = Board(4, 3, 2)
        self.board.board[3][1].repel((3, 1))
        self.board.board[1][0].stone_and_goal((1, 0))
        self.board.board[1][2].stone_and_goal((1, 2))
        self.board.board[2][0].stone((2, 0))
        self.board.board[2][2].stone((2, 2))
        self.board.board[0][0].goal((0, 0))
        self.board.board[0][2].goal((0, 2))
        self.board.board[3][0].goal((3, 0))
        for i in range(3):
            self.board.board[i][1].obstacle((i, 1))

        return self

    def level6(self):
        self.board = Board(3, 5, 2)
        self.board.board[2][0].repel((2, 0))
        self.board.board[1][1].stone((1, 1))
        self.board.board[1][3].stone((1, 3))
        self.board.board[0][3].goal((0, 3))
        self.board.board[1][2].goal((1, 2))
        self.board.board[2][3].goal((2, 3))

        return self

    def level7(self):
        self.board = Board(5, 4, 2)
        self.board.board[2][1].repel((2, 1))
        self.board.board[0][0].goal((0, 0))
        self.board.board[2][3].goal((2, 3))
        self.board.board[4][3].goal((4, 3))
        self.board.board[1][0].stone_and_goal((1, 0))
        self.board.board[3][2].stone_and_goal((3, 2))
        self.board.board[2][0].stone((2, 0))
        self.board.board[3][1].stone((3, 1))
        for i in range(3):
            self.board.board[4][i].obstacle((4, i))

        return self

    def level8(self):
        self.board = Board(3, 4, 2)
        self.board.board[2][0].repel((2, 0))
        self.board.board[0][0].goal((0, 0))
        self.board.board[0][2].goal((0, 2))
        self.board.board[2][2].goal((2, 2))
        self.board.board[1][1].stone((1, 1))
        self.board.board[1][2].stone((1, 2))

        return self

    def level9(self):
        self.board = Board(1, 7, 2)
        self.board.board[0][0].repel((0, 0))
        self.board.board[0][1].goal((0, 1))
        self.board.board[0][6].goal((0, 6))
        self.board.board[0][3].stone_and_goal((0, 3))
        self.board.board[0][5].stone((0, 5))

        return self

    def level11(self):
        self.board = Board(2, 5, 1)
        self.board.board[1][2].attract((1, 2))
        self.board.board[0][1].goal((0, 1))
        self.board.board[0][2].goal((0, 2))
        self.board.board[0][3].goal((0, 3))
        self.board.board[0][0].stone((0, 0))
        self.board.board[0][4].stone((0, 4))
        self.board.board[1][0].obstacle((1, 0))
        self.board.board[1][1].obstacle((1, 1))
        self.board.board[1][3].obstacle((1, 3))
        self.board.board[1][4].obstacle((1, 4))

        return self
