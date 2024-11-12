import tkinter as tk
from random import randrange

class board():
    def __init__(self, snake, width: int = 500, height: int = 500):
        self.app = tk.Tk()
        self.app.title('Snake')
        self.speed = 100
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.app, width=width+5, height=height+5)
        self.food = []
        self.canvas.pack()

        self.snake = snake

        self.snake.x = width // 2
        self.snake.y = height // 2

        self.food_color = 'red'

    def generate_food(self, amount: int = 2):
        print('Generating food')
        for i in range(amount):
            x = randrange(0, self.width, 10)
            y = randrange(0, self.height, 10)
            self.food.append(food(x, y))

    def render_food(self):
        for f in self.food:
            self.canvas.create_oval(f.x, f.y, f.x + f.width, f.y + f.height, fill=self.food_color)

    def render_snake(self):
        self.canvas.create_rectangle(self.snake.x, self.snake.y, self.snake.x + self.snake.width, self.snake.y+ self.snake.height, fill='green')
        for t in self.snake.tail:
            self.canvas.create_rectangle(t.x, t.y, t.x + t.width, t.y + t.height, fill='green')

    def render(self):
        self.render_food()
        self.render_snake()

    def clear(self):
        self.canvas.delete('all')

    def control(self, event):
        direction = event.char
        if direction == 'w':
            self.snake.move('u')
        elif direction == 's':
            self.snake.move('d')
        elif direction == 'a':
            self.snake.move('l')
        elif direction == 'd':
            self.snake.move('r')

    def refresh(self):
        print(self.snake.get_pos())
        self.app.bind("<KeyPress>", lambda event: self.control(event))
        self.clear()
        self.render()
        self.check_collision()
        self.canvas.after(self.speed, self.refresh)

    def check_collision(self):
        for f in self.food:
            if self.snake.x == f.x and self.snake.y == f.y:
                self.snake.grow()
                self.food.remove(f)
                self.generate_food(1)

        if self.snake.x < 0 or self.snake.x > self.width or self.snake.y < 0 or self.snake.y > self.height:
            print('Game Over')
            self.app.destroy()

    def run(self):
        self.generate_food()
        self.refresh()
        self.app.mainloop()


class body:
    def __init__(self, x = 0, y = 0, size=10):
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

    def move(self, direction: str, step: int = 10):
        if direction == 'u':
            self.y -= step
        elif direction == 'd':
            self.y += step
        elif direction == 'l':
            self.x -= step
        elif direction == 'r':
            self.x += step
        else:
            raise ValueError('Invalid direction')

        if self.length >= 0:
            self.last.append(self.get_pos())

        for i in range(self.length):
            self.tail[i].update(self.last[i][0], self.last[i][1])

    def grow(self):
        self.length += 1
        self.tail.append(body(self.last[-1][0], self.last[-1][1]))


if __name__ == '__main__':
    s = snake()

    b = board(snake=s)

    b.run()

    
