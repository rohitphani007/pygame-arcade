import leaderboard
import pygame
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common")))

from colors import *
from constants import *

pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
font = pygame.font.Font(None,30)

base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/snake"))

bg = pygame.image.load(os.path.join(base,"bg.png"))
bg = pygame.transform.scale(bg,(width,height))

obstacle_img = pygame.image.load(os.path.join(base,"obstacle.png"))
obstacle_img = pygame.transform.scale(obstacle_img,(10,10))

snake = [(100,100)]
dx,dy = 10,0

grid = 10

food = (
    random.randrange(0,width,grid),
    random.randrange(0,height,grid)
)

obstacles = []
for _ in range(25):
    obstacles.append((
        random.randrange(0,width,grid),
        random.randrange(0,height,grid)
    ))

speed = 8
score = 0
started = False
paused = False

score_sent = False
game_over = False
player_name = input("PLAYER, ENTER YOUR NAME: ")
top_scores = []

running = True
while running:
    screen.blit(bg,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            started = True

            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_UP and dy != 10:
                dx,dy = 0,-10
            if event.key == pygame.K_DOWN and dy != -10:
                dx,dy = 0,10
            if event.key == pygame.K_LEFT and dx != 10:
                dx,dy = -10,0
            if event.key == pygame.K_RIGHT and dx != -10:
                dx,dy = 10,0

    if paused:
        paused_text = font.render("PAUSED", True, white)
        screen.blit(paused_text, (width//2 - 50,height//2 - 15))

    if started and not paused and not game_over:
        head = (snake[0][0]+dx, snake[0][1]+dy)
        snake.insert(0, head)

        if head == food:
            score += 1
            food = (
                random.randrange(0,width,grid),
                random.randrange(0,height,grid)
            )
        else:
            snake.pop()

        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            game_over = True

        if head in obstacles:
            game_over = True

        body = snake.copy()
        body.pop(0)
        if head in body:
            game_over = True

    for s in snake:
        pygame.draw.rect(screen, green, (*s,10,10))

    for o in obstacles:
        screen.blit(obstacle_img,o)

    pygame.draw.rect(screen, red, (*food,10,10))

    text = font.render(f"Score: {score}", True, white)
    screen.blit(text,(width-120,10))

    if not started:
        msg = font.render("Press any key to start", True, white)
        screen.blit(msg,(180,180))

    if game_over:
        if not score_sent:
            leaderboard.submit_score(player_name, score)
            top_scores = leaderboard.get_top_scores()
            score_sent = True
        
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        msg = font.render("GAME OVER", True, red)
        screen.blit(msg, (width // 2 - 60, height // 2 - 80))
        
        title = font.render("GLOBAL TOP 5 (SNAKE):", True, (255, 215, 0))
        screen.blit(title, (width // 2 - 100, height // 2 - 40))

        y_off = 0
        for entry in top_scores:
            y_off += 30
            score_txt = font.render(f"{entry['name']}: {entry['score']}", True, white)
            screen.blit(score_txt, (width // 2 - 100, height // 2 - 40 + y_off))

        restart_msg = font.render("Press Esc to Quit", True, (200, 200, 200))
        screen.blit(restart_msg, (width // 2 - 70, height // 2 + 150))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()