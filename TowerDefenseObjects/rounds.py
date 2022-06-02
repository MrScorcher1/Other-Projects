from TowerDefenseObjects.enemy import *


class SpawnGroup:
    def __init__(self, delayFromRoundStart, enemyType, numEnemies, spawnInterval):
        self.delayFromRoundStart = delayFromRoundStart
        self.enemyType = enemyType
        self.numEnemies = numEnemies
        self.spawnInterval = spawnInterval * 2

        self.numEnemiesLaunched = 0
        self.stillSpawning = True

        self.spawnCharge = self.spawnInterval

    def spawn(self, enemies, points, angles):

        if self.stillSpawning:
            if self.enemyType == "Soldier":
                #2.5045
                enemies.append(Enemy(3, points, angles, 2.5,  1, "Red"))
                self.numEnemiesLaunched += 1
            elif self.enemyType == "Knight":
                enemies.append(Enemy(5, points, angles, 3.25, 1, "Yellow"))
                self.numEnemiesLaunched += 1
            elif self.enemyType == "Tank":
                #1.4862
                enemies.append(Enemy(20, points, angles, 1.5, 1, "Green"))
                self.numEnemiesLaunched += 1
            elif self.enemyType == "Juggernaut":
                enemies.append(Enemy(15, points, angles, 3, 1, (100, 100, 100)))
                self.numEnemiesLaunched += 1
        self.stillSpawning = (self.numEnemiesLaunched != self.numEnemies)


class Round:
    def __init__(self, roundNumber):
        self.spawns = []
        self.roundNumber = roundNumber
        if roundNumber == 1:
            self.spawns.append(SpawnGroup(delayFromRoundStart=0, enemyType="Soldier", numEnemies=10, spawnInterval=50))
        if roundNumber == 2:
            self.spawns.append(SpawnGroup(0, "Soldier", 12, 60))
            self.spawns.append(SpawnGroup(750, "Soldier", 5, 15))
        if roundNumber == 3:
            self.spawns.append(SpawnGroup(0, "Knight", 5, 25))
            self.spawns.append(SpawnGroup(250, "Soldier", 10, 10))
        if roundNumber == 4:
            self.spawns.append(SpawnGroup(0, "Knight", 12, 60))
        if roundNumber == 5:
            self.spawns.append(SpawnGroup(0, "Knight", 10, 35))
            self.spawns.append(SpawnGroup(0, "Soldier", 20, 17))
        if roundNumber == 6:
            self.spawns.append(SpawnGroup(0, "Knight", 10, 15))
            self.spawns.append(SpawnGroup(500, "Soldier", 50, 10))
        if roundNumber == 7:
            self.spawns.append(SpawnGroup(0, "Knight", 35, 25))
        if roundNumber == 8:
            self.spawns.append(SpawnGroup(0, "Knight", 10, 25))
            self.spawns.append(SpawnGroup(525, "Knight", 25, 15))
        if roundNumber == 9:
            self.spawns.append(SpawnGroup(0, "Tank", 2, 200))
        if roundNumber == 10:
            self.spawns.append(SpawnGroup(0, "Knight", 30, 16))
            self.spawns.append(SpawnGroup(0, "Knight", 20, 24))
        if roundNumber == 11:
            self.spawns.append(SpawnGroup(0, "Soldier", 100, 17))
        if roundNumber == 12:
            self.spawns.append(SpawnGroup(0, "Tank", 5, 100))
            self.spawns.append(SpawnGroup(50, "Knight", 10, 50))
        if roundNumber == 13:
            self.spawns.append(SpawnGroup(0, "Tank", 10, 75))
            self.spawns.append(SpawnGroup(250, "Soldier", 50, 17))
        if roundNumber == 14:
            self.spawns.append(SpawnGroup(0, "Knight", 50, 25))
        if roundNumber == 15:
            self.spawns.append(SpawnGroup(0, "Tank", 10, 50))
            self.spawns.append(SpawnGroup(100, "Knight", 25, 20))
        if roundNumber == 16:
            self.spawns.append(SpawnGroup(0, "Tank", 12, 40))
            self.spawns.append(SpawnGroup(600, "Knight", 25, 20))
        if roundNumber == 17:
            self.spawns.append(SpawnGroup(0, "Soldier", 30, 15))
            self.spawns.append(SpawnGroup(350, "Knight", 30, 15))
            self.spawns.append(SpawnGroup(550, "Tank", 12, 30))
        if roundNumber == 18:
            self.spawns.append(SpawnGroup(0, "Soldier", 30, 13))
            self.spawns.append(SpawnGroup(525, "Knight", 10, 10))
            self.spawns.append(SpawnGroup(1050, "Soldier", 30, 13))
            self.spawns.append(SpawnGroup(1575, "Knight", 15, 13))
            self.spawns.append(SpawnGroup(2100, "Soldier", 30, 13))
        if roundNumber == 19:
            pass



    def doneSpawning(self):
        for group in self.spawns:
            if group.stillSpawning:
                return False
        return True
