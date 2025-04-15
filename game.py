import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox,
    QLabel, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush
from PyQt5.QtCore import Qt, QTimer

class PremiumEmojiTicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌟 Premium Emoji Tic-Tac-Toe")
        self.setFixedSize(500, 500)  # Adjusted the window size for normal tile size

        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player = '❌'
        self.ai = '⭕'
        self.current_turn = self.player
        self.winning_line = []

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()

        # Status label
        self.status = QLabel("Your Turn ❌")
        self.status.setFont(QFont("Arial", 22, QFont.Bold))
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("color: white; margin: 20px;")
        left_layout.addWidget(self.status)

        # Game board with normal sized tiles (100x75)
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)  # Reduced spacing between tiles

        self.buttons = [[QPushButton("") for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                btn.setFixedSize(100, 75)  # Normal tile size of 100x75
                btn.setFont(QFont("Arial", 24, QFont.Bold))  # Adjusted font size for readability
                btn.setStyleSheet(self.premium_button_style())
                btn.clicked.connect(lambda _, r=i, c=j: self.player_move(r, c))
                self.grid_layout.addWidget(btn, i, j)
        
        left_layout.addLayout(self.grid_layout)

        # Restart button
        restart_btn = QPushButton("🔄 Restart Game")
        restart_btn.setFont(QFont("Arial", 14, QFont.Bold))
        restart_btn.setStyleSheet(self.premium_button_style())
        restart_btn.clicked.connect(self.reset_game)
        left_layout.addWidget(restart_btn)

        main_layout.addLayout(left_layout, 2)
        self.setLayout(main_layout)
        self.set_gradient_background()

    def premium_button_style(self):
        return """
            QPushButton {
                background-color: #b3e5fc;
                color: white;
                font-size: 24px;
                border-radius: 15px;
                border: 2px solid #64b5f6;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #64b5f6;
                border: 2px solid #b3e5fc;
                transform: scale(1.05);
            }
        """

    def set_gradient_background(self):
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#b3e5fc"))  # Light blue
        gradient.setColorAt(1.0, QColor("#64b5f6"))  # Slightly darker blue
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def player_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.player
            self.buttons[row][col].setText(self.player)
            self.buttons[row][col].setEnabled(False)
            self.status.setText("🤖 AI Thinking...")

            if self.check_winner(self.player):
                self.end_game("🎉 You Win!", self.player)
                return
            elif self.is_full():
                self.end_game("🤝 It's a draw!", None)
                return

            QTimer.singleShot(500, self.ai_move)

    def ai_move(self):
        row, col = self.best_move()
        if row is not None:
            self.board[row][col] = self.ai
            self.buttons[row][col].setText(self.ai)
            self.buttons[row][col].setEnabled(False)

            if self.check_winner(self.ai):
                self.end_game("💻 AI Wins!", self.ai)
            elif self.is_full():
                self.end_game("🤝 It's a draw!", None)
            else:
                self.status.setText("Your Turn ❌")

    def best_move(self):
        best_score = -math.inf
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.ai
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(self.ai, board):
            return 1
        elif self.check_winner(self.player, board):
            return -1
        elif self.is_full(board):
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = self.ai
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = self.player
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def is_full(self, board=None):
        if board is None:
            board = self.board
        return all(cell != ' ' for row in board for cell in row)

    def check_winner(self, player, board=None):
        if board is None:
            board = self.board
        lines = [
            [(0,0), (0,1), (0,2)],
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],
            [(0,0), (1,0), (2,0)],
            [(0,1), (1,1), (2,1)],
            [(0,2), (1,2), (2,2)],
            [(0,0), (1,1), (2,2)],
            [(0,2), (1,1), (2,0)],
        ]
        for line in lines:
            if all(board[i][j] == player for i, j in line):
                self.winning_line = line
                return True
        return False

    def end_game(self, message, winner):
        self.status.setText(message)
        if winner:
            for i, j in self.winning_line:
                self.buttons[i][j].setStyleSheet("""
                    QPushButton {
                        background-color: #66bb6a;
                        color: white;
                        border-radius: 15px;
                        font-size: 48px;
                    }
                """)
        for row in self.buttons:
            for btn in row:
                btn.setEnabled(False)
        QMessageBox.information(self, "Game Over", message)

    def reset_game(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.winning_line = []
        self.status.setText("Your Turn ❌")
        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                btn.setText("")
                btn.setEnabled(True)
                btn.setStyleSheet(self.premium_button_style())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PremiumEmojiTicTacToe()
    window.show()
    sys.exit(app.exec_())
