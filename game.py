import pygame

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
        self.masiv = []
        self.tower = pygame.image.load('tower_1_lvl.jpeg')
        self.tower_rect = self.tower.get_rect(topleft=(x, y))

    def Draw(self):
        screen.blit(self.tower, self.tower_rect)

    def CheckRange(self, npc):
        xo = self.center[0] - npc[0]
        yo = self.center[1] - npc[1]
        self.theorem = xo ** 2 + yo ** 2
        if self.theorem <= self.radius:
            self.masiv.append(self.theorem)
            print(True)

    def shot(self):
        if self.CheckRange:
            min_range = min(self.masiv)


scorers = Scorers_Tower(200, 200)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((255, 255, 255))
    scorers.Draw()
    scorers.CheckRange((210, 210))
    scorers.CheckRange((324, 210))
    scorers.shot()
    pygame.display.flip()