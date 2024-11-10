# ////////////   2



from level_initializer import LevelInitializer
from message import Message
from Algorithm import Node

def show_path(child: Node):
    child.board.print_board()
    if child.parent is None:
        return
    show_path(child.parent)

def main():
    level_initializer = LevelInitializer()

    

    play = False

    while True:
        Message.message("1- Play")
        Message.message("0- Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            level_initializer.handler()
        elif choice == "0":
            break
        else:
            Message.message("Invalid option. Please try again.")

if __name__ == "__main__":
    main()








