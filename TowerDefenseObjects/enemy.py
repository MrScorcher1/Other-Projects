import pygame
import math

color = {
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Red": (255, 0, 0),
    "Orange": (255, 120, 0),
    "Yellow": (255, 255, 0),
    "Green": (0, 180, 0),
    "Blue": (0, 0, 255),
    "Purple": (195, 33, 204),
    "Pink": (255, 23, 197)
}


class Enemy:
    def __init__(self, maxHealth, pathPoints, pathPointAngles, speed, baseDamage, colorValue, immunity=None):
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.path = pathPoints
        self.nextPathPointIndex = 1
        self.pos = self.path[0]
        self.floatPos = self.pos
        self.movementAngles = pathPointAngles
        self.moveAngle = pathPointAngles[0]
        self.speed = speed
        self.baseDamage = baseDamage
        self.immunity = immunity
        self.color = color[colorValue]
        self.originalSpeed = speed

        self.distTraveled = 0

    def move(self, loadedMap, ff):
        moddedSpeed = self.speed if ff else self.speed / 2

        xVel = moddedSpeed * math.cos(self.moveAngle)
        yVel = moddedSpeed * math.sin(self.moveAngle)
        self.floatPos = (self.floatPos[0] + xVel, self.floatPos[1] + yVel)

        # If we have successfully "collided" with the next path point, change the angle (and next point).
        if math.dist(self.pos, self.path[self.nextPathPointIndex]) < 9:
            self.moveAngle = self.movementAngles[self.nextPathPointIndex]
            self.nextPathPointIndex += 1
            self.distTraveled = 0
        else:
            # Either we are still heading towards the point, or we have overshot. If we overshot, actively correct

            # handle overshoot
            if self.distTraveled > loadedMap.pointDistances[self.nextPathPointIndex - 1]:
                print("Overshot")
                self.nextPathPointIndex += 1

                deltaX = loadedMap.pathPoints[self.nextPathPointIndex][1] - self.pos[0]
                deltaY = loadedMap.pathPoints[self.nextPathPointIndex][0] - self.pos[1]
                self.moveAngle = math.atan2(deltaY, deltaX)
            else:
                self.distTraveled += math.dist(self.floatPos, self.pos)

        self.pos = self.floatPos


    def showBody(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, 20)

    def showHealthBar(self, surface):
        if 0 < self.health < self.maxHealth:
            barRect = pygame.Rect(0, 0, 40, 6)
            barRect.center = self.floatPos[0], self.floatPos[1] - 25
            healthRect = pygame.Rect(0, 0, (self.health / self.maxHealth) * 40, 6)
            healthRect.topleft = barRect.topleft
            surface.fill((0, 0, 0), barRect)
            pygame.draw.rect(surface, (0, 200, 0), healthRect)

