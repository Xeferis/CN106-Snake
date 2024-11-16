import tkinter as tk
from random import randrange, choice


class zone:
    """Adding zones to the game board
    """
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_start(self) -> tuple:
        """Get the start position of the zone

        Returns:
            tuple: (x, y)
        """
        return (self.x, self.y)

    def get_end(self) -> tuple:
        """Get the end position of the zone

        Returns:
            tuple: (x, y)
        """
        return (self.x + self.width, self.y + self.height)

    def render(self, canvas) -> None:  # pragma: no cover
        """Render the zone on the canvas

        Args:
            canvas: The canvas to render the zone on
        """
        canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height, fill="blue"
        )


class board:
    """Game board
    """
    def __init__(
        self, snake, width: int = 500, height: int = 500, difficulty: int = 1
    ) -> None:
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
        self.running = False

        self._add_deadzone(0, 0, 90, 30)
        self._add_deadzone(410, 0, 90, 30)

        # Game init
        start_x = width // 2
        start_y = height // 2

        self.snake = snake
        self.snake.update(start_x, start_y)

        self.level = 1
        self.difficulty_info = self._set_difficulty(difficulty)
        self.food = []
        self.points = 0
        self.won = False
        self.game_over = False

        # Gamesettings
        self.snake_head_color = "dark green"
        self.snakebody_color = "green2"
        self.food_color = "red"

    def _set_difficulty(self, difficulty: int) -> None:
        """Set the difficulty of the game

        Args:
            difficulty (int): Difficulty of the game

        Returns:
            str: Difficulty name
        """
        if difficulty == 1:
            self.speed = 100
            self._speedincrease = 5
            self.points2win = 100
            return "Easy"
        elif difficulty == 2:
            self.speed = 100
            self._speedincrease = 10
            self.points2win = 100
            return "Normal"
        elif difficulty == 3:
            self.speed = 80
            self._speedincrease = 10
            self.points2win = 200
            return "Hard"
        elif difficulty == 4:
            self.speed = 10
            self._speedincrease = 1
            self.points2win = 500
            return "Insane"

    def _add_deadzone(self, x: int, y: int, width: int, height: int) -> None:
        """Add a deadzone to the game board

        Args:
            x (int): start x position
            y (int): start y position
            width (int): Zonewidth
            height (int): Zoneheight
        """
        self.deadzones.append(zone(x, y, width, height))

    def _render_deadzones(self) -> None:  # pragma: no cover
        """Render the deadzones on the canvas
        """
        # ? Render deadzones DEBUG
        for dz in self.deadzones:
            dz.render(self.canvas)

    def _check_deadzone(self, x: int, y: int) -> bool:
        """Check if a position is in a deadzone

        Args:
            x (int): Position x to check
            y (int): Position y to check

        Returns:
            bool: True if the position is in a deadzone
        """
        for dz in self.deadzones:
            dzx, dzy = dz.get_start()
            dzx_end, dzy_end = dz.get_end()
            if dzx <= x <= dzx_end and dzy <= y <= dzy_end:
                return True
        return False

    def _check_food_position(self, x: int, y: int) -> bool:
        """Check if a food is at a position

        Args:
            x (int): Position x to check
            y (int): Position y to check

        Returns:
            bool: True if a food is at the position
        """
        for f in self.food:
            if f.x == x and f.y == y:
                return True
        return False

    def _check_snake_position(self, x: int, y: int) -> bool:
        """Check if the snake is at a position

        Args:
            x (int): Position x to check
            y (int): Position y to check

        Returns:
            bool: True if the snake is at the position
        """
        if self.snake.x == x and self.snake.y == y:
            return True
        return False

    def _progression(self) -> None:
        """Progression calculation. Check if the player has won or leveled up
        """
        if self.points >= self.points2win:
            self.won = True
        if self.points % 5 == 0 and self.points != 0:
            self.points += 6
            self.level += 1
            if self.speed > self._speedincrease:
                self.speed -= self._speedincrease

    def _generate_point(self, padding: int = 10, steps: int = 10) -> tuple:
        """Generate a random point on the game board

        Args:
            padding (int, optional): Distance to Gameboard border. Defaults to 10.
            steps (int, optional): Step value of the render Grid. Defaults to 10.

        Returns:
            tuple: (x, y)
        """
        x = randrange(padding, self.width - padding, steps)
        y = randrange(padding, self.height - padding, steps)
        return (x, y)

    def _generate_food(self, amount: int = 2) -> None:
        """Generate food on the game board

        Args:
            amount (int, optional): Amount of food to generate. Defaults to 2.
        """
        for i in range(amount):
            not_valid = True
            x, y = self._generate_point()

            if (
                self._check_deadzone(x, y)
                or self._check_food_position(x, y)
                or self._check_snake_position(x, y)
            ):
                while not_valid:
                    x, y = self._generate_point()
                    if (
                        not self._check_deadzone(x, y)
                        and not self._check_food_position(x, y)
                        and not self._check_snake_position(x, y)
                    ):
                        not_valid = False
            self.food.append(food(x, y))

    def _render_food(self) -> None:  # pragma: no cover
        """Render the food on the canvas
        """
        for f in self.food:
            self.canvas.create_oval(
                f.x, f.y, f.x + f.width, f.y + f.height, fill=self.food_color
            )

    def _render_snake(self) -> None:  # pragma: no cover
        """Render the snake on the canvas
        """
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

    def _render_infos(self) -> None:  # pragma: no cover
        """Render the game infos on the canvas
        """
        text_width = 100
        text_height = 10
        padding = 10
        self.canvas.create_text(
            padding, text_height, text=f"Points: {self.points}", anchor="nw", width=text_width
        )
        self.canvas.create_text(
            self.width // 2, text_height, text=f"Speed: {self.speed} ms/f", anchor="n", width=text_width
        )
        self.canvas.create_text(
            self.width - text_width + 30 - padding, text_height, text=f"Level: {self.level}", anchor="nw", width=text_width-30
        )

    def _render_gameOver(self) -> None:  # pragma: no cover
        """Render the game over screen
        """
        self.running = False
        score_msg = f"Your Score: {self.points}"
        self.canvas.create_rectangle(
            0, 0, self.width + 20, self.height + 20, fill="black"
        )
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text="Game Over",
            fill="red",
            font=("", 50),
        )
        self.canvas.create_text(
            self.width // 2,
            self.height // 2 + 50,
            text=score_msg,
            fill="white",
            font=("", 20),
        )

    def _render_gameWon(self) -> None:  # pragma: no cover
        """Render the game won screen
        """
        self.running = False
        score_msg = f"Your Score: {self.points}"
        self.canvas.create_rectangle(
            0, 0, self.width + 20, self.height + 20, fill="black"
        )
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text="You Win",
            fill="green",
            font=("", 50),
        )
        self.canvas.create_text(
            self.width // 2,
            self.height // 2 + 50,
            text=score_msg,
            fill="white",
            font=("", 20),
        )

    def _render_start(self) -> None:  # pragma: no cover
        """Render the start screen
        """
        settings = f"Difficulty: {self.difficulty_info} - Points to win: {self.points2win}"
        settings2 = f"Speed: {self.speed} - Speedincrease: {self._speedincrease}"
        explain = "Use WASD to move the snake"

        text_low = [settings, settings2, explain]
        self.canvas.create_rectangle(
            0, 0, self.width + 20, self.height + 20, fill="black"
        )
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text="Press any key to start ...",
            font=("", 20),
        )

        for i, txt in enumerate(text_low):
            self.canvas.create_text(
                self.width // 2,
                self.height // 2 + 50 + i * 20,
                text=txt,
                font=("", 15),
            )

    def _render(self) -> None:  # pragma: no cover
        """Render the game
        """
        if not self.running:
            self._render_start()
        elif self.game_over and not self.won:
            self._render_gameOver()
        elif self.won and not self.game_over:
            self._render_gameWon()
        else:
            self._render_infos()
            self._render_food()
            self._render_snake()

    def _clear(self) -> None:  # pragma: no cover
        """Clear the canvas
        """
        self.canvas.delete("all")

    def _control(self, event) -> None:
        """Control the snake with the keyboard

        Args:
            event (tkinter.event): The event from the keyboard
        """
        direction = event.char
        if direction == "w":
            self.snake.direction = "u"
        elif direction == "s":
            self.snake.direction = "d"
        elif direction == "a":
            self.snake.direction = "l"
        elif direction == "d":
            self.snake.direction = "r"

    # ? For DEBUG
    def _control_manual(self, event) -> None:
        """DEBUG: Control the snake with the keyboard for singlesteps

        Args:
            event (tkinter.event): The event from the keyboard
        """
        direction = event.char
        if direction == "w":
            self.snake.move("u")
        elif direction == "s":
            self.snake.move("d")
        elif direction == "a":
            self.snake.move("l")
        elif direction == "d":
            self.snake.move("r")

    def _start_game(self) -> None:
        """Start the game. And set a random direction for the snake
        """
        possible_directions = ["u", "d", "l", "r"]
        self.running = True

        self.snake.direction = choice(possible_directions)

    def _refresh(self) -> None:  # pragma: no cover
        """Refresh the gamescreens
        """
        self._clear()
        self._progression()
        if not self.running:
            self.app.bind("<KeyPress>", lambda event: self._start_game())
        else:
            self.app.bind("<KeyPress>", lambda event: self._control(event))
            self.snake.move(self.snake.direction)
            self._check_collision()
        self._render()
        if not self.game_over and not self.won:
            self.canvas.after(self.speed, self._refresh)

    def _wall_collision(self) -> bool:
        """Check if the snake collided with a wall

        Returns:
            bool: True if the snake collided with a wall
        """
        if (
            self.snake.x < 0
            or self.snake.x > self.width
            or self.snake.y < 0
            or self.snake.y > self.height
        ):
            return True
        return False

    def _tail_collision(self) -> bool:
        """Check if the snake collided with its tail

        Returns:
            bool: True if the snake collided with its tail
        """
        if self.snake.get_pos() in [t.get_pos() for t in self.snake.tail]:
            return True
        return False

    def _food_collision(self) -> bool:
        """Check if the snake collided with food

        Returns:
            bool: True if the snake collided with food
        """
        for f in self.food:
            if self.snake.get_pos() == f.get_pos():
                self.snake.grow()
                self.snake.last_food = f
                self.points += 1
                self.food.remove(f)
                return True
        return False

    def _check_collision(self) -> None:
        """Check if the snake collided with something
        """
        if not self._food_collision():
            if self._wall_collision() or self._tail_collision():
                self.game_over = True
        else:
            self._generate_food(1)

    def run(self) -> None:  # pragma: no cover
        """Run the game
        """
        self.app.focus_force()
        self._generate_food()
        self._refresh()
        self.app.mainloop()


class body:
    """Body class for the snake and food
    """
    def __init__(self, x: int = 0, y: int = 0, size: int = 10) -> None:
        self.height = size
        self.width = size
        self.x = x
        self.y = y

    def update(self, x: int, y: int) -> None:
        """Update the position of the body

        Args:
            x (int): Position x to update to
            y (int): Position y to update to
        """
        self.x = x
        self.y = y

    def get_pos(self) -> tuple:
        """Get the position of the body

        Returns:
            tuple: (x, y)
        """
        return (self.x, self.y)


class food(body):
    """Food class for the game

    Args:
        body (class): Body class to inherit from
    """
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)


class snake(body):
    """Snake class for the game

    Args:
        body (_type_): Body class to inherit from
    """
    def __init__(self) -> None:
        super().__init__()
        self.length = 0
        self.last = []
        self.tail = []
        self.direction = None

    def move(self, direction: str, step: int = 10) -> None:
        """Move the snake

        Args:
            direction (str): Direction to move the snake into
            step (int, optional): Step value to move the snake should align with Grid of the board. Defaults to 10.

        Raises:
            ValueError: Invalid direction
        """
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
        """Grow the snakes tail
        """
        self.length += 1
        self.tail.append(body(self.last[-1][0], self.last[-1][1]))


if __name__ == "__main__":
    s = snake()

    b = board(snake=s, difficulty=1)

    b.run()
