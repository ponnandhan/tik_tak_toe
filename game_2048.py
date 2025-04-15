import tkinter as tk
import random
import time

SIZE = 4
TILE_COLORS = {
    0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
    16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
    128: "#edcf72", 256: "#edcc61", 512: "#edc850",
    1024: "#edc53f", 2048: "#edc22e"
}

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.won = False

        # Create canvas for drawing tiles
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="#bbada0")
        self.canvas.pack(pady=10)

        # Score and highscore labels
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.pack()
        self.highscore_label = tk.Label(self.root, text="High Score: 0", font=("Helvetica", 16))
        self.highscore_label.pack()

        self.setup_game()
        self.root.bind("<Key>", self.key_handler)

    def setup_game(self):
        # Reset board and score
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.won = False
        self.add_tile()
        self.add_tile()
        self.update_ui()

    def add_tile(self):
        empty = [(i, j) for i in range(SIZE) for j in range(SIZE) if self.board[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def update_ui(self):
        # Update score display
        self.score_label.config(text=f"Score: {self.score}")
        
        # Clear canvas and redraw tiles
        self.canvas.delete("all")

        # Draw grid and tiles
        for i in range(SIZE):
            for j in range(SIZE):
                value = self.board[i][j]
                x1 = j * 100 + 10
                y1 = i * 100 + 10
                x2 = x1 + 80
                y2 = y1 + 80
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=TILE_COLORS.get(value, "#3c3a32"), outline="black", width=2)
                if value != 0:
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(value), font=("Helvetica", 24), fill="black")

    def key_handler(self, event):
        key = event.keysym
        moved = False

        if key == "Left":
            moved = self.move_left()
        elif key == "Right":
            moved = self.move_right()
        elif key == "Up":
            moved = self.move_up()
        elif key == "Down":
            moved = self.move_down()

        if moved:
            self.add_tile()
            self.update_ui()
            if self.is_game_over():
                self.show_popup("Game Over!")

    def move_left(self):
        moved = False
        for i in range(SIZE):
            original = self.board[i][:]
            new = self.merge(self.compress(self.board[i]))
            if new != original:
                moved = True
            self.board[i] = new
        return moved

    def move_right(self):
        moved = False
        for i in range(SIZE):
            original = self.board[i][:]
            new = list(reversed(self.merge(self.compress(reversed(self.board[i])))))
            if new != original:
                moved = True
            self.board[i] = new
        return moved

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_up(self):
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self):
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return self.compress(row)

    def is_game_over(self):
        temp = [row[:] for row in self.board]
        if any([
            self.move_left(), self.move_right(),
            self.move_up(), self.move_down()
        ]):
            self.board = temp
            return False
        return True

    def show_popup(self, message):
        popup = tk.Toplevel()
        popup.title(message)
        tk.Label(popup, text=message, font=("Helvetica", 20)).pack(pady=10)
        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=5)

    # Smooth Tile Animation
    def move_tiles(self, old_positions, new_positions, speed=10):
        """
        Smoothly moves the tiles from old_positions to new_positions
        """
        steps = 10  # Number of steps to animate
        for step in range(steps + 1):
            for i in range(len(old_positions)):
                old_pos = old_positions[i]
                new_pos = new_positions[i]
                if old_pos != new_pos:
                    # Calculate intermediate position
                    delta_x = (new_pos[0] - old_pos[0]) * step / steps
                    delta_y = (new_pos[1] - old_pos[1]) * step / steps
                    x1, y1, x2, y2 = old_pos
                    # Move the tile gradually using canvas
                    self.canvas.coords(self.tiles[i], x1 + delta_x, y1 + delta_y, x2 + delta_x, y2 + delta_y)
            self.canvas.update()
            self.root.after(speed)

    def update_ui_with_animation(self):
        # Clear canvas and redraw tiles
        self.canvas.delete("all")

        # Store tile's initial positions for animation
        old_positions = []
        new_positions = []

        # Draw grid and tiles and save their positions
        for i in range(SIZE):
            for j in range(SIZE):
                value = self.board[i][j]
                x1 = j * 100 + 10
                y1 = i * 100 + 10
                x2 = x1 + 80
                y2 = y1 + 80
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=TILE_COLORS.get(value, "#3c3a32"), outline="black", width=2)

                if value != 0:
                    tile = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(value), font=("Helvetica", 24), fill="black")
                    old_positions.append((x1, y1, x2, y2))
                    new_positions.append((x1, y1, x2, y2))
                    self.tiles = self.tiles + [tile] if not hasattr(self, 'tiles') else [tile]

        # Call the smooth tile animation
        self.move_tiles(old_positions, new_positions)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
