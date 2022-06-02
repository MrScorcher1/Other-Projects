import math
import sys
from enum import IntEnum

import pygame
from pygame import Vector2
from pygame import mixer, mixer_music
import random

pygame.mixer.init()
pygame.init()

screen_size = width, height = (800, 600)
display_surface = pygame.display.set_mode(screen_size)

color = {
         'Red': (255, 0, 0),
         'Orange': (255, 120, 0),
         'Yellow': (255, 255, 0),
         'Green': (0, 150, 0),
         'Blue': (0, 0, 255),
         'Indigo': (75, 0, 130),
         'Pink': (255, 23, 197),
         'Violet': (238, 130, 238),
         'Grey': (128, 128, 128),
         'Brown': (125, 70, 20),
         'White': (255, 255, 255),
         'Black': (0, 0, 0)
         }

class GameState(IntEnum):
    MENU = 1
    PLAY = 2
    GAMEOVER_WIN = 3
    GAMEOVER_LOSE = 4


class Difficulty:
    EASY = 35
    MEDIUM = 50
    HARD = 100

current_state = GameState.MENU
clock = pygame.time.Clock()
frame = 0
frameRate = 120
key_press = 0
difficulty = 100
health = 100
timer = 60
ballPhase = 1
isPlaying = 0
mouseX, mouseY = 0, 0
font = pygame.font.SysFont("arialblack", 50)
medFont = pygame.font.SysFont("arialblack", 41)
smallFont = pygame.font.SysFont("arialblack", 28)
titleFont = pygame.font.SysFont("arialblack", 50)
infinite = False

ball_image = pygame.image.load(("ExtremeDodgeballAssets/ball.png"))
player_image = pygame.image.load(("ExtremeDodgeballAssets/player.png"))
enemy_image = pygame.image.load(("ExtremeDodgeballAssets/enemy.png"))

boss_music = "ExtremeDodgeballAssets/bossmusic.mp3"
bounce1 = "ExtremeDodgeballAssets/bounce1.mp3"
bounce2 = "ExtremeDodgeballAssets/bounce2.mp3"
bounce3 = "ExtremeDodgeballAssets/bounce3.mp3"

steps1 = "C:/Users/Ethan/PycharmProjects/PythonPresentation/ExtremeDodgeballAssets/steps1(online).wav"
steps2 = "C:/Users/Ethan/PycharmProjects/PythonPresentation/ExtremeDodgeballAssets/steps2(online).wav"
steps3 = "C:/Users/Ethan/PycharmProjects/PythonPresentation/ExtremeDodgeballAssets/steps3(online).wav"
steps4 = "C:/Users/Ethan/PycharmProjects/PythonPresentation/ExtremeDodgeballAssets/steps4(online).wav"

step_sounds = [steps1, steps2, steps3, steps4]
bounce_sounds = [bounce1, bounce2, bounce3]


class Button:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.onclick = None

    def show(self):
        display_surface.fill(color["White"], self.rect)

    def hovered(self):
        return self.rect.collidepoint(mouseX, mouseY)


class Character:
    def __init__(self, x, y):
        pos = Vector2()
        pos.x = x
        pos.y = y
        self.pos = pos


# child class
class Player(Character):
    def __init__(self, name, x, y):    # child constructor
        Character.__init__(self, x, y) # super constructor
        self.name = name               # attributes unique to Players
        self.speed = 2

    def show(self):
        circle_pos = tuple(self.pos)
        #pygame.draw.circle(display_surface, color["Green"], (int(circle_pos[0]), int(circle_pos[1])), 20)
        display_surface.blit(player_image, (int(self.pos.x-17), int(self.pos.y-26)))


class Enemy(Character):
    def __init__(self, x, y):
        Character.__init__(self, x, y)

    def show(self):
        circle_pos = tuple(self.pos)
        pygame.draw.circle(display_surface, color["Red"], (int(circle_pos[0]), int(circle_pos[1])), 20)
        display_surface.blit(enemy_image, (int(self.pos.x-23), int(self.pos.y-28)))

class Projectile:

    def __init__(self, spawnX, spawnY, dir):
        self.pos = (spawnX, spawnY)
        self.x_dir = dir[0]
        self.y_dir = dir[1]

    def show(self):
        display_surface.blit(ball_image, (int(self.pos[0]-10), int(self.pos[1]-10)))

    def move(self):
        self.pos = self.pos[0] + self.x_dir, self.pos[1] + self.y_dir


projectiles = []


player = Player("Player1", 50, height//2)


targetpos = Vector2()

easy_button = Button(width//2 - 340, height//2 - 60, 200, 80)
med_button = Button(width//2 - 100, height//2 - 60, 200, 80)
hard_button = Button(width//2 + 140, height//2 - 60, 200, 80)
startGame_button = Button(width//2 - 195, height//2 + 60, 390, 90)
infiniteMode_button = Button(width//2 - 120, height//2 + 190, 240, 60)
title_text = Button(width//2 - 300, height//2 - 235, 500, 150)

buttons = [easy_button, med_button, hard_button, startGame_button, infiniteMode_button, title_text]

def switch_to_easy():
    global difficulty
    difficulty = Difficulty.EASY

def switch_to_medium():
    global difficulty
    difficulty = Difficulty.MEDIUM

def switch_to_hard():
    global difficulty
    difficulty = Difficulty.HARD

def toggle_infinite():
    global infinite
    global timer
    infinite = True
    start_game()
    switch_to_hard()
    timer = 100

def start_game():
    global current_state
    global isPlaying
    current_state = GameState.PLAY
    player.pos = Vector2(50, height//2)
    if isPlaying == 0:
        pygame.mixer.music.load(boss_music)
        pygame.mixer.music.play(-1)
        isPlaying = 1

easy_button.onclick = switch_to_easy
med_button.onclick = switch_to_medium
hard_button.onclick = switch_to_hard
startGame_button.onclick = start_game
infiniteMode_button.onclick = toggle_infinite


def dist(p1, p2):
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)


while True:
    # force a frame rate of 60 fps
    clock.tick(frameRate)
    frame += 1
    # get the mouse position each frame
    mouseX, mouseY = pygame.mouse.get_pos()
    # check the events, and if the QUIT event occurs, close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # give the option to close the window with ESC
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == GameState.MENU:
                for button in buttons:
                    if button.hovered() and button.onclick is not None:
                        button.onclick()


    display_surface.fill(color['Black'])

    if current_state == GameState.MENU:
        infinite = False
        boss = Enemy(width - 80, 100)
        startDir = 179.5237
        projectile_x = 2 * math.cos(startDir)
        projectile_y = 2 * math.sin(startDir)
        projectile_pos = (projectile_x, projectile_y)
        if frame % (frameRate//2) == 0:
            projectiles.append(Projectile(int(boss.pos.x), int(boss.pos.y), projectile_pos))
        for projectile in projectiles:
            projectile.move()
            projectile.show()
            if projectile.pos[0] < -10 or projectile.pos[0] > 810 or projectile.pos[1] < -10 or projectile.pos[1] > 610:
                projectiles.remove(projectile)
        for button in buttons:
            button.show()
        easyText = font.render("EASY", True, color['Black'])
        medText = medFont.render("MEDIUM", True, color['Black'])
        hardText = font.render("HARD", True, color['Black'])
        startGameText = font.render("START GAME", True, color['Blue'])
        infiniteText = smallFont.render("INFINITE MODE", True, color['Black'])
        titleText = titleFont.render("EXTREME DODGEBALL", True, color['Green'])

        easyTextRect = easyText.get_rect()
        easyTextRect.center = easy_button.rect.center
        medTextRect = medText.get_rect()
        medTextRect.center = med_button.rect.center
        hardTextRect = hardText.get_rect()
        hardTextRect.center = hard_button.rect.center
        startGameTextRect = startGameText.get_rect()
        startGameTextRect.center = startGame_button.rect.center
        infiniteTextRect = infiniteText.get_rect()
        infiniteTextRect.center = infiniteMode_button.rect.center
        titleTextRect = titleText.get_rect()
        titleTextRect.center = title_text.rect.center

        texts = [easyText, medText, hardText, startGameText, infiniteText, titleText]
        textRects = [easyTextRect, medTextRect, hardTextRect, startGameTextRect, infiniteTextRect, titleTextRect]

        display_surface.fill(color['Black'], titleTextRect)
        display_surface.fill(color['Black'], title_text)

        for i in range(len(texts)):
            display_surface.blit(texts[i], textRects[i])

    if current_state == GameState.PLAY:

        if pygame.key.get_pressed()[119] and player.pos.y > 20:
            player.pos.y -= player.speed
            pygame.mixer.Sound(steps1).play()

        if pygame.key.get_pressed()[115] and player.pos.y < height-20:
            player.pos.y += player.speed
            pygame.mixer.Sound(steps2).play()

        if pygame.key.get_pressed()[97] and player.pos.x > 20:
            player.pos.x -= player.speed
            pygame.mixer.Sound(steps3).play()

        if pygame.key.get_pressed()[100] and player.pos.x < width-20:
            player.pos.x += player.speed
            pygame.mixer.Sound(steps4).play()

        if (player.pos.x - boss.pos.x) == 0:
            if player.pos.y > boss.pos.y:
                angle = math.pi/2
            else:
                angle = (math.pi/2) * 3
        else:
            angle = math.atan((player.pos.y - boss.pos.y) / (player.pos.x - boss.pos.x)) + math.pi

        if (player.pos.x - boss.pos.x) > 0:
            angle -= math.pi

        projectile_x = 2 * math.cos(angle)
        projectile_y = 2 * math.sin(angle)
        projectile_pos = (projectile_x, projectile_y)

        if frame % timer//1 == 0:
            projectiles.append(Projectile(int(boss.pos.x), int(boss.pos.y), projectile_pos))
            if infinite:
                timer -= 0.2
                if timer < 20:
                    timer = 20

        display_surface.fill(color['Black'])  # this is the background
        # draw stuff here. The order determines the layers.

        player.show()

        for projectile in projectiles:
            projectile.move()
            projectile.show()
            if projectile.pos[0] < -10 or projectile.pos[0] > 810 or projectile.pos[1] < -10 or projectile.pos[1] > 610:
                projectiles.remove(projectile)

            proj_pos = Vector2()
            proj_pos.x, proj_pos.y = projectile.pos[0], projectile.pos[1]
            if dist(proj_pos, player.pos) <= (10 + 20):
                health -= difficulty
                projectiles.remove(projectile)
                if health <= 0:
                    print('You Lose')
                    current_state = GameState.GAMEOVER_LOSE

        if (not infinite) and dist(player.pos, boss.pos) <= (20 + 20):
            print('You Win!')
            current_state = GameState.GAMEOVER_WIN

        # vec2 = Vector2.lerp(Vec2, float)
        targetpos.x, targetpos.y = width-50, player.pos.y

        boss.pos = Vector2.lerp(boss.pos, targetpos, 0.0175)

    boss.show()

    if current_state == GameState.GAMEOVER_LOSE:
        display_surface.blit(pygame.image.load('ethangameover_lose.png'), (0, 0))
        projectiles.clear()
        health = 100
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            current_state = GameState.MENU

    if current_state == GameState.GAMEOVER_WIN:
        display_surface.blit(pygame.image.load('ethangameover_win.png'), (0, 0))
        projectiles.clear()
        health = 100
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            current_state = GameState.MENU


    # flip is all the way at the bottom
    pygame.display.flip()