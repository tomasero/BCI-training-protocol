import pygame, pygbutton, sys, math, numpy, time
from math import pi
from pygame.locals import *
import gradients


#sys.path.append('../ClassyBCI')
#from openbci_collector import *
#collector = OpenBCICollector(port='/dev/tty.usbmodem1411')

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
boxBase = [centerx-75, centerx+75, centery+200, centery+50]
boxLeft = [centerx-225, centerx-75, centery+50, centery-100]

#Arrow positions

up = [[centerx, centery-250], [centerx-75, centery-100], [centerx+75, centery-100]]
right = [[centerx+225, centery-25], [centerx+75, centery+50], [centerx+75, centery-100]]
left = [[centerx-225, centery-25], [centerx-75, centery+50], [centerx-75, centery-100]]
base = [[centerx+75, centery+75], [centerx-75, centery+75], [centerx-75, centery+50], [centerx+75, centery+50]]

#Hands
#hand = pygame.image.load('hand.png')
#handScaled = pygame.transform.scale(hand, (400, 200))
#handRight = handScaled
#handLeft = pygame.transform.flip(handScaled, True, False)
#handDown = pygame.transform.rotate(handScaled, -90)
#handUp = pygame.transform.rotate(handScaled, 90)
leftOpen = pygame.transform.scale(pygame.image.load('leftOpen.png'), MOVE_SIZE)
leftClosed = pygame.transform.scale(pygame.image.load('leftClosed.png'), MOVE_SIZE)
rightOpen = pygame.transform.scale(pygame.image.load('rightOpen.png'), MOVE_SIZE)
rightClosed = pygame.transform.scale(pygame.image.load('rightClosed.png'), MOVE_SIZE)
feetOpen = pygame.transform.scale(pygame.image.load('feetOne.png'), MOVE_SIZE)
feetClosed = pygame.transform.scale(pygame.image.load('feetTwo.png'), MOVE_SIZE)
spider = pygame.transform.scale(pygame.image.load('bciSpider.jpg'), (200, 200))
#leftOpen = pygame.transform.rotate(handOpen, 90)
#rightOpen = pygame.transform.flip(pygame.transform.rotate(handOpen, -90), False, True)
#leftClose = pygame.transform.rotate(handClose, 90)
#rightClose = pygame.transform.flip(pygame.transform.rotate(handClose, -90), False, True)


#Dictionaries
handRight = {'open':rightOpen, 'close':rightClosed}
handLeft = {'open':leftOpen, 'close':leftClosed}
feet = {'open':feetOpen, 'close':feetClosed}
moves = {'right':handRight, 'left':handLeft, 'up':feet}
colors = {'right':RED, 'left':BLUE, 'up':GREEN, 'base': WHITE}
colorsXY = {'up': (0, 0, WIDTH, 500), 'left': (0, 0, 500, HEIGHT), 'right': (WIDTH-500, 0, 500, HEIGHT), 'base': (0, 0, WIDTH, HEIGHT)}

#Buttons

buttonTrain = pygbutton.PygButton((centerx-80, 600, 70, 30), 'Train')
buttonPractice = pygbutton.PygButton((centerx+10, 600, 70, 30), 'Practice')

def drawBase(color):
	pygame.draw.polygon(background, color, base)
	pygame.draw.polygon(background, BLACK, base, 3)

def drawSpider():
	background.blit(spider, (centerx-100, centery-120))

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
	drawBase(GREY)

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
	elif move == 'base':
		begin = white
		end = theColor
		return gradients.horizontal(coor, begin, end)

def resetTraining():
	writeTitle('Battle Spider BCI Training Interface', 40)
	drawSpider()
	offArrows()
	drawButtons()
	updateScreen()

def animateMove(move):
	#start = time.time()
	background.fill(WHITE)
	moveX = centerx-(MOVE_SIZE[0]/2)
	moveY = centery-(MOVE_SIZE[0]/2)
	beginTime = pygame.time.get_ticks()
	state = False
	while(pygame.time.get_ticks()-beginTime < 5000):
		background.fill(WHITE)
		paintColor(move)
		if move != 'base':
			if state:	
				paintMove(move, 'close', moveX, moveY)
				state = False
			else:
				paintMove(move, 'open', moveX, moveY)
				state = True
		writeTitle(move, 70)
		updateScreen()
		pygame.time.delay(200)
	#end = time.time()
	#sendData(move, start, end)
	background.fill(WHITE)
	resetTraining()

#def trainArrow(arrow):
#	paintArrow(arrow, GREEN)
#	screen.blit(background, (0,0))
 #	pygame.display.flip()
#	pygame.time.delay(5000)
#	paintArrow(arrow, GREY)
#	active = None

#def sendData(move, start, end):
#	f = open('data.csv', 'a')
#	f.write('{0}, {1}, {2}'.format(move, start, end))
#	f.write('\n')
#	f.close()

def writeTitle(title, size):
	font = pygame.font.Font(None, size)
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
	elif arrow == base:
		return boxBase
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

#def controlEEG(status):
#	if status == 'start':
#		collector.start_bg_collection()
#	elif status == 'stop':
#		collector.stop_bg_collection()
#		collector.disconnect()

#def tag(status, name):
#	if status == 'start':
#		collector.tag_it(name)
#	elif status == 'stop':
#		collector.tag_it(None)


resetTraining()
updateScreen()

done = False

active = None

#controlEEG('start')
while not done:
	
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			#controlEEG('stop')
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
			elif isCollision(base, pos):
				deactivateArrow()
				clickArrow('base', base)
				active = base
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
				elif active == base:
					tempMove = 'base'

				#tag('start', tempMove)
				print(tempMove)
				animateMove(tempMove)
				#tag('stop', tempMove)
			elif len(eventPractice) > 0 and eventPractice[0] == 'enter':
				print('practice')


	updateScreen()

pygame.quit()