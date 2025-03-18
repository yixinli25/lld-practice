from collections import defaultdict

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol
    
    def get_name(self):
        return self.name

class Board:
    def __init__(self, n):
        self.n = n
        self.board = [["-" for _ in range(n)] for _ in range(n)]
        self.rows = defaultdict(int)
        self.cols = defaultdict(int)
        self.diag = 0
        self.anti_diag = 0
        self.move_count = 0

    def get_board_size(self):
        return self.n

    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def make_move(self, row, col, symbol):
        if (
            row < 0
            or row >= self.n
            or col < 0
            or col >= self.n
            or self.board[row][col] != "-"
        ):
            raise ValueError("Invalid move!")
        
        self.board[row][col] = symbol
        self.rows[row] += 1 if symbol == "X" else -1
        self.cols[col] += 1 if symbol == "X" else -1
        if row == col:
            self.diag += 1 if symbol == "X" else -1
        if row + col == self.n - 1:
            self.anti_diag += 1 if symbol == "X" else -1
        self.move_count += 1

    def is_full(self):
        return self.move_count == self.n ** 2
    
    def has_winner(self):
        for row in self.rows:
            if abs(self.rows[row]) == self.n:
                return True
        
        for col in self.cols:
            if abs(self.cols[col]) == self.n:
                return True
            
        if abs(self.diag) == self.n or abs(self.anti_diag) == self.n:
            return True

        return False
    
class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board(3)
        self.current_player = player1

    def play(self):
        self.board.print_board()
        while not self.board.is_full() and not self.board.has_winner():
            print(f"{self.current_player.get_name()}'s turn.")
            row = self.get_valid_input("Enter row: ")
            col = self.get_valid_input("Enter col: ")
            try:
                self.board.make_move(row, col, self.current_player.get_symbol())
                self.board.print_board()
                self.switch_player()
            except ValueError as e:
                print(str(e))

        if self.board.has_winner():
            self.switch_player()
            print(f"Congratulations! {self.current_player.get_name()} wins!")
        else:
            print("It's a tie!")

    def switch_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def get_valid_input(self, message):
        while True:
            try:
                user_input = int(input(message))
                if 0 <= user_input < self.board.get_board_size():
                    return user_input
                else:
                    print(f"Invalid input. Please enter a number between 0 and {self.board.get_board_size() - 1}")    
            except ValueError:
                print(f"Invalid input. Please enter a number between 0 and {self.board.get_board_size() - 1}")

class TicTacToeDemo:
    @staticmethod
    def run():
        player1 = Player("Alice", "X")
        player2 = Player("Bob", "O")
        game = Game(player1, player2)
        game.play()

if __name__ == "__main__":
    TicTacToeDemo.run()