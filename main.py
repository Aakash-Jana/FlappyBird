import random # for generating random numbers
import sys , pygame
from os import path
from pygame.locals import * #basic pygame imports
#global variables
FPS = 32 # frames per second
SCREENWIDTH = 500#1280
SCREENHEIGHT = 500 #found by trial and error
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT *0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
''' We are dynamically setting the path on the system now. '''
longPath = path.abspath('').split("\\")
FULLPATH = ''
for term in longPath:
    FULLPATH += term + "//"
PLAYER = FULLPATH +'player.png'
BACKGROUND = FULLPATH + 'back.png'
PIPE = FULLPATH + 'pipe.png'

def welComeScreen():
    '''Shows welcome images on the screen'''
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    while True:
        for event in pygame.event.get():
            #if user clicks X button
            evtype = event.type
            if event.type == pygame.KEYDOWN and (event.key==pygame.QUIT or event.key==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif evtype == pygame.KEYDOWN and (event.key==pygame.K_SPACE or event.key==pygame.K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2) # /2
    # create two pipes for blitting on screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    #My list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2),'y': newPipe2[0]['y']}  # newPipe2
    ]
    #My list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[1]['y']}
    ]
    pipeVelX = -4
    playerVelY = -9
    playerMinVelY = -8
    playerMaxVelY = 10
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            evtype = event.type
            # replaced evtye
            if evtype == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif evtype == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    #play flapping sound
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        #player is crashed
        if crashTest:
            return

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos + pipeMidPos + 4:
                #x = 1# useless line
                #score += 1
                print(f'your score is {score}')
                #play game sound
            if playerVelY < playerMaxVelY and not playerFlapped:
                    playerVelY += playerAccY
            if playerFlapped:
                playerFlapped = False
            playerHeight = GAME_SPRITES['player'].get_height()
            playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)
        score += 2  
        #move pipes to the left
        # zip maps elements of two lists two each other corresponding to their positon
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
        # add a new pipe when an old pipe moves out
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        # if the pipe is out of the screen remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        #Lets blit our sprites
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):# lowerPipe['y']
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'], upperPipe['y']))#may give error - have to change upperPipe to something else
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENWIDTH*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery>GROUNDY-25 or playery<0:
        #play hit sound
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x'] < GAME_SPRITES['pipe'][0].get_height())):
            #play hit sound
            return True
    for pipe in lowerPipes:
        if ((playery + GAME_SPRITES['player'].get_height() > pipe['y']) and (abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_height())):
            #play hit sound
            return True
def getRandomPipe():
    '''generate two positions of pipes for blitting on screen'''
    pipe1Height = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - 1.2*offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipe1Height - y2 + offset
    pipe = [
        {'x':pipeX,'y':-y1},
        {'x':pipeX,'y':y2}
    ]
    return pipe

if __name__=='__main__':
    #game starts here
    pygame.init() #initializes pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Aakash (Script KiDDie)')
    GAME_SPRITES['numbers'] = {
       0:pygame.image.load(FULLPATH + '0.png').convert_alpha(),
       1:pygame.image.load(FULLPATH + '1.png').convert_alpha(),
       2:pygame.image.load(FULLPATH + '2.png').convert_alpha(),
       3:pygame.image.load(FULLPATH + '3.png').convert_alpha(),
       4:pygame.image.load(FULLPATH + '4.png').convert_alpha(),
       5:pygame.image.load(FULLPATH + '5.png').convert_alpha(),
       6:pygame.image.load(FULLPATH + '6.png').convert_alpha(),
       7:pygame.image.load(FULLPATH + '7.png').convert_alpha(),
       8:pygame.image.load(FULLPATH + '8.png').convert_alpha(),
       9:pygame.image.load(FULLPATH + '9.png').convert_alpha()
    }
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert()
    
    welComeScreen() 
    while True:
        mainGame()