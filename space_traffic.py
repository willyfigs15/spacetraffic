import pygame, random

# Initialize pygame
pygame.init()

# Set game display
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
space_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Traffic")

# Set FPS and Clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
SPACESHIP_STARTING_LIVES = 5
SPACESHIP_VELOCITY = 5
ASTEROID_STARTING_VELOCITY = 5
ASTEROID_ACCELERATION = .5
BUFFER = 100

score = 0
player_lives = SPACESHIP_STARTING_LIVES
asteroid_velocity = ASTEROID_STARTING_VELOCITY

# Set colors
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (124, 185, 232)
YELLOW = (255, 225, 77)
RED = (255, 42, 0)

# Set fonts
font = pygame.font.SysFont('Skia', 32)
small_font = pygame.font.SysFont('Skia', 20)
smaller_font = pygame.font.SysFont('Skia', 16)

# Set text
score_text = font.render("Score: " + str(score), True, YELLOW)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = font.render("Space Traffic", True, BLUE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

by_willy_text = smaller_font.render("created by willyfigs15", True, WHITE)
by_willy_rect = by_willy_text.get_rect()
by_willy_rect.centerx = WINDOW_WIDTH//2
by_willy_rect.y = 40

lives_text = font.render("Lives: " + str(player_lives), True, YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render("GAMEOVER", True, RED)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = small_font.render("Press the < SPACE KEY > to play again", True, YELLOW)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)

# Set sound and music
point_sound = pygame.mixer.Sound("point_sound.wav")
hit_sound = pygame.mixer.Sound("hit_sound.wav")
hit_sound.set_volume(.2)
pygame.mixer.music.load("space_traffic_music.wav")

# Set images
background_image = pygame.image.load("background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

spaceship_image = pygame.image.load("spaceship.png")
spaceship_image = pygame.transform.rotate(spaceship_image, 90)
spaceship_rect = spaceship_image.get_rect()
spaceship_rect.left = 32
spaceship_rect.centery = WINDOW_HEIGHT//2

asteroid_image = pygame.image.load("asteroid.png")
asteroid_rect = asteroid_image.get_rect()
asteroid_rect.x = WINDOW_WIDTH + BUFFER
asteroid_rect.y = random.randint(64, WINDOW_HEIGHT - 48)


# Game main loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    # Check if player wants to quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Check to see if the player wants to move
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and spaceship_rect.top > 64:
        spaceship_rect.y -= SPACESHIP_VELOCITY
    if keys[pygame.K_DOWN] and spaceship_rect.bottom < WINDOW_HEIGHT:
        spaceship_rect.y += SPACESHIP_VELOCITY

    # Move the asteroid
    if asteroid_rect.x < 0:
        # Player missed the asteroid
        score += 1
        # player_lives -= 1
        point_sound.play()
        asteroid_rect.x = WINDOW_WIDTH + BUFFER
        asteroid_rect.y = random.randint(64, WINDOW_HEIGHT - 48)
        asteroid_velocity += ASTEROID_ACCELERATION
        # asteroid_rect.x -= asteroid_velocity
    else:
        # Move the asteroid
        asteroid_rect.x -= asteroid_velocity

     #Check for collisions
    if spaceship_rect.colliderect(asteroid_rect):
        player_lives -= 1
        hit_sound.play()
        
        asteroid_rect.x = WINDOW_WIDTH + BUFFER
        asteroid_rect.y = random.randint(64, WINDOW_HEIGHT - 48)

    # Update game score and lives
    score_text = font.render("Score: " + str(score), True, YELLOW)
    lives_text = font.render("Lives: " + str(player_lives), True, YELLOW)

    #Check for game over
    if player_lives == 0:
        space_surface.blit(game_over_text, game_over_rect)
        space_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        #Pause the game until player presses a key, then reset the game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                 #The player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                score = 0
                player_lives = SPACESHIP_STARTING_LIVES
                spaceship_rect.y = WINDOW_HEIGHT//2
                asteroid_velocity = ASTEROID_STARTING_VELOCITY
                pygame.mixer.music.play(-1, 0.0)
                is_paused = False
               

    # Fill the display
    space_surface.blit(background_image, background_rect)

    # Blit top text
    space_surface.blit(score_text, score_rect)
    space_surface.blit(title_text, title_rect)
    space_surface.blit(lives_text, lives_rect)
    space_surface.blit(by_willy_text, by_willy_rect)
    pygame.draw.line(space_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)

    # Blit images to screen
    space_surface.blit(spaceship_image, spaceship_rect)
    space_surface.blit(asteroid_image, asteroid_rect)

    # Update display ans tick clock
    pygame.display.update()
    clock.tick(FPS)


# End game
pygame.quit()
