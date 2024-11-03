class Piece:
    def __init__(self, color, type, is_movable=True):
        self.color = color  
        self.type = type 
        self.is_movable = is_movable  



class Board:
    def __init__(self, n, m, target_cells, stone_cells):
        self.n = n
        self.m = m
        self.grid = [[None for _ in range(m)] for _ in range(n)]
        self.target_cells = target_cells  
        self.stone_cells = stone_cells  

        for (x, y) in stone_cells:
            self.grid[x][y] = Piece("stone", "obstacle", False)

    def place_piece(self, piece, x, y):
        if 0 <= x < self.n and 0 <= y < self.m and self.grid[x][y] is None:
            self.grid[x][y] = piece

            

    def display(self):
        for i in range(self.n):
            row = []
            for j in range(self.m):
                if (i, j) in self.target_cells:
                    row.append("T" if self.grid[i][j] is None else self.grid[i][j].color[0].upper())
                elif (i, j) in self.stone_cells:
                    row.append("S") 
                else:
                    row.append("_" if self.grid[i][j] is None else self.grid[i][j].color[0].upper())
            print(" ".join(row))
        print("\n")

    def move_piece(self, x, y, new_x, new_y):
        piece = self.grid[x][y]
        if piece is None or not piece.is_movable or (new_x, new_y) in self.stone_cells:
            return False     

        if 0 <= new_x < self.n and 0 <= new_y < self.m and self.grid[new_x][new_y] is None:
            self.grid[x][y] = None
            self.grid[new_x][new_y] = piece
            if (new_x, new_y) in self.target_cells:
                piece.is_movable = False
            self.apply_attract_repel(new_x, new_y)
            return True
        return False

    def apply_attract_repel(self, x, y):
        piece = self.grid[x][y]
        if piece is None or piece.type != "magnet":
            return
        if piece.color == "red":
            self._attract_all_irons(x, y)
        elif piece.color == "purple":
            self._repel_all_irons(x, y)



    def _attract_all_irons(self, magnet_x, magnet_y):
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] and self.grid[i][j].type == "iron":
                    dx, dy = magnet_x - i, magnet_y - j
                    if abs(dx) > abs(dy):
                        new_x, new_y = i + (1 if dx > 0 else -1), j
                    else:
                        new_x, new_y = i, j + (1 if dy > 0 else -1)
                    if 0 <= new_x < self.n and 0 <= new_y < self.m and self.grid[new_x][new_y] is None:
                        self.move_piece(i, j, new_x, new_y)



    def _repel_all_irons(self, magnet_x, magnet_y):
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] and self.grid[i][j].type == "iron":
                    dx, dy = i - magnet_x, j - magnet_y
                    if abs(dx) > abs(dy):
                        new_x, new_y = i + (1 if dx > 0 else -1), j
                    else:
                        new_x, new_y = i, j + (1 if dy > 0 else -1)
                    if 0 <= new_x < self.n and 0 <= new_y < self.m and self.grid[new_x][new_y] is None:
                        self.move_piece(i, j, new_x, new_y)



    def is_goal_state(self):
        for x, y in self.target_cells:
            if self.grid[x][y] is None:
                return False
        return True



class LogicMagnetsGame:
    def __init__(self, board):
        self.board = board
        self.steps = 0
        self.failed_moves = 0

    def play_move(self, x, y, new_x, new_y):
        if self.board.move_piece(x, y, new_x, new_y):
            self.board.display()
            self.steps += 1
            if self.board.is_goal_state():
                return True
            self.failed_moves = 0
        else:
            print("move not valed .")
            self.failed_moves += 1
        return False


def load_level(level):
    levels = [
        {'n': 3, 'm' : 4, 'targets': [(1, 1), (1, 3)], 'stones' : () , 'pieces': [('purple', 'magnet', 2, 0), ('gray', 'iron', 1, 2)]},
        {
            "n": 5,
            'm': 5 ,
            "targets": [(0, 2), (2, 0), (2, 4), (4, 2), (2, 2)],
            'stones' : () ,
            "pieces": [
                ("purple", "magnet", 4, 0),
                ("gray", "iron", 2, 1),
                ("gray", "iron", 1, 2),
                ("gray", "iron", 2, 3),
                ("gray", "iron", 3, 2),
            ]
        },
        {'n': 3, 'm': 4, 'targets': [(0, 3), (2, 3)], 'stones': [(0, 0) , (0, 1),(0, 2)], 'pieces': [('purple', 'magnet', 2, 0), ('gray', 'iron', 1, 2)]},
        {'n': 5, 'm': 3, 'targets': [(0, 0), (0, 2), (4, 1)], 'stones': [(1, 0) , (3,0)], 'pieces': [('purple', 'magnet', 2, 0), ('gray', 'iron', 1, 1),('gray', 'iron', 3, 1)]},
    ]
    level_data = levels[level - 1]
    n, m = level_data['n'], level_data['m']
    board = Board(n, m, level_data['targets'], level_data['stones'])

    for color, type, x, y in level_data['pieces']:
        if 0 <= x < n and 0 <= y < m:
            board.place_piece(Piece(color, type), x, y)
        else:
            print(f": ({x}, {y}) out board ({n}x{m})")
    return board


def main():
    level = 1
    while level <= 2:
        board = load_level(level)
        game = LogicMagnetsGame(board)

        print(f"level {level} :")
        game.board.display()

        while not game.board.is_goal_state():
            if game.failed_moves >= 3:
                print("you failed! .")
                return

            print("enter move : ")
            x = int(input("enter point spice x: "))
            y = int(input("enter point spice y "))
            new_x = int(input("enter x new: "))
            new_y = int(input("enter y new: "))

            if game.play_move(x, y, new_x, new_y):
                print(f"you win in level{level}!")
                level += 1
                break

        if level > 2:
            print("congurlation!")
            break


if __name__ == "__main__":
    main()











































































