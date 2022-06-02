import pygame
import math
from TowerDefenseObjects.button import TowerUpgradeButton


class Tower:
    # Tower Peramaters
    # pos: Vector2
    # weaponType: string
    # speed: float
    # # imagePath: string
    def __init__(self, cost, weaponType, attackRange, attackDamage, attackSpeed, imagePath=None):
        self.isValidPlacement = False
        self.sellValue = cost

        self.pos = pygame.math.Vector2()
        self.pos.x, self.pos.y = 0, 0
        self.weaponType = weaponType
        # speed is shots per second. Maximum is 60(60 fps)
        self.attackSpeed = attackSpeed
        self.attackDamage = attackDamage
        self.chargeFrames = 60 // attackSpeed
        self.charge = self.chargeFrames
        self.targetEnemy = None
        self.priority = "First"
        self.attackRange = attackRange
        self.modifiedAttackRange = attackRange
        self.image = None

        self.upgradeLevel = {
            "Range": 0,
            "Speed": 0,
            "Pierce": 0,
            "Damage": 0,
        }

        self.new_upgradeLevel = {}

        self.upgradeButtons = []

        if imagePath is not None:
            self.image = pygame.image.load(imagePath)

    def show(self, surface, color=None):
        if color is not None:
            pygame.draw.circle(surface, color, (int(self.pos.x), int(self.pos.y)), 25)
        elif self.image is not None:
            image_rect = self.image.get_rect()
            image_rect_center = self.pos
            surface.blit(self.image, self.pos)
        else:
            print("This tower cannot be shown.")

    def change_priority(self):
        if self.priority == "Close":
            self.priority = "Strong"
        elif self.priority == "Strong":
            self.priority = "First"
        elif self.priority == "First":
            self.priority = "Close"

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

    # Calculate which enemy is the target:
    # First, check which enemies are in range
    # Second, determine single target based on priority

    def getEnemiesInRange(self, enemies):
        if "Range" in self.upgradeLevel.keys():
            self.modifiedAttackRange = self.attackRange + 50 * self.upgradeLevel["Range"]
        else:
            self.modifiedAttackRange = self.attackRange
        enemiesInRange = []
        for enemy in enemies:
            if math.dist((self.pos.x, self.pos.y), (enemy.pos[0], enemy.pos[1])) < self.modifiedAttackRange:
                enemiesInRange.append(enemy)
        return enemiesInRange

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
        Tower.__init__(self, self.cost, "Projectile", 150, 1, 1)
        self.initialProjectileSpeed = 13
        self.projectileSpeed = self.initialProjectileSpeed

        self.rangeCosts = [int(0.75 * level * self.cost) for level in range(1, 4, 1)]
        self.upgradeCosts = [int(1.5 * level * self.cost) for level in range(1, 4, 1)]

        offset = 430
        for upgrade in self.upgradeLevel.keys():
            self.upgradeButtons.append(TowerUpgradeButton(upgrade, 970, offset))
            offset += 30


class Gunner(Tower):
    cost = 400

    def __init__(self):
        Tower.__init__(self, self.cost, "Projectile", 200, 0.6, 4)
        self.initialProjectileSpeed = 13
        self.projectileSpeed = self.initialProjectileSpeed

        self.rangeCosts = [int(0.75 * level * self.cost) for level in range(1, 4, 1)]
        self.upgradeCosts = [int(1.5 * level * self.cost) for level in range(1, 4, 1)]

        offset = 430
        for upgrade in self.upgradeLevel.keys():
            self.upgradeButtons.append(TowerUpgradeButton(upgrade, 970, offset))
            offset += 30


class Sniper(Tower):
    cost = 500

    def __init__(self):
        Tower.__init__(self, self.cost, "Instant", 1500, 3, 0.65)
        del self.upgradeLevel["Pierce"]
        del self.upgradeLevel["Range"]
        self.attackRange = 1500

        self.upgradeCosts = [int(1.5 * level * self.cost) for level in range(1, 4, 1)]

        offset = 430
        for upgrade in self.upgradeLevel.keys():
            self.upgradeButtons.append(TowerUpgradeButton(upgrade, 970, offset))
            offset += 30


class PoisonTower(Tower):
    cost = 600

    def __init__(self):
        Tower.__init__(self, self.cost, "AoE", 100, 1.5, 1)

        self.rangeCosts = [int(2 * level * self.cost) for level in range(1, 4, 1)]
        self.upgradeCosts = [int(1.5 * level * self.cost) for level in range(1, 4, 1)]

        offset = 430
        for upgrade in self.upgradeLevel.keys():
            self.upgradeButtons.append(TowerUpgradeButton(upgrade, 970, offset))
            offset += 30


class Catapult(Tower):
    cost = 300

    def __init__(self):
        Tower.__init__(self, self.cost, "ExplodingProjectile", 175, 1, 1)
        self.initialProjectileSpeed = 4
        self.projectileSpeed = self.initialProjectileSpeed
        self.explosionRadius = 75
        self.modifiedExplosionRadius = 75
        self.targetPos = None
        del self.upgradeLevel["Pierce"]
        self.upgradeLevel["Explosion"] = 0
        self.rangeCosts = [int(0.75 * level * self.cost) for level in range(1, 4, 1)]
        self.upgradeCosts = [int(1.5 * level * self.cost) for level in range(1, 4, 1)]

        offset = 430
        for upgrade in self.upgradeLevel.keys():
            self.upgradeButtons.append(TowerUpgradeButton(upgrade, 970, offset))
            offset += 30
