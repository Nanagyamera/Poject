import pygam
from pygame.locals import *
import random 

#shape parameters
WIDTH, HEIGHT = 1200, 750
road = pygame.Rect(WIDTH/2 - 350, 0, 700, HEIGHT)
roadMark = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

#the various colours of the shapes
BROWN = (139, 69, 19)
GREY = (50, 50, 50)
WHITE = (255, 255, 255)
#location parameters
right_lane = WIDTH/2 + 700/4
left_lane = WIDTH/2 - 700/4
#animation parameters
speed = 5

#Initialize the game
pygame.init()
run = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")
screen.fill(BROWN)

pygame.display.update()

#load player vehicle
car = pygame.image.load("car.png")
car_loc = car.get_rect()
car_loc.center = right_lane, HEIGHT*0.8

#load AI vehicle
car2 = pygame.image.load("aiCar.png")
car2_loc = car2.get_rect()
car2_loc.center = left_lane, HEIGHT*0.2

counter = 0

#game loop
while run:
    counter += 1

    #increases the  difficulty overtime
    if counter == 1000:
        speed += 0.50
        counter = 0
        print("Lets gOoo", speed)

    #animate the aiCar
    car2_loc[1] += speed
    if car2_loc[1] > HEIGHT:
        car2_loc[1] = -200
        if random.randint(0, 1) == 0:
            car2_loc.center = right_lane, -200
        else:
            car2_loc.center = left_lane, -200

    #check for collision and end game
    if car_loc.colliderect(car2_loc):
        print("GAME OVER, YOU LOST!")
        break

    #handle events in pygame and update game state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        keys_pressed = pygame.key.get_pressed()
        #move car to the left side of the road and not outside the road
        if keys_pressed[pygame.K_LEFT] and car_loc.left > 350:
            car_loc = car_loc.move([-350, 0])
        #move car to the right side of the road and not outside the road
        if keys_pressed[pygame.K_RIGHT] and car_loc.right < 700:
            car_loc = car_loc.move([350, 0])

    #draw road
    pygame.draw.rect(screen, GREY, road)
    #draw roadmark
    pygame.draw.rect(screen, WHITE, roadMark)

    #place car images on the screen
    screen.blit(car, car_loc)
    screen.blit(car2, car2_loc)
    #apply changes
    pygame.display.update()

#collapse the application window
pygame.quit()
