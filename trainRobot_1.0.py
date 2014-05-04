import pygame, pygbutton, sys, math, numpy
from math import pi
from pygame.locals import *
import gradients

FPS = 30
pygame.init()

WIDTH  = 700
HEIGHT = 700

size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)
#pygame.display.set_caption('Training')

#Colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
GREY =  (192, 192, 192)
MOVE_SIZE = (500, 500)

#Background

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(WHITE)
centerx = background.get_rect().centerx
centery = background.get_rect().centery

#Boxes

boxUp = [centerx-75, centerx+75, centery-100, centery-250]
boxRight = [centerx+75, centerx+255, centery+50, centery-100]
boxDown = [centerx-75, centerx+75, centery+200, centery+50]
boxLeft = [centerx-225, centerx-75, centery+50, centery-100]

#Arrow positions

up = [[centerx, centery-250], [centerx-75, centery-100], [centerx+75, centery-100]]
right = [[centerx+225, centery-25], [centerx+75, centery+50], [centerx+75, centery-100]]
down = [[centerx, centery+200], [centerx-75, centery+50], [centerx+75, centery+50]]
left = [[centerx-225, centery-25], [centerx-75, centery+50], [centerx-75, centery-100]]

#Hands
#hand = pygame.image.load('hand.png')
#handScaled = pygame.transform.scale(hand, (400, 200))
#handRight = handScaled
#handLeft = pygame.transform.flip(handScaled, True, False)
#handDown = pygame.transform.rotate(handScaled, -90)
#handUp = pygame.transform.rotate(handScaled, 90)
handOpen = pygame.transform.scale(pygame.image.load('open.png'), MOVE_SIZE)
handClose = pygame.transform.scale(pygame.image.load('closed.png'), MOVE_SIZE)
feetOpen = pygame.transform.scale(pygame.image.load('feetOne.png'), MOVE_SIZE)
feetClosed = pygame.transform.scale(pygame.image.load('feetTwo.png'), MOVE_SIZE)
leftOpen = pygame.transform.rotate(handOpen, 90)
rightOpen = pygame.transform.flip(pygame.transform.rotate(handOpen, -90), False, True)
leftClose = pygame.transform.rotate(handClose, 90)
rightClose = pygame.transform.flip(pygame.transform.rotate(handClose, -90), False, True)


#Dictionaries
handRight = {'open':rightOpen, 'close':rightClose}
handLeft = {'open':leftOpen, 'close':leftClose}
feet = {'open':feetOpen, 'close':feetClosed}
moves = {'right':handRight, 'left':handLeft, 'up':feet}
colors = {'right':RED, 'left':BLUE, 'up':GREEN}
colorsXY = {'up': (0, 0, WIDTH, 200), 'left': (0, 0, 200, HEIGHT), 'right': (WIDTH-200, 0, 200, HEIGHT)}

#Buttons

buttonTrain = pygbutton.PygButton((centerx-80, 600, 70, 30), 'Train')
buttonPractice = pygbutton.PygButton((centerx+10, 600, 70, 30), 'Practice')


def drawButtons():
	buttonPractice.draw(background)
	buttonTrain.draw(background)

def drawUp(color):
	pygame.draw.polygon(background, color, up)
	pygame.draw.polygon(background, BLACK, up, 3)

def drawRight(color):
	pygame.draw.polygon(background, color, right)
	pygame.draw.polygon(background, BLACK, right, 3)

def drawDown(color):
	pygame.draw.polygon(background, color, down)
	pygame.draw.polygon(background, BLACK, down, 3)

def drawLeft(color):
	pygame.draw.polygon(background, color, left)
	pygame.draw.polygon(background, BLACK, left, 3)	

def offArrows():
	drawUp(GREY)
	drawRight(GREY)
	#drawDown(GREY)
	drawLeft(GREY)

def paintArrow(arrow, color):
	pygame.draw.polygon(background, color, arrow)
	pygame.draw.polygon(background, BLACK, arrow, 3)

def clickArrow(move, arrow):
	paintArrow(arrow, colors[move])

def deactivateArrow():
	if active != None:
		paintArrow(active, GREY)

def paintMove(move, state, x, y):
	move = moves[move][state]
	background.blit(move, (x, y))

def paintColor(move):
	begin   = (0, 0, 255,255)
	end   = (0, 0, 0, 0)
	coor = colorsXY[move]
	gradient = getGradient(move, colors[move], (coor[2], coor[3]))
	background.blit(gradient, (coor[0], coor[1]))
	#pygame.draw.rect(background, colors[move], colorsXY[move])

def getGradient(move, color, coor):
	white = (WHITE[0], WHITE[1], WHITE[2], 0)
	theColor = (color[0], color[1], color[2], 255)
	if move == 'up':
		begin = theColor
		end = white
		return gradients.vertical(coor, begin, end)
	elif move == 'left':
		begin = theColor
		end = white
		return gradients.horizontal(coor, begin, end)
	elif move == 'right':
		begin = white
		end = theColor
		return gradients.horizontal(coor, begin, end)

def resetTraining():
	offArrows()
	drawButtons()
	updateScreen()

def animateMove(move):
	background.fill(WHITE)
	moveX = centerx-(MOVE_SIZE[0]/2)
	moveY = centery-(MOVE_SIZE[0]/2)
	beginTime = pygame.time.get_ticks()
	state = False
	while(pygame.time.get_ticks()-beginTime < 5000):
		background.fill(WHITE)
		paintColor(move)
		if state:	
			paintMove(move, 'close', moveX, moveY)
			state = False
		else:
			paintMove(move, 'open', moveX, moveY)
			state = True
		writeTitle(move)
		updateScreen()
		pygame.time.delay(200)
	background.fill(WHITE)
	resetTraining()

#def trainArrow(arrow):
#	paintArrow(arrow, GREEN)
#	screen.blit(background, (0,0))
 #	pygame.display.flip()
#	pygame.time.delay(5000)
#	paintArrow(arrow, GREY)
#	active = None

def writeTitle(title):
	font = pygame.font.Font(None, 40)
	text = font.render(title.upper(), 1, BLACK)
	textpos = text.get_rect()
	textpos.centerx = centerx
	textpos.centery = 50
	background.blit(text, textpos)

def getBox(arrow):
	if arrow == up:
		return boxUp
	elif arrow == right:
		return boxRight
	elif arrow == down:
		return boxDown
	elif arrow == left:
		return boxLeft

def isCollision(arrow, pos):
	posX, posY = pos
	box = getBox(arrow)
	x = [box[0], box[1]]
	y = [box[2], box[3]]
	minX = min(x)
	maxX = max(x)
	minY = min(y)
	maxY = max(y)
	insideX = posX > minX and posX < maxX
	insideY = posY > minY and posY < maxY
	if insideX and insideY:
		return True
	else:
		return False

def updateScreen():
	screen.blit(background, (0,0))
	pygame.display.flip()

resetTraining()
updateScreen()

done = False

active = None


while not done:
	for event in pygame.event.get():
	    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
	        pygame.quit()
	        sys.exit()
	        done = True
		#elif 'click' in buttonTrain.handleEvent(event):
		#	print("hola")
	    elif event.type == pygame.MOUSEBUTTONUP:

	    	eventPractice = buttonPractice.handleEvent(event)
	    	eventTrain = buttonTrain.handleEvent(event)
	        ## if mouse is pressed get position of cursor ##
	        pos = pygame.mouse.get_pos()
	        ## check if cursor is on button ##
	        if isCollision(up, pos):
	        	deactivateArrow()
	        	clickArrow('up', up)
	        	active = up
	        elif isCollision(right, pos):
	        	deactivateArrow()
	        	clickArrow('right', right)
	        	active = right
	        #elif isCollision(down, pos):
	        #	deactivateArrow()
	        #	clickArrow(down)
	        #	active = down
	        elif isCollision(left, pos):
	        	deactivateArrow()
	        	clickArrow('left', left)
	        	active = left
	        elif len(eventTrain) > 0 and eventTrain[0] == 'enter' and active != None:
	        	#trainArrow(active)
	        	if active == up:
	        		tempMove = 'up'
	        	elif active == left:
	        		tempMove = 'left'
	        	elif active == right:
	        		tempMove = 'right'
	        	animateMove(tempMove)
	        elif len(eventPractice) > 0 and eventPractice[0] == 'enter':
	        	print('practice')


	updateScreen()

pygame.quit()