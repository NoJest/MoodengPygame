import pygame
from pygame.locals import *
import sys
import random
from music_manager import MusicManager
from button import Button 



pygame.mixer.pre_init(44100,16,1,512)
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


#music and sound
soundtrack = 'assets/Music/mixkit-island-beat-250.mp3'
hippobattletrack = 'assets/Music/Battlemusic.mp3'
fsound = [pygame.mixer.Sound("assets/Music/hungryhippo.mp3"),pygame.mixer.Sound("assets/Music/hungryhippo.mp3")]
wsound = pygame.mixer.Sound("assets/Music/fireball.mp3")
hit = pygame.mixer.Sound("assets/Music/deathsound.mp3")
moodengdeathknell= pygame.mixer.Sound("assets/Music/moodengdeath.mp3")
milksound = pygame.mixer.Sound("assets/Music/milksound.mp3")
 
mmanager = MusicManager()
mmanager.playsoundtrack(soundtrack, -1, 0.05)

#fonts
headingfont = pygame.font.SysFont("Verdana", 40)
regularfont = pygame.font.SysFont('Corbel',25)
smallerfont = pygame.font.SysFont('Corbel',16) 


# light shade of the button 
color_light = (170,170,170)
color_dark = (100,100,100)
color_white = (255,255,255) 
neon_green = (57, 255, 20) 


displaysurface = pygame.display.set_mode((WIDTH, HEIGHT)) #creates display
pygame.display.set_caption("Moodengs Wicked Adventure") #changes default pygame name

#healthbar animations
health_ani = [pygame.image.load("assets/health/heart0.png").convert_alpha(), pygame.image.load("assets/health/heart.png").convert_alpha(),
              pygame.image.load("assets/health/heart2.png").convert_alpha(), pygame.image.load("assets/health/heart3.png").convert_alpha(),
              pygame.image.load("assets/health/heart4.png").convert_alpha(), pygame.image.load("assets/health/heart5.png").convert_alpha()]

# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("assets/moodeng_R_1.xcf").convert_alpha(), pygame.image.load("assets/moodengattackR.xcf").convert_alpha(),
                pygame.image.load("assets/moodengattackR.xcf").convert_alpha(),pygame.image.load("assets/moodengattackR.xcf").convert_alpha(),
                pygame.image.load("assets/moodengattackR.xcf").convert_alpha(),pygame.image.load("assets/moodengattackR.xcf").convert_alpha(),
                pygame.image.load("assets/moodengattackR.xcf").convert_alpha(),pygame.image.load("assets/moodengattackR.xcf").convert_alpha(),
                pygame.image.load("assets/moodengattackR.xcf").convert_alpha(),pygame.image.load("assets/moodengattackR.xcf").convert_alpha(),
                pygame.image.load("assets/moodengattackR.xcf").convert_alpha(),pygame.image.load("assets/moodengattackR.xcf").convert_alpha(),
                pygame.image.load("assets/moodeng_R_1.xcf").convert_alpha()]
 
# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("assets/moodeng_L_1.xcf").convert_alpha(), pygame.image.load("assets/moodengattackL.xcf").convert_alpha(),
                pygame.image.load("assets/moodengattackL.xcf").convert_alpha(),pygame.image.load("assets/moodengattackL.xcf").convert_alpha(),
                pygame.image.load("assets/moodengattackL.xcf").convert_alpha(),pygame.image.load("assets/moodengattackL.xcf").convert_alpha(),
                pygame.image.load("assets/moodengattackL.xcf").convert_alpha(),pygame.image.load("assets/moodengattackL.xcf").convert_alpha(),
                pygame.image.load("assets/moodengattackL.xcf").convert_alpha(),pygame.image.load("assets/moodengattackL.xcf").convert_alpha(),
                pygame.image.load("assets/moodengattackL.xcf").convert_alpha(),pygame.image.load("assets/moodengattackL.xcf").convert_alpha(),
                pygame.image.load("assets/moodeng_L_1.xcf").convert_alpha()]

# Run animation for the RIGHT
run_ani_R = [pygame.image.load("assets/moodeng_R_1.xcf").convert_alpha(), pygame.image.load("assets/moodeng_R_2.xcf").convert_alpha(),
             pygame.image.load("assets/moodeng_R_3.xcf").convert_alpha(),pygame.image.load("assets/moodeng_R_4.xcf").convert_alpha(),
             pygame.image.load("assets/moodeng_R_5.xcf").convert_alpha(),pygame.image.load("assets/moodeng_R_6.xcf").convert_alpha(),
             pygame.image.load("assets/moodeng_R_1.xcf").convert_alpha()]
 
# Run animation for the LEFT
run_ani_L = [pygame.image.load("assets/moodeng_L_1.xcf").convert_alpha(), pygame.image.load("assets/moodeng_L_2.xcf").convert_alpha(),
             pygame.image.load("assets/moodeng_L_3.xcf").convert_alpha(),pygame.image.load("assets/moodeng_L_4.xcf").convert_alpha(),
             pygame.image.load("assets/moodeng_L_5.xcf").convert_alpha(),pygame.image.load("assets/moodeng_L_6.xcf").convert_alpha(),
             pygame.image.load("assets/moodeng_L_1.xcf").convert_alpha()]


class Cursor(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.image = pygame.image.load("assets/Moodeng.xcf")
            self.rect = self.image.get_rect()
            self.wait = 0
      def pause(self):
            if self.wait == 1:
             self.wait = 0
            else:
             self.wait = 1      
      def hover(self):
            if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
             pygame.mouse.set_visible(False)
             cursor.rect.center = pygame.mouse.get_pos()  # update position 
             displaysurface.blit(cursor.image, cursor.rect)
            else:
             pygame.mouse.set_visible(1)
     
      def update (self):
            if cursor.wait == 1:
                  return 

class PButton(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.vec = vec(620, 300)
            self.imgdisp = 0
            
      def render(self, num):
            if (num == 0):
                  self.image = pygame.image.load("assets/home_small.png")
            elif (num == 1):
                  if cursor.wait == 0:
                        self.image = pygame.image.load("assets/pause_small.png")
                  else:
                        self.image = pygame.image.load("assets/play_small.png")             
            displaysurface.blit(self.image, self.vec)      
            
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
        self.image = pygame.image.load("assets/ground2.xcf")
        self.rect = self.image.get_rect(center = (350, 350))
 
    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))  
        
class StatusBar(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.surf = pygame.Surface((90, 66))
            self.rect = self.surf.get_rect(center = (500, 10))
            
            
      def update_draw(self):
      # Create the text to be displayed
            text1 = smallerfont.render("STAGE: " + str(handler.stage) , 1 , color_white)
            text2 = smallerfont.render("EXP: " + str(moodeng.experience) , 1 , color_white)
            text3 = smallerfont.render("MANA: " + str(moodeng.mana) , 1 , color_white)
            text4 = smallerfont.render("FPS: " + str(int(FPS_CLOCK.get_fps())) , 1 , color_white)
      
      # Draw the text to the status bar
            displaysurface.blit(text1, (585, 7))
            displaysurface.blit(text2, (585, 22))
            displaysurface.blit(text3, (585, 37))
            displaysurface.blit(text4, (585, 52))
            
class StageDisplay(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.text = headingfont.render("STAGE: " + str(handler.stage) , 1 , neon_green)
            self.rect = self.text.get_rect()
            self.posx = -100
            self.posy = 100
            self.display = False
            self.clear = False
      def move_display(self):
      # Create the text to be displayed
            self.text = headingfont.render("STAGE: " + str(handler.stage) , 1 , neon_green)
            if self.posx < 720:
                  self.posx += 5
                  displaysurface.blit(self.text, (self.posx, self.posy))
            else:
                  self.display = False
                  self.posx = -100
                  self.posy = 100      
      def stage_clear(self):
            self.text = headingfont.render("Press N to proceed to Next Stage STAGE CLEAR! ", 1 , neon_green)
            button.imgdisp = 0 
            if self.posx < 720:
                  self.posx += 5
                  displaysurface.blit(self.text, (self.posx, self.posy))
            else:
                  self.clear = False
                  self.posx = -100
                  self.posy = 100
                  
      def moodeng_death_knell(self):
            self.text = headingfont.render("!!!YOU KILLED MOODENG!!!!", 1 , neon_green)
            button.imgdisp = 0 
            if self.posx < 720:
                  self.posx += 2
                  displaysurface.blit(self.text, (self.posx, self.posy))
            else:
                  self.clear = False
                  self.posx = -100
                  self.posy = 100
                  
class HealthBar(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.image = pygame.image.load("assets/health/heart5.png")
 
      def render(self):
            displaysurface.blit(self.image, (10,10))

class FireBall(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.direction  = moodeng.direction
            if self.direction == "RIGHT":
                  self.image = pygame.image.load("assets/lazerR.xcf")
            else:
                  self.image = pygame.image.load("assets/lazerL.xcf")           
            self.rect = self.image.get_rect(center = moodeng.pos)
            self.rect.x = moodeng.pos.x
            self.rect.y = moodeng.pos.y - 40      
      def fire(self):
            moodeng.magic_cooldown = 0
      # Runs while the fireball is still within the screen w/ extra margin
            if -10 < self.rect.x < 710:
                  if self.direction == "RIGHT":
                        self.image = pygame.image.load("assets/lazerR.xcf")
                        displaysurface.blit(self.image, self.rect)
                  else:
                        self.image = pygame.image.load("assets/lazerL.xcf")
                        displaysurface.blit(self.image, self.rect)
                   
                  if self.direction == "RIGHT":
                        self.rect.move_ip(12, 0)
                  else:
                        self.rect.move_ip(-12, 0)   
            else:
                  self.kill()
                  moodeng.magic_cooldown = 1
                  moodeng.attacking = False            
class Item(pygame.sprite.Sprite):
      def __init__(self, itemtype):
            super().__init__()
            if itemtype == 1: self.image = pygame.image.load("assets/heart.png")
            elif itemtype == 2: self.image = pygame.image.load("assets/milk.xcf")
            self.rect = self.image.get_rect()
            self.type = itemtype
            self.posx = 0
            self.posy = 0  
                     
      def render(self):
            self.rect.x = self.posx
            self.rect.y = self.posy
            displaysurface.blit(self.image, self.rect)
      def update(self):
            hits = pygame.sprite.spritecollide(self, Moodenggroup, False)
      # Code to be activated if item comes in contact with player
            if hits:
                  if moodeng.health < 5 and self.type == 1:
                        moodeng.health += 1
                        health.image = health_ani[moodeng.health]
                        self.kill()
                  if self.type == 2:
                  # handler.money += 1
                  #commented out until we create  money systep
                        self.kill()
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
        self.slash = 0 
        
        #healthbar /exp bar /mana bar
        self.health = 5
        self.experience = 0
        self.mana = 2
        self.magic_cooldown = 1
        
    def attack(self):   
          
      if cursor.wait == 1:
            return     
      # If attack frame has reached end of sequence, return to base frame      
      if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
      
      if self.attack_frame == 0:
            mmanager.playsound(fsound[self.slash], 0.05)
            
            self.slash += 1
            if self.slash >= 2:
                  self.slash = 0 

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
            self.running = 1
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
        if cursor.wait == 1:
              return
          # Return to base frame if at end of movement sequence 
        if self.move_frame > 6:
                self.move_frame = 0
                return
 
          # Move the character to the next frame if conditions are met 
        if self.jumping == False and self.running == 1:  
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
        if self.cooldown == False:      
            self.cooldown = 1 # Enable the cooldown
            pygame.time.set_timer(hit_cooldown, 1000) # Resets cooldown in 1 second
        
            self.health = self.health - 1
            health.image = health_ani[self.health]
         
            if self.health <= 0:
                  self.kill()
                  mmanager.stop()
                  mmanager.playsound(moodengdeathknell, .1)
                  pygame.display.update() 
            
    def jump(self):
        self.rect.x += 1
 
    # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)
     
        self.rect.x -= 1
 
    # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = 1
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
        self.mana = random.randint(1, 3)  # Randomised mana amount obtained upon kill
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235  
                 
      def move(self):
        if cursor.wait == 1 : 
              return
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
            hits = pygame.sprite.spritecollide(self, Moodenggroup, False)
            f_hits = pygame.sprite.spritecollide(self, Fireballs, False)
            
      # Activates upon either of the two expressions being 1
            if hits and moodeng.attacking == 1 or f_hits:
                  self.kill()
                  mmanager.playsound(hit, 0.05)
                  if moodeng.mana < 100: moodeng.mana += self.mana # Release mana
                  moodeng.experience += 1   # Release expeiriance
                  # if moodeng.health < 5: moodeng.health += 1
                  handler.dead_enemy_count += 1 
            #print("Enemy killed")
                  rand_num = random.randint(0, 100)
                  item_no = 0
                  if rand_num >= 0 and rand_num <= 20:  # 1 / 20 chance for an item (health) drop
                        item_no = 1
                  elif rand_num > 20 and rand_num <= 50:
                        item_no = 2
                  if item_no != 0:
      # Add Item to Items group
                        item = Item(item_no)
                        Items.add(item)
      # Sets the item location to the location of the killed enemy
                        item.posx = self.pos.x
                        item.posy = self.pos.y
      # If collision has occured and player not attacking, call "hit" function            
            elif hits and moodeng.attacking == False:
                  moodeng.moodeng_hit()    
                  
class Arena(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.hide = False
            self.image = pygame.image.load("assets/blackhole2.xcf")
            self.rect = self.image.get_rect()
 
      def update(self):
            if not self.hide:
                  displaysurface.blit(self.image, (500, 200)) 
           
               
                  
class EventHandler():
      def __init__(self):
            self.enemy_count = 0
            self.dead_enemy_count = 0 
            self.battle = False
            self.enemy_generation = pygame.USEREVENT + 2
            self.stage = 1
            
           
            
            self.stage_enemies = []
            for x in range(1,21):
                  self.stage_enemies.append(int((x**2/2)+1)) 
      # def stage_handler(self):
      #       # Code for the Tkinter stage selection window
      #       self.root = Tk()
      #       self.root.geometry('200x170')
             
      #       button1 = Button(self.root, text = "Baby Weight Wrestling Arena", width = 18, height = 2,
      #                       command = self.world1)
      #       button2 = Button(self.root, text = "Bubble Weight Wrestling Arena", width = 18, height = 2,
      #                       command = self.world2)
      #       button3 = Button(self.root, text = "World Championship Arena for Big Girl Hippos", width = 18, height = 2,
      #                       command = self.world3)
              
      #       button1.place(x = 40, y = 15)
      #       button2.place(x = 40, y = 65)
      #       button3.place(x = 40, y = 115)
             
      #       self.root.mainloop()  
      def home(self):
      # Reset Battle code
            pygame.time.set_timer(self.enemy_generation, 0)
            self.battle = False
            self.enemy_count = 0
            self.dead_enemy_count = 0
            self.stage = 1
 
      # Destroy any enemies or items lying around
            for group in Enemies, Items:
                  for entity in group:
                        entity.kill()
       
      # Bring back normal backgrounds
            arena.hide = False
            background.bgimage = pygame.image.load("assets/Background.xcf")
            ground.image = pygame.image.load("assets/ground2.xcf")
            
      def update(self):
            if self.dead_enemy_count == self.stage_enemies[self.stage - 1]:
                  self.dead_enemy_count = 0
                  stage_display.clear = 1
                  stage_display.stage_clear()
                  
            
      def world1(self):
            pygame.time.set_timer(self.enemy_generation, 2000)
            button.imgdisp = 1 
            arena.hide = True
            self.battle = 1
 
      def world2(self):
            self.root.destroy()
            self.battle = 1
            button.imgdisp = 1 
      # Empty for now
      
      def world3(self):
            self.battle = 1
            button.imgdisp = 1 
      # Empty for now   
      def next_stage(self):  # Code for when the next stage starts           
            button.imgdisp = 1 
            self.stage += 1
            print("Stage: "  + str(self.stage))
            self.enemy_count = 0
            self.dead_enemy_count = 0 
            pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))
            mmanager.playsoundtrack(hippobattletrack, -1, 0.05)
                                 
#declaring images and sprite groups
Enemies = pygame.sprite.Group()
background = Background()
ground = Ground()
cursor = Cursor()
button = PButton()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
arena = Arena()
handler = EventHandler()
Fireballs = pygame.sprite.Group()
moodeng = Player()
Moodenggroup = pygame.sprite.Group()
Moodenggroup.add(moodeng)
health = HealthBar()
status_bar= StatusBar()
hit_cooldown = pygame.USEREVENT + 1
stage_display = StageDisplay()
Items = pygame.sprite.Group()
GAME_RUNNING = 1
Death_knell_time = None
DEATH_KNELL_DELAY = 20000


#game looop
while GAME_RUNNING:
    moodeng.gravity_check()   
    mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        # Will run when the close window button is clicked    
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
            
        if event.type == handler.enemy_generation:
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                  enemy = Enemy()
                  Enemies.add(enemy)
                  handler.enemy_count += 1  
             
        # For events that occur upon clicking the mouse (left click) 
        if event.type == pygame.MOUSEBUTTONDOWN:
           
            if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
                  if button.imgdisp == 1:
                        cursor.pause()
                  elif button.imgdisp == 0:
                        handler.home()
 
        # Event handling for a range of different key presses    
        if event.type == pygame.KEYDOWN and cursor.wait == 0:
            if event.key == pygame.K_n:
                  if handler.battle == 1 and len(Enemies) == 0:
                        handler.next_stage() 
                        stage_display = StageDisplay()
                        stage_display.display = 1
                        
            if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_m and moodeng.magic_cooldown == 1:
                        if moodeng.mana >= 2:
                              moodeng.mana -= 2
                              moodeng.attacking = 1
                              fireball = FireBall()
                              Fireballs.add(fireball)
                              mmanager.playsound(wsound, .3 )
            if event.key == pygame.K_e and 400 < moodeng.rect.x < 550:
                  handler.world1()
                  
            if event.key == pygame.K_SPACE:
                moodeng.jump()
            if event.key == pygame.K_RETURN:
                if moodeng.attacking == False:
                    moodeng.attack()
                    moodeng.attacking = 1 
          #make moodeng invincible briefly after being attacked           
        if event.type == hit_cooldown:
             moodeng.cooldown = False
             pygame.time.set_timer(hit_cooldown, 0)   
    
                     
    moodeng.update()
    if moodeng.attacking == 1:
        moodeng.attack()
    moodeng.move()    
    # Render Functions ------
    background.render() 
    ground.render()
    arena.update()
    button.render(button.imgdisp)
    cursor.hover()
    # Render stage display
    if stage_display.display == 1:
          stage_display.move_display()
    if stage_display.clear == 1:
          stage_display.stage_clear()
    #must render player and enemies after background and ground
    if moodeng.health > 0:
      displaysurface.blit(moodeng.image, moodeng.rect)
    health.render()
    
    #fireballs
    for ball in Fireballs:
      ball.fire()
      
    for entity in Enemies:
          entity.update()
          entity.move()
          entity.render()
          
      #render items
    for i in Items:
      i.render()
      i.update()
      
    if moodeng.health == 0:
          stage_display.moodeng_death_knell()
          if Death_knell_time is None:   
            Death_knell_time = pygame.time.get_ticks()
    if Death_knell_time is not None:
          current_time = pygame.time.get_ticks()
          if current_time - Death_knell_time >= DEATH_KNELL_DELAY:
                GAME_RUNNING = False
      # Status bar update and render
    displaysurface.blit(status_bar.surf, (580, 5))
    status_bar.update_draw()
    handler.update()
    
    pygame.display.flip() 
    FPS_CLOCK.tick(FPS)
