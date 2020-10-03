import pygame
import os
import time
import random
pygame.font.init()

WITDH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WITDH, HEIGHT))
pygame.display.set_caption("Space Shooter")

#Load the images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))

#Player Ship
Yellow_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

#Laser
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png" ))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png" ))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png" ))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png" ))

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")),(WITDH, HEIGHT))

class Ship():
	def __init__(self, x,y, health=100):
		self.x = x
		self.y = y
		self.health = health
		self.ship_img = None
		self.laser_img = None
		self.lasers = []
		self.cool_down_counter = 0

	def draw(self, window):
		window.blit(self.ship_img, (self.x, self.y))

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()

class Player(Ship):
	def __init__(self,x,y, health=100):
		super().__init__(x,y,health)
		self.ship_img = Yellow_SPACE_SHIP
		self.laser_img = YELLOW_LASER
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.max_health = health

class Enemy(Ship):
	COLOR_MAP = {
		"red" : (RED_SPACE_SHIP, RED_LASER),
		"blue": (BLUE_SPACE_SHIP, BLUE_LASER),
		"green": (GREEN_SPACE_SHIP, GREEN_LASER)
		}

	def __init__(self, x,y,color, health=100):
		super().__init__(x,y,health)
		self.ship_img, self.laser_img = self.COLOR_MAP[color]
		self.mask = pygame.mask.from_surface(self.ship_img)

	def	move(self, vel):
		self.y += vel
						
		
def main():
	run = True
	FPS = 60
	level = 0
	lives = 5
	main_font = pygame.font.SysFont("comicsans", 50)
	lost_font = pygame.font.SysFont("comicsans", 60)

	player_vel = 5
	player = Player(300,650)

	enemyes = []
	wave_lenght = 5
	enemy_vel = 1
	

	clock = pygame.time.Clock()

	lost = False
	lost_count += 1

	if lost:
		if lost_count > FPS * 3:
			run = False
		else:
			continue

	def redraw_window():
		WIN.blit(BG, (0,0))
		#draw text
		lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255)) 
		level_label = main_font.render(f"Level: {level}", 1, (255,255,255)) 

		WIN.blit(lives_label,(10,10))
		WIN.blit(level_label, (WITDH - level_label.get_width() - 10, 10 ))

		for enemy in enemyes:
			enemy.draw(WIN)

		player.draw(WIN)

		if lost == True:
			lost_label = lost_font.render("You Lose !!!",1,(255,255,255))
			WIN.blit(lost_label, (WITDH/2 - lost_label.get_width()/2, 350))


		pygame.display.update()

	while run:
		clock.tick(FPS)
		redraw_window()

		if lives <= 0 or player.health <= 0:
			lost = True


		if len(enemyes) == 0:
			level += 1
			wave_lenght += 5
			for i in range(wave_lenght):
				enemy = Enemy(random.randrange(50, WITDH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
				enemyes.append(enemy)
		

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False 

		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] and player.x - player_vel > 0: #left
			player.x -= player_vel
		if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WITDH: #right
			player.x += player_vel
		if keys[pygame.K_w] and player.y - player_vel > 0: #up
			player.y -= player_vel
		if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: #down
			player.y += player_vel

		for enemy in enemyes[:]:
			enemy.move(enemy_vel)
			if enemy.y + enemy.get_height() > HEIGHT:
				lives -= 1
				enemyes.remove(enemy)


main()