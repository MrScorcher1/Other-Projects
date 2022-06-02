from pygame import image
import math

pathPoints = [
[
        (0, 75),    (38, 75),   (75, 75),   (111, 75),  (151, 75),  (187, 75),
        (224, 75),  (270, 72),  (312, 70),  (352, 70),  (384, 68),  (428, 66),
        (467, 65),  (516, 60),  (558, 60),  (599, 57),  (631, 60),  (669, 66),
        (701, 80),  (724, 106), (736, 144), (744, 182), (744, 220), (744, 257),
        (744, 294), (744, 334), (740, 373), (731, 407), (713, 445), (681, 465),
        (646, 472), (604, 471), (562, 464), (525, 439), (504, 402), (506, 357),
        (526, 319), (559, 301), (583, 273), (588, 233), (569, 195), (533, 178),
        (495, 168), (453, 162), (413, 164), (373, 172), (343, 188), (332, 232),
        (341, 268), (363, 297), (385, 332), (401, 368), (395, 412), (367, 442),
        (326, 459), (287, 467), (242, 453), (211, 416), (202, 369), (201, 321),
        (207, 281), (208, 243), (200, 204), (163, 186), (122, 181), (77, 181),
        (49, 200),  (45, 241),  (54, 281),  (57, 321),  (62, 361),  (62, 403),
        (59, 435),  (58, 480),  (64, 516),  (94, 536),  (130, 540), (173, 540),
        (211, 540), (251, 540), (291, 540), (336, 540), (382, 540), (424, 540),
        (459, 540), (507, 540), (538, 540), (581, 540), (618, 540), (662, 540),
        (703, 540), (748, 540), (794, 540), (800, 540), (800, 540)
    ],
    [
        (0, 297), (122, 297), (122, 113), (238, 113), (238, 542), (369, 542), (369, 22),
        (474, 22), (474, 549), (574, 549), (574, 114), (689, 114), (689, 298), (795, 298), (795, 298)
    ],
    [
        (2, 265), (24, 263), (41, 262), (89, 263), (142, 262), (152, 226),
        (175, 198), (202, 164), (228, 136), (258, 111), (291, 95), (325, 82),
        (368, 71), (410, 67), (439, 79), (470, 99), (501, 120), (527, 145),
        (556, 173), (583, 201), (607, 238), (627, 279), (639, 326), (643, 373),
        (643, 431), (618, 469), (591, 497), (535, 523), (481, 537), (426, 541),
        (367, 536), (319, 508), (279, 476), (251, 439), (231, 396), (227, 344),
        (237, 281), (257, 239), (292, 205), (324, 192), (356, 194), (386, 205),
        (425, 226), (453, 252), (477, 279), (487, 312), (487, 350), (481, 379),
        (440, 386), (402, 369), (376, 342), (360, 314), (324, 314), (306, 336),
        (307, 368), (315, 399), (326, 422), (354, 431), (390, 437), (424, 442),
        (469, 446), (510, 435), (541, 422), (564, 384), (570, 347), (563, 310),
        (542, 267), (512, 236), (483, 201), (466, 173), (424, 144), (374, 139),
        (323, 144), (274, 163), (238, 197), (203, 228), (178, 269), (157, 311),
        (145, 352), (136, 406), (147, 452), (160, 484), (181, 512), (205, 535),
        (241, 567), (287, 590), (470, 588), (524, 586), (572, 575), (614, 552),
        (646, 521), (671, 492), (690, 452), (707, 405), (719, 371), (722, 325),
        (717, 285), (799, 280), (799, 280)

    ]
]


class Map:
    def __init__(self, number):
        self.image = image.load("TowerDefenseAssets/EthanTDlevel" + str(number)+".png")
        self.pathPoints = pathPoints[number - 1]
        self.number = number
        self.pointDistances = []

        new_pathPoints = []
        for i, point in enumerate(self.pathPoints[:-1]):
            pX, pY = point
            next_pX, next_pY = self.pathPoints[i+1]
            new_pathPoints.append(point)

            minimumPointSpacing = 20
            pointsNeeded = math.dist(point, self.pathPoints[i+1]) // minimumPointSpacing

            if math.dist(point, self.pathPoints[i+1]) > 30:
                angle = math.atan2((next_pY - pY), (next_pX - pX))
                deltaY = minimumPointSpacing*math.sin(angle)
                deltaX = minimumPointSpacing*math.cos(angle)
                for spacing in range(1, int(pointsNeeded)):
                    new_pathPoints.append((int(pX + deltaX * spacing), int(pY + deltaY * spacing)))

        self.pathPoints = new_pathPoints
        self.pathPoints.append(pathPoints[number - 1][-1])
        self.pointAngles = []

        for i, point in enumerate(self.pathPoints):
            if i == len(self.pathPoints) - 1:
                continue
            self.pointDistances.append(math.dist(point, self.pathPoints[i + 1]))

            if self.pathPoints[i + 1][0] - point[0] == 0:
                if self.pathPoints[i + 1][1] > point[1]:
                    self.pointAngles.append(math.pi / 2)
                else:
                    self.pointAngles.append(-1 * math.pi / 2)
            else:
                self.pointAngles.append(math.atan2(self.pathPoints[i+1][1] - point[1], self.pathPoints[i+1][0] - point[0]))

        print(list(map(lambda x: x*(180/math.pi), self.pointAngles)))