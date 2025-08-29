# func.py
# Aaron Taylor
# Moose Abumeeiz
#
# This file contains a many functions that are used throught the game
# 

import os
from utils.const import *
from random import randint

def generateSeed():
	# Create random level seed

	SEED_LENGTH = 8
	characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	charLen = len(characters)
	finalSeed = ""

	for i in range(SEED_LENGTH):
		finalSeed += characters[randint(0, SEED_LENGTH)]

	return finalSeed

def createSave(index, characterIndex, seed):
	f = open("save-%i.dat"%(index+1), "w+")
	f.write(str(characterIndex)+"\n"+seed)
	f.close()

def readSave(index):
	f = open("save-%i.dat"%(index+1), "r")
	data = f.read().split("\n")
	f.close()
	return int(data[0]), data[1]

def deleteSave(index):
	try:
		os.remove("save-%i.dat"%(index+1))
	except:
		pass

# BOSS INTRO

""" face = [None,None,None]
spot = [None,None,None,None,None,None,None]
title = [None,None,None]
bosstitle = [None,None,None]
bossface = [None,None,None]

frame = loadTexture("frame.png", dir="bossIntro")
spot[0] = loadTexture("spot1.png", dir="bossIntro")
spot[1] = loadTexture("spot2.png", dir="bossIntro")
spot[2] = loadTexture("spot3.png", dir="bossIntro")
spot[3] = loadTexture("spot4.png", dir="bossIntro")
spot[4] = loadTexture("spot5.png", dir="bossIntro")
spot[5] = loadTexture("spot6.png", dir="bossIntro")
spot[6] = loadTexture("spot7.png", dir="bossIntro")
bossspot = loadTexture("bossspot.png", dir="bossIntro")
face[1] = loadTexture("issacportrait.png", dir="bossIntro")
face[2] = loadTexture("eveportrait.png", dir="bossIntro")
face[0] = loadTexture("lazarusportrait.png", dir="bossIntro")
title[1] = loadTexture("titleissac.png", dir="bossIntro")
title[2] = loadTexture("titleeve.png", dir="bossIntro")
title[0] = loadTexture("titlelazarus.png", dir="bossIntro")
bosstitle[0] = loadTexture("titlegurdy.png", dir="bossIntro")
bosstitle[1] =  loadTexture("titledukeofflies.png", dir="bossIntro")
bossface[0] = loadTexture("gurdy.png", dir="bossIntro")
bossface[1] = loadTexture("dukeofflies.png", dir="bossIntro")
vs = loadTexture("vs.png", dir="bossIntro")

def bossIntro(screen, char,boss,floor):
	# Slide in character + boss
	for i in range(0,380,14):
		screen.blit(frame,(0,0))
		screen.blit(spot[floor],(-340+i,390))
		screen.blit(bossspot,(860-i,340))
		screen.blit(bossface[boss],(900-i,60))
		screen.blit(face[char],(-275+i,300))
		display.flip()
		
	# Slide in text
	copy = screen.copy()
	for i in range(0,500,16):
		screen.blit(copy,(0,0))
		screen.blit(title[char],(-400+i,10))
		screen.blit(vs,(-390+i,90))
		screen.blit(bosstitle[boss],(-400+i,170))
		display.flip()

	# Slower slide in
	for i in range(0,180,4):
		screen.blit(copy,(0,0))
		screen.blit(title[char],(100+i,10))
		screen.blit(vs,(110+i,90))
		screen.blit(bosstitle[boss],(100+i,170))
		display.flip()

	# Stall for a bit
	for i in range(0, 20):
		display.flip()

	copy = screen.copy()
	screen.blit(copy,(0,0))

# Textures for boss bar
emptybar = loadTexture("emptybar.png", dir="healthBar")
skull = loadTexture("skull.png", dir="healthBar")
fullbar = loadTexture("fullbar.png", dir="healthBar")

def bossbar(screen, health):
	# Draw boss bar with correc health
	
    if health == 1:
        screen.blit(fullbar,(350,-30))
    elif health <= 0:
        screen.blit(emptybar,(350,-30))
    else:
        screen.blit(emptybar,(350,-30))
        draw.rect(screen,(255,0,0),Rect(380,38,int(200*health)+45,16))
        screen.blit(skull,(364,20)) """

def get_center(x=6, y=3):
	centerx = GRIDX + (x + 0.5) * GRATIO
	centery = GRIDY + (y + 0.5) * GRATIO
	return (centerx, centery)

def get_grid_coord(x, y):
	gx = (x - GRIDX) // GRATIO 
	gy = (y - GRIDX) // GRATIO
	return (int(gx), int(gy))

def clamp(v, min_v, max_v):
	return max(min_v, min(max_v, v))