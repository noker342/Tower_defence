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
        self.radius = 300
        self.tower = pygame.image.load('tower_1_lvl.jpeg')
        self.tower_rect = self.tower.get_rect(center=(x, y))
        self.bombs = []
        self.calldown = 100
        self.curent_colldown = self.calldown

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

    def maintainTower(self, screen, npc):
        self.draw()
        self.shoot(npc)
        for bomb in self.bombs:
            bomb.move()
            bomb.draw(screen)
            bomb.explosion()
            if bomb.dead:
                for target in npc:
                    if ((target.rect.x - bomb.core_rect.x) ** 2 + (target.rect.y - bomb.core_rect.y) ** 2) ** 0.5 <= bomb.boomRadius:
                        target.hp -= bomb.damage
                self.bombs.remove(bomb)



        # 1) следит за ядрами мувает их следит за теми которые долетели и убирает их
        # 2) осуществляет прицеивание и стрельбу

    def calldownBomb(self):
        self.curent_colldown -= 1
        if self.curent_colldown == 0:
            self.curent_colldown = self.calldown
        return self.curent_colldown

    def shoot(self, npc):
        if scorers.checkRange(npc) and self.calldownBomb() == self.calldown:
            self.bombs.append(Core(self.center, self.chooseTarget(npc)))


class Core:
    def __init__(self, center, target):
        self.center = center
        self.x, self.y = self.center
        self.boomRadius = 50
        self.damage = 300
        self.speed = 5
        self.core = pygame.image.load('ball1.png')
        self.core = pygame.transform.scale(self.core, (40, 40))
        self.core_rect = self.core.get_rect(center=(self.x, self.y))
        self.explosion_animation = [pygame.image.load(f"boom{i}.png") for i in range(1, 6)]
        self.target = target
        self.hit = False
        self.dead = False

    def draw(self, screen):
        if self.explosion_animation and self.hit:
            screen.blit(self.explosion_animation[0], self.explosion_animation[0].get_rect(center=(self.core_rect.x, self.core_rect.y)))
            self.explosion_animation.pop(0)
        elif self.hit:
            self.dead = True
        else:
            screen.blit(self.core, self.core_rect)

    def move(self):
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
        self.core_rect.y -= dy

    def explosion(self):
        xo = self.core_rect.x - self.target.x
        yo = self.core_rect.y - self.target.y
        distanceFromEpicenter = (xo ** 2 + yo ** 2) ** 0.5
        if distanceFromEpicenter <= self.boomRadius:
            self.hit = True



class Npc:
    def __init__(self, width, height):
        self.x = width
        self.y = height
        self.hp = 500
        self.dead = False
        self.picture = pygame.image.load('boom1.png')
        self.rect = self.picture.get_rect(topleft=(self.x, self.y))

    def draw(self):
        screen.blit(self.picture, self.rect)

    def death(self):
        if self.hp <= 0:
            self.dead = True



scorers = Scorers_Tower(1920 // 2, 1080 // 2)
npc = [Npc(random.randint(300, 1600), random.randint(300, 700)) for _ in range(50)]
ai = True

# for i in range(100):
#     npc.append(Npc(width, height))
while running:
    i = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((255, 255, 255))
    for i in npc:
        i.draw()
        i.death()
        if i.dead:
            npc.remove(i)
    print(len(npc))
    scorers.maintainTower(screen, npc)
    pygame.display.flip()
    clock.tick(60)