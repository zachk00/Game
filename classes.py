import pygame
import random

pygame.init()


class Building:

    def __init__(self, name):
        self.name = name
        self.isComplete = False


class Tile:

    # up, right, down, left

    def __init__(self, sides, image):
        self.image = pygame.Surface((50, 50))
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
    tiles = [[Tile([Building(""), Building(""), Building(""), Building("")], pygame.Surface((50, 50))) for i in
              range(0, 8)] for j in range(0, 8)]
    image = pygame.Surface((400, 400))

    def __init__(self):
        pass

    def checkPlacement(self, tile, x, y):
        for i in range(0, 4):
            if (i == 0):
                adjTile = self.tiles[x][y - 1]
            elif (i == 1):
                adjTile = self.tiles[x - 1][y]
            elif (i == 2):
                adjTile = self.tiles[x][y + 1]
            else:
                adjTile = self.tiles[x + 1][y]

            if (tile.sides[i].name != adjTile.sides[(i + 2) % 4].name and adjTile.sides[(i + 2) % 4].name != "") or \
                    self.tiles[x][y].sides[i].name != "":
                return False
        return True

    def placeTile(self, tile, x, y):
        if self.checkPlacement(tile, x, y):
            self.tiles[x][y] = tile
            self.image.blit(tile.image, (50 * x, 50 * y))

        else:
            print("illegal move")


    def hasCompleteHelper(self, x, y, avoid, prevName, output):
        l = [0, 1, 2, 3]
        l.remove(avoid)
        for i in l:
            if (i == 0):
                adjTile = self.tiles[x][y - 1]
            elif (i == 1):
                adjTile = self.tiles[x - 1][y]
            elif (i == 2):
                adjTile = self.tiles[x][y + 1]
            else:
                adjTile = self.tiles[x + 1][y]
            if self.tiles[x][y].sides[i].name != "grass" and self.tiles[x][y].sides[i].name == prevName and \
                    adjTile.sides[(i + 2) % 4].name != "":
                if (i == 0):
                    self.hasCompleteHelper(x, y - 1, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                elif (i == 1):
                    self.hasCompleteHelper(x - 1, y, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                elif (i == 2):
                    self.hasCompleteHelper(x, y + 1, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                else:
                    self.hasCompleteHelper(x + 1, y, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
            elif self.tiles[x][y].sides[i].name == prevName and adjTile.sides[
                (i + 2) % 4].name == "" and prevName in output:
                output.remove(prevName)

    def hasComplete(self, x, y):
        output = set()

        for i in range(0, 4):
            if self.tiles[x][y].sides[i].name != "grass":
                output.add(self.tiles[x][y].sides[i].name)
        for i in range(0, 4):
            if (i == 0):
                adjTile = self.tiles[x][y - 1]
            elif (i == 1):
                adjTile = self.tiles[x - 1][y]
            elif (i == 2):
                adjTile = self.tiles[x][y + 1]
            else:
                adjTile = self.tiles[x + 1][y]
            if self.tiles[x][y].sides[i].name != "grass" and adjTile.sides[(i + 2) % 4].name != "":
                if (i == 0):
                    self.hasCompleteHelper(x, y - 1, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                elif (i == 1):
                    self.hasCompleteHelper(x - 1, y, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                elif (i == 2):
                    self.hasCompleteHelper(x, y + 1, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
                else:
                    self.hasCompleteHelper(x + 1, y, (i + 2) % 4, self.tiles[x][y].sides[i].name, output)
            elif self.tiles[x][y].sides[i].name == self.tiles[x][y].sides[i].name and adjTile.sides[
                (i + 2) % 4].name == "" and self.tiles[x][y].sides[i].name in output:
                output.remove(self.tiles[x][y].sides[i].name)
        return output

    def buildingSizeHelper(self, x, y, avoid, name, sum):
        l = [0, 1, 2, 3]
        l.remove(avoid)

        for i in l:
            if (i == 0):
                adjTile = self.tiles[x][y - 1]
            elif (i == 1):
                adjTile = self.tiles[x - 1][y]
            elif (i == 2):
                adjTile = self.tiles[x][y + 1]
            else:
                adjTile = self.tiles[x + 1][y]
            if self.tiles[x][y].sides[i].name == name:
                if (i == 0):
                    sum = sum + self.buildingSizeHelper(x, y - 1, (i + 2) % 4, name, sum)
                elif (i == 1):
                    sum = sum + self.buildingSizeHelper(x - 1, y, (i + 2) % 4, name, sum)
                elif (i == 2):
                    sum = sum + self.buildingSizeHelper(x, y + 1, (i + 2) % 4, name, sum)
                else:
                    sum = sum + self.buildingSizeHelper(x + 1, y, (i + 2) % 4, name, sum)
        return sum + 1

    def buildingSize(self, x, y, name):
        sum = -1
        if name in self.hasComplete(x, y):
            sum = 0
            for i in range(0, 4):
                if (i == 0):
                    adjTile = self.tiles[x][y - 1]
                elif (i == 1):
                    adjTile = self.tiles[x - 1][y]
                elif (i == 2):
                    adjTile = self.tiles[x][y + 1]
                else:
                    adjTile = self.tiles[x + 1][y]
                if self.tiles[x][y].sides[i].name == name:
                    if (i == 0):
                        sum = sum + self.buildingSizeHelper(x, y - 1, (i + 2) % 4, name, 0)
                    elif (i == 1):
                        sum = sum + self.buildingSizeHelper(x - 1, y, (i + 2) % 4, name, 0)
                    elif (i == 2):
                        sum = sum + self.buildingSizeHelper(x, y + 1, (i + 2) % 4, name, 0)
                    else:
                        sum = sum + self.buildingSizeHelper(x + 1, y, (i + 2) % 4, name, 0)
        return sum + 1


class TileBoard:

    def __init__(self, tileList, pos):
        self.numOfTiles = 4
        self.image = pygame.Surface((100, 100))
        self.tiles = [[Tile([Building(""), Building(""), Building(""), Building("")], pygame.Surface((50, 50))) for i in
                       range(0, 2)] for j in range(0, 2)]
        self.pos = pos
        for i in [0, 1]:
            for j in [0, 1]:
                self.tiles[i][j] = tileList[random.randrange(0, len(tileList))]
                self.image.blit(self.tiles[i][j].image, (50 * i, 50 * j))
                self.numOfTiles = self.numOfTiles + 1

    def popTile(self, x, y):
        out = self.tiles[x][y]
        self.tiles[x][y] = Tile([Building("grass"), Building("grass"), Building("grass"), Building("grass")],
                                pygame.Surface((50, 50)))
        self.numOfTiles = self.numOfTiles - 1
        for i in [0, 1]:
            for j in [0, 1]:
                self.image.blit(self.tiles[i][j].image, (50 * i, 50 * j))
        return out


class Player:

    def __init__(self):
        self.stockpile = []
        self.score = 0
        self.board = PlayerBoard()
        self.pos = 1

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