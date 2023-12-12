import pygame
import os
import random
import csv

pygame.init()


#Setting up the screen and variables 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.4
ROWS = 16
COLS = 150
MAX_LEVELS = 6
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 1

moving_left = False
moving_right = False

GOING_UP = False

img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/Tile/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)


BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
DARK_GREEN = (40,133,33)

#Draws the backgorund

def draw_bg():
	screen.fill(BG)


#Reseting the level 
def reset_level():

	exit_group.empty()

	#create empty tile list
	data = []
	for row in range(ROWS):
		r = [-1] * COLS
		data.append(r)

	return data

#This is the player class, AKA the character you are controlling
class Soldier(pygame.sprite.Sprite):

	def __init__(self, char_type, x, y, scale, speed, going_up):

		pygame.sprite.Sprite.__init__(self)
		self.char_type = char_type
		self.speed = speed
		
		self.direction = 1
		if going_up: 
			self.vel_y = -7
		else: self.vel_y = 0
		self.vel_x = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()


		#Player animation for moving, standing still, and jumping 
		animation_types = ['Idle', 'Run', 'Jump']
		for animation in animation_types:
			temp_list = []
			num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)

		self.image = self.animation_list[self.action][self.frame_index]
		#self.rect = self.image.get_rect()
		self.rect = self.image.get_rect(topleft=(x, y))
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()

#Update fundtion, in addtion to doing the standard update things, this is where hit registration is detected and the player 
#is moved after they are shot
	def update(self):
		self.update_animation()
		
		for pewpew in enemy_bullet_group:
			
			if pygame.sprite.collide_rect(self, pewpew):
				


				self.vel_y = -9

				if pewpew.direction == 0:
					self.vel_x = 12
					
					#Getting shot from the left
					pewpew.kill()
				elif pewpew.direction == 1:
					self.vel_x = -8
					#Getting shot from the right
					pewpew.kill()
					
			
			
				




	def move(self, moving_left, moving_right):
		dx = 0
		dy = 0

		if moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		if self.jump == True and self.in_air == False:
			self.vel_y = -11
			self.jump = False
			self.in_air = True
		

		self.vel_y += GRAVITY
		if abs(self.vel_x) < 1: 
			self.vel_x = 0 
		if self.vel_x > 0: 
			dx = self.vel_x
			self.vel_x -= GRAVITY
		elif self.vel_x < 0: 
			dx = self.vel_x
			self.vel_x += GRAVITY

		if self.vel_y > 10:
			self.vel_y
			self.jump = False 
			self.in_air = True
		dy += self.vel_y
		

		level_complete = (False,)
		if pygame.sprite.spritecollide(self, exit_group, False):
			if self.rect.y > 560:
				level_complete = (1,self.rect.x)
			else: 
				level_complete = (2,self.rect.x)
				

		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				if self.vel_y < 0:
					self.vel_y = 0
					dy = tile[1].bottom - self.rect.top
				elif self.vel_y >= 0:
					self.vel_y = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom
			


		self.rect.x += dx
		self.rect.y += dy

		return level_complete



	def update_animation(self):
		ANIMATION_COOLDOWN = 100
		self.image = self.animation_list[self.action][self.frame_index]
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0



	def update_action(self, new_action):
		if new_action != self.action:
			self.action = new_action
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()



	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
	

	def shoot(self):
		if self.direction == -1:
			return(Bullet(self.rect.center[0], self.rect.center[1], 10, 0, 1, DARK_GREEN))
		else:
			return(Bullet(self.rect.center[0], self.rect.center[1], 10, 0, 0, DARK_GREEN))

		




class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y, speed, drop, direction, color):
        super().__init__()
        self.direction = direction
        self.speed = speed
        self.drop = drop
        self.width = 11
        self.height = 11
        self.image = pygame.Surface([11,11])
        self.image.fill((color))
        self.rect = self.image.get_rect(center =(pos_x, pos_y))
        

    
    def update(self):
        
        if self.direction == 0:
            self.rect.x += self.speed
        elif self.direction == 1:
            #self.speed *= -1
            self.rect.x -= self.speed
            
        self.rect.y -= self.drop #change this to have arc affect 
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                self.kill()

class Enemy(pygame.sprite.Sprite):

	def __init__(self, alive,x,y,facing,shoot_interval, on_level):
		super().__init__()
		self.alive = alive #will be true or false
		self.image = pygame.Surface([50,50])
		self.image.fill((255,255,255))
		self.rect = self.image.get_rect(center = (x,y))
		self.facing = facing
		self.shoot_interval = shoot_interval
		self.shoot_timer = 0
		self.last_shot = 0
		self.on_level = on_level
		self.start_pos_x = x
		self.start_pos_y = y

	def shoot(self):
		
		if self.facing == "left":

			return(enemy_bullet_group.add(Bullet(self.rect.center[0], self.rect.center[1], 10, 0, 1, BLACK)))
		else:

			return(enemy_bullet_group.add(Bullet(self.rect.center[0], self.rect.center[1], 10, 0, 0, BLACK)))
	
	def hide_me(self):
		self.rect.x = 1000
		self.rect.x = 1000
	
	def show_me(self):
		self.rect.x = self.start_pos_x
		self.rect.y = self.start_pos_y

	
	def update(self):
		if pygame.sprite.spritecollide(self, player_bullet_group, True):
			self.image.fill((255,10,10))
			self.alive = False
		if self.alive == True:
			current_time = pygame.time.get_ticks()
			self.shoot_timer += current_time - self.last_shot
			if self.shoot_timer >= self.shoot_interval:
				self.shoot()
				self.shoot_timer = 0
				self.last_shot = current_time
		if level == self.on_level:
			self.show_me()
		elif level != self.on_level:
			self.hide_me()

		
	
			



#'''



class World():
	def __init__(self):
		self.obstacle_list = []

	def process_data(self, data):
		#parse each value in level data file
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile]
					img_rect = img.get_rect()
					img_rect.x = x * TILE_SIZE
					img_rect.y = y * TILE_SIZE
					tile_data = (img, img_rect)
					if tile >= 0 and tile <= 8:
						self.obstacle_list.append(tile_data)
					elif tile == 15:#create player
						player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 4, GOING_UP)
					elif tile == 20:#create exit
						exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
						exit_group.add(exit)

		return player


	def draw(self):
		for tile in self.obstacle_list:
			screen.blit(tile[0], tile[1])
	





class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))




exit_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
#enemy_group.add(Enemy(Alive, X, Y ,Facing,  Fire rate higher is slower, level))
enemy_group.add(Enemy(True, 700, 550 ,"left", 100000, 1))
enemy_group.add(Enemy(True, 40, 240 ,"right", 10000, 1))

enemy_group.add(Enemy(True, 700, 550 ,"left", 1000, 2))

enemy_group.add(Enemy(True, 700, 450 ,"left", 1000, 3))

enemy_group.add(Enemy(True, 700, 450 ,"left", 1000, 4))

enemy_group.add(Enemy(True, 50, 250 ,"right", 100000, 5))
enemy_group.add(Enemy(True, 50, 200 ,"right", 10000, 5))
enemy_group.add(Enemy(True, 50, 250 ,"right", 10000, 5))
enemy_group.add(Enemy(True, 50, 300 ,"right", 100000, 5))
enemy_group.add(Enemy(True, 50, 350 ,"right", 10000, 5))
enemy_group.add(Enemy(True, 50, 400 ,"right", 100000, 5))
enemy_group.add(Enemy(True, 50, 450 ,"right", 10000, 5))





#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
player = world.process_data(world_data)



#game run loop
run = True
while run:

	clock.tick(FPS)

	#update background
	draw_bg()
	#draw world map
	world.draw()

	player.update()
	player.draw()

	#update and draw groups
	exit_group.update()
	exit_group.draw(screen)
	player_bullet_group.update()
	player_bullet_group.draw(screen)
	enemy_bullet_group.update()
	enemy_bullet_group.draw(screen)
	enemy_group.update()
	enemy_group.draw(screen)
	
	

	if player.in_air:
		player.update_action(2)
	elif moving_left or moving_right:
		player.update_action(1)
	else:
		player.update_action(0)
	player.move(moving_left, moving_right)
	

	level_complete = player.move(moving_left, moving_right)
	
	#MOVING UP 
	if level_complete[0] == 2:
				level += 1
				world_data = reset_level()
				if level <= MAX_LEVELS:
					#load in level data and create world
					GOING_UP = True
					with open(f'level{level}_data.csv', newline='') as csvfile:
						reader = csv.reader(csvfile, delimiter=',')
						for x, row in enumerate(reader):
							for y, tile in enumerate(row):
								world_data[x][y] = int(tile)
					world = World()
					player = world.process_data(world_data)	
					player.rect.x = level_complete[1]
					player.rect.y = 500

	#FALLING
	elif level_complete[0] == 1: 
				level -= 1
				world_data = reset_level()
				if level >= 0:
					GOING_UP = False
					#load in level data and create world
					with open(f'level{level}_data.csv', newline='') as csvfile:
						reader = csv.reader(csvfile, delimiter=',')
						for x, row in enumerate(reader):
							for y, tile in enumerate(row):
								world_data[x][y] = int(tile)
					world = World()
					player = world.process_data(world_data)	
					player.rect.y = 75
					player.rect.x = level_complete[1]


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			#if event.key == pygame.K_t:
				#enemy_group.add(Enemy(True, random.randint(250,750),random.randint(450,550),"left",10000))
			if event.key == pygame.K_SPACE:
				player_bullet_group.add(player.shoot())
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_w:
				player.jump = True
			if event.key == pygame.K_ESCAPE:
				run = False
			if event.key == pygame.K_r:
				world_data = reset_level()
				with open(f'level{level}_data.csv', newline='') as csvfile:
					reader = csv.reader(csvfile, delimiter=',')
					for x, row in enumerate(reader):
						for y, tile in enumerate(row):
							world_data[x][y] = int(tile)
				world = World()
				player = world.process_data(world_data)	



		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_d:
				moving_right = False



	pygame.display.update()

pygame.quit()