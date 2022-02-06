from re import T
from turtle import window_height
import pygame, sys, os
from pygame.locals import *
pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BACKGROUND = (255, 90, 255)

#תמונות
bg1 = pygame.image.load('C:/Users/salav/Downloads/סתם דברים/אנימציות/Free Pixel Art Forest/PNG/Background layers/sui.png').convert_alpha()
bg2 = pygame.image.load('C:/Users/salav/Downloads/סתם דברים/אנימציות/Free Pixel Art Forest/PNG/Background layers/Layer_0001_8.png').convert_alpha()
bg3 = pygame.image.load('C:/Users/salav/Downloads/סתם דברים/אנימציות/Free Pixel Art Forest/PNG/Background layers/Layer_0000_9.png').convert_alpha()
bg4 = pygame.image.load('C:/Users/salav/Downloads/סתם דברים/אנימציות/Free Pixel Art Forest/PNG/Background layers/Layer_0002_7.png').convert_alpha()



CLOCK = pygame.time.Clock()
FPS = 60
GRAVITY = 0.75


moving_left = False
moving_right = False
attack = False
attack_frame = 0

class Player():
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.alive = True
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        
        self.update_time = pygame.time.get_ticks()

        #רשימה של אנימציה 
        animation_type = ['Idle', 'jump', 'run', 'attack1']
        for animation in animation_type:
            temp_list = []
            number_of_frame = len(os.listdir(f'C:/Users/salav/Downloads/סתם דברים/{self.char_type}/{animation}'))
            for i in range(number_of_frame):
                img = pygame.image.load(f'C:/Users/salav/Downloads/סתם דברים/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)   
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        #מעדכן קולדאון
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def move(self, moving_left, moving_right):
        #ריסט הליכה 
        dx = 0 
        dy = 0

        #מגדיר תזוזת שחקן
        if moving_left == True:
            dx -= self.speed
            self.flip = True
            self.direction = -1
        if moving_right == True:
            self.flip = False
            self.direction = 1
            dx += self.speed
        #קפיצה
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True
        
        #כוח משיכה
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #ריצפה
        if self.rect.bottom + dy > 580:
            dy = 580 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy





    


        
    #אנימציה לשחקן
    def update_animation(self):
        ANIMATION_COOLDOWN = 200
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
    
    #אנימציה פעולות
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #בודק עם השחקנים חיים
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    #ציור התמונה 
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)




player = Player('Test Game',300, 200, 3, 5, 20, 100)


run = True 
while run:
    CLOCK.tick(FPS)


    screen.blit(bg1,(0,0))
      
    player.update()   
    player.draw()

    screen.blit(bg2,(0,0))
    screen.blit(bg3,(0,0))
    screen.blit(bg4,(0,0))

    if player.alive:       
        if player.in_air:
            player.update_action(1)#jump
        elif attack:
            attack_frame += 0.18
            player.update_action(3)#attack
        elif moving_left or moving_right:
            player.update_action(2)#run 
        else:
            player.update_action(0)#idle player
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

        #מקלדת שאתה לוחץ
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_f:         
                attack = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True                
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        
        if attack_frame > 9:
            attack_frame = 0
            attack = False
        

        #שאתה משחרר את לחצנים של המקלדת
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False   
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

    pygame.display.update()
   
   