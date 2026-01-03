import tkinter as tk

class PongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Ping Pong")

        self.width = 600
        self.height = 400
        self.ball_speed_x = 2
        self.ball_speed_y = 2
        self.paddle_speed = 20
        self.game_over = False

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        
        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill="white")
        self.left_paddle = self.canvas.create_rectangle(10, 150, 25, 250, fill="blue")
        self.right_paddle = self.canvas.create_rectangle(575, 150, 590, 250, fill="red")

        self.root.bind("<w>", lambda e: self.move_paddle(self.left_paddle, -self.paddle_speed))
        self.root.bind("<s>", lambda e: self.move_paddle(self.left_paddle, self.paddle_speed))
        self.root.bind("<Up>", lambda e: self.move_paddle(self.right_paddle, -self.paddle_speed))
        self.root.bind("<Down>", lambda e: self.move_paddle(self.right_paddle, self.paddle_speed))

        self.update_game()

    def move_paddle(self, paddle, distance):
        coords = self.canvas.coords(paddle)
        if (coords[1] + distance >= 0) and (coords[3] + distance <= self.height):
            self.canvas.move(paddle, 0, distance)

    def update_game(self):
        if self.game_over:
            return

        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
        ball_pos = self.canvas.coords(self.ball)

        winner = self.check_corner(ball_pos)
        if winner:
            self.end_game(winner)
            return

        if ball_pos[1] <= 0 or ball_pos[3] >= self.height:
            self.ball_speed_y *= -1

        if self.check_collision(ball_pos, self.left_paddle) or self.check_collision(ball_pos, self.right_paddle):
            self.ball_speed_x *= -1

        if ball_pos[0] <= 0 or ball_pos[2] >= self.width:
            self.canvas.coords(self.ball, 290, 190, 310, 210)
            self.ball_speed_x *= -1

        self.root.after(10, self.update_game)

    def check_corner(self, ball_pos):
        if ball_pos[0] <= 0 and ball_pos[1] <= 0:
            return "Blue"

        if ball_pos[0] <= 0 and ball_pos[3] >= self.height:
            return "Blue"

        if ball_pos[2] >= self.width and ball_pos[1] <= 0:
            return "Red"

        if ball_pos[2] >= self.width and ball_pos[3] >= self.height:
            return "Red"

    def end_game(self, winner):
        self.canvas.create_text(
            self.width / 2,
            self.height / 2,
            font=("Arial", 30),
            text="{winner} WINS!"
        )
        self.game_over = True

    def check_collision(self, ball_pos, paddle):
        paddle_pos = self.canvas.coords(paddle)
        if ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2]:
            if ball_pos[3] >= paddle_pos[1] and ball_pos[1] <= paddle_pos[3]:
                return True
        return False


if __name__ == "__main__":
    game_root = tk.Tk()
    app = PongGame(game_root)
    game_root.mainloop()

#Add on to this game - if the ball touches one of the corners, then the game ends
#And one player is declared the winner - red or blue