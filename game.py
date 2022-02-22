import pygame
import random

pygame.init()
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
running = True
clock = pygame.time.Clock()
picture = pygame.image.load('ball1.png')
picture = pygame.transform.scale(picture, (40, 40))


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

    def maintainTower(self, screen):
        self.draw()
        for bomb in self.bombs:
            bomb.move()
            bomb.draw(screen)
            bomb.explosion()
            if bomb.hit:
                self.bombs.remove(bomb)

        # 1) следит за ядрами мувает их следит за теми которые долетели и убирает их
        # 2) осуществляет прицеивание и стрельбу

    def calldownBomb(self):
        if self.calldown == 1000:
            self.calldown -= 1
        elif self.calldown == 0:
            self.calldown = 1000
        else:
            self.calldown -= 1

    def shoot(self, npc):
        if scorers.checkRange(npc):
            self.bombs.append(Core(self.center, self.chooseTarget(npc)))


class Core:
    def __init__(self, center, target):
        self.hit = False
        self.center = center
        self.x, self.y = self.center
        self.boomRadius = 100
        self.damage = 300
        self.speed = 2
        self.core = picture
        self.core_rect = self.core.get_rect(center=(self.x, self.y))
        self.explosion_animation = [pygame.image.load(f"boom{i}.png") for i in range(1, 6)]
        self.target = target

    def draw(self, screen):
        screen.blit(self.core, self.core_rect)

    def move(self):
        # if self.target.hp > 0:
        #     if self.x > self.target.x:
        #         self.x -= 1
        #     if self.x < self.target.x:
        #         self.x += 1
        #     if self.y > self.target.y:
        #         self.y -= 1
        #     if self.y < self.target.y:
        #         self.y += 1
        # self.core_rect = self.core.get_rect(center=(self.x, self.y))
        dx, dy = 0, 0
        dist_x = self.core_rect.x - self.target.x
        dist_y = self.core_rect.y - self.target.y
        dist = (dist_x ** 2 + dist_y ** 2) ** 0.5
        if dist:
            cos = round(dist_x / dist, 2)
            sin = round(dist_y / dist, 2)
            if dist_x != 0 and dist_y != 0:
                dx, dy = -self.speed * cos, self.speed * sin
            if cos == 1 or cos == -1:
                dx = -cos * self.speed
            if sin == 1 or sin == -1:
                dy = -sin * self.speed
        self.core_rect.x += dx
        self.core_rect.y += dy
        print(dx, dy)

    def explosion(self):
        for i in range(len(npc)):
            xo = self.target.x - npc[i].x
            yo = self.target.y - npc[i].y
            distanceFromEpicenter = (xo ** 2 + yo ** 2) ** 0.5
            if distanceFromEpicenter <= self.boomRadius:
                self.target.hp -= self.damage
        self.hit = True


class Npc:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.hp = 1000
        self.picture = pygame.image.load('boom1.png')
        self.picture_rect = self.picture.get_rect(topleft=(self.x, self.y))

    def draw(self):
        screen.blit(self.picture, self.picture_rect)


scorers = Scorers_Tower(1920 // 2, 1080 // 2)
npc = []
ai = True

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
    scorers.checkRange(npc)
    for i in npc:
        if i == scorers.chooseTarget(npc):
            i.draw()
    scorers.shoot(npc)
    scorers.calldownBomb()
    scorers.maintainTower(screen)
    pygame.display.flip()
    clock.tick(60)
