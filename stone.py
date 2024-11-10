# ////////////////////////////////   2
from stone_type_enum import StoneType
from position import Position

class Stone:
    def __init__(self, type=StoneType.EMPTY, can_move=True, position=Position(0, 0)):
        self.type = type
        self.name = ""
        self.naming(type)
        self.can_move = can_move
        self.position = position

    def naming(self, stone_type):
        if stone_type == StoneType.REPEL:
            self.name = " R "
        elif stone_type == StoneType.ATTRACT:
            self.name = " A "
        elif stone_type == StoneType.STONE:
            self.name = " S "
        elif stone_type == StoneType.GOAL:
            self.name = " G "
        elif stone_type == StoneType.OBSTACLE:
            self.name = " O "
        elif stone_type == StoneType.EMPTY:
            self.name = "   "

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
        self.name = "  "
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
        self.name = "G+R"
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






