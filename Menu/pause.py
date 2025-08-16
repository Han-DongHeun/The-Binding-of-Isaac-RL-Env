# pause.py
# Aaron Taylor
# Moose Abumeeiz
#
# The pause menu takes over the game and displays the
# players current stats and seed.
# 


from pygame import *
from math import *
from utils.const import *
from utils.func import *
from utils.loadResource import *

def pause(screen, seed, textures : dict[str, Surface], fonts, stats):
	running = True
	arrowpoint = 0
	pausecard = textures["pauseCard"]
	ticker = fonts["ticks"]
	digitstwo = fonts["main"]
	seedcard = textures["seedCard"]
	arrow = textures["arrow"]
	arrowlocation = [(350,375),(380,420)]
	seed = list(seed.upper())
	speed, shotspeed, damage, luck, firerate, distance = stats
	clock = time.Clock()

	slide = darken(screen.copy(), .6)

	pausecard_rect = pausecard.get_rect(center=(WIDTH//2, HEIGHT//2))
	seedcard_rect = seedcard.get_rect()

	roading_frame = 20
	for i in reversed(range(roading_frame)):
		clock.tick(60)
		screen.blit(slide,(0,0))

		pausecard_rect.centerx = WIDTH//2 - WIDTH//roading_frame * i
		screen.blit(pausecard, pausecard_rect)

		seedcard_rect.centerx = pausecard_rect.left
		seedcard_rect.top = pausecard_rect.top
		screen.blit(seedcard, seedcard_rect)
		display.flip()

	while running:
		for e in event.get():
			if e.type == QUIT:
				quit()
			elif (e.type == KEYDOWN and e.key == 27) or (e.type == KEYDOWN and e.key == 32 and arrowpoint == 0):
				running = False
			elif e.type == KEYDOWN and e.key == 32 and arrowpoint == 1:
				return False
					
			if e.type == KEYDOWN and e.key == 273:
				arrowpoint -= 1
			elif e.type == KEYDOWN and e.key == 274:
				arrowpoint += 1

			if arrowpoint > 1:
				arrowpoint = 0
			elif arrowpoint < 0:
				arrowpoint = 1

		screen.blit(slide,(0,0)) 
		screen.blit(pausecard,pausecard_rect)
		screen.blit(seedcard,seedcard_rect)

		seed1 = write(seed[0:4],digitstwo)
		seed2 = write(seed[4:],digitstwo)
		seed1_rect = seed1.get_rect(midbottom=seedcard_rect.center)
		seed2_rect = seed2.get_rect(midtop=seedcard_rect.center)
		screen.blit(seed1, seed1_rect)
		screen.blit(seed2, seed2_rect)
		""" screen.blit(arrow,(arrowlocation[arrowpoint]))
		for i in range(speed):
			screen.blit(ticker[i],(429+(i*8),193))
		for i in range(distance):
			screen.blit(ticker[i],(545+(i*8),193))
		for i in range(firerate):
			screen.blit(ticker[i],(429+(i*8),225))
		for i in range(damage):
			screen.blit(ticker[i],(429+(i*8),260))
		for i in range(shotspeed):
			screen.blit(ticker[i],(545+(i*8),225))
		for i in range(luck):
			screen.blit(ticker[i],(545+(i*8),260)) """

		clock.tick(60)               

		display.flip()

	for i in range(roading_frame):
		clock.tick(60)

		screen.blit(slide,(0,0))

		pausecard_rect.centerx += WIDTH//roading_frame
		seedcard_rect.centerx = pausecard_rect.left
		seedcard_rect.top = pausecard_rect.top
		screen.blit(pausecard, pausecard_rect)
		screen.blit(seedcard, seedcard_rect)
		display.flip()

	return True