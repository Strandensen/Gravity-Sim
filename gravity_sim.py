#!/usr/bin/python3

#import libraries
#================
#from math import *
import math

#to use some terminal commands (e.g., 'clear')
import os

import random
import pygame
import pygame.math
#================

pygame.init()

#initial constants
res = pygame.Vector2((1920,1060))
screen = pygame.display.set_mode((int(res.x),int(res.y)))
pygame.display.set_caption("Simple Gravity Simulator")

#Actual gravitational constant: 6.67430 x 10^{-11}
GRAVITY = 667
num_objects = 2


#Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
ORANGE = (255,127,0)
YELLOW = (255,255,0)
LIME = (127,255,0)
GREEN = (0,255,0)
CHARTREUSE = (0,255,127)
CYAN = (0,255,255)
SKY = (0,127,255)
BLUE = (0,0,255)
PURPLE = (127,0,255)
MAGENTA = (255,0,255)
FUSCHIA = (255,0,127)

COLOR = [MAGENTA,FUSCHIA,RED,ORANGE,YELLOW,LIME,GREEN,CHARTREUSE,CYAN,SKY,BLUE,PURPLE,WHITE,BLACK]


#\begin{Functions
def unit_Normal(vec):
	return pygame.Vector2((-vec.y/vec.length(),vec.x/vec.length()))

def end_Program():
	pygame.quit()
	exit()

#assign radius based on log(mass)
	#return math.floor(math.log10(mass))
def radius_Map(mass):
	if mass < 513:
		return 10*math.floor(math.log(mass,2))
	else:
		return 100
#\end{Functions


#Stable orbit values
dist = 600
solar_mass = 4000
initialVelocity = math.sqrt(GRAVITY*solar_mass/dist)

#symmertric values
speed = 3
dist = 500


#Define Circ class
class Circ:
	def __init__(self,
				#mass=solar_mass,
				#position=pygame.Vector2((res.x/2,res.y/2)),
				#velocity=pygame.Vector2((0,0)),
				mass=40+random.randrange(100),#122
				position=pygame.Vector2((0,(res.y+dist)/2)),
				velocity=pygame.Vector2((speed,0)),
				color=COLOR[random.randrange(12)]):
		self.mass = mass
		self.position = position
		self.velocity = velocity
		self.acceleration = pygame.Vector2()
		self.radius = radius_Map(self.mass)
		self.color = color

	#calculate new position vector
	def move(self):
		#use acceleration to find new velocity vector
		self.velocity += self.acceleration

		#Use velocity to find new position vector
		self.position += self.velocity



#Create list of 'planets'
planet = [Circ(),Circ(mass=25+random.randrange(100),
					#position=pygame.Vector2((res.x/2,dist+res.y/2)),
					#velocity=pygame.Vector2((initialVelocity,0)),
					position=pygame.Vector2((res.x,(res.y-dist)/2)),
					velocity=pygame.Vector2((-speed,0)),
					color=COLOR[random.randrange(12)])]


#Creat some displays for parameters
font = pygame.font.SysFont('Lucida Console',18)
velocityDisplay = 'Planet {0:d} Velocity: {1:.2f}m/s, Mass: {2:d}'

text = []
textRect = []

for i in range(len(planet)):
	text.append(
		font.render(velocityDisplay.format(
			i,
			planet[i].velocity.length(),
			planet[i].mass),
			True,planet[i].color))
	textRect.append(text[i].get_rect())


#Loop until the user clicks the 'close' button
done = False

#Manage how quickly the screen updates
clock = pygame.time.Clock()


#-------Main Loop-------
while not done:
	#user did something
	for event in pygame.event.get():
		#if user clicked 'close'
		if event.type == pygame.QUIT:
			end_Program()
			done = True
		#'ESC' will also close the game
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				end_Program()
				done = True

	##first clear the window
	screen.fill(BLACK)

	#\begin{Game logic
	distance_vector = pygame.Vector2((planet[1].position.x-planet[0].position.x,planet[1].position.y-planet[0].position.y))
	buff = 75
	dist = distance_vector.length() if distance_vector.length() > buff else buff

	for i in range(len(planet)):
		#Calculate acceleration vectors
		j = len(planet) - (i + 1)

		planet[i].acceleration = ((-1) ** i)*(GRAVITY)*(1/(dist ** 3))*(planet[j].mass)*distance_vector

		#Move the current planet
		planet[i].move()


		#\end{Game logic

		#\begin{Drawing code
		#List of things that can be drawn: http://www.pygame.org/docs/ref/draw.html

		#Draw the current planet
		pygame.draw.circle(screen,planet[i].color,(int(planet[i].position.x),int(planet[i].position.y)),planet[i].radius)
	#end of for loop

	#Process text display
		text[i] = font.render(velocityDisplay.format(i,planet[i].velocity.length(),planet[i].mass),True,planet[i].color)
		textRect[i] = text[i].get_rect()
		textRect[i].bottomleft = (int(0),int(res.y-18*i))
		screen.blit(text[i],textRect[i])

	#update screen
	pygame.display.flip()

	#limit to 60 frames/sec
	clock.tick(60)
	#\end{Drawing code




pygame.quit()