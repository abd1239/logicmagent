# ////////////////


class StoneType:
    REPEL = 1
    ATTRACT = 2
    STONE = 3
    GOAL = 4
    OBSTACLE = 5
    EMPTY = 6
    STONEANDGOAL = 7
    REPELANDGOAL = 8
    ATTRACTANDGOAL = 9


class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Stone:
    def __init__(self, stone_type=None, can_move=True, position=None):
        if position is None:
            position = Position(0, 0)
        self.type = stone_type if stone_type is not None else StoneType.EMPTY
        self.name = self.naming(self.type)
        self.can_move = can_move
        self.position = position

    def naming(self, stone_type):
        if stone_type == StoneType.REPEL:
            return " R "
        elif stone_type == StoneType.ATTRACT:
            return " A "
        elif stone_type == StoneType.STONE:
            return " S "
        elif stone_type == StoneType.GOAL:
            return " G "
        elif stone_type == StoneType.OBSTACLE:
            return " O "
        elif stone_type == StoneType.EMPTY:
            return "   "

    def repel(self, current_position):
        self.name = " R "
        self.type = StoneType.REPEL
        self.can_move = True
        self.position = current_position
        return self

    def attract(self, current_position):
        self.name = " A "
        self.type = StoneType.ATTRACT
        self.can_move = True
        self.position = current_position
        return self

    def empty(self, current_position):
        self.name = "   "
        self.type = StoneType.EMPTY
        self.can_move = True
        self.position = current_position
        return self

    def stone(self, current_position):
        self.name = " S "
        self.type = StoneType.STONE
        self.can_move = True
        self.position = current_position
        return self

    def stone_and_goal(self, current_position):
        self.name = "S+G"
        self.type = StoneType.STONEANDGOAL
        self.can_move = True
        self.position = current_position
        return self

    def obstacle(self, current_position):
        self.name = " O "
        self.type = StoneType.OBSTACLE
        self.can_move = False
        self.position = current_position
        return self

    def goal(self, current_position):
        self.name = " G "
        self.type = StoneType.GOAL
        self.can_move = False
        self.position = current_position
        return self

    def repel_and_goal(self, current_position):
        self.name = "R+G"
        self.type = StoneType.REPELANDGOAL
        self.can_move = True
        self.position = current_position
        return self

    def attract_and_goal(self, current_position):
        self.name = "G+A"
        self.type = StoneType.ATTRACTANDGOAL
        self.can_move = True
        self.position = current_position
        return self


def remove_whitespace(s):
    return "".join(s.split())
