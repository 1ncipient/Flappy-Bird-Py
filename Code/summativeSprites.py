'''
Henry So
May 3rd 2018
ICS3U1, Summative Assignment Module. Flappy Bird.
this .py file is the module for summative.py. This module contains classes that include
Player (), Pillar(), Ground (), ScoreKeeper().
'''
import pygame, random

class Ground (pygame.sprite.Sprite):
    ''' This class defines the sprite for our scrolling background.'''
    def __init__ (self,screen):
        '''
        This initializer takes the screen as a surface. It initializes the image, rect, and dx attributes.
        '''
        #Call the parent __init__ () method 
        pygame.sprite.Sprite.__init__ (self)
        
        #1920 x 80
        self.image = pygame.image.load ("ground.png")
        self.image = self.image.convert()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,560)
        self.rect.bottom = screen.get_height()
        
        self.__dx = -5
        
    def stop (self):
        '''This method is called when the player dies so that the scrolling background stops.'''
        self.__dx = 0
        
    def update (self):
        ''' This method will be called automatically to reposition the background so it gives the illusion that it is neverending.'''
        self.rect.right += self.__dx
        #self.rect.left starts at 0 so i cannot use self.rect.left == 0. Must use self.rect.centerx 
        #When the middle of the image hits the 0 the image will reset @ 960
        if self.rect.centerx == 0:
            self.rect.left  = 0
            
class Player (pygame.sprite.Sprite):
    ''' This class defines the sprite for our Player.'''
    def __init__ (self, screen):
        ''' This initializer takes screen surface as a parameter, initializes the image and rect attributes, as well as
        the screen, dead, dy, and frame.
        '''
        #Call the parent __init__ () method
        pygame.sprite.Sprite.__init__ (self)
        
        self.image = pygame.image.load ("flap0.png")        
        
        self.rect = self.image.get_rect()
        self.rect.center = ((screen.get_width() / 3), screen.get_height() / 2) #(160,320)
        
        self.__screen = screen
        self.__dead = False
        
        self.__dy = 0
        self.__frame = 0
    def flightless (self):
        '''This method will be run when the bird collides with either a pillar or ground.'''
        self.__dy = 15
        
    def gravity (self):
        '''This method is the gravity on the bird. The dy of the bird will be set to 5, causing it to go down. '''
        self.__dy = 7
    
    def fly (self):
        ''' This method changes the flappy bird's image so it gives the appearance that it is flying'''
        
        flySound = pygame.mixer.Sound("fly.ogg")
        flySound.play()
        self.rect.bottom += -75
        
    def dead (self):
        '''
        This method sets self.__dead as True and returns the method
        '''
        self.__dead = True
        return self.__dead
    
    def update (self): 
        '''
        As long as the bird is in the air, and the bird's dy is positive, then the bird will always go down. '''
        
        if ((self.rect.bottom < 560) and (self.__dy > 0)) :
            self.rect.bottom += self.__dy
            if self.__frame < 3:
                self.image = pygame.image.load ("flap" +str(self.__frame) + ".png")
                self.__frame +=1
            if self.__frame == 3:
                self.__frame = 0        
            
class Pillar (pygame.sprite.Sprite):
    ''' This class defines the sprite for the pillars.'''
    def __init__ (self,screen,pillar,x_pos):
        ''' This initializer takes a screen surface, pillar, and x_pos as parameters. It 
        initializes the following variables; randomY, image, rect,and dx.
        
        Depending on the parameter given, the appropriate image will be selected
        '''
        #Call the parent __init__ () method
        pygame.sprite.Sprite.__init__ (self)
        
        self.__randomY = random.randint (80,360)
        
        if pillar == 1: 
            self.image = pygame.image.load ("top_pillar.png")
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (x_pos,self.__randomY)
        elif pillar == 2:
            self.image = pygame.image.load ("bot_pillar.png")
            self.rect = self.image.get_rect()
            self.rect.topleft = (x_pos,self.__randomY)
        #factor the pillars will shift to the left by
        self.__dx = -5
        
    def setRandom (self):
        ''' This method creates a random integer to use for the shift of the pipes.''' 
        self.rect.bottom = random.randint (80,380)
   
    def stop (self):
        '''This method runs when the bird hits an obstacle that will lead to a loss (ground, pillar). It is run in order to stop the pillars from moving. '''
        self.__dx = 0
        
    def reset (self):
        '''This method resets the pillars to the right to create an infinite loop of pillars until the player loses.'''
        self.rect.left = 480
        
        
    def update (self):
        ''' The pillar will go back to the right side of the screen when its rect.right is zero (when it is off the screen). It will always move left by a factor of self.__dx.'''
        self.rect.left += self.__dx
        
        if (self.rect.right <= 0) :
            self.reset()
            self.setRandom()
              
class ScoreIndicator (pygame.sprite.Sprite):
    ''' This class defines the sprite for the score indicator in between the pillars, in the gap. '''
    def __init__ (self,screen,x_pos):
        '''This initializer takes a screen surface and x_pos as parameters. It initializes the following
        instance variables; image,rect, screen, dx and timesPassed.
        
        The x_pos should be the same as the pillars x_pos.
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__ (self)
        
        self.__placementY = random.randint (80,480)
        
        self.image = pygame.image.load ("invisibleScoreKeeper.png") #1x135, transparent
        self.rect = self.image.get_rect ()
        self.rect.top = self.__placementY
        self.rect.left = x_pos
        
        self.__dx = -5
        self.__timesPassed = 0
        self.__screen = screen
        
    def hit (self):
        '''This method defines the amount of times this invisible sprite is hit. The amount of times the sprite is hit, the timesPassed will add 1 to itself.'''
        self.__timesPassed += 1
        
    def getTimesPassed (self):
        '''This method returns self.__timesPassed'''
        return self.__timesPassed
        
    def stop (self):
        '''This method stops the indicator from moving when the player loses.'''
        self.__dx = 0
        
    def update (self):
        '''
        Like the pillars, it resets itself on the right of the screen when its rect.right is less or equal to 0
        '''
        self.rect.left += self.__dx
        if (self.rect.right <= 0) :
            self.rect.left = 480
        
class ScoreKeeper (pygame.sprite.Sprite):
    '''This class defines the sprite for the scorekeeper'''
    def __init__ (self,screen):
        ''' This initializer takes the screen surface as a parameter. The following attributes are initialized;
        font,score,screen
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__ (self)
        
        #load custom font
        self.__font = pygame.font.Font("digital-7.ttf", 48)
        self.__score = 0
        self.__screen = screen
        
    def playerScore (self, timesPassed):
        '''This method is the total score accumulated by the player. It takes timesPassed as a parameter in order to add 
        the amount of times the player passes the pipes onto the final score.'''
        self.__score += timesPassed
        
    def update (self):
        ''' This update method is called automatically to display the current score at the topright of the window. '''
        scoreboard = "%d" % (self.__score)
        self.image = self.__font.render (scoreboard, 1, (255,255,255)) 
        self.rect = self.image.get_rect()
        #positions the scoreboard on the top right of the screen.
        self.rect.center = (self.__screen.get_width() - 50, 30)    
