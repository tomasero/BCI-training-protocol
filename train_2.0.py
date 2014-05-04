from math import pi
import pygame, pygbutton, sys
from pygame.locals import *

FPS = 30
pygame.init()

size = [700, 700]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Training')

#Colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
GREY =  (192, 192, 192)


# Display some text
font = pygame.font.Font(None, 36)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(WHITE)
centerx = background.get_rect().centerx
centery = background.get_rect().centery

text = font.render("UP", 1, BLACK)
textpos = text.get_rect()
textpos.centerx = centerx
textpos.centery = 50
background.blit(text, textpos)

boxUp = [centerx-75, centerx+75, centery-100, centery-250]
boxRight = [centerx+75, centerx+255, centery+50, centery-100]
boxDown = [centerx-75, centerx+75, centery+200, centery+50]
boxLeft = [centerx-225, centerx-75, centery+50, centery-100]

up = [[centerx, centery-250], [centerx-75, centery-100], [centerx+75, centery-100]]
right = [[centerx+225, centery-25], [centerx+75, centery+50], [centerx+75, centery-100]]
down = [[centerx, centery+200], [centerx-75, centery+50], [centerx+75, centery+50]]
left = [[centerx-225, centery-25], [centerx-75, centery+50], [centerx-75, centery-100]]
hand = pygame.image.load('hand.png')
handScaled = pygame.transform.scale(hand, (400, 200))
handRight = handScaled
handLeft = pygame.transform.flip(handScaled, True, False)
handDown = pygame.transform.rotate(handScaled, -90)
handUp = pygame.transform.rotate(handScaled, 90)

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
	drawDown(GREY)
	drawLeft(GREY)

def paintArrow(arrow, color):
	pygame.draw.polygon(background, color, arrow)
	pygame.draw.polygon(background, BLACK, arrow, 3)

def deactivateArrow():
	if active != None:
		paintArrow(active, GREY)

def updateScreen():
	screen.blit(background, (0,0))
	pygame.display.flip()

def paintHand(hand, x, y):
	background.blit(hand, (x, y))

def resetTraining():
	offArrows()
	drawButtons()
	updateScreen()

def animateHand(hand):
	background.fill(WHITE)
	originX = centerx-(hand.get_width()/2)
	originY = centery-(hand.get_height()/2)
	handX = originX
	handY = originY
	beginTime = pygame.time.get_ticks()
	while(pygame.time.get_ticks()-beginTime < 5000):
		background.fill(WHITE)
		paintHand(hand, handX, handY)
		if hand == handUp:
			handY-=10
			if handY <= 10:
				handY = originY
		elif hand == handDown:
			handY+=10
			if handY >= background.get_height()-10-hand.get_height():
				handY = originY
		elif hand == handLeft:
			handX-=10
			if handX <= 10:
				handX = originX
		else:
			handX+=10
			if handX >= background.get_width()-10-hand.get_width():
				handX = originX
		updateScreen()
	background.fill(WHITE)
	resetTraining()


def clickArrow(arrow):
	paintArrow(arrow, RED)

def trainArrow(arrow):
	paintArrow(arrow, GREEN)
	screen.blit(background, (0,0))
 	pygame.display.flip()
	pygame.time.delay(5000)
	paintArrow(arrow, GREY)
	active = None

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

resetTraining()

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
	        	clickArrow(up)
	        	active = up
	        elif isCollision(right, pos):
	        	deactivateArrow()
	        	clickArrow(right)
	        	active = right
	        elif isCollision(down, pos):
	        	deactivateArrow()
	        	clickArrow(down)
	        	active = down
	        elif isCollision(left, pos):
	        	deactivateArrow()
	        	clickArrow(left)
	        	active = left
	        elif len(eventTrain) > 0 and eventTrain[0] == 'enter' and active != None:
	        	#trainArrow(active)
	        	if active == up:
	        		tempArrow = handUp
	        	elif active == down:
	        		tempArrow = handDown
	        	elif active == left:
	        		tempArrow = handLeft
	        	elif active == right:
	        		tempArrow = handRight
	        	animateHand(tempArrow)
	        elif len(eventPractice) > 0 and eventPractice[0] == 'enter':
	        	print('Train')



                
 
	screen.blit(background, (0,0))
 
    # This draws a triangle using the polygon command
  

	pygame.display.flip()

pygame.quit()