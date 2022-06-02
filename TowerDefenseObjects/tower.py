import pygame
import math
from TowerDefenseObjects.button import TowerUpgradeButton


class TowerUpgrade:
    def __init__(self, baseCost, costMultiplier):
        self.level = 0
        self.cost = [int(baseCost*costMultiplier*level) for level in range(1, 4)]


class Tower:
    # Constructor parameters
    # weaponType: string
    # speed: float
    # imagePath: string
    def __init__(self, cost, weaponType, attackRange, attackDamage, shotsPerSecond, imagePath=None):
        self.isValidPlacement = False
        self.sellValue = cost

        self.pos = pygame.math.Vector2()
        self.pos.x, self.pos.y = 0, 0

        # speed is shots per second. Maximum is 60 (60 fps)
        self.shotsPerSecond = shotsPerSecond
        self.numFramesToFullCharge = 60 // shotsPerSecond
        self.charge = self.numFramesToFullCharge

        self.priority = "First"
        self.targetEnemy = None

        self.weaponType = weaponType
        self.attackRange = attackRange
        self.modifiedAttackRange = attackRange
        self.attackDamage = attackDamage

        self.upgradeButtons = []

        self.image = None
        if imagePath is not None:
            self.image = pygame.image.load(imagePath)

    def show(self, surface, color=None):
        if self.targetEnemy is not None:
            # pygame.draw.line(surface, (0, 0, 0), (self.pos.x, self.pos.y), self.targetEnemy.floatPos, width=3)
            pass
        if self.image is not None:
            self.image = pygame.transform.smoothscale(self.image, (56, 75))
            image_rect = self.image.get_rect()
            image_rect.center = tuple(self.pos)
            surface.blit(self.image, image_rect)
        elif color is not None:
            pygame.draw.circle(surface, color, (int(self.pos.x), int(self.pos.y)), 25)
        else:
            print("This tower cannot be shown on the screen.")

    def change_priority(self):
        if self.priority == "Close":
            self.priority = "Strong"
        elif self.priority == "Strong":
            self.priority = "First"
        elif self.priority == "First":
            self.priority = "Close"

    def getEnemiesInRange(self, enemies):  # enemies is the global list
        enemiesInRange = []
        for enemy in enemies:
            if math.dist((self.pos.x, self.pos.y), (enemy.pos[0], enemy.pos[1])) < self.attackRange:
                enemiesInRange.append(enemy)
        return enemiesInRange

    def calculate_projectile_velocities(self, targetEnemy, speed):
        if targetEnemy is None:
            return 0, 0

        if (targetEnemy.pos[0] - self.pos.x) == 0:
            if targetEnemy.pos[1] > self.pos.y:
                angle = math.pi/2
            else:
                angle = (math.pi/2) * 3
        else:
            angle = math.atan((targetEnemy.pos[1] - self.pos.y) / (targetEnemy.pos[0] - self.pos.x)) + math.pi

        if targetEnemy.pos[0] - self.pos.x > 0:
            angle -= math.pi

        return speed*math.cos(angle), speed*math.sin(angle)

    def determineSingleTarget(self, enemiesInRange):
        targetEnemy = None
        closestDist = self.modifiedAttackRange
        if self.priority == "Close":
            for enemy in enemiesInRange:
                thisDist = math.dist((self.pos.x, self.pos.y), (enemy.pos[0], enemy.pos[1]))
                if thisDist < closestDist:
                    targetEnemy = enemy
                    closestDist = thisDist
        if self.priority == "Strong":
            targetEnemy = max(enemiesInRange, key=lambda enemy: enemy.health)
        if self.priority == "First":
            targetEnemy = max(enemiesInRange, key=lambda enemy: enemy.nextPathPointIndex)
        self.targetEnemy = targetEnemy
        return math.dist((self.pos.x, self.pos.y), (targetEnemy.pos[0], targetEnemy.pos[1]))


class Archer(Tower):
    cost = 200

    def __init__(self):
        # cost, weaponType, attackRange, attackDamage, shotsPerSecond
        Tower.__init__(self, self.cost, "TargetedProjectile", 150, 1, 1, "TowerDefenseAssets/TDArcher.png")
        self.upgradeList = {
            "Range": TowerUpgrade(self.cost, costMultiplier=0.75),
            "Damage": TowerUpgrade(self.cost, costMultiplier=1.5),
            "Pierce": TowerUpgrade(self.cost, costMultiplier=1.5),
            "Speed": TowerUpgrade(self.cost, costMultiplier=1.5)
        }
        self.initialProjectileSpeed = 13
        self.projectileSpeed = self.initialProjectileSpeed

        offset = 390
        for name, upgrade in self.upgradeList.items():
            self.upgradeButtons.append(TowerUpgradeButton(name, upgrade, 1000, offset))
            offset += 30

    def getEnemiesInRange(self, enemies):  # enemies is the global list
        self.modifiedAttackRange = self.attackRange + 50 * self.upgradeList["Range"].level
        enemiesInRange = []
        for enemy in enemies:
            if math.dist((self.pos.x, self.pos.y), (enemy.pos[0], enemy.pos[1])) < self.modifiedAttackRange:
                enemiesInRange.append(enemy)
        return enemiesInRange


class Gunner(Tower):
    cost = 400

    def __init__(self):
        # cost, weaponType, attackRange, attackDamage, shotsPerSecond
        Tower.__init__(self, self.cost, "TargetedProjectile", 200, 0.5, 4)
        self.upgradeList = {
            "Range": TowerUpgrade(self.cost, costMultiplier=0.75),
            "Damage": TowerUpgrade(self.cost, costMultiplier=1.5),
            "Pierce": TowerUpgrade(self.cost, costMultiplier=1.5),
            "Speed": TowerUpgrade(self.cost, costMultiplier=1.5)
        }
        self.initialProjectileSpeed = 13
        self.projectileSpeed = self.initialProjectileSpeed
        offset =390
        for name, upgrade in self.upgradeList.items():
            self.upgradeButtons.append(TowerUpgradeButton(name, upgrade, 1000, offset))
            offset += 30

    def getEnemiesInRange(self, enemies):
        self.modifiedAttackRange = self.attackRange + 50 * self.upgradeList["Range"].level
        enemiesInRange = []
        for enemy in enemies:
            if math.dist((self.pos.x, self.pos.y), (enemy.pos[0], enemy.pos[1])) < self.modifiedAttackRange:
                enemiesInRange.append(enemy)
        return enemiesInRange


class Sniper(Tower):
    cost = 500

    def __init__(self):
        # cost, weaponType, attackRange, attackDamage, shotsPerSecond
        Tower.__init__(self, self.cost, "TargetedInstant", 1500, 3, 0.65)
        self.upgradeList = {
            "Damage": TowerUpgrade(self.cost, costMultiplier=1.5),
            "Speed": TowerUpgrade(self.cost, costMultiplier=1.5)
        }
        self.attackRange = 2000
        offset = 390
        for name, upgrade in self.upgradeList.items():
            self.upgradeButtons.append(TowerUpgradeButton(name, upgrade, 1000, offset))
            offset += 30


class PoisonTower(Tower):
    cost = 600

    def __init__(self):
        Tower.__init__(self, self.cost, "AoE", 100, 1.5, 1)
        self.upgradeList = {
            "Range": TowerUpgrade(self.cost, costMultiplier=2),
            "Damage": TowerUpgrade(self.cost, costMultiplier=1.5),
            "Speed": TowerUpgrade(self.cost, costMultiplier=1.5)
        }
        offset = 390
        for name, upgrade in self.upgradeList.items():
            self.upgradeButtons.append(TowerUpgradeButton(name, upgrade, 1000, offset))
            offset += 30

    def getEnemiesInRange(self, enemies):
        self.modifiedAttackRange = self.attackRange + 50 * self.upgradeList["Range"].level
        enemiesInRange = []
        for enemy in enemies:
            if math.dist((self.pos.x, self.pos.y), (enemy.pos[0], enemy.pos[1])) < self.modifiedAttackRange:
                enemiesInRange.append(enemy)
        return enemiesInRange


class Catapult(Tower):
    cost = 300

    def __init__(self):
        Tower.__init__(self, self.cost, "ExplodingProjectile", 175, 1, 1)
        self.upgradeList = {
            "Range": TowerUpgrade(self.cost, costMultiplier=0.75),
            "Damage": TowerUpgrade(self.cost, costMultiplier=1.5),
            "Explosion": TowerUpgrade(self.cost, costMultiplier=1),
            "Speed": TowerUpgrade(self.cost, costMultiplier=1.5)
        }
        self.initialProjectileSpeed = 4
        self.projectileSpeed = self.initialProjectileSpeed
        self.explosionRadius = 75
        self.modifiedExplosionRadius = 75
        self.targetPos = None

        offset = 390
        for name, upgrade in self.upgradeList.items():
            self.upgradeButtons.append(TowerUpgradeButton(name, upgrade, 1000, offset))
            offset += 30

    def getEnemiesInRange(self, enemies):
        self.modifiedAttackRange = self.attackRange + 50 * self.upgradeList["Range"].level
        enemiesInRange = []
        for enemy in enemies:
            if math.dist((self.pos.x, self.pos.y), (enemy.pos[0], enemy.pos[1])) < self.modifiedAttackRange:
                enemiesInRange.append(enemy)
        return enemiesInRange


class Dragon(Tower):
    cost = 4000

    def __init__(self):

        Tower.__init__(self, self.cost, "TargetedProjectile", 1500, 0.5, 15)
        self.upgradeList = {
            "Fire": TowerUpgrade(self.cost, costMultiplier=1.5),
            "Damage": TowerUpgrade(self.cost, costMultiplier=1.5),
            "Pierce": TowerUpgrade(self.cost, costMultiplier=1.5),
            "Speed": TowerUpgrade(self.cost, costMultiplier=1.5)
        }
        self.initialProjectileSpeed = 50
        self.projectileSpeed = self.initialProjectileSpeed

        self.pathCenter = (400, 300)
        self.pathRadius = 200
        self.imgCenter = self.pathCenter

        self.originalImage = pygame.Surface((80, 80))
        self.originalImage.fill((255, 120, 0))
        self.originalImage.set_colorkey((0, 0, 0))

        self.rect = self.originalImage.get_rect()
        self.rect.center = self.pathCenter
        self.rotation_amount = 0
        self.rotation_speed = 1

        self.new_image = None

        self.fireballPoints = []

        offset = 390
        for name, upgrade in self.upgradeList.items():
            self.upgradeButtons.append(TowerUpgradeButton(name, upgrade, 1000, offset))
            offset += 30

    def move(self):
        # inverted sin/cos
        self.rotation_amount = (self.rotation_amount + self.rotation_speed) % 360
        self.new_image = pygame.transform.rotate(self.originalImage, self.rotation_amount)
        self.rect = self.new_image.get_rect()

        angleRadians = self.rotation_amount * (math.pi / 180)
        x = self.pathRadius * math.sin(self.rotation_amount * (math.pi / 180)) + self.pathCenter[0]
        y = self.pathRadius * math.cos(self.rotation_amount * (math.pi / 180)) + self.pathCenter[1]
        self.rect.center = (int(x), int(y))

        self.fireballPoints.clear()
        for r in range(52, 200, 10):
            px = r * math.sin(angleRadians + math.pi / 2) + x
            py = r * math.cos(angleRadians + math.pi / 2) + y
            self.fireballPoints.append((int(px), int(py)))

    def show(self, displaySurface, color=None):
        # pygame.draw.rect(display_surface, color["Orange"], self.rect)
        displaySurface.blit(self.new_image, self.rect)
        for point in self.fireballPoints:
            pygame.draw.circle(displaySurface, (255, 0, 0), point, 20 + self.fireballPoints.index(point) * 3)

    def getEnemiesInRange(self, enemies):
        return enemies

    def calculate_projectile_velocities(self, targetEnemy, speed):
        if targetEnemy is None:
            return 0, 0

        if (targetEnemy.pos[0] - self.rect.centerx) == 0:
            if targetEnemy.pos[1] > self.rect.centery:
                angle = math.pi/2
            else:
                angle = (math.pi/2) * 3
        else:
            angle = math.atan((targetEnemy.pos[1] - self.rect.centery) / (targetEnemy.pos[0] - self.rect.centerx)) + math.pi

        if targetEnemy.pos[0] - self.rect.centerx > 0:
            angle -= math.pi

        return speed * math.cos(angle), speed * math.sin(angle)


class Frost(Tower):
    cost = 350

    def __init__(self):
        Tower.__init__(self, self.cost, "AoE", 120, 0, 120)
        self.upgradeList = {
            "Range": TowerUpgrade(self.cost, costMultiplier=1.5),
            "Slow": TowerUpgrade(self.cost, costMultiplier=1.2),
            "Speed": TowerUpgrade(self.cost, costMultiplier=1.5)
        }
        offset = 390
        for name, upgrade in self.upgradeList.items():
            self.upgradeButtons.append(TowerUpgradeButton(name, upgrade, 1000, offset))
            offset += 30

    def getEnemiesInRange(self, enemies):
        self.modifiedAttackRange = self.attackRange + 50 * self.upgradeList["Range"].level
        enemiesInRange = []
        for enemy in enemies:
            if math.dist((self.pos.x, self.pos.y), (enemy.pos[0], enemy.pos[1])) < self.modifiedAttackRange:
                enemiesInRange.append(enemy)
        return enemiesInRange
