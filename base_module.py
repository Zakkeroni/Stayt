#!/usr/local/bin/python3.5m

import pygame
import Genmod
import random

FPS = 60 #frames per second setting

fpsClock = pygame.time.Clock()

pygame.init()


"""colors"""
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)



"""screen dimensions"""
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

HALF_SCREEN_WIDTH = int(SCREEN_WIDTH / 2)
HALF_SCREEN_HEIGHT = int(SCREEN_HEIGHT / 2)



"""player sprites and locations"""
gas_sprite = pygame.image.load('gas_sprite.png')
solid_sprite = pygame.image.load('solid_sprite.png')
liquid_sprite = pygame.image.load('liquid_sprite.png')



"""Starting stats"""
Xspeed = 25
Yspeed = 25
Gravity = 1
airtick = 0
State = 0
player = solid_sprite
playersizex = 83
playersizey = 68
endx = 5000
score = 0


# default platform size
platwidth = 120 
platheight = 50


#player starting location
playerx = 75
playery = SCREEN_HEIGHT/2 - platheight/2 - playersizey



player_faceleft = pygame.transform.flip(player, True, False) #flips the sprite to face left
player_faceright = pygame.transform.flip(player_faceleft, True, False) #flips the sprite to face right


level = Genmod.genlvl(15)

    

"""screen details"""
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Stayt")



cameralimitleft = 400
cameralimitright = 700
cameralimitup = 300
cameralimitdown = 1000

camerax = 0
cameray = 0


"""render objects"""
def render_objects(X, Y):
    global level
    global endx
    screen.blit(player, (playerx, playery)) # the player
    Genmod.buildlvl(level, screen) # platforms
    Genmod.floorbuild(screen) # bottom kill plane
    Genmod.topbuild(screen) # top kill plane
    Genmod.endbuild(screen, endx) #end of level plane
    

"""Calculate gravity"""
def CalcGrav():
    global Gravity
    global playery
    global airtick
    if airtick > 35:
     airtick = 35
    playery += Gravity*(airtick)
 
 
 
 
"""State Update"""
def Stateup(state):
    
    global Gravity
    global State
    global player
    global playerx
    global playery
    global Xspeed
    global Yspeed
    global player_faceleft
    global player_faceright
    global playersizex
    global playersizey    


    if state == 0: #solid
        player = solid_sprite
        player_faceleft = pygame.transform.flip(player, True, False) #flips the sprite to face left
        player_faceright = pygame.transform.flip(player_faceleft, True, False) #flips the sprite to face right
        Xspeed = 25
        Yspeed = 25
        Gravity = 1
        playersizex = 83
        playersizey = 68
        State = 0
        
    if state == 1: #gas
        player = gas_sprite
        player_faceleft = pygame.transform.flip(player, True, False) #flips the sprite to face left
        player_faceright = pygame.transform.flip(player_faceleft, True, False) #flips the sprite to face right
        Xspeed = 0
        Yspeed = 0
        Gravity = -1
        playersizex = 92
        playersizey = 62
        State = 1
        
    if state == 2: #liquid
        player = liquid_sprite
        player_faceleft = pygame.transform.flip(player, True, False) #flips the sprite to face left
        player_faceright = pygame.transform.flip(player_faceleft, True, False) #flips the sprite to face right
        Xspeed = 25
        Yspeed = 25
        Gravity = 1
        playersizex = 78
        playersizey = 51
        State = 2
        
    
    
"""Collision detections"""


"""Collision with the floor, celling and the end of the level"""
def BorderCol():
    global playerx
    global playery
    global airtick
    global playersizex
    global playersizey
    global SCREEN_HEIGHT
    global SCREEN_WIDTH
    global level
    global endx
    global score
    
    
    if playery + playersizey > SCREEN_HEIGHT - 5: # bottom kill plane
        playery = SCREEN_HEIGHT/2 - platheight/2 - playersizey
        playerx = 75
        airtick = 0
        print(score)
        score = 0
        level = Genmod.genlvl(15)
        Stateup(0)
        endx = 5000
 
     
    if playery < 0: #top kill plane
        playery = SCREEN_HEIGHT/2 - platheight/2 - playersizey
        playerx = 75
        airtick = 0
        print(score)
        score = 0
        level = Genmod.genlvl(15)
        Stateup(0)
        endx = 5000
        
    
    if playerx > endx: # goaline 
        print('You finshed a level!')
        playery = SCREEN_HEIGHT/2 - platheight/2 - playersizey
        playerx = 75
        airtick = 0
        score += 1
        level = Genmod.genlvl(15)
        Stateup(0)
        endx = 5000
     


    
        


"""Collision with Platforms"""
def PLatCol(State):
    global playerx
    global playery
    global airtick
    global playersizex
    global playersizey
    
    colision = False 
    for x in range(len(level)):
     for y in range(len(level[x])): 
        if playerx + playersizex < level[x][y][0]: #top
            col = 'top'
        elif playerx > level[x][y][0] + platwidth: #bottom
            col = 'bottom'
        elif playery + playersizey < level[x][y][1]: #left
            col = 'left'
        elif playery > level[x][y][1] + platheight: #right
            col = 'right'          
        else:
         if level[x][y][2] <= 5 and State == 0: # checking if player is in right state to collide
            colision = True
         elif 5 < level[x][y][2] <= 10 and State == 2:
            colision = True
         elif level[x][y][2] == 11:
            colision = True
         else:
            colision = False
            
        if colision == True:
         
            if level[x][y][0] < playerx + playersizex/2 < level[x][y][0] + platwidth:
                
             if level[x][y][1] < playery + playersizey < level[x][y][1] + platheight/2:
                playery = level[x][y][1] - playersizey
            
             if level[x][y][1] + platheight/2 < playery + playersizey:
                 colision = False
            
            
    if colision == True:
        airtick = 0
          
    else:
       airtick += 1
        
        


"""moving the camera"""
def move_camera() :
    global playerx
    global playery
    global Xspeed
    global Yspeed
    global endx
    
    global cameralimit
    global cameralimitleft
    global cameralimitright
    
    global camerax
    global cameray
    global HALF_SCREEN_HEIGHT
    global HALF_SCREEN_WIDTH
    
    playerCenterx = playerx + int(playerx / 2)
    playerCentery = playery + int(playery / 2)
    if (camerax + HALF_SCREEN_WIDTH) - playerCenterx > cameralimitleft:
        playerx += Xspeed
        for x in range(len(level)):
             for y in range(len(level[x])): 
                 level[x][y][0] += Xspeed
        
        
        endx += Xspeed  
                 
    elif playerCenterx - (camerax + HALF_SCREEN_WIDTH) > cameralimitright:
        playerx -= Xspeed
        for x in range(len(level)):
            for y in range(len(level[x])): 
                level[x][y][0] -= Xspeed
     
     
        endx -= Xspeed   
                

    
"""movement options"""
pressed_right = False
pressed_left = False
pressed_down = False
pressed_up = False

def go_right() :
    #moves player right
    global playerx
    playerx += Xspeed

def go_left() :
    #moves player left
    global playerx
    playerx -= Xspeed #speed at which the player moves

def go_up() :
    #moves player up
    global playery
    playery -= Yspeed #speed at which the player moves

def go_down() :
    #moves player up
    global playery
    playery += Yspeed #speed at which the player moves


"""key presses"""
def pressed_keys(pygame) :
    #which global variables the function is referencing
    global Gravity
    global State
    global player
    global playerx
    global playery
    global Xspeed
    global Yspeed
    global current_state
    global player_faceleft
    global player_faceright
    global playersizex
    global playersizey
    global level 
    
    global pressed_right
    global pressed_left
    global pressed_down
    global pressed_up
    
    for event in pygame.event.get():
        #when a button is pressed
        if event.type == pygame.KEYDOWN:
            
            #moving left
            if event.key == pygame.K_LEFT:
                pressed_left = True
                player = player_faceleft
                #go_left()
                
            #moving right
            if event.key == pygame.K_RIGHT:
                pressed_right = True
                player = player_faceright
                #go_right()
                
            #moving up/jumping
            if event.key == pygame.K_UP:
                pressed_up = True
                #go_up()
                
            #changing state to solid
            if event.key == pygame.K_a:
                State = 0
                Stateup(0)
                
            #changing state to gas
            if event.key == pygame.K_s:
                State = 1
                Stateup(1)

                
            #changing state to liquid
            if event.key == pygame.K_d:
                State = 2
                Stateup(2)
                
            
            #restarting level
            
            if event.key == pygame.K_i:
                level = Genmod.genlvl(15)
                playerx = 75
                playersizey = SCREEN_HEIGHT/2
                
                
            if event.key == pygame.K_c:
                print(playerx)
                print(playery)
                print(endx)
                
            
            #closing game
            if event.key == pygame.K_ESCAPE:
                    print('You hit escape')
                    print('That quits the game')
                    quit()
            
        
        #when a button isnt pressed            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pressed_left = False
            if event.key == pygame.K_RIGHT:
                pressed_right = False
            if event.key == pygame.K_UP:
                pressed_up = False


"""main loop"""
def main () :
    #which global variables the function is referencing
    global pressed_right
    global pressed_left
    global ressed_down
    global pressed_up
    
    global player
    global playerx
    global playery
    global player_faceleft
    global player_faceright
    global state
    
    pygame.init()
    
    game_running = False

    while game_running == False :
        pygame.init()
        
        """run key press detection"""
        pressed_keys(pygame)
        
        if pressed_left:
            go_left()
            #player = player_faceleft
        if pressed_right:
            go_right()
            #player = player_faceright
        if pressed_up:
            go_up()
        
        
        """main loop"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = True
                pygame.quit()
                quit()
            
            #closing game through escape key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = True
        
        #fill screen background
        screen.fill(white)
        
        #render player
        render_objects(pygame, screen)
        
        #detect collision
        PLatCol(State)
        BorderCol()
        
        #Calculate Gravity
        CalcGrav()
        
        #move the camera
        move_camera()
        
        #update screen
        pygame.display.flip()
        
        #update screen rate
        fpsClock.tick(FPS)
        
main()
