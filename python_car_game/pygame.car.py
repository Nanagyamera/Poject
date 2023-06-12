import pygame
from pygame.locals import *
import random
import pygame.font

# shape parameters
WIDTH, HEIGHT = 1200, 750
road = pygame.Rect(WIDTH / 2 - 350, 0, 700, HEIGHT)
roadMark = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)

# the various colours of the shapes
BROWN = (139, 69, 19)
GREY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# location parameters
right_lane = WIDTH / 2 + 700 / 4
left_lane = WIDTH / 2 - 700 / 4

# animation parameters
speed = 5

# Initialize the game
pygame.init()
run = True
game_over = False
restart = False
score = 0
#set the screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#set screen title
pygame.display.set_caption("Car Game")
#set screen colour
screen.fill(BROWN)
#set the font type and size
font = pygame.font.Font(None, 40)

# load player vehicle
car = pygame.image.load("car.png")
car_loc = car.get_rect()
#placing the car at the bottom right lane
car_loc.center = right_lane, HEIGHT * 0.8

# load AI vehicle
car2 = pygame.image.load("aiCar.png")
car2_loc = car2.get_rect()
#placing the AI car at the top left lane 
car2_loc.center = left_lane, HEIGHT * 0.2

counter = 0

# game loop
while run:
    counter += 1

    # increases the difficulty overtime
    if counter == 1000:
        speed += 0.50
        counter = 0
        print("Let's go", speed)

    # animate the aiCar
    car2_loc[1] += speed
    if car2_loc[1] > HEIGHT:
        car2_loc[1] = -200
        #randomly select lane
        if random.randint(0, 1) == 0:
            car2_loc.center = right_lane, -200
        else:
            car2_loc.center = left_lane, -200

    # handle events in pygame and update game state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update game logic
    if not game_over:
        keys_pressed = pygame.key.get_pressed()
        # move car to the left side of the road and not outside the road
        if keys_pressed[pygame.K_LEFT] and car_loc.left > 350:
            car_loc = car_loc.move([-350, 0])
        # move car to the right side of the road and not outside the road
        if keys_pressed[pygame.K_RIGHT] and car_loc.right < 700:
            car_loc = car_loc.move([350, 0])

        #check for a successful dodge and increase the score
        if car2_loc.y > car_loc.y + car_loc.height:
            score += 1

        # check for collision and end game
        if car_loc.colliderect(car2_loc):
            game_over = True

    screen.fill(BROWN)

    # Draw road
    pygame.draw.rect(screen, GREY, road)
    # Draw road mark
    pygame.draw.rect(screen, WHITE, roadMark)

    # Place car images on the screen
    screen.blit(car, car_loc)
    screen.blit(car2, car2_loc)

    # Render score
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (WIDTH - 200, 50))

    pygame.display.update()

    if game_over:
        # Render game over text and options
        game_over_text = font.render("GAME OVER, YOU LOST!", True, BLACK)
        restart_text = font.render("Press R to try again!", True, GREEN)
        give_up_text = font.render("Press Q to give up!", True, RED)

        #draw the various text on the screen
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(restart_text, (WIDTH // 2 - 700 // 3, 400))
        screen.blit(give_up_text, (WIDTH // 2 + 700 // 5, 400))

        pygame.display.update()

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_over = False
                keys_pressed = pygame.key.get_pressed()
                #press the r key to restart
                if keys_pressed[pygame.K_r]:
                    restart = True
                    score = 0
                    game_over = False
                #press the q key to quit
                elif keys_pressed[pygame.K_q]:
                    run = False
                    game_over = False

            if restart:
                # Reset necessary game variables and states
                # Set car to initial position
                car_loc.center = (right_lane, HEIGHT * 0.8)  
                # Set AI car to initial position
                car2_loc.center = (left_lane, HEIGHT * 0.2)
                # Reset game over flag  
                game_over = False  
                restart = False
                score = 0

                continue

    # Apply changes
    pygame.display.update()

# Collapse the application window
pygame.quit()
