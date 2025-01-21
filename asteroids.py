import pygame
import sys
from pygame.locals import *
import time
import random
from gpiozero import LED

pygame.init()

#LEDs
GREEN_LED = LED(17)
YELLOW_LED = LED(20)
RED_LED = LED(22)

#Window heigt and width
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 750

#Movement speed of the ship
SHIP_SPEED = 27
ENEMY_SPEED = 20
LASER_SPEED = -20

#Ship spawn position
SHIP_SPAWN_POS_X = 375
SHIP_SPAWN_POS_Y = 550

# Set up the display
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroids - Score: 0")
Clock = pygame.time.Clock()
FRAME_RATE = 30

#Sprites
PLAYER_SPRITE = "/home/ianp/Documents/Asteroids-Final/Assets/PlayerSprite110px.png"
ENEMY_SPRITE = "/home/ianp/Documents/Asteroids-Final/Assets/AsteroidSprite130px.png"
ENEMY_2_SPRITE = "/home/ianp/Documents/Asteroids-Final/Assets/CometSprite150px.png"
LASER_SPRITE = "/home/ianp/Documents/Asteroids-Final/Assets/Laser.png"
BACKGROUND = "/home/ianp/Documents/Asteroids-Final/Assets/SpacePixelArt.png"
PAUSE_BACKGROUND = "/home/ianp/Documents/Asteroids-Final/Assets/SpacePixelArt-BW.png"

#Sound effects
OUCH_SOUND = pygame.mixer.Sound("/home/ianp/Documents/Asteroids-Final/Assets/hit.wav")
PAUSE_SOUND = pygame.mixer.Sound("/home/ianp/Documents/Asteroids-Final/Assets/pause.wav")
GAME_OVER_SOUND = pygame.mixer.Sound("/home/ianp/Documents/Asteroids-Final/Assets/scream.wav")


# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Fonts
FONT = pygame.font.SysFont(None, 25)

# Game state variables
paused = False

#Player move direction
move_direction = "NONE"

#laser_state = "Inactive"

def do_keypress_event(event):
    global paused
    if event.key == pygame.K_LEFT:
        return "LEFT"
    elif event.key == pygame.K_RIGHT:
        return "RIGHT"
    elif event.key == pygame.K_UP:
        return "UP"
    elif event.key == pygame.K_DOWN:
        return "DOWN"
    elif event.key == pygame.K_ESCAPE: # Escape pauses the game
        paused = True
    #elif event.key == pygame.K_SPACE:
        #return "SPACE"
        
def pause_check():
    global paused
    # Pause mechanism
    if paused:
        pygame.mixer.Sound.play(PAUSE_SOUND)
    while paused:
        WINDOW.fill(BLACK)
        pause_background_image = pygame.image.load(PAUSE_BACKGROUND)
        WINDOW.blit(pause_background_image, (0, 0)) 
        message("Game is paused! Press [Space] to continue or [Escape] to quit.", GREEN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                        # Straight kill the game
                    pygame.quit() # Kill game
                    quit() # Kill program
                    
                       
#Message display                        
def message(msg, color):
    mesg = FONT.render(msg, True, color)
    WINDOW.blit(mesg, [WINDOW_WIDTH / 6, WINDOW_HEIGHT / 3])

def input_event():
    global move_direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # An attempt to close the window or program
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            new_direction = do_keypress_event(event) 
            move_direction = new_direction #if new_direction != None else direction
    return move_direction

#def laser_input_event():
    #global laser_state
    #for event in pygame.event.get():
        #if event.type == pygame.KEYDOWN:
            #input_check = do_keypress_event(event)
            #if input_check == "SPACE":
                #if laser_state == "Inactive":
                    #laser_state = "Active"
    #return laser_state
    

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() #Initializing player sprite
        self.image = pygame.image.load(PLAYER_SPRITE )
        self.rect = self.image.get_rect()
        self.rect.center = (SHIP_SPAWN_POS_X, SHIP_SPAWN_POS_Y)
    
    def draw_player(self, surface): #Drawing player sprite to Screen
        surface.blit(self.image, self.rect)
    
    def move_player(self, direction): #Player movement
        
        if self.rect.y > 0:
            if direction == "UP":
                self.rect.y -= SHIP_SPEED
        
        if self.rect.y < WINDOW_HEIGHT - 120:
            if direction == "DOWN":
                self.rect.y += SHIP_SPEED
                
        if self.rect.x < WINDOW_WIDTH - 120:
            if direction == "RIGHT":
                self.rect.x += SHIP_SPEED
        
        if self.rect.x > 0:
            if direction == "LEFT":
                self.rect.x -= SHIP_SPEED
                

class Asteroid(pygame.sprite.Sprite): #Initializing, drawing, and moving the enemy
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(ENEMY_SPRITE)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, WINDOW_WIDTH - 30), 0)
    
    def draw_enemy(self, surface):
        surface.blit(self.image, self.rect)
    
    def move_enemy(self):
        self.rect.y += ENEMY_SPEED
        if(self.rect.y > 800):
            self.rect.y = 0
            self.rect.center = (random.randint(30, WINDOW_WIDTH - 30), 0)

class Comet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(ENEMY_2_SPRITE)
        self.rect = self.image.get_rect()
        self.rect.center = (0, random.randint(30, WINDOW_HEIGHT - 30))
    
    def draw_enemy_2(self, surface):
        surface.blit(self.image, self.rect)
    
    def move_enemy_2(self):
        self.rect.x += ENEMY_SPEED
        if(self.rect.x > 800):
            self.rect.x = 0
            self.rect.center = (0, random.randint(30, WINDOW_HEIGHT - 30))
            
        
#class Laser(pygame.sprite.Sprite):
    #def __init__(self):
        #super().__init__()
        #self.image = pygame.image.load(LASER_SPRITE)
        #self.rect = self.image.get_rect()
        #self.rect.center = (0, 0)
        
    #def draw_laser(self, surface):
        #surface.blit(self.image, self.rect)
    
    #def fix_to_ship(self, pos_x, pos_y):
       # self.rect.x = pos_x
        #self.rect.y = pos_y

    #def move_laser(self):
        #self.rect.y -= LASER_SPEED      

Player = Ship()
Enemy = Asteroid()
Enemy_2 = Comet()

# The game loop
def game_loop():
    global move_direction
    
    end_sequence = False
    GREEN_LED.on()
    
    score = 0
    frame_count = 0
    damage_buffer_count = 0
    health = 2
    can_take_damage = True
    
    GREEN_LED.on()
    YELLOW_LED.on()
    RED_LED.on()
    
    while True:

        pause_check()
        
        WINDOW.fill(BLACK)
        
        background_image = pygame.image.load(BACKGROUND)
        WINDOW.blit(background_image, (0, 0)) 
    
        #laser_state = laser_input_event()

        #if laser_state == "Active":
            #laser_state = "Moving"
            #Projectile.fix_to_ship(ship_x, ship_y)
        
        #if laser_state == "Moving":
            #Projectile.move_laser()
        
        #if Projectile.rect.y < 0:
            #laser_state = "Inactive"
        
        move_direction = input_event()
        Player.move_player(move_direction)
        Enemy.move_enemy()
        Enemy_2.move_enemy_2()
        
        if pygame.Rect.colliderect(Player.rect, Enemy.rect):
            if can_take_damage:
                health -= 1
                GREEN_LED.off()
                pygame.mixer.Sound.play(OUCH_SOUND)
                can_take_damage = False
        
        if pygame.Rect.colliderect(Player.rect, Enemy_2.rect):
            if can_take_damage:
                health -= 1
                GREEN_LED.off()
                pygame.mixer.Sound.play(OUCH_SOUND)
                can_take_damage = False
                
        if can_take_damage == False:
            damage_buffer_count += 1
            
        if damage_buffer_count == 30:
            can_take_damage = True
        
        if health == 0:
            end_sequence = True
            
        
        Player.draw_player(WINDOW)
        Enemy.draw_enemy(WINDOW)
        Enemy_2.draw_enemy_2(WINDOW)
        
        if end_sequence:
            pygame.mixer.Sound.play(GAME_OVER_SOUND)
            YELLOW_LED.off()
        
        while end_sequence:
            WINDOW.fill(BLACK)
            ouch_background_image = pygame.image.load(PAUSE_BACKGROUND)
            WINDOW.blit(ouch_background_image, (0, 0)) 
            message(f"Ouch, Game Over! Your Score Was '{score}'! Press [ESCAPE] to Quit.", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # Kill game
                    quit() # Kill program
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit() 
                        
        frame_count = frame_count + 1
        
        if frame_count == 30:
            score += 1
            frame_count = 0
        pygame.display.set_caption(f"Asteroids - Score: {score}")
        

        pygame.display.update()
        Clock.tick(FRAME_RATE)

if __name__ == '__main__':
    try:
        game_loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        pass