import pygame
import random

pygame.init()
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
running = True
clock = pygame.time.Clock()


class Scorers_Tower:
    def __init__(self, x, y):
        self.width, self.height = 75, 75
        self.center = x, y
        self.x, self.y = x - self.width // 2, y - self.height // 2
        self.radius = 200
        self.tower = pygame.image.load('tower_1_lvl.jpeg')
        self.tower_rect = self.tower.get_rect(center=(x, y))
        self.bombs = []
        self.calldown = 1000

    def draw(self):
        screen.blit(self.tower, self.tower_rect)

    def checkRange(self, npc):
        npcInRange = []
        for i in range(len(npc)):
            print(npc[i])
            xo = self.center[0] - npc[i].x
            yo = self.center[1] - npc[i].y
            distance = (xo ** 2 + yo ** 2) ** 0.5
            if distance <= self.radius:
                if self.calldown == 1000:
                    self.bombs.append(Core((1920 // 2, 1080 // 2), scorers.chooseTarget(scorers.checkRange(npc))))
                    self.calldown -= 1
                elif self.calldown == 0:
                    self.calldown = 1000
                else:
                    self.calldown -= 1
                npcInRange.append((npc[i], distance))
                print(self.bombs)
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

    def maintainTower(self, npc_array, screen):
        for bomb in self.bombs:
            bomb.move(npc_array)
            bomb.draw(screen)
            bomb.explosion(npc_array)
            if bomb.hit:
                self.bombs.remove(bomb)

        # 1) следит за ядрами мувает их следит за теми которые долетели и убирает их
        # 2) осуществляет прицеивание и стрельбу


class Core:
    def __init__(self, center, target):
        self.hit = False
        self.center = center
        self.x, self.y = self.center
        self.boomRadius = 100
        self.damage = 300
        self.core = pygame.image.load('ball1.png')
        self.core_rect = self.core.get_rect(center=(self.x, self.y))
        self.explosion_animation = [pygame.image.load(f"boom{i}.png") for i in range(1, 6)]
        self.target = target

    def draw(self, screen):
        if self.hit:
            if self.explosion_animation:
                screen.blit(self.explosion_animation[0], self.core_rect)
                self.explosion_animation.pop(0)
        else:
            screen.blit(self.core, self.core_rect)

    def move(self, npc_array):
        for i in range(len(npc_array)):
            if npc_array[i][0].hp > 0:
                if self.x > npc_array[i][0].x:
                    self.x -= 1
                    self.core_rect = self.core.get_rect(center=(self.x, self.y))
                if self.x < npc_array[i][0].x:
                    self.x += 1
                    self.core_rect = self.core.get_rect(center=(self.x, self.y))
                if self.y > npc_array[i][0].y:
                    self.y -= 1
                    self.core_rect = self.core.get_rect(center=(self.x, self.y))
                if self.y < npc_array[i][0].y:
                    self.y += 1
                    self.core_rect = self.core.get_rect(center=(self.x, self.y))

    def explosion(self, npc_array):
        if npc_array and self.target:
            for i in range(len(npc_array)):
                if self.target[0] == npc_array[i].x and self.target[1] == npc_array[i].y:
                    xo = self.target[0] - npc_array[i].x
                    yo = self.target[1] - npc_array[i].y
                    distanceFromEpicenter = (xo ** 2 + yo ** 2) ** 0.5
                    if distanceFromEpicenter <= self.boomRadius:
                        npc_array[i].hp -= self.damage
            self.hit = True


class Npc:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.hp = 1000


scorers = Scorers_Tower(1920 // 2, 1080 // 2)
npc = []
ai = True
c = Core((1920 // 2, 1080 // 2), scorers.chooseTarget(scorers.checkRange(npc)))

for i in range(100):
    npc.append(Npc(width, height))
while running:
    i = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((255, 255, 255))
    scorers.draw()
    c.draw(screen)
    scorers.maintainTower(scorers.checkRange(npc), screen)
    scorers.checkRange(npc)
    pygame.display.flip()
    clock.tick(60)
