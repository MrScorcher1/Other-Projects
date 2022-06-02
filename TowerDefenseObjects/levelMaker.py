import pygame
import sys

pygame.init()

screen_size = width, height = (800, 600)

display_surface = pygame.display.set_mode(screen_size)

level_image = pygame.image.load("../TowerDefenseAssets/EthanTDlevel3.png")

level_pathpoints_file = open("pathpoints.txt", "w")

testPoints = [
]

entriesInRow = 0

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            level_pathpoints_file.close()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if entriesInRow < 6:
                testPoints.append((mouseX, mouseY))
                level_pathpoints_file.write(str((mouseX, mouseY))+", ")
                entriesInRow += 1
            else:
                entriesInRow = 0
                level_pathpoints_file.write("\n")
    display_surface.fill((0, 0, 0))
    display_surface.blit(level_image, pygame.Rect(0, 0, 800, 600))

    for point in testPoints:
        pygame.draw.circle(display_surface, (0, 0, 255), point, 10)
    
    if len(testPoints) > 1:
        pygame.draw.lines(display_surface, (255, 255, 255), False, testPoints, 3)
    pygame.display.flip()
