"""Author: (c)copyright Earl Martin Momongan"""
"""email: techwiz@csu.fullerton.edu"""
"""phone: (714)510-7497"""

import pygame
import MyPRNG
import time
import sys
import math

prng = MyPRNG.MyPRNG() #uses my PRNG
pygame.init()

#loads in sounds and music
pop_sound = pygame.mixer.Sound("sounds/pop_sound.wav")

display_width = 1200 #width of screen
display_height = 900 #height of screen

background = pygame.image.load("images/snakes_ladders_board1.png") #loads in a background image
background = pygame.transform.scale(background,(900,900))

title = pygame.image.load("images/title.png")                     #loads in the title logo
title = pygame.transform.scale(title,(960, 720))

#loads in dice images
dice1 = pygame.image.load("images/dice1.png") 
dice2 = pygame.image.load("images/dice2.png")
dice3 = pygame.image.load("images/dice3.png")
dice4 = pygame.image.load("images/dice4.png")
dice5 = pygame.image.load("images/dice5.png")
dice6 = pygame.image.load("images/dice6.png")

dice1 = pygame.transform.scale(dice1,(150,150))
dice2 = pygame.transform.scale(dice2,(150,150))
dice3 = pygame.transform.scale(dice3,(150,150))
dice4 = pygame.transform.scale(dice4,(150,150))
dice5 = pygame.transform.scale(dice5,(150,150))
dice6 = pygame.transform.scale(dice6,(150,150))

die = {1:dice1,2:dice2,3:dice3,4:dice4,5:dice5,6:dice6}               #die dictionary
ladders = {0:37,3:13,8:30,20:41,27:83,35:43,50:66,70:90,79:99}        #ladders dictionary
snakes = {15:5,46:25,48:10,55:52,61:18,63:59,86:23,92:72,94:74,97:77} #snakes dictionary

#initializes colors to be used
black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
yellow = (247, 231, 56)

hRed = (255,0,0)
hGreen = (0,255,0)
hBlue = (0,0,255)
hYellow = (255, 252, 99)

gameDisplay = pygame.display.set_mode((display_width, display_height)) #sets the games display
pygame.display.set_caption("Snakes and Ladders")  
clock = pygame.time.Clock() #sets the game clock for use such as "fps"

#creates an object for the text to be displayed on
#takes in a string value, style of font, and font color
def text_objects(text, font, fontColor): 
    textSurface = font.render(text, True, fontColor)
    return textSurface, textSurface.get_rect()
    
#displays text 
#takes in a string, pygame.font.Font() value, font color, and a x and y value
def message_display(text,fontSize,x,y,fontColor):
    fontStyle = pygame.font.Font('freesansbold.ttf',fontSize)
    textSurf, textRect = text_objects(text, fontStyle,fontColor)
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)
    
#creates a button
#takes in a 2 color values, the x y w h values, a string value, font size, and the font color
def button(color,highlight,x,y,w,h,text,fontSize,fontColor,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    #checks to see if the mouse is clicked
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay,highlight,(x,y,w,h))
        if click[0] == 1 and action != None:
            pygame.mixer.Sound.play(pop_sound)
            time.sleep(0.8)
            result = action()
            return result
    else:    
        pygame.draw.rect(gameDisplay,color,(x,y,w,h))
        
    message_display(text,fontSize,(x+(w/2)),(y+(h/2)),fontColor)
    
    
#runs the intro sequence of the game    
def game_intro():
    pygame.mixer.music.stop()
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
                
        gameDisplay.fill(white)
        gameDisplay.blit(title,(150,100))
        message_display("Snakes and Ladders",100,(display_width/2),((display_height/2)-75),yellow)
        
        button(green,hGreen,150,500,200,100,"PLAY",40,black,game_loop) #play button
        button(blue,hBlue,497,500,200,100,"CREDITS",40,black,credits)  #credits button
        button(red,hRed,844,500,200,100,"RULES",40,black,rules)        #rules button
                
        pygame.display.update()
        clock.tick(60)
           
#runs the game loop     
def game_loop():
    
    current1Pos = -1  #starting tile on board
    current2Pos = -1  #starting tile on board
    turnCount = 1     #count of turn
    playerTurn = True #assigns the player turn
    phase = 1         #assigns the phase
    endPhase = False  #checks to see if the phase has ended
    aiRolled = False  #checks to see if the ai has rolled
    endTurn = False   #checks to see if the turn has ended
    
    player1 = player_init(10) #initializes possible locations 
    player2 = player_init(50) #initializes possible locations
    
    pygame.mixer.music.play(-1) #sets music to loop infinitely
    roll = False                #checks to see if the user has rolled
    gameExit = False            #exits game if set to True
    dice = dice6                #dice image is initialized to dice 6

    while not gameExit:
        for event in pygame.event.get(): #gets any even that happens (mouse clicks, etc)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        gameDisplay.fill(white)
        gameDisplay.blit(background,(0,0))
        message_display(("Turn "+str(turnCount)),30,1044,75,black)
        button(yellow,hYellow,944,150,200,100,"BACK",30,black,game_intro) #back button to main menu

        #checks to see if player 1 is on a ladder or snake
        if current1Pos in ladders:
            if endPhase == True:
                time.sleep(1.5)
                current1Pos = ladders[current1Pos]
                endPhase = False
        elif current1Pos in snakes:
            if endPhase == True:
                time.sleep(1.5)
                current1Pos = snakes[current1Pos]
                endPhase == False
                
        #checks to see if player 2 is on a ladder or snake
        if current2Pos in ladders:
            time.sleep(1.5)
            current2Pos = ladders[current2Pos]
        elif current2Pos in snakes:
            time.sleep(1.5)
            current2Pos = snakes[current2Pos]
        
        #checks to see if player 1 or 2 has reached the end
        if current1Pos >= 99:
            time.sleep(2)
            player_win(1,hBlue)
        elif current2Pos >= 99:
            time.sleep(2)
            player_win(2,hRed)
            
        if endPhase == True:
            time.sleep(1.5)
            endPhase = False
        if playerTurn == False:
            phase = 2
        elif playerTurn == True:
            phase = 1

        #player 1 turn
        if playerTurn == True and phase == 1:

            roll = button(green,hGreen,944,750,200,100,"ROLL DICE",30,black,rolled)
            if roll == True:
                container = player_move(playerTurn,current1Pos,turnCount)
                dice = container[0]
                current1Pos = container[1]
                if current1Pos >= 99:
                    current1Pos = 99
                playerTurn = container[2]
                player_display(blue,hRed)
                endPhase = True

            gameDisplay.blit(dice,(969,575))
            player_display(hBlue,red)

        #player 2 turn
        elif playerTurn == False and phase == 2:

            if aiRolled == False:
                container = player_move(playerTurn,current2Pos,turnCount)
                dice = container[0]
                current2Pos = container[1]
                if current2Pos >= 99:
                    current2Pos = 99

            aiRolled = True
            gameDisplay.blit(dice,(969,575))
            player_display(blue,hRed)

            endTurn = button(yellow,hYellow,944,750,200,100,"END TURN",30,black,end_turn)
            if endTurn == True:
                aiRolled = False
                playerTurn = container[2]
                turnCount = container[3]                    


        if current1Pos != -1:
            pygame.draw.ellipse(gameDisplay,hBlue,player1[current1Pos])
        if current2Pos != -1:
            pygame.draw.ellipse(gameDisplay,hRed,player2[current2Pos])

        pygame.display.update() #updates the display  
        clock.tick(60)          #sets the fps

#credits window
def credits():
    rules = True
    
    while rules:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
                
        gameDisplay.fill(white)
        message_display("CREDITS",80,(display_width/2),((display_height/2)-350),black)
        #background image
        message_display("https://s-media-cache-ak0.pinimg.com/originals/28/d3/d9/28d3d9de28b3b886028d063f2f0c218f.jpg",20,(display_width/2),((display_height/2)-280),black)
        #logo image
        message_display("http://devine.co.uk/peter/wp-content/uploads/2015/01/snakes-ladders.png",20,(display_width/2),((display_height/2)-230),black)
        #dice 1
        message_display("http://www.clipartkid.com/images/160/dice-1-clip-art-at-clker-com-vector-clip-art-online-royalty-free-GIXbjz-clipart.png",20,(display_width/2),((display_height/2)-180),black)
        #dice 2
        message_display("https://uchicago.s3.amazonaws.com/d02.png",20,(display_width/2),((display_height/2)-130),black)
        #dice 3
        message_display("http://www.clipartkid.com/images/160/dice-3-clip-art-at-clker-com-vector-clip-art-online-royalty-free-UvzDUn-clipart.png",20,(display_width/2),((display_height/2)-80),black)
        #dice 4
        message_display("http://hearmewhisper.ddns.net/dice/die4.png",20,(display_width/2),((display_height/2)-30),black)
        #dice 5
        message_display("http://images.clipartpanda.com/low-clipart-dice-5-md.png #dice",20,(display_width/2),((display_height/2)+20),black)
        #dice 6
        message_display("http://www.clipartkid.com/images/214/dice-6-clip-art-at-clker-com-vector-clip-art-online-royalty-free-yPbWet-clipart.png",20,(display_width/2),((display_height/2)+70),black)
        #pop sound effect
        message_display("https://www.freesound.org/people/debsound/sounds/320549/",20,(display_width/2),((display_height/2)+120),black)
        #music was covered by myself and my band
        message_display("Donkey Kong music theme owned by Nintendo.",20,(display_width/2),((display_height/2)+170),black)
        
        button(green,hGreen,497,750,200,100,"BACK",40,black, game_intro)
                
        pygame.display.update()
        clock.tick(60)

#rules window
def rules():
    rules = True
    
    while rules:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
                
        gameDisplay.fill(white)
        message_display("RULES",80,(display_width/2),((display_height/2)-350),black)
        message_display("The player will play as player 1 against player 2",30,(display_width/2),((display_height/2)-280),black)
        message_display("Players move through the board based on dice rolls",30,(display_width/2),((display_height/2)-230),black)
        message_display("If a player lands on a ladder, travel up the ladder",30,(display_width/2),((display_height/2)-180),black)
        message_display("If a player lands on a snake, travel down the snake",30,(display_width/2),((display_height/2)-130),black)
        message_display("The first one to reach the 100th tile wins",30,(display_width/2),((display_height/2)-80),black)
        message_display("To roll dice, click on Roll Dice button on player 1 turn",30,(display_width/2),((display_height/2)-30),black)
        message_display("To end turn, click on End Turn button after player 2 turn",30,(display_width/2),((display_height/2)+20),black)
        
        button(green,hGreen,497,600,200,100,"BACK",40,black, game_intro)
                
        pygame.display.update()
        clock.tick(60)

#initializes player and returns the coordinates
def player_init(value):
    player = []
    loop = 1
    for j in range(9,-1,-1):
        if loop == 1 or loop == 3 or loop == 5 or loop == 7 or loop == 9:
            for x in range(0,10):
                player.append([value+(89*x),11+(88.7*j),34,78])
            loop = loop + 1
        elif loop == 2 or loop == 4 or loop == 6 or loop == 8 or loop == 10:
            for n in range(9,-1,-1):
                player.append([value+(89*n),11+(88.7*j),34,78])
            loop = loop + 1
    return player

#uses prng to simulate dice rolls
def dice_roll():    
    for i in range(100):
        prn = prng.next_prn()
    prn = (prn % 6) + 1
    return prn

#moves player token and rolls the die
def player_move(isPlayer,currentPos,turn):    
    roll = dice_roll()    
    
    if roll in die:
        dice = die[roll]
        currentPos = currentPos + roll
        
    if isPlayer == True:
        isPlayer = False        
    elif isPlayer == False:
        isPlayer = True
        turn = turn + 1

    return (dice,currentPos,isPlayer,turn)

#displays whose turn it is
def player_display(color1,color2):    
    pygame.draw.rect(gameDisplay,color1,(944,350,200,100))
    pygame.draw.rect(gameDisplay,color2,(944,450,200,100))
    message_display("Player 1",30,(944+(200/2)),(350+(100/2)),black)
    message_display("Player 2",30,(944+(200/2)),(450+(100/2)),black)    

#checks to see if the dice has been rolled
def rolled():
    return True

#checks to see if the turn ended
def end_turn():
    return True

#sets the player win message
def player_win(player, color):
    win = True
    
    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
                
        gameDisplay.fill(white)
        gameDisplay.blit(title,(150,100))
        message_display("Player "+str(player)+" Wins!",100,(display_width/2),((display_height/2)-75),color)        
                
        pygame.display.update()
        clock.tick(60)
    
def main():
    game_intro()
    pygame.quit()
    sys.exit(0)
    
if __name__ == "__main__":
    main()