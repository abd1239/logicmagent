# ////////////

import sys
from level_initializer import LevelInitializer
from message import Message


def showPath(child):
    child.board.printBoard()
    if child.parent is None:
        return
    showPath(child.parent)


def main():
    levelInitializer = LevelInitializer()
    play = False
    while True:
        Message.message("1- Play")
        Message.message("0- Exit")
        play = int(input())
        if play == 0:
            break
        levelInitializer.handler()
    return 0


if __name__ == "__main__":
    # sys.exit(main())
    main()
