import pygame
from pygame.locals import *
from pygame.sprite import Group
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60


screen_width = 864
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Bauhaus 93', 40)

#define colours
white = (255, 255, 255)

#define game variables
ground_scroll = 0
scroll_speed = 4 #4 -> pixels
flying = False
game_over = False #whenever bird touches the ground, game should stop
pipe_gap = 175 # setting the gap between top and bottom pipe as 150 pixels
pipe_frequency = 1500  #milli seconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# Load the best score from a file (or create the file if it doesn't exist)
try:
    with open('best_score.txt', 'r') as file:
        best_score = int(file.read())
except FileNotFoundError:
    with open('best_score.txt', 'w') as file:
        best_score = 0
        file.write(str(best_score))



#load images background
bg = pygame.image.load('D:\\Adiiii\\CodeGym\\VS code\\Python\\project\\Flappy bird\\bg.png')
ground_image = pygame.image.load('D:\\Adiiii\\CodeGym\\VS code\\Python\\project\\Flappy bird\\ground.png')
#button_img = 
button_img = pygame.image.load('D:\\Adiiii\\CodeGym\\VS code\\Python\\project\\Flappy bird\\restart.png')

# Scale the background image to fit the screen
bg = pygame.transform.scale(bg, (screen_width, screen_height))


frame_height1 = bg.get_height()
frame_height2 = ground_image.get_height()  # Use the ground image's height


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    global best_score  # Add this line to indicate that you want to modify the global best_score variable
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [] #creat a list of images
        self.index = 0
        self.counter = 0 
        #iteratively adding images into the list 
        for num in range(1, 4):
            img = pygame.image.load(f'D:\\Adiiii\\CodeGym\\VS code\\Python\\project\\Flappy bird\\bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.velocity = 0
        self.clicked = False

    def update(self):

        #gravity
        if flying == True:
            self.velocity += 0.4
            if self.velocity > 8:
                self.velocity = 8
            #now the bird will fall and go out of the screen
            #lets make it fall on the groud image's heigth
            if self.rect.bottom < screen_height - frame_height2:         #and self.rect.top > screen_height - frame_height1:
                self.rect.y += int(self.velocity)

        if game_over == False:
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = -10  #for going upwards  -> negative velocity
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        

            #handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1

                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)

        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('D:\\Adiiii\\CodeGym\\VS code\\Python\\project\\Flappy bird\\pipe.png')
        self.rect = self.image.get_rect()

        #position 1 is from top , -1 is from bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)  # to flip the bottom pipe into top pipe
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]  # 75 pixels gap from bottom  --> 150 /2

        if position == -1:    
            self.rect.topleft = [x, y + int(pipe_gap/2)]  # 75 pixels gap from top  --> 150 /2

    def update(self):
        self.rect.x -= scroll_speed  #scrtooling the pipe at the speed of scroll_ground i.e 4 pixels
        if self.rect.right < 0 :
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):


        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

#int(screen_height / 2) --> middle of the screen
flappy = Bird(100, int(screen_height / 2)) #object of bird class
bird_group.add(flappy)

#create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
while run:

    clock.tick(fps)

    #draw background 
    screen.blit(bg, (0, screen_height - frame_height1))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    
    
    #draw the ground 
    screen.blit(ground_image, (ground_scroll , screen_height - frame_height2))

    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True

        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text("Current Score: " + str(score), font, white, 10, 10)
    draw_text("Best Score: " + str(best_score), font, white, 10, 50)
    #check for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: # collision between bird and pipe group
        game_over = True


    #check if bird has hit the ground
    if flappy.rect.bottom >= screen_height - frame_height2:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        pipe_height = random.randint(-100, 100)
        if time_now - last_pipe > pipe_frequency:

            bottom_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)  #object -> Pipe class
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now



        #draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll)>35:
            ground_scroll = 0
        
        pipe_group.update()


    #check for game over and reset
    if game_over and button.draw():
        game_over = False
        score = reset_game()

    if score > best_score:
        best_score = score

    # Save the best score to a file
    with open('best_score.txt', 'w') as file:
        file.write(str(best_score))

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()