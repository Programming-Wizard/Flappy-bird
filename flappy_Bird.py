import pygame
import sys
import random


def draw_floor():
    screen.blit(floor, (floor_x, 576))
    screen.blit(floor, (floor_x + 576, 576))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    random_pipe_dist = random.choice(pipe_distance)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos - random_pipe_dist))
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 676:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 576:
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score : {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f"High Score : {int(high_score)}", True, (255, 255, 255)
        )
        high_score_rect = high_score_surface.get_rect(center=(288, 500))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_caption("Flappy Bird")


icon = pygame.image.load("D:/repos/Flappy-bird/resources/yellowbird-midflap.png")
icon = pygame.transform.scale(icon, (32, 32))

screen = pygame.display.set_icon(icon)
screen = pygame.display.set_mode((576, 676))
clock = pygame.time.Clock()

current_time = 0
change_time = 0

game_font = pygame.font.Font("D:/repos/Flappy-bird/resources/04B_19__.TTF", 40)

# game variables
gravity = 0.2
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load(
    "D:/repos/Flappy-bird/resources/background-day.png"
).convert()
bg_surface = pygame.transform.scale(bg_surface, (576, 676))
bg_surface_night = pygame.image.load(
    "D:/repos/Flappy-bird/resources/background-night.png"
).convert()
bg_surface_night = pygame.transform.scale(bg_surface_night, (576, 676))

backgroud = bg_surface_night

floor = pygame.image.load("D:/repos/Flappy-bird/resources/base.png").convert()
floor = pygame.transform.scale(floor, (576, 100))
floor_x = 0

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_midflap = pygame.image.load(
#     "D:/repos/Flappy-bird/resources/yellowbird-midflap.png"
# ).convert_alpha()
# bird_rect = bird_midflap.get_rect(center=(100, 338))
# bird_downflap = pygame.image.load(
#     "D:/repos/Flappy-bird/resources/yellowbird-downflap.png"
# ).convert_alpha()
# bird_rect = bird_downflap.get_rect(center=(100, 338))
# bird_upflap = pygame.image.load(
#     "D:/repos/Flappy-bird/resources/yellowbird-upflap.png"
# ).convert_alpha()
bird_midflap = pygame.image.load(
    "D:/repos/Flappy-bird/resources/redbird-midflap.png"
).convert_alpha()
bird_rect = bird_midflap.get_rect(center=(100, 338))
bird_downflap = pygame.image.load(
    "D:/repos/Flappy-bird/resources/redbird-downflap.png"
).convert_alpha()
bird_rect = bird_downflap.get_rect(center=(100, 338))
bird_upflap = pygame.image.load(
    "D:/repos/Flappy-bird/resources/redbird-upflap.png"
).convert_alpha()
bird_rect = bird_upflap.get_rect(center=(100, 338))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 338))

# pipe_surface = pygame.image.load(
#     "D:/repos/Flappy-bird/resources/pipe-red.png"
# ).convert()
# pipe_surface = pygame.transform.scale(pipe_surface, (65, 400))
pipe_surface = pygame.image.load(
    "D:/repos/Flappy-bird/resources/pipe-green.png"
).convert()
pipe_surface = pygame.transform.scale(pipe_surface, (65, 400))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 600)
pipe_height = [388, 400, 450, 310]
pipe_distance = [600, 620, 580, 575, 590, 610, 550]

game_over_surface = pygame.image.load(
    "D:/repos/Flappy-bird/resources/message.png"
).convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (200, 283))
game_over_rect = game_over_surface.get_rect(center=(288, 325))

flap_sound = pygame.mixer.Sound("D:/repos/Flappy-bird/resources/wing.wav")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            flap_sound.stop()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 1
                bird_movement -= 6
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 338)
                bird_movement = 0
                score = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and game_active:
            game_active = True
            bird_movement = 1
            bird_movement -= 6
            flap_sound.play()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_active == False:
            game_active = True
            pipe_list.clear()
            bird_rect.center = (100, 338)
            bird_movement = 0
            score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()
    screen.blit(bg_surface_night, (0, 0))

    if game_active:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display("main_game")
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    # Floor
    floor_x -= 1
    draw_floor()
    if floor_x <= -576:
        floor_x = 0

    pygame.display.update()
    clock.tick(100)
