# main.py
# Aaron Taylor
# Moose Abumeeiz
#
# The main file for our final project. This is a replica of
# the popular game The Binding waof Isaac: Rebirth.
# 

from utils.const import *
from pygame import *
from random import *
from utils.func import *
from Game import *
from Menu.menu import *
import os

init() # Initalize pygame

# Create display
screen = display.set_mode((WIDTH, HEIGHT))

def playMusic(name, sound_on=HUMAN_MODE):
	if sound_on == False:
		return
	mixer.music.load(os.path.join('res', 'music', name))
	mixer.music.play(-1)

# Setup display
display.set_caption("The Binding of Isaac: Rebirth")
display.set_icon(image.load(os.path.join('res','textures', 'icon.png')))

# Load all needed textures
textures = {
    # --- 캐릭터 및 UI 관련 ---
    "arrow": loadTexture("arrow.png", dir="pause", double=False),
    "character": {
		"lazarus": darken(loadTexture("lazarus.png"), 0.1),
        "isaac": darken(loadTexture("isaac.png"), 0.1),
        "eve": darken(loadTexture("eve.png"), 0.1),
    },
    "controls": loadTexture("controls.png"),
    "tears": {
        "tears": loadTexture("tears.png"),
        "tear_pop": loadTexture("tear_pop.png"),
    },
    "hearts": loadTexture("hearts.png"),
    "loading": [loadTexture(f"{i+1}.png", dir="loading") for i in range(56)],
    "map": {
        "background": loadTexture("minimap.png").subsurface(0, 0, 112, 102),
        "boss": loadTexture("minimap.png").subsurface(113, 64, 16, 16),
        "in": loadTexture("minimap.png").subsurface(113, 0, 16, 16),
        "entered": loadTexture("minimap.png").subsurface(113, 16, 16, 16),
        "item": loadTexture("minimap.png").subsurface(113, 48, 16, 16),
        "seen": loadTexture("minimap.png").subsurface(113, 32, 16, 16),
    },
    "overlays": [loadTexture(f"{i}.png", dir="overlays") for i in range(5)],
    "pauseCard": loadTexture("pauseCard.png", dir="pause"),
    "seedCard": loadTexture("seedcard.png", dir="pause"),
    "shading": loadTexture("shading.png"),
    
    # --- 맵 및 환경 요소 ---
    "doors": {
        "angel_door": darken(loadTexture("angel_door.png"), 0.25),
        "boss_door": darken(loadTexture("boss_door.png"), 0.25),
        "dark_door": darken(loadTexture("dark_door.png"), 0.25),
        "devil_door": darken(loadTexture("devil_door.png"), 0.25),
        "door": darken(loadTexture("door.png"), 0.25),
        "red_door": darken(loadTexture("red_door.png"), 0.25),
        "treasure_door": darken(loadTexture("treasure_door.png"), 0.25),
    },
    "fires": {
        "fire_bottom": loadTexture("fire_bottom.png"),
        "fire_top": loadTexture("fire_top.png"),
    },
    "floors": {
        "basement": loadTexture("basement.png"),
        "catacombs": loadTexture("catacombs.png"),
        "caves": loadTexture("caves.png"),
        "depths": loadTexture("depths.png"),
        "necropolis": loadTexture("necropolis.png"),
        "shop": loadTexture("shop.png"),
        "utero": loadTexture("utero.png"),
        "womb": loadTexture("womb.png"),
    },
    "poops": loadTexture("poops.png"),
    "rocks": darken(loadTexture("rocks.png"), 0.1),
    "trapdoor": loadTexture("trap_door.png"),

    # --- 아이템 및 픽업류 ---
    "bombs": {
        "bombs": loadTexture("bombs.png").subsurface(0,0,64,64),
        "explosion": loadTexture("explosion.png"),
        "smut": loadTexture("smut.png"),
    },
    "coins": {
        "dime": loadTexture("dime.png"),
        "nickel": loadTexture("nickel.png"),
        "penny": loadTexture("penny.png"),
    },
    "keys": loadTexture("keys.png").subsurface(0,0,32,64),
    "phd": loadTexture("phd.png"),
    "pickupHearts": loadTexture("pickup_hearts.png"),
    "pickups": loadTexture("pickups.png"),
    "pills": loadTexture("pills.png"),

    # --- 적 및 보스 ---
    "bosses": {
        "duke": loadTexture("duke.png", dir="bosses"),
        "gurdy": loadTexture("gurdy.png", dir="bosses"),
    },
    "enemies": {
        "boil": loadTexture("boil.png", dir="enemies"),
        "fly": loadTexture("fly.png", dir="enemies"),
        "host": loadTexture("host.png", dir="enemies"),
        "maw": loadTexture("maw.png", dir="enemies"),
        "pooter": loadTexture("pooter.png", dir="enemies"),
    },
    
    # --- 기타 효과 ---
    "streak": loadTexture("streak.png"),
}

textures["character"].update({
	name : {
		"heads" : [texture.subsurface(Rect((i*64)*2, 0, 64, 64)) for i in range(3)] + \
			[transform.flip(texture.subsurface(Rect((1*64)*2, 0, 64, 64)), True, False)],
		"tearHeads" : [texture.subsurface(Rect(64 + (i*64)*2, 0, 64, 64)) for i in range(3)] + \
			[transform.flip(texture.subsurface(Rect((64 + 1*64)*2, 0, 64, 64)), True, False)],
		"feet" : [
			[texture.subsurface(Rect((i*64), 64, 64, 64)) for i in range(8)],
			[texture.subsurface(Rect((i*64), 64*2, 64, 64)) for i in range(8)],
			[texture.subsurface(Rect((i*64), 64, 64, 64)) for i in range(8)],
			[transform.flip(texture.subsurface(Rect((i*64), 64*2, 64, 64)), True, False) for i in range(8)],
		],
		"specialFrames" : [texture.subsurface(i*128, 272+128, 128, 128) for i in (1, 2)],
	} for name, texture in textures["character"].items()
})

textures["tears"].update({
	"frames" : [textures["tears"]["tear_pop"].subsurface(Rect((i*128 - ((i)//4)*128*4), ((i//4)*128), 128, 128)) for i in range(12)],
	"tear" : textures["tears"]["tears"].subsurface(Rect(5 * 64, 0, 64, 64)),
	"blood" : textures["tears"]["tears"].subsurface(Rect(5 * 64, 2 * 64, 64, 64))
})

textures["rocks"] = {
	"rock" : [textures["rocks"].subsurface(Rect((variant*64), 0, 64, 64)) for variant in range(3)],
	"broken" : textures["rocks"].subsurface(Rect((3*64), 0, 64, 64)),
}

textures["poops"] = [[textures["poops"].subsurface(Rect((i*64), variant*64, 64, 64)) for i in range(5)] for variant in (0, 1, 3)]

textures["fires"] = {
	"fireFrames" : [textures["fires"]["fire_top"].subsurface(Rect(96*i, 0, 96, 104)) for i in range(6)],
	"woodFrames" : [
		[textures["fires"]["fire_bottom"].subsurface(Rect((64*i - (i//2)*128)+xMod, (i//2)*64+yMod, 64, 64)) for i in range(4)]
		for xMod, yMod in ((0, 0), (64 * 2, 0), (0, 64 * 2))
	]
}

textures["doors"] = {
	name : {
		"doorFrame" : texture.subsurface(0, 0, 64*2, 48*2),
		"doorBack" : texture.subsurface(64*2, 0, 64*2, 48*2),
		"lDoor" : texture.subsurface(0, 48*2, 64*2, 48*2),
		"rDoor" : texture.subsurface(64*2, 48*2, 64*2, 48*2),
		"lockedDoor" : texture.subsurface(64*2, 96*2, 64*2, 48*2),
	} for name, texture in textures["doors"].items() if name != "angel_door" and name != "devil_door"
}

textures["pickupHearts"] = [textures["pickupHearts"].subsurface(0,64*variant,64,64) for variant in range(3)]

textures["coins"] = {
	name : [texture.subsurface(i*128, 0, 128, 128) for i in range(6)]
		for name, texture in textures["coins"].items()
}

textures["bombs"]["explosion"] = [textures["bombs"]["explosion"].subsurface(192 * (i % 4), 192 * (i // 4), 192, 192) for i in range(12)]
textures["bombs"]["smut"] = [textures["bombs"]["smut"].subsurface(192*x, 128*y, 192, 128) for x, y in ((0, 0), (1, 0), (0, 1), (1, 1))]

textures["enemies"].update({
	"fly" : [textures["enemies"]["fly"].subsurface(i * 64, 0, 64, 64) for i in range(2)],
	"pooter" : [textures["enemies"]["pooter"].subsurface(i * 64, 0, 64, 64) for i in range(2)],
	"boil" : [textures["enemies"]["boil"].subsurface(64 * (i % 4), 64 * (i // 4), 64, 64) for i in reversed(range(10))],
	"host" : [textures["enemies"]["host"].subsurface(i*64, 0, 64, 128) for i in range(2)],
	"maw" : [textures["enemies"]["maw"].subsurface(0, 0, 64, 64)]
})

def resizing(textures):
	if isinstance(textures, Surface):
		w = textures.get_width() * SIZING
		h = textures.get_height() * SIZING
		return transform.scale(textures, (w, h))
	elif isinstance(textures, list):
		return [resizing(texture) for texture in textures]
	elif isinstance(textures, dict):
		return {name : resizing(texture) for name, texture in textures.items()}
	else:
		raise TypeError(f"Unsupported type for resizing: {type(textures).__name__}")
	
textures = resizing(textures)

# Load all sounds we need
sounds = {
	"pop": loadSound("pop.wav"),
	"explosion": loadSound("explosion.wav"),
	"hurt": [loadSound("hurt1.wav"), loadSound("hurt2.wav")],
	"tear": [loadSound("tear1.wav"), loadSound("tear2.wav"), loadSound("tearPop.wav"), loadSound("tearSplat.wav")],
	"unlock": loadSound("unlock.wav"),
	"devilRoomAppear": loadSound("devilRoomAppear.wav"),
	"angelRoomAppear": loadSound("angelRoomAppear.wav"),
	"coinDrop": loadSound("coinDrop.wav"),
	"coinPickup": loadSound("coinPickup.wav"),
	"fireBurn": loadSound("fireBurning.wav"),
	"steam": loadSound("steam.wav"),
	"keyDrop": loadSound("keyDrop.wav"),
	"keyPickup": loadSound("keyPickup.wav"),
	"heartIntake": loadSound("heartIntake.wav"),
	"holy": loadSound("holy.wav"),
	"rockBreak": loadSound("rockBreak.wav"),
	"doorOpen": loadSound("doorOpen.wav"),
	"doorClose": loadSound("doorClose.wav"),
	"deathBurst": loadSound("deathBurst.wav"),
	"pageTurn": loadSound("pageTurn.wav"),
	"error": loadSound("error.wav"),
	"selectLeft": loadSound("selectLeft.wav"),
	"selectRight": loadSound("selectRight.wav"),
	"bossIntro": loadSound("bossIntro.wav"),
}

# Load fonts
fonts = {
	"main": loadCFont("main.png", 20, 16, 36, size=1.8),
	"pickups": loadCFont("pickup.png", 10, 12, 10),
	"ticks": loadCFont("ticks.png", 4, 17 , 8),
}

# Begin main loop
running = True
while running:
	# Start by playing the title screen music
	playMusic("titleScreenLoop.ogg")

	# Begin menu
	characterType, controls, floorSeed = menu(screen, sounds)
	characterType = ("lazarus", "isaac", "eve")[characterType]

	# Floor setup
	seed(floorSeed)

	# Play the normal game music
	playMusic("basementLoop.ogg")

	# Start game
	game = Game(characterType, controls, floorSeed)
	game.run(screen, sounds, textures, fonts)

quit()