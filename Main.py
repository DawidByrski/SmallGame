import pygame
import sys
import random
from pygame.locals import *

pygame.init()

DISPLAY_SIZE = (1000, 800)
SPEED = (DISPLAY_SIZE[0]//100 + DISPLAY_SIZE[1]//100)//2
DISPLAY = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption('MiniGame')

FPS = 30
FPS_CLOCK = pygame.time.Clock()

minimum_time = 0
done = False
#Lost = False

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

platform = pygame.Rect(DISPLAY_SIZE[0]//2, DISPLAY_SIZE[1]-100, 100, 10)
kill_zone = pygame.Rect(0, DISPLAY_SIZE[1]-10, DISPLAY_SIZE[0], 10)
print(SPEED)


class Ball:
    def __init__(self):
        self.x = 250
        self.y = 200
        self.vel = {
            "x": random.choice([SPEED, SPEED*-1])+random.choice([SPEED//5, SPEED//5*-1]),
            "y": SPEED*-1+random.choice([SPEED//5, SPEED//5*-1])
        }
        self.radius = 10
        self.rect = pygame.Rect(self.x-self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)

    def __del__(self):
        return None

    def update(self):
        if self.x <= 0 or self.x >= DISPLAY_SIZE[0]:
            self.vel["x"] *= -1
        if self.y <= 0 or self.y >= DISPLAY_SIZE[1] or platform.colliderect(self.rect):
            self.vel["y"] *= -1
        self.x += self.vel["x"]
        self.y += self.vel["y"]
        self.rect.center = (self.x, self.y)
        pygame.draw.circle(DISPLAY, GREEN, (self.x, self.y), self.radius)


ball_num = 1
balls = list()
balls.append(Ball())

while not done:
    DISPLAY.fill(BLACK)
    pygame.draw.rect(DISPLAY, RED, kill_zone)
    platform.centerx = pygame.mouse.get_pos()[0]
    pygame.draw.rect(DISPLAY, BLUE, platform)
    for i in range(0, len(balls)):
        if len(balls) >= i:
            if balls[i].y >= DISPLAY_SIZE[1]-10:
                balls.pop(i)
                ball_num = ball_num - 1
            else:
                balls[i].update()
    if ball_num == 0:
        print(ball_num)
        print("game lost")
    pygame.display.flip()
    if random.randint(0, 100) == 1 and minimum_time >= 150:
        minimum_time = 0
        ball_num = ball_num + 1
        print(ball_num)
        balls.append(Ball())
    minimum_time += 1
    for e in pygame.event.get():
        if e.type == QUIT or pygame.key.get_pressed()[pygame.K_q]:
            pygame.quit()
            sys.exit()
    FPS_CLOCK.tick(FPS)
