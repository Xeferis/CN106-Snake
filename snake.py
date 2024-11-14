import tkinter as tk
from random import randrange

class zone:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_start(self) -> tuple:
        return (self.x, self.y)

    def get_end(self) -> tuple:
        return (self.x + self.width, self.y + self.height)

    def render(self, canvas) -> None:
        canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="blue")

class board:
    def __init__(self, snake, width: int = 500, height: int = 500) -> None:
        # App init
        self.app = tk.Tk()
        self.app.title("Snake")
        self.app.resizable(False, False)
        self.app.configure(bg="black")
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.app, width=width, height=height)
        self.canvas.pack(padx=10, pady=10)
        self.deadzones = []

        self._add_deadzone(0, 0, 90, 30)
        self._add_deadzone(410, 0, 90, 30)

        # Game init
        start_x = width // 2
        start_y = height // 2

        self.snake = snake
        self.snake.update(start_x, start_y)

        self.level = 1
        self.speed = 100
        self.food = []
        self.points = 0
        self.won = False
        self.game_over = False

        # Gamesettings
        self.snake_head_color = "dark green"
        self.snakebody_color = "green"
        self.food_color = "red"

    def _add_deadzone(self, x: int, y: int, width: int, height: int) -> None:
        self.deadzones.append(zone(x, y, width, height))

    def _render_deadzones(self) -> None:
        # ? Render deadzones DEBUG
        for dz in self.deadzones:
            dz.render(self.canvas)

    def _check_deadzone(self, x: int, y: int) -> bool:
        for dz in self.deadzones:
            dzx, dzy = dz.get_start()
            dzx_end, dzy_end = dz.get_end()
            if dzx <= x <= dzx_end and dzy <= y <= dzy_end:
                return True
        return False
    
    def _check_food_position(self, x: int, y: int) -> bool:
        for f in self.food:
            if f.x == x and f.y == y:
                return True
        return False
    
    def _check_snake_position(self, x: int, y: int) -> bool:
        if self.snake.x == x and self.snake.y == y:
            return True
        return False

    def _progression(self) -> None:
        if self.points >= 30:
            self.won = True
        if self.points % 5 == 0 and self.points != 0:
            self.points += 6
            self.level += 1
            if self.speed > 10:
                self.speed -= 10

    def _generate_point(self, padding: int = 10, steps: int = 10) -> tuple:
        x = randrange(padding, self.width - padding, steps)
        y = randrange(padding, self.height - padding, steps)
        return (x, y)

    def _generate_food(self, amount: int = 2) -> None:
        print("Generating food")
        for i in range(amount):
            not_valid = True
            x, y = self._generate_point()

            if self._check_deadzone(x, y) or self._check_food_position(x, y) or self._check_snake_position(x, y):
                while not_valid:
                    x, y = self._generate_point()
                    if not self._check_deadzone(x, y) and not self._check_food_position(x, y) and not self._check_snake_position(x, y):
                        not_valid = False
            self.food.append(food(x, y))

    def _render_food(self) -> None:
        for f in self.food:
            self.canvas.create_oval(
                f.x, f.y, f.x + f.width, f.y + f.height, fill=self.food_color
            )

    def _render_snake(self) -> None:
        self.canvas.create_rectangle(
            self.snake.x,
            self.snake.y,
            self.snake.x + self.snake.width,
            self.snake.y + self.snake.height,
            fill=self.snake_head_color,
        )
        for t in self.snake.tail:
            self.canvas.create_rectangle(
                t.x, t.y, t.x + t.width, t.y + t.height, fill=self.snakebody_color
            )

    def _render_infos(self) -> None:
        self.canvas.create_text(10, 10, text=f"Points: {self.points}", anchor="nw", width=70)
        self.canvas.create_text(430, 10, text=f"Level: {self.level}", anchor="nw", width=70)

    def _render_gameOver(self) -> None:
        self.canvas.create_rectangle(0, 0, self.width+20, self.height+20, fill="black")
        self.canvas.create_text(
            self.width // 2, self.height // 2, text="Game Over", fill="red", font=("", 50)
        )

    def _render_gameWon(self) -> None:
        score_msg = f"Your Score: {self.points}"
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black")
        self.canvas.create_text(
            self.width // 2, self.height // 2, text="You Win", fill="green", font=("", 50)
        )
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 50, text=score_msg, fill="white", font=("", 20)
        )

    def _render(self) -> None:
        if self.game_over and not self.won:
            self._render_gameOver()
        elif self.won and not self.game_over:
            self._render_gameWon()
        else:
            self._render_infos()
            self._render_food()
            self._render_snake()

    def _clear(self) -> None:
        self.canvas.delete("all")

    def _control(self, event) -> None:
        direction = event.char
        if direction == "w":
            self.snake.direction = "u"
        elif direction == "s":
            self.snake.direction = "d"
        elif direction == "a":
            self.snake.direction = "l"
        elif direction == "d":
            self.snake.direction = "r"

    def _control_manual(self, event) -> None:
        direction = event.char
        if direction == "w":
            self.snake.move("u")
        elif direction == "s":
            self.snake.move("d")
        elif direction == "a":
            self.snake.move("l")
        elif direction == "d":
            self.snake.move("r")

    def _refresh(self) -> None:
        self._clear()
        self._progression()
        self.app.bind("<KeyPress>", lambda event: self.control(event))
        self.snake.move(self.snake.direction)
        self._check_collision()
        self._render()
        if not self.game_over:
            self.canvas.after(self.speed, self.refresh)

    def _wall_collision(self) -> bool:
        if (
            self.snake.x < 0
            or self.snake.x > self.width
            or self.snake.y < 0
            or self.snake.y > self.height
        ):
            return True
        return False

    def _tail_collision(self) -> bool:
        if self.snake.get_pos() in [t.get_pos() for t in self.snake.tail]:
            return True
        return False

    def _food_collision(self) -> bool:
        for f in self.food:
            if self.snake.get_pos() == f.get_pos():
                self.snake.grow()
                self.snake.last_food = f
                self.points += 1
                self.food.remove(f)
                return True
        return False

    def _check_collision(self) -> bool:
        if not self._food_collision():
            if self._wall_collision() or self._tail_collision():
                self.game_over = True
        else:
            self._generate_food(1)

    def run(self) -> None:
        self.app.lift()
        self._generate_food()
        self._refresh()
        self.app.mainloop()


class body:
    def __init__(self, x: int = 0, y: int = 0, size: int = 10) -> None:
        self.height = size
        self.width = size
        self.x = x
        self.y = y

    def update(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_pos(self) -> Tuple:
        return (self.x, self.y)


class food(body):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)


class snake(body):
    def __init__(self) -> None:
        super().__init__()
        self.length = 0
        self.last = []
        self.tail = []
        self.direction = None

    def move(self, direction: str, step: int = 10) -> None:
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

    def grow(self) -> None:
        self.length += 1
        self.tail.append(body(self.last[-1][0], self.last[-1][1]))

if __name__ == "__main__":
    s = snake()

    b = board(snake=s)

    b.run()
