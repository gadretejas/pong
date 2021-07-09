import pygame, sys
import random

pygame.init()
clock = pygame.time.Clock()

two_player = False

def ball_movement():
    global player_score, opponent_score
    global ball_speed_y, ball_speed_x
    global score_time, halt_movement

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    if ball.left <= 0:
        # player on right won
        player_score += 1
        halt_movement = True
        #ball_restart()
        score_time = pygame.time.get_ticks()
    if ball.right >= WIDTH:
        # player or left won
        opponent_score += 1
        halt_movement = True
        #ball_restart()
        score_time = pygame.time.get_ticks()
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_movement():
    if not halt_movement:
        player.y += player_speed
        if player.top <= 0:
            player.top = 0
        if player.bottom >= HEIGHT:
            player.bottom = HEIGHT

def opponent_movement():
    if not two_player:
        if not halt_movement:
            if opponent.top < ball.y:
                opponent.top += oppponent_speed
            if opponent.bottom > ball.y:
                opponent.bottom -= oppponent_speed
            if opponent.top <= 0:
                opponent.top = 0
            if opponent.bottom >= HEIGHT:
                opponent.bottom = HEIGHT

    else:
        if not halt_movement:
            opponent.y += oppponent_speed
            if opponent.top <= 0:
                opponent.top = 0
            if opponent.bottom >= HEIGHT:
                opponent.bottom = HEIGHT

def ball_restart():
    # bring the ball back to centre and start in some random direction
    global ball_speed_y, ball_speed_x, score_time, halt_movement

    current_time = pygame.time.get_ticks()
    ball.center = (WIDTH / 2, HEIGHT / 2)
    ###########
    # This block is used to show countdown on the screen before the ball is released
    if current_time - score_time < 700:
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (WIDTH/2-10, HEIGHT/2+20))
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, light_grey)
        screen.blit(number_two, (WIDTH/2-10, HEIGHT/2+20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, light_grey)
        screen.blit(number_one, (WIDTH/2-10, HEIGHT/2+20))
    ############
    if current_time - score_time < 2100:
        ball_speed_y, ball_speed_x = 0, 0
        #halt_movement = False
    else:
        ball_speed_y = 7*random.choice((-1, 1))
        ball_speed_x = 7*random.choice((-1, 1))
        score_time = None
        halt_movement = False

# setting up window
WIDTH = 1280
HEIGHT = 960
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# game rectangles
ball = pygame.Rect(WIDTH/2 - 15, HEIGHT/2 - 15, 30, 30)
player = pygame.Rect(WIDTH-20, HEIGHT/2 - 70, 10, 140)
opponent = pygame.Rect(10, HEIGHT/2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# speeds
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
oppponent_speed = 0
if two_player:
    oppponent_speed = 0
else:
    oppponent_speed = 7
halt_movement = False

# text display setup
player_score = 0
opponent_score = 0

game_font = pygame.font.Font('freesansbold.ttf', 32)

# timer
score_time = True

while True:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
            if two_player:
                if event.key == pygame.K_w:
                    oppponent_speed -= 7
                if event.key == pygame.K_s:
                    oppponent_speed += 7
        if event.type == pygame.KEYUP:
            if event.type == pygame.K_DOWN:
                player_speed -= 7
            if event.type == pygame.K_UP:
                player_speed += 7
            if two_player:
                if event.key == pygame.K_w:
                    oppponent_speed += 7
                if event.key == pygame.K_s:
                    oppponent_speed -= 7

    # movement functions
    ball_movement()
    player_movement()
    opponent_movement()

    # Drawing rects on the surface
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (WIDTH/2,0), (WIDTH/2, HEIGHT))

    # display text
    if score_time:
        ball_restart()

    player_text = game_font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text, (660, 470))
    opponent_text = game_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (600, 470))

    # updating the window
    pygame.display.flip()
    clock.tick(60)
