import pygame, sys
from copy import deepcopy
from math import *

class Player(pygame.sprite.Sprite):
	def __init__(self,pos, choice, group):
		super().__init__(group)
		self.direction = pygame.math.Vector2()
		self.speed = 4
		self.image = pygame.Surface((50,100))
		self.rect = self.image.get_rect(topleft = pos)
		if choice == 1:
			self.move_keys = {'up': pygame.K_z, 'down': pygame.K_s, 'left': pygame.K_q, 'right': pygame.K_d, 'sprint': pygame.K_LSHIFT}
		else:
			self.move_keys = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'sprint': pygame.K_RCTRL}
	def input(self):
		keys = pygame.key.get_pressed()

		if keys[self.move_keys['up']]:
			self.direction.y = -1
		elif keys[self.move_keys['down']]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[self.move_keys['right']]:
			self.direction.x = 1
		elif keys[self.move_keys['left']]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

		# camera offset 
		self.offset = pygame.math.Vector2()
		self.offset2 = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		# ground
		self.ground_surf =  pygame.image.load('DWARF/test_background.png').convert_alpha()
		self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

		# zoom
		self.zoom_scale = 1
		self.internal_surf_size = (1280,617)
		self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
		self.internal_rect = self.internal_surf.get_rect(topleft = (self.half_w,self.half_h))
		self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)

		# box setup
		l = 0
		t = 0
		w = self.ground_surf.get_width()
		h = self.ground_surf.get_height()
		self.camera_rect = pygame.Rect(l,t,w,h)
		
	def center_target_camera(self,target1, target2):
		self.offset.x = (target1.rect.centerx + target2.rect.centerx)/2 - self.half_w
		self.offset.y = (target1.rect.centery + target2.rect.centery)/2 - self.half_h

	def box_camera(self, target1, target2):
		self.offset2.x = self.camera_rect.left
		self.offset2.y = self.camera_rect.top
		

	def realign(self):
		camera_rect = pygame.Rect((self.offset.x, self.offset.y), (1280, 617))
		if camera_rect.left < self.ground_rect.left:
			print("aaaaaaaaaaaaaaaaaaaaa")
			self.offset.x = 0
		if camera_rect.right > self.ground_rect.right:
			print("bbbbbbbbbbbbbbbbbbbb")
		if camera_rect.top < self.ground_rect.top:
			print("cccccccccccccccccccc")
		if camera_rect.bottom > self.ground_rect.bottom:
			print("dddddddddddddddddddd")

	def zoom(self):
		if 900 > difference_length > 800 or 600 > difference_length > 500 or 400 > difference_length > 300:
			self.zoom_scale += sqrt((w2 - w1)**2 + (h2 - h1)**2) / sqrt((x2 - x1)**2 + (y2 - y1)**2)*0.006
	
	def dezoom(self):
		if 900 > difference_length > 800 or 600 > difference_length > 500 or 400 > difference_length > 300:
			self.zoom_scale -= sqrt((w2 - w1)**2 + (h2 - h1)**2) / sqrt((x2 - x1)**2 + (y2 - y1)**2)*0.007
		if self.zoom_scale < 1:
			self.zoom_scale = 1

	def choose_zoom(self):
		if difference_length < difference_length_save:
			self.zoom()
		elif difference_length > difference_length_save:
			self.dezoom()

	def custom_draw(self,player1, player2):
		self.internal_surf.fill('#71ddee')
		self.center_target_camera(player1, player2)
		self.realign()
		# ground 
		ground_offset = self.ground_rect.topleft - self.offset
		self.internal_surf.blit(self.ground_surf,ground_offset)

		# active elements
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.internal_surf.blit(sprite.image,offset_pos)

		self.choose_zoom()
		scaled_surf = pygame.transform.scale(self.internal_surf,self.internal_surface_size_vector * self.zoom_scale)
		scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))
		self.display_surface.blit(scaled_surf,scaled_rect)

		'''rect = pygame.Rect((self.offset.x, self.offset.y), (1230, 617))
		surf = pygame.Surface((rect.width,rect.height))
		surf.set_alpha(128)
		surf.fill('red')
		self.display_surface.blit(surf,rect)'''
		
		


pygame.init()
screen = pygame.display.set_mode((1280,617))
clock = pygame.time.Clock()
pygame.event.set_grab(True)
# setup 
camera_group = CameraGroup()

player1 = Player((0,0),1,camera_group)
player2 = Player((1230,517),2,camera_group)
player_group = pygame.sprite.Group()
player_group.add(player1,player2)

player1_pos_save, player2_pos_save = deepcopy([player1.rect.x, player1.rect.y]), deepcopy([player2.rect.x, player2.rect.y])
difference_save = [abs(player1.rect.x-player2.rect.x),abs(player1.rect.y-player2.rect.y)]
difference_length_save = sqrt(difference_save[0]*difference_save[0]+difference_save[1]*difference_save[1])

frame_x, frame_y = camera_group.ground_surf.get_width()/12, camera_group.ground_surf.get_height()/7
w1, w2 = player1.image.get_width()/2+frame_x, camera_group.ground_surf.get_width() - player2.image.get_width()/2 - frame_x
h1, h2 = player1.image.get_height()/2+frame_y, camera_group.ground_surf.get_height() - player2.image.get_height()/2 - frame_y
x1, x2 = player1.rect.centerx, player2.rect.centerx
y1, y2 = player1.rect.centery, player2.rect.centery

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_k:
				pygame.quit()
				sys.exit()

		if event.type == pygame.MOUSEWHEEL:
			camera_group.zoom_scale += event.y * 0.03
	difference = [abs(player1.rect.x-player2.rect.x),abs(player1.rect.y-player2.rect.y)]
	difference_length = sqrt(difference[0]*difference[0]+difference[1]*difference[1]) # pythagore
	new_length = abs(difference_length - difference_length_save)

	screen.fill('#71ddee')
	
	camera_group.update()
	camera_group.custom_draw(player1, player2)
	player1_pos_save, player2_pos_save = deepcopy([player1.rect.x,player1.rect.y]), deepcopy([player2.rect.x,player2.rect.y])
	difference_length_save = deepcopy(difference_length)
	pygame.display.update()
	clock.tick(60)
	