import pygame

class Projectile:
    # pos: Tuple[int, int]
    def __init__(self, originTower, spawnX, spawnY, x_dir, y_dir):
        self.originTower = originTower
        self.pos = (spawnX, spawnY)
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.enemiesCollided = []
        self.moving = True

    def show(self, surface, fillcolor):
        pygame.draw.circle(surface, fillcolor, (int(self.pos[0]), int(self.pos[1])), 10)

    def move(self, ff):
        if ff:
            self.pos = self.pos[0] + self.x_dir, self.pos[1] + self.y_dir
        else:
            self.pos = self.pos[0] + self.x_dir/2, self.pos[1] + self.y_dir/2


class ExplodingProjectile(Projectile):
    def __init__(self, originTower, spawnX, spawnY, x_dir, y_dir):
        Projectile.__init__(self, originTower, spawnX, spawnY, x_dir, y_dir)
        self.distanceTraveled = 0
        self.distanceToTarget = 0
        self.explosionTimer = 10
        self.exploding = False

