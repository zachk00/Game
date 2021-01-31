
from random import random

import pygame
import random




class Building:
    name = ""
    isComplete = False

    def __init__(self, name):
        self.name = name


class Tile:
    sides = [Building(""), Building(""), Building(""), Building("")]
    # up, right, down, left
    polygon = pygame.Surface((100, 100))

    image = polygon

    def __init__(self, sides, image):
        self.sides = sides
        self.image = image

    def rotateTile(self, direction):
        newSides = [Building(""), Building(""), Building(""), Building("")]
        if direction == "right":
            self.image = pygame.transform.rotate(self.image, 270)
            for i in [0, 1, 2, 3]:
                newSides[(i + 1) % 4] = self.sides[i]
            self.sides = newSides
        elif direction == "left":
            self.image = pygame.transform.rotate(self.image, 90)
            for i in [0, 1, 2, 3]:
                newSides[i] = self.sides[(i + 1) % 4]
            self.sides = newSides


class PlayerBoard:
    tiles = [[Tile([Building(""), Building(""), Building(""), Building("")], pygame.Surface((100, 100))) for i in range(0,8)] for j in range(0,8)]
    image = pygame.Surface((800, 800))

    def __init__(self):
        pass

    def checkPlacement(self, tile, x, y):
        for i in range(0,4):
            if (i == 0):
                adjTile = self.tiles[x][y-1]
            elif (i == 1):
                adjTile = self.tiles[x-1][y]
            elif(i == 2):
                adjTile = self.tiles[x][y+1]
            else:
                adjTile = self.tiles[x+1][y]


            if (tile.sides[i].name != adjTile.sides[(i+2) % 4].name and adjTile.sides[(i+2) % 4].name != "") or self.tiles[x][y].sides[i].name != "":
                return False
        return True

    def placeTile(self, tile, x, y):
        if self.checkPlacement(tile,x,y):
            self.tiles[x][y] = tile
            self.image.blit(tile.image, (100 * x, 100 * y))
        else:
            print("illegal move")

    def hasCompleteHelper(self, x, y, avoid, prevName, output):
        l = [0,1,2,3]
        l.remove(avoid)
        for i in l:
            if (i == 0):
                adjTile = self.tiles[x][y-1]
            elif (i == 1):
                adjTile = self.tiles[x-1][y]
            elif(i == 2):
                adjTile = self.tiles[x][y+1]
            else:
                adjTile = self.tiles[x+1][y]
            if self.tiles[x][y].sides[i].name != "grass" and self.tiles[x][y].sides[i].name == prevName and adjTile.sides[(i+2) % 4].name != "":
                if (i == 0):
                    self.hasCompleteHelper(x, y-1, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                elif (i == 1):
                    self.hasCompleteHelper(x-1, y, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                elif (i == 2):
                    self.hasCompleteHelper(x, y+1, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                else:
                    self.hasCompleteHelper(x+1, y, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
            elif self.tiles[x][y].sides[i].name == prevName and adjTile.sides[(i+2) % 4].name == "" and prevName in output:
                output.remove(prevName)

    def hasComplete(self, x, y):
        output = set()

        for i in range(0,4):
            if self.tiles[x][y].sides[i].name != "grass":
                output.add(self.tiles[x][y].sides[i].name)
        for i in range(0,4):
            if (i == 0):
                adjTile = self.tiles[x][y-1]
            elif (i == 1):
                adjTile = self.tiles[x-1][y]
            elif(i == 2):
                adjTile = self.tiles[x][y+1]
            else:
                adjTile = self.tiles[x+1][y]
            if self.tiles[x][y].sides[i].name != "grass" and adjTile.sides[(i+2) % 4].name != "":
                if (i == 0):
                    self.hasCompleteHelper(x, y-1, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                elif (i == 1):
                    self.hasCompleteHelper(x-1, y, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                elif (i == 2):
                    self.hasCompleteHelper(x, y+1, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                else:
                    self.hasCompleteHelper(x+1, y, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
            elif self.tiles[x][y].sides[i].name == self.tiles[x][y].sides[i].name and adjTile.sides[(i+2) % 4].name == "" and self.tiles[x][y].sides[i].name in output:
                output.remove(self.tiles[x][y].sides[i].name)
        return output

class TileBoard:
    tiles = [[Tile([Building(""), Building(""), Building(""), Building("")], pygame.Surface((100, 100))) for i in range(0,2)] for j in range(0,2)]
    image = pygame.Surface((800, 800))
    numOfTiles = 0
    pos = 0

    def __init__(self, tileList, pos):
        self.pos = pos
        for i in [0,1]:
            for j in [0,1]:
                self.tiles[i][j] = tileList[random.randrange(0,len(tileList))]
                self.image.blit(self.tiles[i][j].image, (100 * i, 100 * j))
                self.numOfTiles = self.numOfTiles + 1

    def popTile(self, x, y):
        out = self.tiles[x][y]
        self.tiles[x][y] = Tile([Building(""), Building(""), Building(""), Building("")], pygame.Surface((100, 100)))
        self.numOfTiles = self.numOfTiles - 1
        for i in [0,1]:
            for j in [0,1]:
                self.image.blit(self.tiles[i][j].image, (100 * i, 100 * j))
        return out



class Player:
    stockpile = []
    score = 0
    x = 0
    y = 0
    board = PlayerBoard()
    pos = 1

    def __init__(self):
        pass

    def move(self, direction):
        if direction == 'up':
            if self.pos == 7:
                self.pos = 1
            else:
                self.pos += 1
        else:
            if self.pos == 1:
                self.pos = 7
            else:
                self.pos -= 1

    def get_board(self):
        return self.board

    def get_pos(self):
        return self.pos

class ScoreCard:


    def __init__(self):
        pass

screen = pygame.display.set_mode((800, 600))

running = True
rectangle = pygame.Rect(100, 100, 100, 100)

screenLayer = pygame.Surface((100, 100))
pygame.draw.polygon(screenLayer, pygame.Color(00, 100, 00), [(100, 100), (0, 100), (0, 0), (100, 0)])

tile1 = Tile([Building("grass"), Building("grass"), Building("blue"), Building("grass")], pygame.image.load("testImage.png"))
tile2 = Tile([Building("blue"), Building("grass"), Building("blue"), Building("grass")], pygame.image.load("testImage2.png"))
tile3 = Tile([Building("grass"), Building("grass"), Building("blue"), Building("grass")], pygame.image.load("testImage.png"))

board = PlayerBoard()

for i in [1,4] :
    for j in [1] :
        board.placeTile(tile1, i, j)


board.placeTile(tile2,1,2)

tile3.rotateTile("left")
tile3.rotateTile("left")

board.placeTile(tile3,1,3)
board.placeTile(tile3,1,3)


a = board.hasComplete(1,3)
print(a)

b = TileBoard([tile1,tile2], 0)
b.popTile(0, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screenLayer = pygame.Surface((800, 800))

    pygame.Surface.blit(screen, b.image, (0, 0))

    pygame.display.update()
    pygame.time.delay(10)

