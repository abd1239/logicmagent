

from board import Board
from message import Message
from Algorithm import Algorithm
from Node import Node
from RepelActions import RepelAction
from stone import StoneType
import time



def show_node_path(child):
    child.board.print_board()
    if child.parent is None:
        return
    return show_node_path(child.parent)


class LevelInitializer(RepelAction):
  
    def __init__(self):
        self.board = Board()

    def play(self):
        for _ in range(self.board.allowed_moves):
            valid_movable = True

            while valid_movable:
                movable_row = int(input("Select Movable row: "))
                movable_col = int(input("Select Movable Column: "))

                selected_movable = self.board.board[movable_row][movable_col]
                print(selected_movable.type)
                  
                if selected_movable.type in {StoneType.REPELANDGOAL, StoneType.REPEL, StoneType.ATTRACTANDGOAL, StoneType.ATTRACT}:
                    if selected_movable.type in {StoneType.REPELANDGOAL, StoneType.REPEL}:
                        self.move_repel(selected_movable)
                        self.board.print_board() 
                    elif selected_movable.type in {StoneType.ATTRACTANDGOAL, StoneType.ATTRACT}:
                        self.board.move_attract(selected_movable)
                        self.board.print_board()
                    else:
                      Message.message("Error: Select A Valid Movable Stone")
                      valid_movable = False  # تغيير هذا لتكرار المحاولة في حال عدم اختيار حجر قابل للتحريك


                    if self.board.check_win():
                        Message.message("You Win")
                        return

    def handler(self):
        level_number = int(input("Select A Level Number: From (1) To (12): "))

        level_methods = {
            1: self.level1,
            2: self.level2,
            # 3: self.level3,
            # 4: self.level4,
            # 5: self.level5,
            # 6: self.level6,
            # 7: self.level7,
            # 8: self.level8,
            # 9: self.level9,
            # 10: self.level10,
            # 11: self.level11,
            # 12: self.level12,
            # 21: self.level21,
            # 27: self.level27
        }

        level_method = level_methods.get(level_number, self.level1)
        level_method().handle_choices()

    def handle_choices(self):
        valid_selection = True
        while valid_selection:
            self.board.print_board()
            choice = int(input(
                "If You Want To Play Press (1)\n"
                "If You Want To Solve It With BFS Algorithm Press (2)\n"
                "If You Want To Solve It With DFS Algorithm Press (3)\n"
                # "If You Want To Solve It With UCS Algorithm Press (3)\n"
                # "If You Want To Solve It With Hill Climbing Algorithm Press (4): "
            ))

            if choice == 1:
                self.play()
                return
            elif choice == 2:
                self.apply_algorithm(self.board, Algorithm.bfs)
                return
            elif choice == 3:
                self.apply_algorithm(self.board, Algorithm.dfs)
                return
            else:
                Message.message("Invalid Selection Try Again")
                valid_selection = False

    @staticmethod
    def apply_algorithm(desired_board, algorithm):
        start_time = time.time()
        algorithm(desired_board)
        end_time = time.time()
        print("-------------------------------------------------------------")
        print(f"Execution Time In Seconds: {end_time - start_time:.6f} seconds")
        print("-------------------------------------------------------------")

    # Placeholder methods for each level
    def level1(self):
        self.board = Board(3, 4, 2)
        self.board.board[2][0].repel((2, 0))
        self.board.board[1][2].stone((1, 2))
        self.board.board[1][1].goal((1, 1))
        self.board.board[1][3].goal((1, 3))
        self.board.init_movables()
        return self

    def level2(self):
        self.board = Board(3, 4, 2)
        self.board.board[1][0].repel((1, 0))
        self.board.board[1][2].stone((1, 2))
        self.board.board[1][1].goal((1, 1))
        self.board.board[1][3].goal((1, 3))
        self.board.init_movables()
        return self

  
