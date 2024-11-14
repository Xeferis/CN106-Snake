from snake import snake, board

s = snake()

game = board(snake=s, points2win=100)

game.run()
