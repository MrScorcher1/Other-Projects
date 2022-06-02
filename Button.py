import pygame


class Button:
    def __init__(self, x, y, w, h, onclick=None, text=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.onclick = onclick
        self.text = text

    def show(self, surface, fillcolor, font=None, textColor=None, outlineColor=(255, 255, 255), outline=True):
        surface.fill(fillcolor, self.rect)
        if outline:
            pygame.draw.rect(surface, outlineColor, (self.rect.left - 3, self.rect.top - 3, self.rect.width + 6, self.rect.height + 6), border_radius=10, width=3)

        if self.text is not None:
            buttonText = font.render(self.text, True, textColor)
            textRect = buttonText.get_rect()
            textRect.center = self.rect.center[0], self.rect.center[1]
            surface.blit(buttonText, textRect)

    def hovered(self, mX, mY):
        return self.rect.collidepoint(mX, mY)