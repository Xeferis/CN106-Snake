import tkinter as tk
from random import randrange


class board:
    def __init__(self, snake, width: int = 500, height: int = 500):
        # App init
        self.app = tk.Tk()
        self.app.title("Snake")
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.app, width=width, height=height)
        self.canvas.pack()

        # Game init
        start_x = width // 2
        start_y = height // 2

        self.snake = snake
        self.snake.update(start_x, start_y)

        self.level = 1
        self.speed = 100
        self.food = []
        self.points = 0
        self.game_over = False

        # Gamesettings
        self.food_color = "red"

    def progression(self):
        if self.points % 5 == 0 and self.points != 0:
            self.points += 6
            self.level += 1
            if self.speed > 10:
                self.speed -= 10

    def generate_food(self, amount: int = 2):
        print("Generating food")
        for i in range(amount):
            x = randrange(10, self.width-10, 10)
            y = randrange(10, self.height-10, 10)
            self.food.append(food(x, y))

    def render_food(self):
        for f in self.food:
            self.canvas.create_oval(
                f.x, f.y, f.x + f.width, f.y + f.height, fill=self.food_color
            )

    def render_snake(self):
        self.canvas.create_rectangle(
            self.snake.x,
            self.snake.y,
            self.snake.x + self.snake.width,
            self.snake.y + self.snake.height,
            fill="green",
        )
        for t in self.snake.tail:
            self.canvas.create_rectangle(
                t.x, t.y, t.x + t.width, t.y + t.height, fill="green"
            )

    def render_infos(self):
        self.canvas.create_text(10, 10, text=f"Points: {self.points}", anchor="nw")
        self.canvas.create_text(10, 20, text=f"Level: {self.level}", anchor="nw")

    def render(self):
        self.render_infos()
        self.render_food()
        self.render_snake()

    def clear(self):
        self.canvas.delete("all")

    def control(self, event):
        direction = event.char
        if direction == "w":
            self.snake.direction = "u"
        elif direction == "s":
            self.snake.direction = "d"
        elif direction == "a":
            self.snake.direction = "l"
        elif direction == "d":
            self.snake.direction = "r"

    def control_manual(self, event):
        direction = event.char
        if direction == "w":
            self.snake.move("u")
        elif direction == "s":
            self.snake.move("d")
        elif direction == "a":
            self.snake.move("l")
        elif direction == "d":
            self.snake.move("r")

    def refresh(self):
        self.clear()
        self.progression()
        self.app.bind("<KeyPress>", lambda event: self.control(event))
        self.snake.move(self.snake.direction)
        self.check_collision()
        self.render()
        if not self.game_over:
            self.canvas.after(self.speed, self.refresh)

    def wall_collision(self):
        if (
            self.snake.x < 0
            or self.snake.x > self.width
            or self.snake.y < 0
            or self.snake.y > self.height
        ):
            return True
        return False

    def tail_collision(self):
        # ! Tail collition not working with jsut one Tail yet
        if self.snake.get_pos() in [t.get_pos() for t in self.snake.tail]:
            return True
        return False

    def food_collision(self):
        for f in self.food:
            if self.snake.get_pos() == f.get_pos():
                self.snake.grow()
                self.snake.last_food = f
                self.points += 1
                self.food.remove(f)
                return True
        return False

    def check_collision(self):
        if not self.food_collision():
            if self.wall_collision() or self.tail_collision():
                self.gameOver()
        else:
            self.generate_food(1)

    def gameOver(self):
        print("Game Over")
        self.canvas.create_text(
            self.width // 2, self.height // 2, text="Game Over", fill="red"
        )
        self.game_over = True

    def gameWon(self):
        print("You Win")
        self.canvas.create_text(
            self.width // 2, self.height // 2, text="You Win", fill="green"
        )
        self.game_over = True

    def run(self):
        self.generate_food()
        self.refresh()
        self.app.mainloop()


class body:
    def __init__(self, x=0, y=0, size=10):
        self.height = size
        self.width = size
        self.x = x
        self.y = y

    def update(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y


class food(body):
    def __init__(self, x, y):
        super().__init__(x, y)


class snake(body):
    def __init__(self):
        super().__init__()
        self.length = 0
        self.last = []
        self.tail = []
        self.direction = None

    def move(self, direction: str, step: int = 10):
        if self.length >= 0:
            if len(self.last) > self.length:
                self.last.pop(0)
            self.last.append(self.get_pos())

        if direction == "u":
            self.y -= step
        elif direction == "d":
            self.y += step
        elif direction == "l":
            self.x -= step
        elif direction == "r":
            self.x += step
        elif direction is None:
            print("press wasd to move")
        else:
            raise ValueError("Invalid direction")

        for i in range(self.length):
            self.tail[i].x = self.last[i][0]
            self.tail[i].y = self.last[i][1]

    def grow(self):
        self.length += 1
        self.tail.append(body(self.last[-1][0], self.last[-1][1]))

if __name__ == "__main__":
    s = snake()

    b = board(snake=s)

    b.run()
