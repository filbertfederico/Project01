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
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50] #free up space by removing existing passed pipes 
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 330:
            screen.blit(pipe_surface,pipe)
        else:   
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) 
            # ^ becuz there are 2 booleans the first one is for X axis and the latter is for the Y axis
            screen.blit(flip_pipe,pipe)

def entity_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
    if bird_rect.top <= -20 or bird_rect.bottom >= 431:
            return False 
    return True

def moving_floor():
    screen.blit(floor_surface,(floor_shift,431))
    screen.blit(floor_surface,(floor_shift + 288,431))

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 6,1)
    print()
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}",True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface, score_rect)
        #highscore
        high_score_surface = game_font.render(f"High score: {int(high_score)}",True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,405))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
    

###################################

#to initiate mixer in a certain way
# pygame.mixer.pre_init(frequency= 44100, size= 16, channels= 1, buffer= 512) --> for lower pygame version lower than pygame 2 version
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
score = 0
high_score = 0
can_score = True
    #ingame Text for scoring system
game_font = pygame.font.Font("04B_19.ttf",40)

#img 
bg_surface = pygame.image.load("assets/background-day.png").convert()

floor_surface = pygame.image.load("assets/base.png")
floor_shift = 0

bird_downflap = pygame.image.load("assets/bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50,230))

# predecessor of the above:
# bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
# bird_rect = bird_surface.get_rect(center=(50,230))

#timer for animation so per 200 ms bird change flaps :
birdflaps = pygame.USEREVENT + 1  
pygame.time.set_timer(birdflaps,200) 

pipe_surface = pygame.image.load("assets/pipe-green.png")
pipe_list = []
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1500)
pipe_height = [140,192,256,293,330]

#game over msg
game_over_surface = pygame.image.load("assets/message.png")
game_over_rect = game_over_surface.get_rect(center = (144,240))

#audio input
flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 500

#game loop, so it keeps running
while True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0 # stopped for a sec so theres no downward momentum
                bird_movement -= 4.5 #bird fly height
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True 
                pipe_list.clear()
                bird_rect.center = (50,230)
                bird_movement = 0
                score = 0

        if event.type == spawnpipe:
            pipe_list.extend(create_pipe()) 
            print("pipe")

        if event.type == birdflaps :
            if bird_index < 2:
                bird_index += 1 
            else:
                bird_index = 0

            bird_surface,bird_rect = bird_animation()
             
    
    #put image in the game 
    screen.blit(bg_surface,(0,0)) #blit : put one surface on another surface

    if game_active:
        #bird mechanics
        bird_movement += gravity
        rotation = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement # falling down
        screen.blit(rotation, bird_rect)
        game_active = entity_collision(pipe_list)

        #pipe mechanics
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)

        #scoring mechanics
        if pipe_list:
            for pipe in pipe_list :
                if 45  < pipe.centerx < 50 and can_score :
                    score += 1
                    score_sound.play()
                    can_score = False
                if pipe.centerx < 0:
                    can_score = True

        score_display("main_game")
        
    else :
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")


    #trickery for moving floor
    floor_shift -= 3 # floor speed
    moving_floor()
    if floor_shift <= -289:
        floor_shift = 0

    pygame.display.update()
    clock.tick(64)
