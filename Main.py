import pygame
import sys
import random
from pygame.locals import *

pygame.init()

mode = "game"
DISPLAY_SIZE = (1000, 800)
SPEED = (DISPLAY_SIZE[0]//100 + DISPLAY_SIZE[1]//100)//2
DISPLAY = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption('MiniGame')

FPS = 30
FPS_CLOCK = pygame.time.Clock()

minimum_time = 0
done = False

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

FONT = pygame.font.Font('freesansbold.ttf', 32)
TEXT_LOSE = FONT.render('YOU LOST', True, RED)
TEXT_QUIT = FONT.render('QUIT', True, BLACK)
TEXT_RESET = FONT.render('AGAIN', True, BLACK)
text_rect = TEXT_LOSE.get_rect()
text_rect.center = (DISPLAY_SIZE[0]//2, DISPLAY_SIZE[1]//2)

button_reset_rect = pygame.Rect(DISPLAY_SIZE[0]//2-150, DISPLAY_SIZE[1]//2+100, 120, 40)
button_quit_rect = pygame.Rect(DISPLAY_SIZE[0]//2+50, DISPLAY_SIZE[1]//2+100, 100, 40)
platform = pygame.Rect(DISPLAY_SIZE[0]//2, DISPLAY_SIZE[1]-100, 100, 10)
kill_zone = pygame.Rect(0, DISPLAY_SIZE[1]-10, DISPLAY_SIZE[0], 10)


class Ball:
    def __init__(self):
        self.x = DISPLAY_SIZE[0]//2
        self.y = DISPLAY_SIZE[1]//2
        self.vel = {
            "x": random.choice([SPEED, SPEED*-1])+random.choice([SPEED//5, SPEED//5*-1]),
            "y": SPEED*-1+random.choice([SPEED//5, SPEED//5*-1])
        }
        self.radius = 10
        self.rect = pygame.Rect(self.x-self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)

    def __del__(self):
        return None

    def update(self, ball_list):
        if self.x <= 0 or self.x >= DISPLAY_SIZE[0]:
            self.vel["x"] *= -1
        if self.y <= 0 or self.y >= DISPLAY_SIZE[1] or platform.colliderect(self.rect) and self.y < DISPLAY_SIZE[1]-95:
            self.vel["y"] *= -1
        self.x += self.vel["x"]
        self.y += self.vel["y"]
        self.rect.center = (self.x, self.y)
        pygame.draw.circle(DISPLAY, GREEN, (self.x, self.y), self.radius)
        for ball in ball_list:
            try:
                for key in self.ball_collision(ball):
                    self.vel[key] *= -1
            except TypeError:
                continue

    def ball_collision(self, ball):
        for point in ball.rect.topleft, ball.rect.topright, ball.rect.bottomleft, ball.rect.bottomright:
            if self.rect.collidepoint(point):
                return ["x", "y"]
        for point in ball.rect.midleft, ball.rect.midright:
            if self.rect.collidepoint(point):
                return ["x"]
        for point in ball.rect.midbottom, ball.rect.midtop:
            if self.rect.collidepoint(point):
                return ["y"]


ball_num = 1
balls = list()
balls.append(Ball())
# Main Loop
while not done:
    while mode == "game":
        DISPLAY.fill(BLACK)
        pygame.draw.rect(DISPLAY, RED, kill_zone)
        platform.centerx = pygame.mouse.get_pos()[0]
        pygame.draw.rect(DISPLAY, BLUE, platform)
        # Ball update
        for i in range(0, len(balls)):
            if len(balls) > i:
                if balls[i].y >= DISPLAY_SIZE[1]-10:
                    balls.pop(i)
                    ball_num = ball_num - 1
                else:
                    balls[i].update(filter(lambda x: x != balls[i], balls))
        if ball_num == 0:
            mode = "lost"
            continue
        pygame.display.flip()
        # Ball spawning
        if random.randint(0, 100) == 1 and minimum_time >= 150:
            minimum_time = 0
            ball_num = ball_num + 1
            balls.append(Ball())
        minimum_time += 1
        for e in pygame.event.get():
            if e.type == QUIT or pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
        FPS_CLOCK.tick(FPS)
    while mode == "lost":
        DISPLAY.fill(BLACK)
        DISPLAY.blit(TEXT_LOSE, text_rect)
        pygame.draw.rect(DISPLAY, WHITE, button_quit_rect)
        pygame.draw.rect(DISPLAY, WHITE, button_reset_rect)
        DISPLAY.blit(TEXT_RESET, button_reset_rect)
        DISPLAY.blit(TEXT_QUIT, button_quit_rect)
        pygame.display.flip()
        FPS_CLOCK.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and button_reset_rect.collidepoint(pygame.mouse.get_pos()):
                mode = "game"
                minimum_time = 0
                ball_num = 1
                balls.append(Ball())
            if e.type == QUIT or pygame.key.get_pressed()[pygame.K_q] or e.type == pygame.MOUSEBUTTONDOWN and button_quit_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()
