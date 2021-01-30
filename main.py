import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# player has a board, boards have tiles, tiles have types

def turn(curr): #turn/round
    if curr == 1:
        board = playerOne.getBoard()

    else:
        board = playerTwo.getBoard()
    # drawPlayerBoard(board)


def draw_player_board(board):
    size = 100
    for x in range(0, 600, 100):
        for y in range(0, 600, 100):
            image = board[x / 100][y / 100]
            rect = pygame.Rect(x, y, size, size)
            pygame.draw.rect(screen, WHITE, rect, 1)
            screen.blit(image, rect)

def draw_tile_boards():
    num_tile = 0
    size = 100
    for x in range(600, 900, 100):
        for y in range(0, 300, 100):
            if num_tile != 7:
                image = tile_Boards.pop(num_tile)
                rect = pygame.Rect(x, y, size, size)
                pygame.draw.rect(screen, WHITE, rect, 1)
                screen.blit(image, rect)
                num_tile -= 1
            else:
                break




def select_tile(player):
    position = player.getPos()

    draw_tile_boards()

def main():
    global screen
    global currPlayer
    global playerOne, playerTwo
    global tile_Boards

    playerOne = Player()
    playerTwo = Player()
    # need to create new tile boards every 7 turns
    for i in range(7):
        tile_Boards.append(tileBoard())
    currPlayer = 1

    pygame.init()
    screen = pygame.display.set_mode((900, 900))
    screen.fill(BLACK)
    running = True
    while running:
        draw_player_board()
        draw_tile_boards()
        for event in pygame.event.get():
            if currPlayer == 1:
                # turn(currPlayer)
                currPlayer = 2
            if currPlayer == 2:
                # turn(currPlayer)
                currPlayer = 1
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()


main()
