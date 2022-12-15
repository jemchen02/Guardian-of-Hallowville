import pygame #make sure to pip install pygame
import pygame.freetype

import random

pygame.mixer.init() #background music
pygame.mixer.music.load("Halloween_music.mp3")
pygame.mixer.music.play(loops= -1)

from pygame.locals import ( #necessary to detect keydowns
	RLEACCEL,
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	K_q,
	K_w,
	K_r,
	K_t,
	KEYDOWN,
	QUIT,
)

SCREEN_WIDTH = 800 #screen dimensions
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.surf = pygame.image.load("gunman.png").convert()
		self.surf.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.surf.get_rect(center=(140,SCREEN_HEIGHT/2))

	def update(self, pressed_keys):
		if pressed_keys[K_UP]: #handling key-downs for movement
			self.rect.move_ip(0, -5)
		if pressed_keys[K_DOWN]:
			self.rect.move_ip(0, 5)
		if pressed_keys[K_LEFT]:
			self.rect.move_ip(-5, 0)
		if pressed_keys[K_RIGHT]:
			self.rect.move_ip(5, 0)

		if self.rect.left < 140: #preventing player from leaving edge of screen
			self.rect.left = 140
		elif self.rect.right > SCREEN_WIDTH:
			self.rect.right = SCREEN_WIDTH
		if self.rect.top <= 0:
			self.rect.top = 0
		elif self.rect.bottom >= SCREEN_HEIGHT:
			self.rect.bottom = SCREEN_HEIGHT

class Wall(pygame.sprite.Sprite): #wall to be defended
	def __init__(self):
		super(Wall, self).__init__()
		self.surf = pygame.image.load("wall.png").convert()
		self.surf.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.surf.get_rect(center=(50,250))

class Barrier(pygame.sprite.Sprite): #protects wall from one enemy
	def __init__(self):
		super(Barrier, self).__init__()
		self.surf = pygame.image.load("barrier.png").convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.surf.get_rect(center=(159,300))

class Mine(pygame.sprite.Sprite): #stationary mine that kills one enemy upon contact
	def __init__(self, x, y):
		super(Mine, self).__init__()
		self.surf = pygame.image.load("mine.png").convert()
		self.surf.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.surf.get_rect(
			center=(x,y)
	)
class Enemy(pygame.sprite.Sprite): #regular ghost monsters that move horizontally
	def __init__(self, speed):
		super(Enemy, self).__init__()
		self.surf = pygame.image.load("ghost.png").convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)
		self.rect = self.surf.get_rect(
			center=(
				random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
				random.randint(20, SCREEN_HEIGHT - 20),
			)
		)
		self.speed = random.randint(speed, speed * 2)

	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()

class Enemy2(pygame.sprite.Sprite): #special bat monsters capable of moving diagonally
	def __init__(self, speed):
		super(Enemy2, self).__init__()
		self.surf = pygame.image.load("bat.png").convert()
		self.surf.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.surf.get_rect(
			center=(
				random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
				random.randint(20, SCREEN_HEIGHT - 20),
			)
		)
		self.speedx = random.randint(speed, speed * 2)
		self.speedy = random.randint(-speed, speed)

	def update(self):
		self.rect.move_ip(-self.speedx, self.speedy)
		if self.rect.right < 0:
			self.kill()
		elif self.rect.top <= 0: #bounces off top and bottom to move diagonally in other direction
			self.rect.top = 0
			self.speedy *= -1
		elif self.rect.bottom >= SCREEN_HEIGHT:
			self.rect.bottom = SCREEN_HEIGHT
			self.speedy *= -1

class Bullet(pygame.sprite.Sprite): #moving projectile fired by player that kills one enemy hit
	def __init__(self, x, y):
		super(Bullet, self).__init__()
		self.surf = pygame.image.load("bullet.png").convert()
		self.surf.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.surf.get_rect(
			center=(x,y)
		)
		self.spread = random.randint(-2,2)
	def update(self):
		self.rect.move_ip(15, self.spread)
		if self.rect.right > SCREEN_WIDTH:
			self.kill()
     
class Laser(pygame.sprite.Sprite): #moving projectile fired by turret that kills one enemy hit
	def __init__(self, x, y):
		super(Laser, self).__init__()
		self.surf = pygame.image.load("laser.png").convert()
		self.surf.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.surf.get_rect(
			center=(x,y)
		)
		self.spread = random.randint(-2,2)
	def update(self):
		self.rect.move_ip(15, self.spread)
		if self.rect.right > SCREEN_WIDTH:
			self.kill()

class Shield(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Shield, self).__init__()
		self.surf = pygame.image.load("shield.png").convert()
		self.surf.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.surf.get_rect(
			center = (x, y)
		)
		self.start_time = pygame.time.get_ticks()

	def update(self):
		
		self.rect.move_ip(player.rect.centerx-new_shield.rect.centerx, player.rect.centery-new_shield.rect.centery)
		
		if (pygame.time.get_ticks()-self.start_time)/1000> 5:
			self.kill()
                


class ShieldBoost(pygame.sprite.Sprite):
	def __init__(self):
		super(ShieldBoost, self).__init__()
		self.surf = pygame.image.load("shieldBoost.png").convert()
		self.surf.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.surf.get_rect(
			center = (
				random.randint(150, SCREEN_WIDTH),
				random.randint(20, SCREEN_HEIGHT - 20)
                        )
		)

class Boost(pygame.sprite.Sprite): #pickup item that temporarily allows player to fire two bullets at a time
	def __init__(self):
		super(Boost, self).__init__()
		self.surf = pygame.image.load("boost.png").convert()
		self.surf.set_colorkey((255,255,255), RLEACCEL)
		self.rect = self.surf.get_rect(
			center = (
				random.randint(150, SCREEN_WIDTH),
				random.randint(20, SCREEN_HEIGHT - 20)
			)
		)

class Turret(pygame.sprite.Sprite): #turret that can be activated to fire lasers at enemies
	def __init__(self):
		super(Turret, self).__init__()
		self.surf = pygame.image.load("turret.png").convert()
		self.surf.set_colorkey((255,255,255),RLEACCEL)
		self.rect = self.surf.get_rect(
			center = (100,300)
		)
	def activate(self, y):
		self.rect.centery = y


pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#spawning enemies and boosters periodically
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

ADDENEMY2 = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMY2, 2000)

ADDBOOST = pygame.USEREVENT + 3
pygame.time.set_timer(ADDBOOST, 10000)

ADDSHIELD = pygame.USEREVENT + 4
pygame.time.set_timer(ADDSHIELD, 20000)

player = Player()
new_wall = Wall()
new_turret = Turret()

players = pygame.sprite.Group()
players.add(player)
barriers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemies2 = pygame.sprite.Group()
mines = pygame.sprite.Group()
bullets = pygame.sprite.Group()
lasers = pygame.sprite.Group()
boosts = pygame.sprite.Group()
shields = pygame.sprite.Group()
shieldboosts = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(new_wall)
all_sprites.add(new_turret)

x = 0 #time counter for enemy speed increases
y = 1 #enemy speed
score = 0
cash = 0
ramp = 1500 #number for x to reach before enemy speed increase

mine_time = 0 #time counter, cooldown, and maximum number of mines
mine_cooldown = 40
mine_storage = 5

boosted = 0 #number of times player can fire two shots at once left
built = False #is the turret built?
cost = 250 #cost of turret upgrades

font = pygame.freetype.SysFont("arial", 0) #for in-game text

laser_time = 0 #turret fire counter
laser_cooldown = 32 #time required for turret to fire once

running = True
while running:
	if(mine_time < mine_cooldown * mine_storage): #mine counter only increases if not at capacity
		mine_time += 1
	x += 1
	score += 1
	cash += 1
	if(x >= ramp):
		y += 1
		x = 0

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE: #ends game on esc key down
				running = False
			elif event.key == K_q: #uses a mine on q key down if available
				if(mine_time >= mine_cooldown):
					mine_time -= mine_cooldown
					new_mine = Mine(player.rect.centerx, player.rect.centery)
					mines.add(new_mine)
					all_sprites.add(new_mine)
			elif event.key == K_w: #player fires a bullet on w key down
				new_bullet = Bullet(player.rect.centerx, player.rect.centery)
				bullets.add(new_bullet)
				all_sprites.add(new_bullet)
				if boosted > 0: #fires again if boost remains
					boosted -= 1
					new_bullet = Bullet(player.rect.centerx, player.rect.centery)
					bullets.add(new_bullet)
					all_sprites.add(new_bullet)
			elif event.key == K_t: #activates turret or upgrades on t key down if player has enough cash
				if built:
					if cash >= cost and laser_cooldown >= 1:
						laser_cooldown /= 2
						cash -= cost
						cost *= 2
				else:
					if(cash >= 250):
						cash -= 250
						built = True
						new_turret.activate(player.rect.centery)
			elif event.key == K_r: #activates a barrier on r key down if player has enough cash
				if cash >= 300:
					cash -= 300
					new_barrier = Barrier()
					barriers.add(new_barrier)
					all_sprites.add(new_barrier)

		elif event.type == QUIT: #if player hits x out of the game, ends game
			running = False

		elif event.type == ADDENEMY: #spawning enemies and boosts
			new_enemy = Enemy(y)
			enemies.add(new_enemy)
			all_sprites.add(new_enemy)
		elif event.type == ADDENEMY2:
			new_enemy2 = Enemy2(y)
			enemies2.add(new_enemy2)
			all_sprites.add(new_enemy2)
		elif event.type == ADDBOOST:
			new_boost = Boost()
			boosts.add(new_boost)
			all_sprites.add(new_boost)
		elif event.type == ADDSHIELD:
			new_shieldboost = ShieldBoost()
			shieldboosts.add(new_shieldboost)
			all_sprites.add(new_shieldboost)

	if built: #fires lasers if turret is activated and laser_time is at laser_cooldown
		laser_time += 1
		if laser_time >= laser_cooldown:
			laser_time -= laser_cooldown
			new_laser = Laser(new_turret.rect.centerx + 50, new_turret.rect.centery)
			lasers.add(new_laser)
			all_sprites.add(new_laser)

	pressed_keys = pygame.key.get_pressed()
	player.update(pressed_keys)

	enemies.update()
	enemies2.update()
	bullets.update()
	boosts.update()
	lasers.update()
	barriers.update()
	shieldboosts.update()
	shields.update()

	screen.fill((252,76,2))

	header_rect = font.get_rect("GUARDIAN OF HALLOWVILLE", size = 40)
	header_rect.center = (450,40)
	font.render_to(screen, header_rect, "GUARDIAN OF HALLOWVILLE", (0,255,255), size = 40)

	controls_rect = font.get_rect("Controls: mine-q, shoot-w, move-arrow keys", size = 20)
	controls_rect.center = (350, 510)
	font.render_to(screen, controls_rect, "Controls: mine-q, shoot-w, move-arrow keys", (255,255,0), size = 20)

	cash_rect = font.get_rect("$" + str(cash), size = 20)
	cash_rect.center = (320, 550)
	font.render_to(screen, cash_rect, "$" + str(cash), (255,255,0), size = 20)

	shopmsg = "(t) Activate turret: $250"
	if(built):
		shopmsg = "(t) Upgrade turret: $" + str(cost)

	shop_rect = font.get_rect(shopmsg, size = 20)
	shop_rect.center = (440, 550)
	font.render_to(screen, shop_rect, shopmsg, (255,255,0), size = 20)

	shield_rect = font.get_rect("(r) Buy Wall Barrier: $300", size = 20)
	shield_rect.center = (630, 550)
	font.render_to(screen, shield_rect, "(r) Buy Wall Barrier: $300", (255,255,0), size = 20)

	score_rect = font.get_rect("Score: " + str(score), size = 25)
	score_rect.center = (250, 75)
	font.render_to(screen, score_rect, "Score: " + str(score), (0,0,255), size = 25)

	mine_rect = font.get_rect("Mines: " + str(mine_time // mine_cooldown), size = 20)
	mine_rect.center = (250,550)
	font.render_to(screen, mine_rect, "Mines: " + str(mine_time // mine_cooldown), (255,255,0), size = 20)

	for entity in all_sprites:
		screen.blit(entity.surf, entity.rect)

	if pygame.sprite.spritecollideany(player, shieldboosts):
		new_shield = Shield(player.rect.centerx,player.rect.centery)
		shields.add(new_shield)
		all_sprites.add(new_shield)
	pygame.sprite.groupcollide(players, shieldboosts, False, True)
	pygame.sprite.groupcollide(enemies, shields, True, False)
	pygame.sprite.groupcollide(enemies2, shields, True, False)

	if pygame.sprite.spritecollideany(new_wall, enemies) or pygame.sprite.spritecollideany(new_wall, enemies2):
		running = False

	pygame.sprite.groupcollide(enemies, mines, True, True)
	pygame.sprite.groupcollide(enemies, bullets, True, True)
	pygame.sprite.groupcollide(enemies, lasers, True, True)
	pygame.sprite.groupcollide(enemies, barriers, True, True)
	pygame.sprite.groupcollide(enemies2, mines, True, True)
	pygame.sprite.groupcollide(enemies2, bullets, True, True)
	pygame.sprite.groupcollide(enemies2, lasers, True, True)
	pygame.sprite.groupcollide(enemies2, barriers, True, True)

	if pygame.sprite.spritecollideany(player, boosts):
		boosted = 25
	pygame.sprite.groupcollide(players, boosts, False, True)
	if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, enemies2):
		# If so, remove the player
		player.kill()
		running = False

	pygame.display.flip()
	clock.tick(30)
pygame.quit()