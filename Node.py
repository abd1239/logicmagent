# ///////////   2


class Node:
    def __init__(self, level):
        self.board = level
        self.children = []
        self.depth = 0
        self.parent = None
        self.cost = 0
        self.heuristic_cost = 0
        self.visited = False

    def add_child(self, child_node):
        self.children.append(child_node)

    @staticmethod
    def create_node(level):
        return Node(level)
