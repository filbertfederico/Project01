import sys
import pygame
import random

def create_pipe():
    random_pipe_position = random.choice(pipe_height) #random-inator
    bottom_pipe = pipe_surface.get_rect(midtop = (300,random_pipe_position))
    top_pipe = pipe_surface.get_rect(midbottom = (300, random_pipe_position - 100))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes :
        pipe.centerx -= 2.5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 330:
            screen.blit(pipe_surface,pipe)
        else:   
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) 
            # ^ becuz there are 2 booleans the first one is for X axis and the latter is for the Y axis
            screen.blit(flip_pipe,pipe)

def entity_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -20 or bird_rect.bottom >= 431:
            return False 
    return True

def moving_floor():
    screen.blit(floor_surface,(floor_shift,431))
    screen.blit(floor_surface,(floor_shift + 288,431))

###################################

#start game
pygame.init()

#display screen
screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

#game variable
gravity = 0.25 
bird_movement = 0 #move bird_rect down
game_active = True

#img 
bg_surface = pygame.image.load("assets/background-day.png").convert()

floor_surface = pygame.image.load("assets/base.png")
floor_shift = 0

bird_surface = pygame.image.load("assets/bluebird-midflap.png")
bird_rect = bird_surface.get_rect(center=(50,230))

pipe_surface = pygame.image.load("assets/pipe-green.png")
pipe_list = []
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1500)
pipe_height = [140,192,256,293,330]


#game loop, so it keeps running
while True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0 # stopped for a sec so theres no downward momentum
                bird_movement -= 4.5 #bird fly height
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True 
                pipe_list.clear()
                bird_rect.center = (50,230)
                bird_movement = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe()) 
            print("pipe")
    
    #put image in the game 
    screen.blit(bg_surface,(0,0)) #blit : put one surface on another surface

    if game_active:
        #bird mechanics
        bird_movement += gravity
        bird_rect.centery += bird_movement # falling down
        screen.blit(bird_surface, bird_rect)
        game_active = entity_collision(pipe_list)

        #pipe mechanics
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)

    #trickery for moving floor
    floor_shift -= 3 # floor speed
    moving_floor()
    if floor_shift <= -289:
        floor_shift = 0

    pygame.display.update()
    clock.tick(64)




