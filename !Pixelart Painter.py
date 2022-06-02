import pygame
import sys

pygame.init()

screen_size = width, height = (800, 600)
display_surface = pygame.display.set_mode(screen_size)

color = {'Red': (255, 0, 0),
         'Orange': (255, 120, 0),
         'Yellow': (255, 255, 0),
         'Green': (0, 180, 0),
         'Blue': (0, 0, 255),
         'Indigo': (75, 0, 130),
         'Pink': (255, 23, 197),
         'Purple': (238, 130, 238),
         'Grey': (128, 128, 128),
         'Brown': (125, 70, 20),
         'White': (255, 255, 255),
         'Black': (0, 0, 0)
         }


# global variables here
cellSize = 25
paletteSize = 50
backgroundColor = color['White']
stored_color = color['Black']
rows = (height - paletteSize*3)//cellSize

class Cell:
    def __init__(self, gridX, gridY, size):
        self.x = gridX
        self.y = self.y = gridY
        self.COLOR = backgroundColor
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.topleft = int(self.x*size), (self.y*size)


    def show(self):
        display_surface.fill(self.COLOR, self.rect)


class Slider:
    def __init__(self, x, y, leftText):
        self.x = x
        self.y = y
        self.value = 0
        self.text = leftText
        self.held = False
        self.sliderRect = sliderRect = pygame.Rect(0, 0, 20, 40)
        self.sliderRect.center = self.x + 105, self.y + 18

    def show(self):
        font = pygame.font.SysFont('arial', 32)
        text = font.render(self.text, True, color['Black'])
        textRect = text.get_rect()
        textRect.topright = self.x + 95, self.y
        display_surface.blit(text, textRect)
        pygame.draw.line(display_surface, color['Black'], (self.x + 105, self.y + 18),(self.x + 275, self.y + 18), 12)
        text = font.render(str(self.value), True, color['Black'])
        textRect = text.get_rect()
        textRect.topleft = self.x + 285, self.y
        display_surface.blit(text, textRect)

        display_surface.fill(color[self.text], self.sliderRect)


red_slider = Slider(60, height - 135, 'Red')
green_slider = Slider(60, height - 85, 'Green')
blue_slider = Slider(60, height - 35, 'Blue')

sliders = [red_slider, green_slider, blue_slider]


def mapRange(val , min1, max1, min2, max2):
    inputSpan = max1 - min1
    outputSpan = max2 - min2
    scaledValue = float(val - min1) / float(inputSpan)
    return min2 + (scaledValue * outputSpan)



# set up the initial field of cells
# cells is 1D - there are not seperate rows and columns
cells = []
for X in range(paletteSize, width, cellSize):
    for Y in range(0, cellSize*rows, cellSize):
        new_cell = Cell(X/cellSize+1/100000, Y//cellSize, cellSize)
        cells.append(new_cell)

palette = []
for Y in range(0, height, paletteSize):
    palette.append(Cell(0, Y//paletteSize, paletteSize))

i = 0
for key, value in color.items():
    palette[i].COLOR = value
    i += 1

custom_rect = pygame.Rect(0, 0, 80, 80)

clock = pygame.time.Clock()
while True:
    # force a frame rate of 60 fps
    # clock.tick(60)
    # get the mouse position each frame
    mouseX, mouseY = pygame.mouse.get_pos()

    custom_color = (red_slider.value, green_slider.value, blue_slider.value)
    
    # check the events, and if the QUIT event occurs, close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # give the option to close the window with ESC
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_b:
                stored_color = color['Blue']
            if event.key == pygame.K_z:
                stored_color = color['Black']
            if event.key == pygame.K_y:
                stored_color = color['Yellow']
            if event.key == pygame.K_g:
                stored_color = color['Green']
            if event.key == pygame.K_w:
                stored_color = color['White']
            if event.key == pygame.K_p:
                stored_color = color['Pink']
            if event.key == pygame.K_v:
                stored_color = color['Purple']
            if event.key == pygame.K_o:
                stored_color = color['Orange']
            if event.key == pygame.K_r:
                stored_color = color['Red']
            if event.key == pygame.K_s:
                pygame.image.save(display_surface, "Image.png")

        if pygame.mouse.get_pressed()[0]:
            click_pos = pygame.mouse.get_pos()
            for index, cell in enumerate(cells):
                if cell.rect.collidepoint(click_pos[0], click_pos[1]):
                    cell.COLOR = stored_color

            for slider in sliders:
                if slider.sliderRect.left < mouseX < slider.sliderRect.right and slider.sliderRect.top < mouseY < slider.sliderRect.bottom:
                    slider.sliderRect.centerx = mouseX
                if slider.sliderRect.left < slider.x + 105:
                    slider.sliderRect.left = slider.x + 105
                if slider.sliderRect.right > slider.x + 276:
                    slider.sliderRect.right = slider.x + 276

                slider.value = int(mapRange(slider.sliderRect.centerx, 175, 326, 0, 255))


        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = pygame.mouse.get_pos()
            for cell in palette:
                if cell.rect.collidepoint(click_pos[0], click_pos[1]):
                    stored_color = cell.COLOR
            if custom_rect.collidepoint(click_pos[0], click_pos[1]):
                stored_color = custom_color





    display_surface.fill(backgroundColor)  # this is the background
    # draw stuff here. The order determines the layers.

    for cell in cells:
        cell.show()

    for paletteCell in palette:
        paletteCell.show()

    red_slider.show()
    green_slider.show()
    blue_slider.show()


    for x in range(paletteSize, width, cellSize):
        if x == paletteSize:
            pygame.draw.line(display_surface, color['Black'], (x, 0), (x, height))
        else:
            pygame.draw.line(display_surface, color['Black'], (x, 0), (x, cellSize*rows))

    for y in range(0, cellSize*rows+cellSize, cellSize):
        pygame.draw.line(display_surface, color['Black'], (paletteSize, y), (width, y))

    custom_rect.centery = green_slider.sliderRect.centery
    custom_rect.centerx = 450

    display_surface.fill(custom_color, custom_rect)

    custom_rect_corners = [custom_rect.topleft, custom_rect.bottomleft, custom_rect.bottomright, custom_rect.topright]
    pygame.draw.lines(display_surface, color['Black'], True, custom_rect_corners)

    # flip is all the way at the bottom
    pygame.display.flip()