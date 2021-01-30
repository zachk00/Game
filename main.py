import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# player has a board, boards have tiles, tiles have types




def drawPlayerBoard():
    tileSize = 20
    for x in range(20, 120, 20):
        for y in range(20, 120, 20):
            rect = pygame.Rect(x, y, tileSize, tileSize)
            pygame.draw.rect(screen, WHITE, rect, 1)


def main():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    screen.fill(BLACK)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.update()

main()