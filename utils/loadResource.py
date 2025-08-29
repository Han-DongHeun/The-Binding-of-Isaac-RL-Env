from pygame import *
from utils.const import *
import os

from functools import lru_cache

def darken(image, amount):
    "Darken the image but preseve transparency"

    darken_level = max(0, int(255 * (1 - amount)))
    darken_color = (darken_level, darken_level, darken_level)

    darkened_image = image.convert_alpha()

    darkened_image.fill(darken_color, special_flags=BLEND_RGB_MULT)

    return darkened_image

@lru_cache(maxsize=16)
def loadImage(path):
	full_path = os.path.join('res', 'textures', *path.split('/'))
	texture = image.load(full_path).convert_alpha()

	return texture

def loadTexture(path, topleft=(0, 0), cell_size=None, scale_factor=SIZING*2):
	texture = loadImage(path)
	if cell_size != None:
		texture = texture.subsurface(topleft, cell_size)

	w, h = texture.get_size()
	scaled_size = (w * scale_factor, h * scale_factor)

	texture = transform.scale(texture, scaled_size)

	return texture

@lru_cache(maxsize=16)
def loadTextures(path, topleft, cell_size, grid_size, scale_factor=SIZING*2):
	spritesheet = loadImage(path)

	x, y = topleft
	w, h = cell_size
	r, c = grid_size

	scaled_size = (w * scale_factor, h * scale_factor)

	textures = [
		transform.scale(spritesheet.subsurface(x + j * w, y + i * h, w, h), scaled_size) 
		for i in range(r) for j in range(c)
		]

	return textures

class DummySound:
	def play(self, *args):
		pass

	def stop(self, *args):
		pass

def loadSound(path, sound_on=HUMAN_MODE):
	if sound_on:
		s = mixer.Sound(os.path.join('res','sounds', *path.split('/')))
	else:
		s = DummySound()

	return s

def loadCFont(path, total, cell_size, scale_factor=SIZING*2):
	# Load custom font

	full_path = os.path.join('res', 'fonts', *path.split('/'))
	spritesheet = image.load(full_path).convert_alpha()

	w, h = cell_size

	scaled_size = (w * scale_factor, h * scale_factor)

	digits = [
		transform.scale(spritesheet.subsurface(w * i, 0, w, h), scaled_size)
		for i in range(total)
		]
	space = Surface(scaled_size).convert_alpha()
	space.fill((0,0,0,0))

	digits.append(space)

	return digits

fonts = {
	"main": loadCFont("main.png", 20, (36, 16)),
	"pickups": loadCFont("pickup.png", 10, (10, 12)),
	"ticks": loadCFont("ticks.png", 4, (8, 17)),
}

alph = "abcdefghijklmnopqrstuvwxyz0123456789 "
def write(text, font, alph=alph, dark=.8):
	# Create surface with special font

	width = font[0].get_width()
	height = font[0].get_height()

	writing = Surface((width*len(text), height)).convert_alpha()
	writing.fill((0,0,0,0))
	for i in range(len(text)):
		writing.blit(font[alph.index(text[i].lower())], (i*width, 0))
	return darken(writing, dark)

def resizing(textures, rate=SIZING):
	if isinstance(textures, Surface):
		w = textures.get_width() * rate
		h = textures.get_height() * rate
		return transform.scale(textures, (w, h))
	elif isinstance(textures, list):
		return [resizing(texture, rate) for texture in textures]
	elif isinstance(textures, dict):
		return {name : resizing(texture, rate) for name, texture in textures.items()}

# Load all needed textures
textures = {
    "arrow": loadTexture("pause/arrow.png"),
    "isaac": {
		"heads" : loadTextures("isaac.png", (0, 0), (32, 32), (1, 6))[0::2],
		"tearHeads" : loadTextures("isaac.png", (0, 0), (32, 32), (1, 6))[1::2],
		"feet" : loadTextures("isaac.png", (0, 32), (32, 32), (2, 8)),
		"specialFrames" : loadTextures("isaac.png", (0, 32 * 4), (64, 64), (3, 4)),
	},
    "controls": loadTexture("controls.png"),
    "tears": {
		"tearPop" : loadTextures("tear_pop.png", (0, 0), (64, 64), (3, 4)),
		"tear" : loadTextures("tears.png", (0, 0), (32, 32), (2, 8))[:13],
		"blood" : loadTextures("tears.png", (0, 64), (32, 32), (2, 8))[:13],
    },
    "hearts": [
		loadTextures("hearts.png", (0, 0), (16, 16), (1, 3))[::-1],
		loadTextures("hearts.png", (0, 16), (16, 16), (1, 2))[::-1],
		loadTextures("hearts.png", (32, 16), (16, 16), (1, 2))[::-1],
	],
    "loading": [loadTexture(f"loading/{i+1}.png") for i in range(56)],
    "map": {
        "background": loadTexture("minimap.png", cell_size=(56, 51)),
        "in": loadTexture("minimap.png", (56, 0), (8, 8)),
        "entered": loadTexture("minimap.png", (56, 8), (8, 8)),
        "seen": loadTexture("minimap.png", (56, 16), (8, 8)),
        "item": loadTexture("minimap.png", (56, 24), (8, 8)),
        "boss": loadTexture("minimap.png", (56, 32), (8, 8)),
    },
    "overlays": [loadTexture(f"overlays/{i}.png") for i in range(5)],
    "pauseCard": loadTexture("pause/pauseCard.png"),
    "seedCard": loadTexture("pause/seedcard.png"),
    "shading": loadTexture("shading.png"),
    
    "doors": {
		name : dict(zip(("doorFrame", "doorBack", "lDoor", "rDoor", "brokenDoor", "lockedDoor"), loadTextures(name+'.png', (0, 0), (64, 48), (3, 2))))
		for name in ("door", "treasure_door", "boss_door")
    },
    "fires": {
		"fireFrames" : [resizing(loadTextures("fire_top.png", (0, 0), (48, 48), (1, 6)), rate=0.8**(4-health)) for health in range(5)],
		"woodFrames" : [loadTextures('fire_bottom.png', (x, y), (32, 32), (2, 2)) for x, y in ((0, 0), (64, 0), (0, 64))],
    },
    "floors": {
		name : loadTexture(name + '.png', (0, 0), (221, 143))
		for name in ("basement", "catacombs", "caves", "depths", "necropolis", "shop", "utero", "womb")
    },
    "poops": [list(reversed(loadTextures("poops.png", (0, variant * 32), (32, 32), (1, 5)))) for variant in range(5)],
    "rocks": {
		"rock" : loadTextures("rocks.png", (0, 0), (32, 32), (1, 3)),
		"broken" : loadTexture("rocks.png", (32 * 3, 0), (32, 32)),
	},
    "trapdoor": loadTexture("trap_door.png"),

    # --- 아이템 및 픽업류 ---
    "bombs": {
        "bombs": [loadTexture("bombs.png", (0, 0), (32, 32))],
		"explosion" : loadTextures("explosion.png", (0, 0), (96, 96), (3, 4)),
		"smut" : loadTextures("smut.png", (0, 0), (96, 64), (3, 3))[:8],
    },
    "coins": {
		name : loadTextures(name + '.png', (0, 0), (64, 64), (1, 6)) for name in ("dime", "nickel", "penny")
    },
    "keys": loadTexture("keys.png", (0, 0), (16, 32)),
    "phd": loadTexture("phd.png"),
    "pickupHearts": [loadTextures("pickup_hearts.png", (0, 32 * variant), (32, 32), (1, 2)) for variant in range(3)],
    "pickups": dict(zip(("coin", "bomb", "key"), loadTextures("pickups.png", (0, 0), (16, 16), (2, 2)))),
    "pills": loadTexture("pills.png"),

    # --- 적 및 보스 ---
    "bosses": {
        "duke": loadTextures("bosses/duke.png", (0, 0), (80, 64), (2, 2)),
        #"gurdy": loadTexture("gurdy.png", dir="bosses"),
    },
    "enemies": {
		"fly" : loadTextures("enemies/fly.png", (0, 0), (32, 32), (1, 2)),
		"attackFly" : loadTextures("enemies/fly.png", (0, 32), (32, 32), (1, 2)),
		"pooter" : loadTextures("enemies/pooter.png", (0, 0), (32, 32), (1, 2)),
		"boil" : loadTextures("enemies/boil.png", (0, 0), (32, 32), (3, 4))[9::-1],
		"sack" : loadTextures("enemies/sack.png", (0, 0), (32, 32), (3, 4))[9::-1],
		"host" : loadTextures("enemies/host.png", (0, 0), (32, 64), (1, 3)),
		"maw" : loadTextures("enemies/maw.png", (0, 0), (32, 32), (1, 1)),
		"horf" : loadTextures("enemies/horf.png", (0, 0), (32, 32), (2, 2))[:3],
		"legs" : loadTextures("enemies/legs.png", (0, 0), (32, 32), (5, 4)),
		"gusherEffect" : loadTextures("enemies/legs.png", (128, 0), (32, 32), (4, 2)),
		"spider" : loadTextures("enemies/spider.png", (32, 0), (32, 16), (4, 1)),
		"bigSpider" : loadTextures("enemies/bigSpider.png", (32, 0), (32, 16), (4, 1)),
		"trite" : loadTextures("enemies/trite.png", (0, 0), (48, 48), (3, 4)),
    },
    
    # --- 기타 효과 ---
    "streak": loadTexture("streak.png"),
}

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