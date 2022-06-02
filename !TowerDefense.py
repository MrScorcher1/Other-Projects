import pygame
import sys
import math
from enum import IntEnum
import os

from TowerDefenseObjects.enemy import Enemy
from TowerDefenseObjects.tower import Archer
from TowerDefenseObjects.tower import PoisonTower
from TowerDefenseObjects.tower import Sniper
from TowerDefenseObjects.tower import Gunner
from TowerDefenseObjects.tower import Catapult
from TowerDefenseObjects.tower import Dragon
from TowerDefenseObjects.tower import Frost
from TowerDefenseObjects.projectile import Projectile
from TowerDefenseObjects.projectile import ExplodingProjectile
from TowerDefenseObjects.button import Button
from TowerDefenseObjects.rounds import Round
from TowerDefenseObjects.Map import Map

pygame.init()

crosshairImage = pygame.image.load(os.path.join("TowerDefenseAssets/Crosshair_small.png"))
fireballImage = pygame.image.load(os.path.join("TowerDefenseAssets/fireball.png"))
rockImage = pygame.image.load(os.path.join("TowerDefenseAssets/Catapult_Rock_small.png"))
coinImage = pygame.image.load(os.path.join("TowerDefenseAssets/coin.png"))
bubbleImage = pygame.image.load(os.path.join("TowerDefenseAssets/popupbubble.png"))
upgradeBubbleImage = pygame.image.load(os.path.join("TowerDefenseAssets/popupbubble_upgrade.png"))
heartImage = pygame.image.load(os.path.join("TowerDefenseAssets/Heart.png"))
heartOutlineImage = pygame.image.load(os.path.join("TowerDefenseAssets/HeartOutline.png"))

screen_size = width, height = (1030, 600)
display_surface = pygame.display.set_mode(screen_size)
tempSurface = pygame.Surface(screen_size, pygame.SRCALPHA)
tempSurface.set_alpha(255)

fps = 120
fastForward = False

font = pygame.font.SysFont("arielblack", 50)
medFont = pygame.font.SysFont("arialblack", 50)
medLargeFont = pygame.font.SysFont("arialblack", 82)
basicFont = pygame.font.SysFont("arialblack", 20)
largeFont = pygame.font.SysFont("arialblack", 100)
smallFont = pygame.font.SysFont("arialblack", 16)
smallishFont = pygame.font.SysFont("arialblack", 17)
largerSmallishFont = pygame.font.SysFont("arialblack", 18)


class GameMode(IntEnum):
    MENU = 1
    PLAY = 2
    BUILD = 3
    GAME_OVER_LOSE = 4
    GAME_OVER_WIN = 5
    PAUSE = 6


gameState = GameMode.MENU
previousGameState = gameState

# globals
max_base_health = 100
current_base_health = max_base_health
starting_money = 1000
money = starting_money
loaded_map = Map(1)
selectedMapNumber = 1
numberOfMaps = 3
mapImagePath = "TowerDefenseAssets/EthanTDlevel" + str(selectedMapNumber) + ".png"
mapImage = pygame.image.load(os.path.join(mapImagePath))
mapImage = pygame.transform.smoothscale(mapImage, (648, 486))
current_round = Round(1)
mouseX, mouseY = 0, 0
selectedTower = None
purchasedTower = None
totalRounds = 18


def isPoint_onEllipse(towerX, towerY):
    p = ((math.pow((towerX - 400), 2) / (380 ** 2)) +
         (math.pow((towerY - 300), 2) / (280 ** 2)))

    return p <= 1


towers = []
enemies = []
projectiles = []
buttons = []

upgradeButtons = []


def start_round():
    global frameCount
    global gameState
    global projectiles
    frameCount = 0
    gameState = GameMode.PLAY
    projectiles.clear()


def switchToBuild():
    global gameState
    global frameCount
    frameCount = 0
    gameState = GameMode.BUILD


def round_over():
    return current_round.doneSpawning() and len(enemies) == 0


def reset_game():
    global money
    global current_round
    global current_base_health
    global selectedTower
    global purchasedTower
    global fastForward
    money = starting_money
    current_round = Round(1)
    enemies.clear()
    towers.clear()
    projectiles.clear()
    current_base_health = max_base_health
    selectedTower = None
    purchasedTower = None
    fastForward = False
    

sellButton = Button(width-190, height-47, 180, 40, None, "Sell Tower")
roundStartButton = Button(width-190, 10, 180, 40, start_round, "Start Round")
fastForwardButton = Button(width-190, 10, 180, 40, None, ">>")
changeTargetingPriorityButton = Button(width-190, height-90, 180, 36)

nextMapButton = Button(width-150, height//2 - 13, 100, 100, None, ">")
previousMapButton = Button(50, height//2 - 13, 100, 100, None, "<")
mapButton = Button(188, 94, 648, 486, switchToBuild)
titleButton = Button(width//2, 42, 0, 0, None, "Tower Defense")
playAgainButton = Button(width//2 - 138, height//2, 276, 75, None, "Play Again")
mainMenuButton = Button(width//2 - 138, height//2 + 100, 276, 75, None, "Main Menu")

pauseContinueButton = Button(width//2 + 128, height//2 - 209, 45, 45, None, "X")
pausedButton = Button(width//2 - 149, height//2 - 115, 300, 65, None, "Paused")
pauseMainMenuButton = Button(width//2 - 149, height//2 + 5, 300, 65, None, "Main Menu")
pauseRestartButton = Button(width//2 - 149, height//2 + 115, 300, 65, None, "Restart")

recorded_path = open("angles.txt", "w")

color = {
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Red": (255, 0, 0),
    "Orange": (255, 120, 0),
    "Yellow": (255, 255, 0),
    "Green": (0, 180, 0),
    "Blue": (0, 0, 255),
    "Purple": (195, 33, 204),
    "Pink": (255, 23, 197),
    "Grey": (150, 150, 150)
}


def purchase_tower(towerType):
    global purchasedTower
    global selectedTower
    global money
    if purchasedTower is None:
        if money >= towerType.cost:
            purchasedTower = towerType
            selectedTower = None

        # towers.append(purchasedTower)
    else:
        print("Not enough money")


towerPurchaseButtons = [
    Button(width-190, 130, 80, 40, purchase_tower, "Archer"),
    Button(width-190, 180, 80, 40, purchase_tower, "Sniper"),
    Button(width-100, 130, 80, 40, purchase_tower, "Gunner"),
    Button(width-100, 180, 80, 40, purchase_tower, "Poison"),
    Button(width-190, 230, 80, 40, purchase_tower, "Catapult"),
    Button(width-100, 230, 80, 40, purchase_tower, "Dragon"),
    Button(width-100, 280, 80, 40, purchase_tower, "Frost")
]


def place_tower():
    global towers
    global money
    global purchasedTower
    global selectedTower
    if purchasedTower is not None and purchasedTower.isValidPlacement:
        money -= purchasedTower.cost
        towers.append(purchasedTower)
        selectedTower = purchasedTower
        purchasedTower = None


def show_non_dragon_towers():
    for tower in towers:
        if not isinstance(tower, Dragon):
            tower.show(display_surface, color["Blue"])
            tower.show(tempSurface, color["Blue"])


def showAndMove_enemies():
    global enemy
    global current_base_health
    for enemy in enemies:
        if enemy.nextPathPointIndex+1 == len(loaded_map.pathPoints):
            current_base_health -= enemy.baseDamage
            enemies.remove(enemy)
            continue
        enemy.showBody(display_surface)
        enemy.showBody(tempSurface)
        enemy.showHealthBar(display_surface)
        enemy.showHealthBar(tempSurface)
        enemy.move(loaded_map, fastForward)


def show_dragon_towers():
    for tower in towers:
        if isinstance(tower, Dragon):
            tower.move()
            tower.show(display_surface, color["Orange"])
            tower.show(tempSurface, color["Orange"])


wipeTransition = True
wipeImage = mapImage
wipeDirection = ""
wipeImagePos = (mapButton.x, mapButton.y)


def draw_Menu_UI():
    global wipeImagePos
    global wipeTransition

    mapImageRect = mapImage.get_rect()
    mapImageRect.center = mapButton.rect.center
    mapBorderRect = mapImageRect.copy().inflate(4, 4)

    if not wipeTransition:
        display_surface.blit(mapImage, mapImageRect)

    #display_surface.fill(color["White"], mapBorderRect)

    if wipeImagePos == mapButton.rect.topleft:
        wipeTransition = False
    if wipeTransition:
        wipeImagePos = pygame.math.Vector2(wipeImagePos).lerp(pygame.math.Vector2(mapButton.rect.topleft), 0.05)
        mapButton.show(display_surface, color["Black"], None, None, None, False)
            
        display_surface.blit(wipeImage, wipeImagePos)
        pygame.draw.rect(display_surface, color["Black"], mapBorderRect.copy().inflate(200, 200), width=200)

    nextMapButton.show(display_surface, color["Black"], largeFont, color["White"], outline=False)
    previousMapButton.show(display_surface, color["Black"], largeFont, color["White"], outline=False)
    titleButton.show(display_surface, color["Black"], largeFont, color["Green"], outline=False)

    pygame.draw.rect(display_surface, color["White"], mapBorderRect, width=4)


def draw_UI():
    global coinImage
    global bubbleImage
    global upgradeBubbleImage

    if selectedTower is not None:
        pygame.draw.circle(tempSurface, (200, 200, 200, 50), (int(selectedTower.pos.x), int(selectedTower.pos.y)),
                           int(selectedTower.modifiedAttackRange))
        tempSurface.fill(color["Black"], pygame.Rect(width - 230, 0, 230, height))

        for b in selectedTower.upgradeButtons:
            # b.show(tempSurface, color["Black"])
            if len(b.name) < 7:
                b.showName(tempSurface, basicFont)
            else:
                b.showName(tempSurface, largerSmallishFont)

            b.showPlus(tempSurface, basicFont, color["White"])

        sellButton.show(tempSurface, color['Red'], basicFont, color['White'])
        changeTargetingPriorityButton.text = selectedTower.priority
        changeTargetingPriorityButton.show(tempSurface, color["White"], basicFont, color["Black"])

        for button in selectedTower.upgradeButtons:
            for upgradeLevel in range(selectedTower.upgradeList[button.name].level):
                pygame.draw.rect(tempSurface, color["Green"], pygame.Rect(936 + 22*upgradeLevel, button.rect.y, 18, 20))
            for x in range(936, 981, 22):
                pygame.draw.rect(tempSurface, color["White"], pygame.Rect(x, button.rect.y, 18, 20), 3)

            if button.hovered(mouseX, mouseY):
                upgradeBubbleImage = pygame.transform.smoothscale(upgradeBubbleImage, (75, 35))
                upgradeBubbleImageRect = upgradeBubbleImage.get_rect()
                upgradeBubbleImageRect.midbottom = (button.rect.midtop[0] - 25, button.rect.midtop[1])
                tempSurface.blit(upgradeBubbleImage, upgradeBubbleImageRect)

                coin = pygame.transform.scale(coinImage, (23, 23))
                coinImageRect = coin.get_rect()
                coinImageRect.center = (upgradeBubbleImageRect.left + 15, upgradeBubbleImageRect.centery - 2)
                tempSurface.blit(coin, coinImageRect)

                costForUpgrade = 0

                upgrade = selectedTower.upgradeList[button.name]
                if upgrade.level < 3:
                    costForUpgrade = upgrade.cost[upgrade.level]

                if costForUpgrade != 0:
                    costText = smallFont.render(f"-{costForUpgrade}", True, color["Black"])
                    textRect = costText.get_rect()
                    textRect.midleft = (coinImageRect.right + 5, coinImageRect.centery)
                    tempSurface.blit(costText, textRect)

    for b in towerPurchaseButtons:
        if len(b.text) > 6:
            b.show(tempSurface, color["Blue"], smallishFont, color["White"])
        else:
            b.show(tempSurface, color["Blue"], basicFont, color["White"])

    if gameState == GameMode.BUILD:
        roundStartButton.show(tempSurface, color["Green"], basicFont, color["Black"])
    else:
        fastForwardButton.show(tempSurface, color["Green"], basicFont, color["Black"])

    roundText = smallFont.render("Round " + str(current_round.roundNumber) + " of " + str(totalRounds), True, color["White"])
    textRect = roundText.get_rect()
    textRect.midleft = (width - 188, 73)
    tempSurface.blit(roundText, textRect)

    coinText = basicFont.render(": " + str(money), True, color["Yellow"])
    textRect = coinText.get_rect()
    textRect.midleft = (width - 158, 105)
    tempSurface.blit(coinText, textRect)

    coinImage = pygame.transform.smoothscale(coinImage, (27, 27))
    coinImageRect = coinImage.get_rect()
    coinImageRect.center = (width-177, 106)
    tempSurface.blit(coinImage, coinImageRect)

    for b in towerPurchaseButtons:
        if b.hovered(mouseX, mouseY):
            bubbleImage = pygame.transform.smoothscale(bubbleImage, (75, 35))
            bubbleImageRect = bubbleImage.get_rect()
            bubbleImageRect.midbottom = b.rect.midtop
            tempSurface.blit(bubbleImage, bubbleImageRect)

            coin = pygame.transform.scale(coinImage, (23, 23))
            coinImageRect = coin.get_rect()
            coinImageRect.center = (bubbleImageRect.left+15, bubbleImageRect.centery-2)
            tempSurface.blit(coin, coinImageRect)

            cost = 0
            if b.text == "Archer":
                cost = Archer.cost
            if b.text == "Gunner":
                cost = Gunner.cost
            if b.text == "Sniper":
                cost = Sniper.cost
            if b.text == "Poison":
                cost = PoisonTower.cost
            if b.text == "Catapult":
                cost = Catapult.cost
            if b.text == "Dragon":
                cost = Dragon.cost
            if b.text == "Frost":
                cost = Frost.cost
            if cost != 0:
                costText = smallFont.render(f"-{cost}", True, color["Black"])
                textRect = costText.get_rect()
                textRect.midleft = (coinImageRect.right + 5, coinImageRect.centery)
                tempSurface.blit(costText, textRect)
                
    for heartHeight in range(0, height, 24):
        heartImageRect = heartImage.get_rect()
        heartImageRect.y = heartHeight
        heartImageRect.x = 802
        tempSurface.blit(heartImage, heartImageRect)

    baseHealthRect = pygame.Rect(802, 0, 26, 0)
    baseHealthRect.height = height - int(height * current_base_health / max_base_health)
    tempSurface.fill((0, 0, 0), baseHealthRect)

    for heartHeight in range(0, height, 24):
        heartOutlineImageRect = heartImage.get_rect()
        heartOutlineImageRect.y = heartHeight
        heartOutlineImageRect.x = 802
        tempSurface.blit(heartOutlineImage, heartOutlineImageRect)

    display_surface.blit(tempSurface, (0, 0))


clock = pygame.time.Clock()
frameCount = 0

while True:
    # force a frame rate of 60 fps
    clock.tick(fps)
    frameCount += 1

    # get the mouse position each frame
    mouseX, mouseY = pygame.mouse.get_pos()
    # check the events, and if the QUIT event occurs, close the window

    #######################################
    #               EVENT LOOP            #
    #######################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # give the option to close the window with ESC
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if gameState in [GameMode.PLAY, GameMode.BUILD]:
                    previousGameState = gameState
                    gameState = GameMode.PAUSE
                elif gameState == GameMode.PAUSE:
                    gameState = previousGameState

            if event.key == pygame.K_1:
                purchase_tower(Archer())
            if event.key == pygame.K_2:
                purchase_tower(Sniper())
            if event.key == pygame.K_3:
                purchase_tower(Gunner())
            if event.key == pygame.K_4:
                purchase_tower(PoisonTower())
            if event.key == pygame.K_5:
                purchase_tower(Catapult())
            if event.key == pygame.K_6:
                purchase_tower(Dragon())
            if event.key == pygame.K_7:
                purchase_tower(Frost())

            if event.key == pygame.K_e:
                enemies.append(Enemy(3, loaded_map.pathPoints, loaded_map.pointAngles, 4, 1, "White"))
            if event.key == pygame.K_SPACE:
                pass

            if event.key == pygame.K_TAB:
                if selectedTower is not None:
                    selectedTower.change_priority()
        if event.type == pygame.MOUSEBUTTONDOWN:

            if gameState == GameMode.MENU:
                if mapButton.hovered(mouseX, mouseY):
                    mapButton.onclick()
                    loaded_map = Map(selectedMapNumber)
                if nextMapButton.hovered(mouseX, mouseY):
                    selectedMapNumber = selectedMapNumber + 1 if selectedMapNumber < numberOfMaps else 1
                    wipeDirection = "Right"
                    wipeTransition = True

                if previousMapButton.hovered(mouseX, mouseY):
                    selectedMapNumber = selectedMapNumber - 1 if selectedMapNumber > 1 else numberOfMaps
                    wipeDirection = "Left"
                    wipeTransition = True

                mapImagePath = "TowerDefenseAssets/EthanTDlevel" + str(selectedMapNumber) + ".png"
                mapImage = pygame.image.load(os.path.join(mapImagePath))
                mapImage = pygame.transform.smoothscale(mapImage, (648, 486))
                mapImageRect = mapImage.get_rect()

                if wipeTransition:
                    wipeImage = mapImage
                    if wipeDirection == "Left":
                        wipeImagePos = mapButton.rect.topright
                    if wipeDirection == "Right":
                        wipeImagePos = (mapButton.rect.x-640, mapButton.rect.y)

            if gameState in [GameMode.GAME_OVER_LOSE, GameMode.GAME_OVER_WIN]:
                if playAgainButton.hovered(mouseX, mouseY):
                    gameState = GameMode.BUILD
                if mainMenuButton.hovered(mouseX, mouseY):
                    gameState = GameMode.MENU

            if gameState == GameMode.PLAY:
                if fastForwardButton.hovered(mouseX, mouseY):
                    fastForward = not fastForward  # toggle T/F
                    fastForwardButton.text = ">>" if fastForward else ">"

            if gameState == GameMode.BUILD:
                if roundStartButton.hovered(mouseX, mouseY):
                    start_round()

            if gameState in [GameMode.PLAY, GameMode.BUILD]:

                if event.button == 3:           # Right-click to cancel a tower a tower purchase.
                    purchasedTower = None
                for tower in towers:
                    if isinstance(tower, Dragon):
                        if math.dist((mouseX, mouseY), tower.rect.center) < 30:
                            selectedTower = tower
                            break
                    elif math.dist((mouseX, mouseY), tower.pos) < 25:
                        selectedTower = tower
                        break
                else:
                    if mouseX < 800:
                        selectedTower = None
                if selectedTower is not None:
                    for button in selectedTower.upgradeButtons:

                        if button.hovered(mouseX, mouseY):
                            upgrade = selectedTower.upgradeList[button.name]
                            if upgrade.level < 3:
                                costForUpgrade = upgrade.cost[upgrade.level]

                                if money >= costForUpgrade:
                                    money -= costForUpgrade
                                    upgrade.level += 1
                                    if button.name == "Range":
                                        selectedTower.getEnemiesInRange(enemies)
                                else:
                                    print("Not enough money!")

                    if sellButton.hovered(mouseX, mouseY):
                        money += int(selectedTower.cost * 0.75)
                        towers.remove(selectedTower)
                        selectedTower = None

                    if changeTargetingPriorityButton.hovered(mouseX, mouseY):
                        selectedTower.change_priority()

                for index, b in enumerate(towerPurchaseButtons):
                    if b.hovered(mouseX, mouseY):
                        selectedTower = None
                        purchasedTower = None
                        if b.text == "Archer":
                            purchase_tower(Archer())
                        if b.text == "Gunner":
                            purchase_tower(Gunner())
                        if b.text == "Sniper":
                            purchase_tower(Sniper())
                        if b.text == "Poison":
                            purchase_tower(PoisonTower())
                        if b.text == "Catapult":
                            purchase_tower(Catapult())
                        if b.text == "Dragon":
                            purchase_tower(Dragon())
                        if b.text == "Frost":
                            purchase_tower(Frost())

            if gameState == GameMode.PAUSE:
                if pauseMainMenuButton.hovered(mouseX, mouseY):
                    reset_game()
                    gameState = GameMode.MENU
                    tempSurface.fill(color["Black"])
                    display_surface.blit(tempSurface, (0, 0))

                if pauseContinueButton.hovered(mouseX, mouseY):
                    gameState = previousGameState

                if pauseRestartButton.hovered(mouseX, mouseY):
                    reset_game()
                    gameState = GameMode.BUILD

        if event.type == pygame.MOUSEBUTTONUP:
            if purchasedTower is not None:
                place_tower()

    if gameState == GameMode.MENU:
        draw_Menu_UI()

    if gameState in [GameMode.PLAY, GameMode.BUILD]:

        display_surface.fill(color['Black'])  # this is the background
        # draw stuff here. The order determines the layers.
        display_surface.blit(loaded_map.image, (0, 0))
        tempSurface.fill(color['Black'])
        tempSurface.blit(loaded_map.image, (0, 0))

        if current_base_health <= 0:
            gameState = GameMode.GAME_OVER_LOSE

        if purchasedTower is not None and not isinstance(purchasedTower, Dragon):

            purchasedTower.pos.x, purchasedTower.pos.y = mouseX, mouseY
            purchasedTower.isValidPlacement = True
            rangeIndicatorColor = (200, 200, 200, 50)
            for tower in towers:
                if math.dist((purchasedTower.pos.x, purchasedTower.pos.y), (tower.pos.x, tower.pos.y)) < 50:
                    rangeIndicatorColor = (255, 0, 0, 50)
                    purchasedTower.isValidPlacement = False

            for point in loaded_map.pathPoints:
                if math.dist((purchasedTower.pos.x, purchasedTower.pos.y), point) < 40:
                    rangeIndicatorColor = (255, 0, 0, 50)
                    purchasedTower.isValidPlacement = False

            if loaded_map.number == 2 and not isPoint_onEllipse(purchasedTower.pos.x, purchasedTower.pos.y):
                rangeIndicatorColor = (255, 0, 0, 50)
                purchasedTower.isValidPlacement = False

            if purchasedTower.pos.x > width - 250:
                purchasedTower.isValidPlacement = False
                rangeIndicatorColor = (255, 0, 0, 50)

            else:
                pygame.draw.circle(tempSurface, rangeIndicatorColor, (int(purchasedTower.pos.x), int(purchasedTower.pos.y)), purchasedTower.modifiedAttackRange)

                # display_surface.blit(tempSurface, (0, 0))
                purchasedTower.show(tempSurface, color["Blue"])
        elif isinstance(purchasedTower, Dragon):
            purchasedTower.isValidPlacement = True
            purchasedTower.pos.x, purchasedTower.pos.y = (400, 300)

        # BUILD OR PLAY MODE: Draw game UI and towers
        draw_UI()

        show_non_dragon_towers()

        show_dragon_towers()

    if gameState == GameMode.PAUSE:
        #TODO: Pause Menu Buttons
        pauseMenuRect = pygame.Rect(width//2 - 180, height//2 - 216, 360, 432)
        tempSurface.fill((0, 0, 0, 5))
        tempSurface.fill(color["Green"], pauseMenuRect)
        pygame.draw.rect(tempSurface, color["White"], (pauseMenuRect.left - 3, pauseMenuRect.top - 3, pauseMenuRect.width + 6, pauseMenuRect.height + 6), border_radius=10, width=3)
        pauseContinueButton.show(tempSurface, color["Red"], basicFont, color["White"], outlineColor=color["Black"])
        pauseMainMenuButton.show(tempSurface, color["White"], basicFont, color["Black"], outlineColor=color["Black"])
        pauseRestartButton.show(tempSurface, color["White"], basicFont, color["Black"], outlineColor=color["Black"])
        pausedButton.show(tempSurface, color["Green"], medLargeFont, color["Blue"], outlineColor=color["Green"])
        display_surface.blit(tempSurface, (0, 0))

    #pygame.draw.lines(display_surface, color['White'], False, loaded_map.pathPoints)
    #for point in loaded_map.pathPoints:
     #   pygame.draw.circle(display_surface, color['White'], point, 8)
        # pass

    if gameState == GameMode.PLAY:
        for spawnGroup in current_round.spawns:
            delayFramesRemaining = (spawnGroup.delayFromRoundStart - frameCount) * (1 if fastForward else 0.5)
            # if spawnGroup is activated
            if frameCount >= delayFramesRemaining:
                # if the current frame matches the correct frame to spawn an enemy, do so.
                framesUntilNextSpawn = (spawnGroup.spawnInterval - spawnGroup.spawnCharge) * (2 if fastForward else 1)
                if framesUntilNextSpawn <= 0:
                    spawnGroup.spawn(enemies, loaded_map.pathPoints, loaded_map.pointAngles)
                    spawnGroup.spawnCharge = 0
                spawnGroup.spawnCharge += (2 if fastForward else 1)
        if round_over():
            gameState = GameMode.BUILD
            money += 100
            print(money)
            if current_round.roundNumber <= totalRounds:
                current_round = Round(current_round.roundNumber + 1)
            else:
                gameState = GameMode.GAME_OVER_WIN

        for tower in towers:    # PLAY MODE: Charge, determine targets, and determine fire
            chargeRemaining = (tower.numFramesToFullCharge - tower.charge) * (1 if fastForward else 0.5)
            if not fastForward:

                tower.charge += (1 + tower.upgradeList["Speed"].level) / 2
            else:
                tower.charge += 1 + tower.upgradeList["Speed"].level
            #print(tower.charge)

            if chargeRemaining <= 0:
                enemiesInRange = tower.getEnemiesInRange(enemies)

                if len(enemiesInRange) > 0:

                    if tower.weaponType == "TargetedProjectile":

                        if isinstance(tower, Dragon):
                            tower.determineSingleTarget(enemiesInRange)
                            p_dirX, p_dirY = tower.calculate_projectile_velocities(tower.targetEnemy, tower.projectileSpeed)
                            projectiles.append(Projectile(tower, tower.rect.centerx, tower.rect.centery, p_dirX, p_dirY))

                        else:
                            tower.projectileSpeed = tower.initialProjectileSpeed + (tower.initialProjectileSpeed * 0.5 * tower.upgradeList["Range"].level)
                            tower.determineSingleTarget(enemiesInRange)
                            p_dirX, p_dirY = tower.calculate_projectile_velocities(tower.targetEnemy, tower.projectileSpeed)
                            projectiles.append(Projectile(tower, tower.pos.x, tower.pos.y, p_dirX, p_dirY))

                    if tower.weaponType == "ExplodingProjectile":
                        tower.projectileSpeed = (tower.initialProjectileSpeed + tower.initialProjectileSpeed * 0.5 * tower.upgradeList["Range"].level)
                        dist = tower.determineSingleTarget(enemiesInRange)
                        tower.targetPos = tower.targetEnemy.pos
                        p_dirX, p_dirY = tower.calculate_projectile_velocities(tower.targetEnemy, tower.projectileSpeed)
                        projectiles.append(ExplodingProjectile(tower, tower.pos.x, tower.pos.y, p_dirX, p_dirY))
                        projectiles[-1].distanceToTarget = dist

                    if tower.weaponType == "TargetedInstant":
                        tower.determineSingleTarget(enemiesInRange)
                        tower.targetEnemy.health -= tower.attackDamage
                        pygame.draw.line(tempSurface, color["Black"], (int(tower.pos.x), int(tower.pos.y)), (int(tower.targetEnemy.pos[0]), int(tower.targetEnemy.pos[1])), 3)
                        pygame.draw.line(display_surface, color["Black"], (int(tower.pos.x), int(tower.pos.y)), (int(tower.targetEnemy.pos[0]), int(tower.targetEnemy.pos[1])), 3)
                        if tower.targetEnemy.health <= 0:
                                money += tower.targetEnemy.maxHealth
                                enemies.remove(tower.targetEnemy)

                    if tower.weaponType == "AoE":
                        if isinstance(tower, Frost):
                            pygame.draw.circle(tempSurface, (150, 150, 255, 70), (int(tower.pos.x), int(tower.pos.y)), tower.modifiedAttackRange)

                            for enemy in enemiesInRange:
                                enemy.speed = enemy.originalSpeed - ((tower.upgradeList["Slow"].level * 0.1) + (enemy.originalSpeed * 0.3))
                                if tower.upgradeList["Slow"].level == 3 and frameCount % 100 <= 15:
                                    enemy.speed = 0

                            for enemy in enemies:
                                if enemy not in enemiesInRange:
                                    enemy.speed = enemy.originalSpeed

                        for enemy in enemiesInRange:
                            enemy.health -= tower.attackDamage
                        if not isinstance(tower, Frost):
                            pygame.draw.circle(display_surface, color["Green"], (int(tower.pos.x), int(tower.pos.y)), tower.modifiedAttackRange)

                    if tower.weaponType == "DummyProjectile":
                        pass

                    tower.charge = 0
                    draw_UI()
                    display_surface.blit(tempSurface, (0, 0))

        # PLAY MODE: Determine dead enemies
        for enemy in enemies:
            if enemy.health <= 0:
                money += enemy.maxHealth
                enemies.remove(enemy)

        showAndMove_enemies()
        # PLAY MODE: Draw projectiles and determine hits on enemies
        for projectile in projectiles:
            origin = projectile.originTower
            projectile.show(display_surface, color["White"])
            if projectile.moving:
                projectile.move(fastForward)
            if projectile.pos[0] > width or projectile.pos[0] < 0:
                projectiles.remove(projectile)
                continue
            if projectile.pos[1] > height or projectile.pos[1] < 0:
                projectiles.remove(projectile)
                continue

            if isinstance(projectile, ExplodingProjectile):
                rockRect = rockImage.get_rect()
                rockRect.center = (int(projectile.pos[0]), int(projectile.pos[1]))
                display_surface.blit(rockImage, rockRect)
                projectile.distanceTraveled += origin.projectileSpeed
                if projectile.distanceTraveled >= projectile.distanceToTarget:
                    if not projectile.exploding:
                        for enemy in enemies:
                            if math.dist(projectile.pos, enemy.floatPos) <= origin.modifiedExplosionRadius:
                                enemy.health -= origin.attackDamage + origin.attackDamage * origin.upgradeList["Damage"].level
                        projectile.moving = False
                        projectile.exploding = True
                    else:
                        projectile.explosionTimer -= 1
                        origin.modifiedExplosionRadius = origin.explosionRadius + 15 * origin.upgradeList["Explosion"].level
                        diameter = origin.modifiedExplosionRadius*2
                        fireballImage = pygame.transform.smoothscale(fireballImage, (diameter, diameter))
                        fireballRect = fireballImage.get_rect()
                        fireballRect.center = origin.targetPos
                        display_surface.blit(fireballImage, fireballRect)
                    if projectile.explosionTimer <= 0:
                        projectiles.remove(projectile)
                else:
                    pass
                    #crosshairRect = crosshairImage.get_rect()
                    #crosshairRect.center = origin.targetPos
                    #display_surface.blit(crosshairImage, crosshairRect)
            else:
                for enemy in enemies:
                    if math.dist(projectile.pos, enemy.floatPos) < 30 and enemy not in projectile.enemiesCollided:
                        enemy.health -= origin.attackDamage + origin.attackDamage * origin.upgradeList["Damage"].level
                        projectile.enemiesCollided.append(enemy)
                        if len(projectile.enemiesCollided) > origin.upgradeList["Pierce"].level:
                            projectiles.remove(projectile)
                            break

    if gameState == GameMode.GAME_OVER_LOSE:
        reset_game()
        tempSurface.fill((0, 0, 0, 3))
        # TODO: Game Over Transition Visual Effect
        gameOverText = largeFont.render("You Died!!", True, color["Red"])
        playAgainButton.show(tempSurface, (0, 0, 0, 3), medFont, color["White"], None, False)
        mainMenuButton.show(tempSurface, (0, 0, 0, 3), medFont, color["White"], None, False)
        textRect = gameOverText.get_rect()
        textRect.center = (width//2, height//2 - 100)
        display_surface.blit(gameOverText, textRect)
        display_surface.blit(tempSurface, (0, 0))

    if gameState == GameMode.GAME_OVER_WIN:
        reset_game()
        tempSurface.fill((0, 0, 0, 3))
        gameOverText = largeFont.render("You Win!!", True, color["Green"])
        playAgainButton.show(tempSurface, (0, 0, 0, 3), medFont, color["White"], None, False)
        mainMenuButton.show(tempSurface, (0, 0, 0, 3), medFont, color["White"], None, False)
        textRect = gameOverText.get_rect()
        textRect.center = (width // 2, height // 2 - 100)
        display_surface.blit(gameOverText, textRect)
        display_surface.blit(tempSurface, (0, 0))

    # flip is all the way at the bottom
    pygame.display.flip()
