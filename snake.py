from random import randint

class board():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.food = []

    def generate_food(self, amount: int = 1):
        for i in range(amount):
            x = randint(1, self.width-2)
            y = randint(1, self.height-2)
            self.food.append(food(x, y))

    def render(self, s):
        self.generate_food()

        # ! Temporary render function
        for i in range(self.height):
            for j in range(self.width):
                for f in self.food:
                    if i == f.y and j == f.x:
                        print('X', end='')
                        break
                if i == 0 or i == self.height-1:
                    print('-', end='')
                elif j == 0 or j == self.width-1:
                    print('|', end='')
                elif i == s.y and j == s.x:
                    print('O', end='')
                else:
                    print(' ', end='')
            print()
        # ! End of render function

    def clear(self):
        # ! Temporary clear function
        print('\033[H\033[J')

    def control(self, s):
        # ! Temporary control function
        direction = input('Enter direction: ')
        s.move(direction)

    def refresh(self, s):
        self.control(s)
        self.clear()
        self.render(s)


class body:
    def __init__(self, x, y, size=10):
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
    def __init__(self, x, y):
        super().__init__(x, y)
        self.length = 0
        self.last = []
        self.tail = []

    def move(self, direction: str, step: int = 1):
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

        if self.length > 0:
            self.last.append(self.get_pos())

        for i in range(self.length):
            self.tail[i].update(self.last[i][0], self.last[i][1])

    def grow(self):
        self.length += 1
        self.tail.append(body(self.last[-1][0], self.last[-1][1]))

    def check_collision(self, board: board) -> bool:
        if self.x < 0 or self.x >= board.width or self.y < 0 or self.y >= board.height:
            return True
        return False


if __name__ == '__main__':
    b = board(30, 20)
    s = snake(15, 10)

    b.render(s)

    while True:
        b.refresh(s)
        if s.check_collision(b):
            print('Game Over')
            break
