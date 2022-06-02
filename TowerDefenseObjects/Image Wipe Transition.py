import pygame
import sys

pygame.init()

screen_size = width, height = (800, 600)
display_surface = pygame.display.set_mode(screen_size)

color = {'White': (255, 255, 255),
         'Black:': (0, 0, 0),
         'Red': (255, 0, 0),
         'Green': (0, 150, 0),
         'Blue': (0, 0, 255)
         }

images = [
"../TowerDefenseAssets/EthanTDlevel1.png"
"../TowerDefenseAssets/EthanTDlevel2.png"
]

imageIndex = 0


def beginWipeTransition(imagePath, direction):
    image = pygame.image.load(imagePath)
    if direction == 'right':
        pass
    if direction == 'left':
        pass


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
        # give the option to close the window with ESC
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RIGHT:
                beginWipeTransition(images[imageIndex+1 if imageIndex < len(images)-1 else 0], "right")
            if event.key == pygame.K_LEFT:
                beginWipeTransition(images[imageIndex+1 if imageIndex > 0 else len(images)-1], "left")

    display_surface.fill(color['Green'])  # this is the background
    # draw stuff here. The order determines the layers.

    # flip is all the way at the bottom
    pygame.display.flip()
