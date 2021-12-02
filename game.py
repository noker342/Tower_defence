import pygame
import random

pygame.init()
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
running = True


class Scorers_Tower:
    def __init__(self, x, y):
        self.width, self.height = 75, 75
        self.center = x, y
        self.x, self.y = x - self.width // 2, y - self.height // 2
        self.radius = 200
        self.boomRadius = 100
        self.tower = pygame.image.load('tower_1_lvl.jpeg')
        self.tower_rect = self.tower.get_rect(topleft=(x, y))

    def draw(self):
        screen.blit(self.tower, self.tower_rect)

    def checkRange(self, npc):
        npcInRange = []
        for i in range(len(npc)):
            xo = self.center[0] - npc[i].x
            yo = self.center[1] - npc[i].y
            distance = (xo ** 2 + yo ** 2) ** 0.5
            if distance <= self.radius:
                npcInRange.append((npc[i], distance))
        return npcInRange

    def chooseTarget(self, npc):
        npcInRange = self.checkRange(npc)
        if npcInRange:
            for i in range(len(npcInRange)):
                minimum = i
                for j in range(i + 1, len(npcInRange)):
                    if npcInRange[j][1] < npcInRange[minimum][1]:
                        minimum = j
                    npcInRange[minimum], npcInRange[i] = npcInRange[i], npcInRange[minimum]
        return npcInRange[0][0]

    def shot(self, npc, npc_array):
        for i in range(len(npc_array)):
        xo = npc.x - npc_array[i].x
        yo = npc.y - self.boomRadius
        boom = (xo ** 2 + yo ** 2) ** 0.5
        if boom <= self.boomRadius:
            health -= 100

class Npc:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)


scorers = Scorers_Tower(1920 // 2, 1080 // 2)
npc = []
for i in range(100):
    npc.append(Npc(width, height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((255, 255, 255))
    scorers.draw()
    scorers.checkRange(npc)
    scorers.chooseTarget(npc)
    scorers.shot(scorers.chooseTarget(npc), npc)
    pygame.display.flip()
