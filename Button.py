import pygame

pygame.init()


class Button:
    polygon = pygame.Surface((100, 40))
    image = polygon
    image = pygame.image.load("Sprites/Button.png")

    WHITE = (255, 255, 255)

    def __init__(self, pos, num):

        if num == 1:
            self.image = pygame.image.load("Sprites/1Button.png")
        elif num == 2:
            self.image = pygame.image.load("Sprites/2Button.png")
        elif num == 3:
            self.image = pygame.image.load("Sprites/3Button.png")
        elif num == 4:
            self.image = pygame.image.load("Sprites/4Button.png")

        self.num = num
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 100, 40)

    def draw_button(self, screen):
        pygame.Surface.blit(screen, self.image, (self.pos[0], self.pos[1]))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.num
            else:
                return 0
