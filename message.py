# ////////   2
class Message:
    @staticmethod
    def message(msg):
        height = 1
        width = len(msg) + 8
        horizontal_line = '-' * width
        vertical_line = f"| {msg}      |"

        # Print the top border
        for i in range(height):
            if i == 0:
                print(horizontal_line)
            else:
                print(f"| {' ' * (len(msg) + 8)} |")

        # Print the message
        print(vertical_line)

        # Print the bottom border
        for i in range(height):
            if i == height - 1:
                print(horizontal_line)
            else:
                print(f"| {' ' * (len(msg) + 8)} |")

