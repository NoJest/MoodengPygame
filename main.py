import pygame
from pygame.locals import *
import sys
import random


pygame.init()  # Begin pygame
 
# Declaring variables to be used through the program
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT)) #creates display
pygame.display.set_caption("Moodengs Wicked Adventure") #changes default pygame name

#healthbar animations
health_ani = [pygame.image.load("assets/health/heart0.png"), pygame.image.load("assets/health/heart.png"),
              pygame.image.load("assets/health/heart2.png"), pygame.image.load("assets/health/heart3.png"),
              pygame.image.load("assets/health/heart4.png"), pygame.image.load("assets/health/heart5.png")]

# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("assets/moodeng_R_1.xcf"), pygame.image.load("assets/moodengattackR.xcf"),
                pygame.image.load("assets/moodeng_R_2.xcf"),pygame.image.load("assets/moodengattackR.xcf"),
                pygame.image.load("assets/moodeng_R_3.xcf"),pygame.image.load("assets/moodengattackR.xcf"),
                pygame.image.load("assets/moodeng_R_4.xcf"),pygame.image.load("assets/moodengattackR.xcf"),
                pygame.image.load("assets/moodeng_R_5.xcf"),pygame.image.load("assets/moodengattackR.xcf"),
                pygame.image.load("assets/moodeng_R_6.xcf"),pygame.image.load("assets/moodengattackR.xcf"),
                pygame.image.load("assets/moodeng_R_1.xcf")]
 
# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("assets/moodeng_L_1.xcf"), pygame.image.load("assets/moodengattackL.xcf"),
                pygame.image.load("assets/moodeng_L_2.xcf"),pygame.image.load("assets/moodengattackL.xcf"),
                pygame.image.load("assets/moodeng_L_3.xcf"),pygame.image.load("assets/moodengattackL.xcf"),
                pygame.image.load("assets/moodeng_L_4.xcf"),pygame.image.load("assets/moodengattackL.xcf"),
                pygame.image.load("assets/moodeng_L_5.xcf"),pygame.image.load("assets/moodengattackL.xcf"),
                pygame.image.load("assets/moodeng_L_6.xcf"),pygame.image.load("assets/moodengattackL.xcf"),
                pygame.image.load("assets/moodeng_L_1.xcf")]

# Run animation for the RIGHT
run_ani_R = [pygame.image.load("assets/moodeng_R_1.xcf"), pygame.image.load("assets/moodeng_R_2.xcf"),
             pygame.image.load("assets/moodeng_R_3.xcf"),pygame.image.load("assets/moodeng_R_4.xcf"),
             pygame.image.load("assets/moodeng_R_5.xcf"),pygame.image.load("assets/moodeng_R_6.xcf"),
             pygame.image.load("assets/moodeng_R_1.xcf")]
 
# Run animation for the LEFT
run_ani_L = [pygame.image.load("assets/moodeng_L_1.xcf"), pygame.image.load("assets/moodeng_L_2.xcf"),
             pygame.image.load("assets/moodeng_L_3.xcf"),pygame.image.load("assets/moodeng_L_4.xcf"),
             pygame.image.load("assets/moodeng_L_5.xcf"),pygame.image.load("assets/moodeng_L_6.xcf"),
             pygame.image.load("assets/moodeng_L_1.xcf")]

class Background(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()      
            self.bgimage = pygame.image.load("assets/Background.xcf")        
            self.bgY = 0
            self.bgX = 0
 
      def render(self):
            displaysurface.blit(self.bgimage, (self.bgX, self.bgY))
 
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Ground.xcf")
        self.rect = self.image.get_rect(center = (350, 350))
 
    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))  
           
class HealthBar(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.image = pygame.image.load("assets/health/heart5.png")
 
      def render(self):
            displaysurface.blit(self.image, (10,10))
            
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Moodeng_R_1.xcf")
        self.rect = self.image.get_rect()
        
        #moving
        self.jumping = False
        self.running = False
        self.move_frame = 0
 
        # attacking
        self.attacking = False
        self.attack_frame = 0
        
        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "RIGHT"
        
        # combat
        self.attacking = False
        self.cooldown = False
        self.attack_frame = 0
        
        #healthbar
        self.health = 5
        
    def attack(self):        
      # If attack frame has reached end of sequence, return to base frame      
      if self.attack_frame > 12:
            self.attack_frame = 0
            self.attacking = False
 
      # Check direction for correct animation to display  
      if self.direction == "RIGHT":
             self.image = attack_ani_R[self.attack_frame]
      elif self.direction == "LEFT":
             self.image = attack_ani_L[self.attack_frame] 
      # Update the current attack frame  
      self.attack_frame += 1 
            
    def move(self):
      # Keep a constant acceleration of 0.5 in the downwards direction (gravity)
      self.acc = vec(0,0.5)
 
      # Will set running to False if the player has slowed down to a certain extent
      if abs(self.vel.x) > 0.3:
            self.running = True
      else:
            self.running = False
 
      # Returns the current key presses
      pressed_keys = pygame.key.get_pressed()
 
      # Accelerates the player in the direction of the key press
      if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
      if pressed_keys[K_RIGHT]:
            self.acc.x = ACC 
 
      # Formulas to calculate velocity while accounting for friction
      self.acc.x += self.vel.x * FRIC
      self.vel += self.acc
      self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values
 
      # This causes character warping from one point of the screen to the other
      if self.pos.x > WIDTH:
            self.pos.x = 0
      if self.pos.x < 0:
            self.pos.x = WIDTH
     
      self.rect.midbottom = self.pos  # Update rect with new pos 
      
    
    def update(self):
          # Return to base frame if at end of movement sequence 
        if self.move_frame > 6:
                self.move_frame = 0
                
 
          # Move the character to the next frame if conditions are met 
        if self.jumping == False and self.running == True:  
                if self.vel.x > 0:
                      self.image = run_ani_R[self.move_frame]
                      self.direction = "RIGHT"
                else:
                      self.image = run_ani_L[self.move_frame]
                      self.direction = "LEFT"
                self.move_frame += 1
 
          # Returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
                self.move_frame = 0
                if self.direction == "RIGHT":
                      self.image = run_ani_R[self.move_frame]
                elif self.direction == "LEFT":
                      self.image = run_ani_L[self.move_frame]
      
    def gravity_check(self):
      hits = pygame.sprite.spritecollide(moodeng ,ground_group, False)
      if self.vel.y > 0:
          if hits:
              lowest = hits[0]
              if self.pos.y < lowest.rect.bottom:
                  self.pos.y = lowest.rect.top + 1
                  self.vel.y = 0
                  self.jumping = False
                  
    def moodeng_hit(self):
        if not self.cooldown:      
            self.cooldown = True # Enable the cooldown
            pygame.time.set_timer(hit_cooldown, 1000) # Resets cooldown in 1 second
        
            self.health -= 1
            health.image = health_ani[self.health]
         
            if self.health <= 0:
                  self.kill()
                  pygame.display.update() 
            
    def jump(self):
        self.rect.x += 1
 
    # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)
     
        self.rect.x -= 1
 
    # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/PurrInBoots.xcf")
        self.rect = self.image.get_rect()     
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        
        #randomize enemies
        self.direction = random.randint(0,1) # 0 for Right, 1 for Left
        self.vel.x = random.randint(2,6) / 2  # Randomized velocity of the generated enemy
        # Sets the intial position of the enemy (direction of movement determines spawn point)
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235  
                 
      def move(self):
  # Causes the enemy to change directions upon reaching the end of screen    
        if self.pos.x >= (WIDTH-20):
          self.direction = 1
        elif self.pos.x <= 0:
          self.direction = 0  
          #updates position \/
        if self.direction == 0:
          self.pos.x += self.vel.x
        if self.direction == 1:
          self.pos.x -= self.vel.x
 
        self.rect.center = self.pos # Updates rect
        
      def render(self):
            # Displayed the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))

      def update(self):
      # Checks for collision with the Player
            if moodeng.attacking:
                  if pygame.sprite.spritecollide(self, Moodenggroup, False):
                        print ("hit by attack")
                        self.kill()
                        print(f"Enemies group size:0")  # Should decrease when an enemy is killed
 
      # If collision has occured and player not attacking, call "hit" function            
            if pygame.sprite.collide_rect(self, moodeng):
                  moodeng.moodeng_hit()    
                  

                                 
#declaring images and sprite groups

background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
moodeng = Player()
Moodenggroup = pygame.sprite.Group()
Moodenggroup.add(moodeng)
health = HealthBar()
enemy = Enemy()


hit_cooldown = pygame.USEREVENT + 1
#game looop
while True:
    moodeng.gravity_check()   
    
    for event in pygame.event.get():
        # Will run when the close window button is clicked    
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
            
    
        # For events that occur upon clicking the mouse (left click) 
        if event.type == pygame.MOUSEBUTTONDOWN:
              pass
 
        # Event handling for a range of different key presses    
        if event.type == pygame.KEYDOWN:
          
            if event.key == pygame.K_SPACE:
                moodeng.jump()
            if event.key == pygame.K_RETURN:
                if moodeng.attacking == False:
                    moodeng.attacking = True 
                    moodeng.attack()
          #make moodeng invincible briefly after being attacked           
        if event.type == hit_cooldown:
             moodeng.cooldown = False
             pygame.time.set_timer(hit_cooldown, 0)   
                     
    moodeng.update()
    if moodeng.attacking == True:
        moodeng.attack()
    moodeng.move()    
    # Render Functions ------
    background.render() 
    ground.render()
    
    enemy.update()
    enemy.move()
    enemy.render()    
    #must render player and enemies after background and ground
#     
    if moodeng.health > 0:
      displaysurface.blit(moodeng.image, moodeng.rect)
    health.render()
    

    pygame.display.update() 
    FPS_CLOCK.tick(FPS)