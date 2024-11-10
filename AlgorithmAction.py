# /////////////   2

from board import Board
# from stone import Stone
from stone import Stone, StoneType

class AlgorithmAction:
    @staticmethod
    def move(board: Board, selected_stone: Stone, row: int, col: int) -> Board:
        current_cell = board.board[selected_stone.position.row][selected_stone.position.col]
        target_cell = board.board[row][col]
        board.dirty = False

        result = AlgorithmAction.handle_movable(selected_stone, row, col, current_cell, target_cell)
        if result:
            board.dirty = True
            if selected_stone.type in (StoneType.REPEL, StoneType.REPELANDGOAL):
                board.handle_repel_reflection(row, col)
            elif selected_stone.type in (StoneType.ATTRACTANDGOAL, StoneType.ATTRACT):
                board.handle_attract_reflection(row, col)

        return board

    @staticmethod
    def handle_movable(stone: Stone, row: int, col: int, current_cell: Stone, target_cell: Stone) -> bool:
        if target_cell.type == StoneType.EMPTY and current_cell.type in (StoneType.ATTRACT, StoneType.ATTRACTANDGOAL):
            current_cell.empty(stone.position)
            target_cell.attract((row, col))
            return True
        elif target_cell.type == StoneType.GOAL and current_cell.type in (StoneType.ATTRACT, StoneType.ATTRACTANDGOAL):
            current_cell.goal(stone.position)
            target_cell.attract_and_goal((row, col))
            return True
        return False
