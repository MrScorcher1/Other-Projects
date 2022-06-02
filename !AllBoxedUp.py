import pygame
import sys
from copy import deepcopy
import os
from Grids import *
from Button import *
from enum import IntEnum

pygame.init()

screen_size = width, height = (800, 600)
display_surface = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

buttonImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Red Button 2.png"))
boxImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Box.png"))
doorImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Exit Door.png"))
retryImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Retry Symbol.png"))
undoImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Undo Symbol.png"))
holeImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Hole 3.png"))
playerImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Player.png"))

smallBoldFont = pygame.font.SysFont("comicsansms", 30, True)
smallerBoldFont = pygame.font.SysFont("comicsansms", 36, True)
boldFont = pygame.font.SysFont("comicsansms", 50, True)
bigBoldFont = pygame.font.SysFont("comicsansms", 100, True)

retryButton = Button(width-60, 10, 50, 50, None, None)
undoButton = Button(width-60, 70, 50, 50, None, None)
playLevelsButton = Button(width//2 - 175, height//2 - 50, 350, 85, None, "Normal Levels")
playButton = Button((width//2 - 175), (height//2 - 50), 350, 85, None, "Play")
playAgainButton = Button(width//2 - 365, height//2 + 70, 350, 85, None, "Play Again")
menuButton = Button(width//2 - 175, height//2 + 180, 350, 85, None, "Main Menu")
bonusLevelsButton = Button(width//2 - 175, height//2 + 50, 350, 85, None, "Bonus Levels")
bonusLevelsButton2 = Button(width//2 + 15, height//2 + 70, 350, 85, None, "Bonus Levels")
levelsButton = Button(width//2 - 175, height//2 + 50, 350, 85, None, "Levels")
quitButton = Button((width//2 - 175), (height//2 + 150), 350, 85, None, "Quit")
levelButton = None

color = {'Red': (255, 0, 0),
         'Orange': (255, 120, 0),
         'Yellow': (255, 255, 0),
         'Green': (0, 180, 0),
         'Blue': (0, 0, 255),
         'Indigo': (75, 0, 130),
         'Pink': (255, 23, 197),
         'Purple': (238, 130, 238),
         'Grey': (128, 128, 128),
         'Light_Grey': (220, 220, 220),
         'Dark_Grey': (70, 70, 70),
         'Brown': (125, 70, 20),
         'White': (255, 255, 255),
         'Black': (0, 0, 0)
         }

retryButton.show(display_surface, color['Green'], boldFont, color['Black'])
retryImage = pygame.transform.smoothscale(retryImage, (retryButton.w + 4, retryButton.h + 4))

undoButton.show(display_surface, color['Green'], boldFont, color['Black'])
undoImage = pygame.transform.smoothscale(undoImage, (retryButton.w - 8, retryButton.h - 8))

fileName = open("levels.txt", "r")
farthestLevel = int(fileName.read())
level = farthestLevel


class GameMode(IntEnum):
    MENU = 1
    PLAY_MENU = 2
    PLAY = 3
    GAME_OVER = 4
    PAUSE = 5
    LEVEL_MENU = 6


gameState = GameMode.MENU

grid = deepcopy(grids[level])
originalGrids = deepcopy(grids)
previousGrids = []
previousGrid = -1
numRows = len(grid)
numCols = len(grid[0])
exitPos = 0, 0
playerPos = 0, 0
levelInterval = 0
complete = False

print(grid)
print(numRows)
print(numCols)
square_width = width // numCols
square_height = height // numRows


class Player:
    def __init__(self, pos, levelGrid):
        self.pos = pos
        self.grid = levelGrid
        self.previousPos = pos


def restartLevel(): 
    grid = deepcopy(grids[level])
    print(grid)
    print("Grid:", grids[level])
    nextLevel()


def nextLevel():
    global goalPos, square_width, square_height, numRows, numCols, onButton, previousGrids, farthestLevel
    print(grid)
    numRows = len(grid)
    numCols = len(grid[0])
    square_width = width // numCols
    square_height = height // numRows
    goalPos = []
    onButton = []
    previousGrids = []
    if level > farthestLevel:
        fileName = open("levels.txt", "w")
        fileName.write(str(level))
        farthestLevel = level


def showTiles(tiles):
    global playerPos
    global exitPos
    global square_width, square_height
    global buttonImage, boxImage, doorImage, holeImage, playerImage
    square_width = width // len(tiles[0])
    square_height = height// len(tiles)
    for y, row in enumerate(tiles):
        for x in range(0, len(tiles[0])):
            tileNum = tiles[y][x]
            tileColor = color["White"]

            if tileNum == 0:
                tileColor = color["Black"]

            elif tileNum == 1:
                tileColor = color["Dark_Grey"]

            elif tileNum == 5:
                tileColor = color["Purple"]

            rect = pygame.Rect(x * square_width, y * square_height, square_width, square_height).inflate(-2, -2)
            pygame.draw.rect(display_surface, tileColor, rect)

            if tileNum == 3:
                boxImageRect = boxImage.get_rect()
                if boxImageRect.width != square_width or boxImageRect.height != square_height:
                    boxImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Box.png"))
                    boxImage = pygame.transform.smoothscale(boxImage, (square_width, square_height))
                boxImageRect.center = (x * square_width + square_width // 2, y * square_height + square_height // 2)
                display_surface.blit(boxImage, boxImageRect)

            elif tileNum == 7:
                buttonImageRect = buttonImage.get_rect()
                if buttonImageRect.width != square_width or buttonImageRect.height != square_height:
                    buttonImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Red Button 2.png"))
                    buttonImage = pygame.transform.smoothscale(buttonImage, (square_width, square_height))
                buttonImageRect.center = (x * square_width + square_width//2, y * square_height + square_height//2)
                display_surface.blit(buttonImage, buttonImageRect)

            elif tileNum == 6:
                exitPos = x, y
                grid[y][x] = 0
                doorImageRect = doorImage.get_rect()
                if doorImageRect.width != square_width or doorImageRect.height != square_height:
                    doorImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Exit Door.png"))
                    doorImage = pygame.transform.smoothscale(doorImage, (square_width, square_height))
                doorImageRect.center = (x * square_width + square_width//2, y * square_height + square_height//2)
                display_surface.blit(doorImage, doorImageRect)

            elif tileNum == 2:
                holeImageRect = holeImage.get_rect()
                if holeImageRect.width != square_width or holeImageRect.height != square_height:
                    holeImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Hole 3.png"))
                    holeImage = pygame.transform.smoothscale(holeImage, (square_width, square_height))
                holeImageRect.center = (x * square_width + square_width // 2, y * square_height + square_height // 2)
                display_surface.blit(holeImage, holeImageRect)

            elif tileNum == 4:
                playerPos = x, y
                playerImageRect = playerImage.get_rect()
                if playerImageRect.width != square_width or playerImageRect.height != square_height:
                    playerImage = pygame.image.load(os.path.join("AllBoxedUpAssets/Player.png"))
                    playerImage = pygame.transform.smoothscale(playerImage, (square_width, square_height))
                playerImageRect.center = (x * square_width + square_width // 2, y * square_height + square_height // 2)
                display_surface.blit(playerImage, playerImageRect)


add1 = False
onButton = []
newPos = 0
goalPos = []
levelButtons = []
player = Player(playerPos, grid)
clock = pygame.time.Clock()
while True:
    # force a frame rate of 60 fps
    clock.tick(60)
    # get the mouse position each frame
    mouseX, mouseY = pygame.mouse.get_pos()
    # check the events, and if the QUIT event occurs, close the window
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if gameState != GameMode.MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameState = GameMode.MENU
                    nextLevel()
                    grids = deepcopy(originalGrids)
                    grid = deepcopy(grids[farthestLevel])

        if gameState == GameMode.MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if playButton.hovered(mouseX, mouseY):
                    if not complete:
                        gameState = GameMode.PLAY
                        grid = deepcopy(grids[farthestLevel])
                    else:
                        gameState = GameMode.PLAY_MENU
                        print(farthestLevel)
                        grid = deepcopy(grids[farthestLevel])
                        break
                if levelsButton.hovered(mouseX, mouseY):
                    gameState = GameMode.LEVEL_MENU
                    print(farthestLevel)
                    grid = deepcopy(grids[farthestLevel])
                if quitButton.hovered(mouseX, mouseY):
                    sys.exit()

        if gameState == GameMode.LEVEL_MENU:
            for button in range(len(levelButtons)):
                levelText = int(levelButtons[button].text) - 1
                if levelButtons[button].hovered(mouseX, mouseY):
                    grid = deepcopy(grids[levelText])

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if levelButtons[button].hovered(mouseX, mouseY):
                        if (levelText <= level or complete) and levelText in range(levelInterval, levelInterval + 10):
                            level = int(levelButtons[button].text) - 1
                            grid = deepcopy(grids[level])
                            gameState = GameMode.PLAY

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and levelInterval + 20 <= len(grids):
                    levelInterval += 10

                if event.key == pygame.K_UP and levelInterval - 10 >= 0:
                    levelInterval -= 10

        if gameState == GameMode.PLAY_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if playLevelsButton.hovered(mouseX, mouseY):
                    gameState = GameMode.PLAY
                    grids = deepcopy(originalGrids)
                    grid = deepcopy(grids[farthestLevel])
                    level = farthestLevel
                if bonusLevelsButton.hovered(mouseX, mouseY):
                    gameState = GameMode.PLAY
                    grids = deepcopy(bonusGrids)
                    level = 0
                    grid = deepcopy(grids[level])
                    nextLevel()

        if gameState == GameMode.PLAY:

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if retryButton.hovered(mouseX, mouseY):
                    grid = deepcopy(grids[level])
                    nextLevel()

                if undoButton.hovered(mouseX, mouseY):
                    previousGrid = len(previousGrids) - 1
                    if previousGrid >= 0:
                        grid = deepcopy(previousGrids[previousGrid])
                        previousGrids.remove(grid)

            # give the option to close the window with ESC
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    grid = deepcopy(grids[level])
                    print(grid)
                    print("Grid:", grids[level])
                    nextLevel()

                if event.key == pygame.K_z:
                    previousGrid = len(previousGrids) - 1
                    if previousGrid >= 0:
                        grid = deepcopy(previousGrids[previousGrid])
                        previousGrids.remove(grid)

                if event.key in {pygame.K_d, pygame.K_RIGHT} and playerPos[0] < numCols - 1:
                    if grid[player.pos[1]][player.pos[0] + 1] != 1 and grid[player.pos[1]][player.pos[0] + 1] != 2:
                        if (grid[player.pos[1]][player.pos[0] + 1] == 3 and playerPos[0] < numCols - 2 and (grid[player.pos[1]][player.pos[0] + 2] != 1 and grid[player.pos[1]][player.pos[0] + 2] != 3)) or grid[player.pos[1]][player.pos[0] + 1] != 3:
                            previousGrids.append(deepcopy(grid))

                        if grid[player.pos[1]][player.pos[0] + 1] == 7:
                            onButton.append((playerPos[0] + 1, playerPos[1]))

                        if grid[player.pos[1]][player.pos[0] + 1] == 6:
                            print("Level Complete!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            if level < len(grids) - 1:
                                level += 1
                                grid = deepcopy(grids[level])
                                nextLevel()
                                continue
                            else:
                                complete = True
                                farthestLevel = 0
                                level = farthestLevel
                                nextLevel()
                                gameState = GameMode.GAME_OVER
                        if grid[player.pos[1]][player.pos[0] + 1] == 0 or grid[player.pos[1]][player.pos[0] + 1] == 5 or grid[player.pos[1]][player.pos[0] + 1] == 7:
                            player.previousPos = player.pos
                            grid[player.pos[1]][player.pos[0] + 1] = 4
                            grid[player.previousPos[1]][player.previousPos[0]] = 0
                        elif grid[player.pos[1]][player.pos[0] + 1] == 3 and playerPos[0] < numCols - 2 and grid[player.pos[1]][player.pos[0] + 2] != 1 and grid[player.pos[1]][player.pos[0] + 2] != 3:
                            if grid[player.pos[1]][player.pos[0] + 2] == 0 or grid[player.pos[1]][player.pos[0] + 2] == 2 or grid[player.pos[1]][player.pos[0] + 2] == 5:
                                player.previousPos = player.pos
                            if grid[player.pos[1]][player.pos[0] + 1] == 3 and playerPos[0] < numCols - 2 and grid[player.pos[1]][player.pos[0] + 2] == 2:
                                print("level Complete")
                                goalPos.append((playerPos[0] + 2, playerPos[1]))
                                newPos = player.pos[1], player.pos[0] + 2
                            if grid[player.pos[1]][player.pos[0] + 1] == 3 and playerPos[0] < numCols - 2 and grid[player.pos[1]][player.pos[0] + 2] == 7:
                                onButton.append((playerPos[0] + 2, playerPos[1]))

                            grid[player.pos[1]][player.pos[0] + 2] = 3
                            grid[player.pos[1]][player.pos[0] + 1] = 4
                            grid[player.previousPos[1]][player.previousPos[0]] = 0
                            if newPos != 0:
                                grid[newPos[0]][newPos[1]] = 5
                                newPos = 0
                    break

                if event.key in {pygame.K_a, pygame.K_LEFT} and playerPos[0] > 0:
                    print(player.pos)
                    if grid[player.pos[1]][player.pos[0] - 1] != 1 and grid[player.pos[1]][player.pos[0] - 1] != 2:
                        if (grid[player.pos[1]][player.pos[0] - 1] == 3 and playerPos[0] > 1 and (grid[player.pos[1]][player.pos[0] - 2] != 1 and grid[player.pos[1]][player.pos[0] - 2] != 3)) or grid[player.pos[1]][player.pos[0] - 1] != 3:
                            previousGrids.append(deepcopy(grid))

                        if grid[player.pos[1]][player.pos[0] - 1] == 7:
                            onButton.append((playerPos[0] - 1, playerPos[1]))

                        if grid[player.pos[1]][player.pos[0] - 1] == 6:
                            print("Level Complete!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            if level < len(grids) - 1:
                                level += 1
                                grid = deepcopy(grids[level])
                                nextLevel()
                                continue
                            else:
                                complete = True
                                farthestLevel = 0
                                level = farthestLevel
                                nextLevel()
                                gameState = GameMode.GAME_OVER
                        if grid[player.pos[1]][player.pos[0] - 1] == 0 or grid[player.pos[1]][player.pos[0] - 1] == 5 or grid[player.pos[1]][player.pos[0] - 1] == 7:
                            player.previousPos = player.pos
                            grid[player.pos[1]][player.pos[0] - 1] = 4
                            grid[player.previousPos[1]][player.previousPos[0]] = 0
                        elif grid[player.pos[1]][player.pos[0] - 1] == 3 and playerPos[0] > 1 and grid[player.pos[1]][player.pos[0] - 2] != 1 and grid[player.pos[1]][player.pos[0] - 2] != 3:
                            if grid[player.pos[1]][player.pos[0] - 2] == 0 or grid[player.pos[1]][player.pos[0] - 2] == 2 or grid[player.pos[1]][player.pos[0] - 2] == 5:
                                player.previousPos = player.pos
                            if grid[player.pos[1]][player.pos[0] - 1] == 3 and playerPos[0] > 1 and grid[player.pos[1]][player.pos[0] - 2] == 2:
                                print("level Complete")
                                goalPos.append((playerPos[0] - 2, playerPos[1]))
                                newPos = player.pos[1], player.pos[0] - 2
                            if grid[player.pos[1]][player.pos[0] - 1] == 3 and playerPos[0] > 1 and grid[player.pos[1]][player.pos[0] - 2] == 7:
                                onButton.append((playerPos[0] - 2, playerPos[1]))

                            grid[player.pos[1]][player.pos[0] - 2] = 3
                            grid[player.pos[1]][player.pos[0] - 1] = 4
                            grid[player.previousPos[1]][player.previousPos[0]] = 0
                            if newPos != 0:
                                grid[newPos[0]][newPos[1]] = 5
                                newPos = 0
                    break

                if event.key in {pygame.K_s, pygame.K_DOWN} and playerPos[1] < numRows - 1:
                    print(player.pos)
                    if grid[player.pos[1] + 1][player.pos[0]] != 1 and grid[player.pos[1] + 1][player.pos[0]] != 2:
                        if (grid[player.pos[1] + 1][player.pos[0]] == 3 and playerPos[1] < numRows - 2 and (grid[player.pos[1] + 2][player.pos[0]] != 1 and grid[player.pos[1] + 2][player.pos[0]] != 3)) or grid[player.pos[1] + 1][player.pos[0]] != 3:
                            previousGrids.append(deepcopy(grid))

                        if grid[player.pos[1] + 1][player.pos[0]] == 7:
                            onButton.append((playerPos[0], playerPos[1] + 1))

                        if grid[player.pos[1] + 1][player.pos[0]] == 6:
                            print("Level Complete!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            if level < len(grids) - 1:
                                level += 1
                                grid = deepcopy(grids[level])
                                nextLevel()
                                continue
                            else:
                                complete = True
                                farthestLevel = 0
                                level = farthestLevel
                                nextLevel()
                                gameState = GameMode.GAME_OVER
                        if grid[player.pos[1] + 1][player.pos[0]] == 0 or grid[player.pos[1] + 1][player.pos[0]] == 5 or grid[player.pos[1] + 1][player.pos[0]] == 7:
                            player.previousPos = player.pos
                            grid[player.pos[1] + 1][player.pos[0]] = 4
                            grid[player.previousPos[1]][player.previousPos[0]] = 0
                        elif grid[player.pos[1] + 1][player.pos[0]] == 3 and playerPos[1] < numRows - 2 and grid[player.pos[1] + 2][player.pos[0]] != 1 and grid[player.pos[1] + 2][player.pos[0]] != 3:
                            if grid[player.pos[1] + 2][player.pos[0]] == 0 or grid[player.pos[1] + 2][player.pos[0]] == 2 or grid[player.pos[1] + 2][player.pos[0]] == 5:
                                player.previousPos = player.pos
                            if grid[player.pos[1] + 1][player.pos[0]] == 3 and playerPos[1] < numRows - 2 and grid[player.pos[1] + 2][player.pos[0]] == 2:
                                print("level Complete")
                                goalPos.append((playerPos[0], playerPos[1] + 2))
                                print(goalPos)
                                newPos = player.pos[1] + 2, player.pos[0]
                            if grid[player.pos[1] + 1][player.pos[0]] == 3 and playerPos[1] < numRows - 2 and grid[player.pos[1] + 2][player.pos[0]] == 7:
                                onButton.append((playerPos[0], playerPos[1] + 2))

                            grid[player.pos[1] + 2][player.pos[0]] = 3
                            grid[player.pos[1] + 1][player.pos[0]] = 4
                            grid[player.previousPos[1]][player.previousPos[0]] = 0
                            if newPos != 0:
                                grid[newPos[0]][newPos[1]] = 5
                                newPos = 0
                    break

                if event.key in {pygame.K_w, pygame.K_UP} and playerPos[1] > 0:
                    print(player.pos)
                    if grid[player.pos[1] - 1][player.pos[0]] != 1 and grid[player.pos[1] - 1][player.pos[0]] != 2:
                        if (grid[player.pos[1] - 1][player.pos[0]] == 3 and playerPos[1] > 1 and (grid[player.pos[1] - 2][player.pos[0]] != 1 and grid[player.pos[1] - 2][player.pos[0]] != 3)) or grid[player.pos[1] - 1][player.pos[0]] != 3:
                            previousGrids.append(deepcopy(grid))

                        if grid[player.pos[1] - 1][player.pos[0]] == 7:
                            onButton.append((playerPos[0], playerPos[1] - 1))

                        if grid[player.pos[1] - 1][player.pos[0]] == 6:
                            print("Level Complete!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            if level < len(grids) - 1:
                                level += 1
                                grid = deepcopy(grids[level])
                                nextLevel()
                                continue
                            else:
                                complete = True
                                farthestLevel = 0
                                level = farthestLevel
                                nextLevel()
                                gameState = GameMode.GAME_OVER
                        if grid[player.pos[1] - 1][player.pos[0]] == 0 or grid[player.pos[1] - 1][player.pos[0]] == 5 or grid[player.pos[1] - 1][player.pos[0]] == 7:
                            player.previousPos = player.pos
                            grid[player.pos[1] - 1][player.pos[0]] = 4
                            grid[player.previousPos[1]][player.previousPos[0]] = 0
                        elif grid[player.pos[1] - 1][player.pos[0]] == 3 and playerPos[1] > 1 and grid[player.pos[1] - 2][player.pos[0]] != 1 and grid[player.pos[1] - 2][player.pos[0]] != 3:
                            if grid[player.pos[1] - 2][player.pos[0]] == 0 or grid[player.pos[1] - 2][player.pos[0]] == 2 or grid[player.pos[1] - 2][player.pos[0]] == 5:
                                player.previousPos = player.pos
                            if grid[player.pos[1] - 1][player.pos[0]] == 3 and playerPos[1] > 1 and grid[player.pos[1] - 2][player.pos[0]] == 2:
                                print("level Complete")
                                goalPos.append((playerPos[0], playerPos[1] - 2))
                                print(goalPos)
                                newPos = player.pos[1] - 2, player.pos[0]
                            if grid[player.pos[1] - 1][player.pos[0]] == 3 and playerPos[1] > 1 and grid[player.pos[1] - 2][player.pos[0]] == 7:
                                onButton.append((playerPos[0], playerPos[1] - 2))

                            grid[player.pos[1] - 2][player.pos[0]] = 3
                            grid[player.pos[1] - 1][player.pos[0]] = 4
                            grid[player.previousPos[1]][player.previousPos[0]] = 0
                            if newPos != 0:
                                grid[newPos[0]][newPos[1]] = 5
                                newPos = 0
                    break

        if gameState == GameMode.GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if playAgainButton.hovered(mouseX, mouseY):
                    gameState = GameMode.PLAY
                    grids = deepcopy(originalGrids)
                    grid = deepcopy(grids[farthestLevel])

                if menuButton.hovered(mouseX, mouseY):
                    gameState = GameMode.MENU
                    nextLevel()
                    grid = deepcopy(grids[farthestLevel])

                if bonusLevelsButton2.hovered(mouseX, mouseY):
                    gameState = GameMode.PLAY
                    grids = deepcopy(bonusGrids)
                    level = 0
                    grid = deepcopy(grids[level])
                    nextLevel()

    display_surface.fill(color['Grey'])  # this is the background
    # draw stuff here. The order determines the layers.
    mapGoals = sum(r.count(7) for r in grid)
    showTiles(grid)
    if mapGoals == 0 and grid[exitPos[1]][exitPos[0]] != 6:
        grid[exitPos[1]][exitPos[0]] = 6

    if gameState == GameMode.MENU:
        titleText = bigBoldFont.render("All Boxed Up", True, color["Light_Grey"])
        textRect = titleText.get_rect()
        textRect.midtop = (width // 2, height // 2 - 200)
        playButton.show(display_surface, color['Grey'], boldFont, color['White'])
        levelsButton.show(display_surface, color['Grey'], boldFont, color['White'])
        quitButton.show(display_surface, color['Grey'], boldFont, color['White'])
        display_surface.blit(titleText, textRect)
        
    if gameState == GameMode.LEVEL_MENU:
        row = 0
        col = 0
        for i in range(levelInterval, levelInterval + 10):
            levelButton = Button(40 + col * 160, (height // 2 - 80) + (160 * row), 80, 80, None, str(i + 1))
            if i <= level or complete:
                levelButton.show(display_surface, color['Grey'], boldFont, color['Green'])
            else:
                levelButton.show(display_surface, color['Grey'], boldFont, color['Red'])

            levelButtons.append(levelButton)
            col += 1

            if (i + 1) % 5 == 0:
                row += 1
                col = 0
                continue

    if gameState == GameMode.PLAY_MENU:
        playText = bigBoldFont.render("Play", True, color["Light_Grey"])
        textRect = playText.get_rect()
        textRect.midtop = (width//2, height//2 - 200)
        playLevelsButton.show(display_surface, color['Grey'], boldFont, color['White'])
        bonusLevelsButton.show(display_surface, color['Grey'], boldFont, color['White'])
        display_surface.blit(playText, textRect)

    if gameState == GameMode.PLAY:
        for pos in range(0, len(onButton)):
            buttonPos = onButton[pos][0], onButton[pos][1]
            if grid[buttonPos[1]][buttonPos[0]] not in (3, 4, 7):
                grid[buttonPos[1]][buttonPos[0]] = 7
        for pos in range(0, len(goalPos)):
            newPos = goalPos[pos][0], goalPos[pos][1]
            if grid[newPos[1]][newPos[0]] not in (3, 4, 2, 5):
                grid[newPos[1]][newPos[0]] = 5

        levelText = boldFont.render("Level " + str(level + 1), True, color["White"])
        if grids == deepcopy(bonusGrids):
            levelText = boldFont.render("Bonus Level " + str(level + 1), True, color["White"])
        levelTextRect = levelText.get_rect()
        levelTextRect.topleft = (10, -5)
        display_surface.blit(levelText, levelTextRect)

        sizeText = smallBoldFont.render(str(numCols) + "x" + str(numRows), True, color["White"])
        sizeTextRect = sizeText.get_rect()
        sizeTextRect.bottomright = (width - 7, height)
        display_surface.blit(sizeText, sizeTextRect)

        retryButton.show(display_surface, color['Green'], boldFont, color['Black'])
        display_surface.blit(retryImage, (retryButton.x - 3, retryButton.y - 2))

        undoButton.show(display_surface, color['Green'], boldFont, color['Black'])
        display_surface.blit(undoImage, (undoButton.x + 3, undoButton.y + 3))

        newPos = 0
        player = Player(playerPos, grid)

    if gameState == GameMode.GAME_OVER:
        display_surface.fill(color['Grey'])
        blankGrid = [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]]
        showTiles(blankGrid)
        winText = bigBoldFont.render("Congratulations!", True, color["Light_Grey"])
        textRect = winText.get_rect()
        textRect.midtop = (width // 2, height // 2 - 200)
        display_surface.blit(winText, textRect)
        if len(grids) > 30:
            completeText = smallerBoldFont.render("You have completed all of the normal levels", True, color["Light_Grey"])
            completeText2 = smallBoldFont.render("You are now a puzzle solving master!", True, color["Light_Grey"])
            textRect = completeText2.get_rect()
            textRect.midtop = (width // 2, height // 2 - 10)
            display_surface.blit(completeText2, textRect)
        else:
            completeText = smallerBoldFont.render("You have completed all of the bonus levels", True, color["Light_Grey"])
            grids = deepcopy(bonusGrids)
            level = 39

        textRect = completeText.get_rect()
        textRect.midtop = (width // 2, height // 2 - 50)
        display_surface.blit(completeText, textRect)
        playAgainButton.show(display_surface, color['Grey'], boldFont, color['White'])
        menuButton.show(display_surface, color['Grey'], boldFont, color['White'])
        bonusLevelsButton2.show(display_surface, color['Grey'], boldFont, color['White'])

    # flip is all the way at the bottom
    pygame.display.flip()
