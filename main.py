import pygame
import classes
import Button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw_player_board(board):
    size = 50
    image = board.image

    pygame.Surface.blit(screen, image, (0, 0))
    board_rects = []
    for x in range(8):
        for y in range(8):
            rect = pygame.Rect(x * 50, y * 50, size, size)
            pygame.draw.rect(screen, WHITE, rect, 1)
            board_rects.append(rect)
    return board_rects


def draw_tile_boards(boards):
    board_pos = 0

    for x in range(400, 800, 100):
        board = boards[board_pos]
        pygame.Surface.blit(screen, board.image, (x, 0))
        board_pos += 1
    for x in range(400, 700, 100):
        if board_pos != 7:
            board = boards[board_pos]
            pygame.Surface.blit(screen, board.image, (x, 100))
            board_pos += 1


def select_tile_placement(rects, event, pos):
    for rect in rects:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                index = player_board_index(pos)
                return 1, index[0], index[1]
    return 0, 0, 0


def player_board_index(pos):
    return pos[0] // 50, pos[1] // 50


def create_tile_boards():
    tile_boards = [classes.TileBoard(classes.tileList, i) for i in range(7)]

    return tile_boards


def init_buttons():
    buttons = []
    one = Button.Button((0, 500), 1)
    two = Button.Button((100, 500), 2)
    three = Button.Button((200, 500), 3)
    four = Button.Button((300, 500), 4)
    moveUp = Button.Button((600, 500), 5)
    moveDown = Button.Button((700, 500), 6)
    buttons.append(one)
    buttons.append(two)
    buttons.append(three)
    buttons.append(four)
    buttons.append(moveUp)
    buttons.append(moveDown)

    return buttons


def button_num_to_tile(num):
    if num == 1:
        return 0, 0
    elif num == 2:
        return 1, 0
    elif num == 3:
        return 0, 1
    else:
        return 1, 1


def draw_tile_selection(buttons, screen):
    for button in buttons:
        button.draw_button(screen)


def main():
    global screen
    global currPlayer
    global playerOne, playerTwo
    global tile_Boards
    global turnCounter
    global round
    needs_Move = True
    needs_Tile = False
    isScoringPhase = False

    turnCounter = 0
    round = 1
    currPlayer = 1
    rects = []
    button_num = 0
    tile = classes.Grass

    pygame.init()
    screen = pygame.display.set_mode((1600, 800))
    screen.fill(BLACK)
    running = True

    playerOne = classes.Player()
    playerTwo = classes.Player()
    tile_Boards = create_tile_boards()
    buttons = init_buttons()
    draw_tile_selection(buttons, screen)


    while running:
        if currPlayer == 1:
            rects = draw_player_board(playerOne.get_board())
       # else:
            #rects = draw_player_board(playerTwo.get_board())

        draw_tile_boards(tile_Boards)

        for event in pygame.event.get():

            if currPlayer == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in buttons:
                            button_num = button.handle_event(event)
                            if button_num == 5 :
                                playerOne.move("up")
                                needs_Move = False
                                needs_Tile = True
                            elif button_num :
                                playerOne.move("down")
                                needs_Move = False
                                needs_Tile = True
                            if 0 < button_num < 5:
                                needs_Tile = False
                                tile_board = tile_Boards[playerOne.pos]
                                tile = tile_board.popTile(button_num_to_tile(button_num)[0],
                                                          button_num_to_tile(button_num)[1])

                        placement = select_tile_placement(rects, event, pygame.mouse.get_pos())
                        if placement[0] == 1:
                            playerOne.board.placeTile(tile, placement[1], placement[2])
                            needs_Move = True
                            currPlayer = 1
                # if currPlayer == 2:


            if isScoringPhase:
                print("interesting")
                isScoringPhase = False
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()


main()
