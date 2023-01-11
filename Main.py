import pygame
import sys
import random
from pygame.locals import *

pygame.init()

mode = "menu"
DISPLAY_SIZE = (1000, 800)
NORMAL_SPEED = (DISPLAY_SIZE[0]//100 + DISPLAY_SIZE[1]//100)//2
speed = 0
DISPLAY = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption('MiniGame')

FPS = 30
FPS_CLOCK = pygame.time.Clock()

score = 0
minimum_time = 0
done = False

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)

FONT = pygame.font.Font('freesansbold.ttf', 32)
TEXT_LOSE = FONT.render('YOU LOST', True, RED)
TEXT_QUIT = FONT.render('QUIT', True, BLACK)
TEXT_RESET = FONT.render('AGAIN', True, BLACK)
text_rect = TEXT_LOSE.get_rect()
text_rect.center = (DISPLAY_SIZE[0]//2, DISPLAY_SIZE[1]//2)


platform = pygame.Rect(DISPLAY_SIZE[0]//2, DISPLAY_SIZE[1]-100, 100, 10)
kill_zone = pygame.Rect(0, DISPLAY_SIZE[1]-10, DISPLAY_SIZE[0], 10)


class Ball:
    def __init__(self):
        self.x = DISPLAY_SIZE[0]//2
        self.y = DISPLAY_SIZE[1]//2
        self.vel = {
            "x": random.choice([speed, speed*-1])+random.choice([speed//5, speed//5*-1]),
            "y": speed*-1+random.choice([speed//5, speed//5*-1])
        }
        self.radius = 10
        self.rect = pygame.Rect(self.x-self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)

    def __del__(self):
        return None

    def update(self, ball_list):
        global score
        if self.x <= 0 or self.x >= DISPLAY_SIZE[0]:
            self.vel["x"] *= -1
        if self.y <= 0 or self.y >= DISPLAY_SIZE[1]:
            self.vel["y"] *= -1
        if platform.colliderect(self.rect) and self.y < DISPLAY_SIZE[1]-95:
            score += 1
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


def text_gen(text, pos, color):
    text = FONT.render(text, True, color)
    rect = text.get_rect()
    rect.center = pos
    DISPLAY.blit(text, rect)


def button_gen(text, font_color, color, rect):
    text = FONT.render(text, True, font_color)
    text_rect = text.get_rect()
    text_rect.center = (rect.center[0], rect.center[1])
    pygame.draw.rect(DISPLAY, color, rect)
    DISPLAY.blit(text, text_rect)


# Main Loop
while not done:
    while mode == "menu":
        ball_num = 1
        minimum_time = 0
        score = 0
        balls = list()
        DISPLAY.fill(BLACK)
        text_gen("The RandomMiniGame", (DISPLAY_SIZE[0]//2, DISPLAY_SIZE[1]//2-50), WHITE)
        easy_rect = pygame.Rect(DISPLAY_SIZE[0] // 2 - 200, DISPLAY_SIZE[1] // 2, 100, 40)
        mid_rect = pygame.Rect(DISPLAY_SIZE[0] // 2 - 80, DISPLAY_SIZE[1] // 2, 160, 40)
        hard_rect = pygame.Rect(DISPLAY_SIZE[0] // 2 + 100, DISPLAY_SIZE[1] // 2, 100, 40)
        button_gen("EASY", WHITE, GREEN, easy_rect)
        button_gen("MEDIUM", WHITE, ORANGE, mid_rect)
        button_gen("HARD", WHITE, RED, hard_rect)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == QUIT or pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and easy_rect.collidepoint(pygame.mouse.get_pos()):
                mode = "game"
                speed = NORMAL_SPEED//1.5
                balls.append(Ball())
            if e.type == pygame.MOUSEBUTTONDOWN and mid_rect.collidepoint(pygame.mouse.get_pos()):
                mode = "game"
                speed = NORMAL_SPEED
                balls.append(Ball())
            if e.type == pygame.MOUSEBUTTONDOWN and hard_rect.collidepoint(pygame.mouse.get_pos()):
                mode = "game"
                speed = round(NORMAL_SPEED*1.5)
                balls.append(Ball())
        FPS_CLOCK.tick(FPS)
    while mode == "game":
        DISPLAY.fill(BLACK)
        pygame.draw.rect(DISPLAY, RED, kill_zone)
        platform.centerx = pygame.mouse.get_pos()[0]
        pygame.draw.rect(DISPLAY, BLUE, platform)
        text_gen(str(score), (50, 50), WHITE)
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
        reset_rect = pygame.Rect(DISPLAY_SIZE[0] // 2 - 150, DISPLAY_SIZE[1] // 2 + 100, 120, 40)
        menu_rect = pygame.Rect(DISPLAY_SIZE[0] // 2 + 50, DISPLAY_SIZE[1] // 2 + 100, 100, 40)
        button_gen("RESET", WHITE, GREEN, reset_rect)
        button_gen("MENU", WHITE, RED, menu_rect)
        pygame.display.flip()
        FPS_CLOCK.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and reset_rect.collidepoint(pygame.mouse.get_pos()):
                mode = "game"
                minimum_time = 0
                ball_num = 1
                score = 0
                balls.append(Ball())
            if e.type == pygame.MOUSEBUTTONDOWN and menu_rect.collidepoint(pygame.mouse.get_pos()):
                mode = "menu"
            if e.type == QUIT or pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
