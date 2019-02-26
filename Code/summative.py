'''
Henry So
May 3rd / 2018
ICS3U1, Summative Assignment : Flappy Bird
Flappy Bird is a single player game in which the player tries to get as many points as possible.
The player must get the bird through the gap in between two pillars in order to score a point
Along the way, coins will be show up occassionally in the gaps of the pillars. Coins will be worth
+5 towards the final score. The only control is the spacebar to control the y movement of the bird.
The x movement is fixed.
'''

#I- IMPORT AND INITIALIZE
import pygame, summativeSprites, random
pygame.init()
pygame.mixer.init()

def main ():
    ''' This function defines the 'mainline logic' for the Flappy Bird game.'''
    
    #D - Display
    pygame.display.set_caption ("Flappy Bird")
    
    #set screen to 480x640
    screen = pygame.display.set_mode ((480,640))
    
    #Entities
    background = pygame.image.load ("background.png")
    screen.blit (background, (0,0))
    
    #Background music
    pygame.mixer.music.load ("curb_your_enthusiasm_theme.mp3")
    pygame.mixer.music.set_volume (0.1)
    pygame.mixer.music.play (-1)
    
    #Sound FX
    losefx = pygame.mixer.Sound("lose.ogg")
    pointfx = pygame.mixer.Sound ("score.ogg")
    
    #Gameover Font
    gameoverFont = pygame.font.Font ("game_over.ttf", 100)
    #Displays this message if user takes a L (loss)
    gameoverLabelL = gameoverFont.render ("GAME OVER", 1, (255,255,255))    
    
    #Pillars
    topPillar = summativeSprites.Pillar(screen,1,480)
    botPillar = summativeSprites.Pillar(screen,2,480)
    topPillar2 = summativeSprites.Pillar(screen,1,720)
    botPillar2 = summativeSprites.Pillar(screen,2,720)
    
    #pillar group
    pillars = [topPillar,botPillar,topPillar2,botPillar2]
    
    #scoreIndicators
    scoreIndicator = summativeSprites.ScoreIndicator (screen, 480)
    scoreIndicator2 = summativeSprites.ScoreIndicator (screen, 720)
    
    #scoreIndicator list & group
    scoreIndicators = [scoreIndicator,scoreIndicator2]
    scoreIndicatorGroup = pygame.sprite.Group (scoreIndicators)
    
    scoreKeeper = summativeSprites.ScoreKeeper (screen)
    player = summativeSprites.Player (screen)
    ground = summativeSprites.Ground (screen)
    
    
    allSprites = pygame.sprite.OrderedUpdates (pillars, scoreIndicators, scoreKeeper, ground, player)
    #A - Action (ALTER)
    
    #A - Assign values to key variables
    clock = pygame.time.Clock()
    
    keepGoing = True
    score = scoreIndicator.hit()
    dead = player.dead()
    scored = True
    timesPassed = scoreIndicator.getTimesPassed()
    #Hide mouse
    pygame.mouse.set_visible (False)
    #L - Loop
    while keepGoing:
        
        #Timer to set refresh rate (frame rate)
        clock.tick(30)
        hit = False
        stop = False
        
        #E - Event handling
        for event in pygame.event.get():
            #entities rect are set in the game loop because the pipes reset as they leave the screen
            botPillar.rect.top = topPillar.rect.bottom+135
            botPillar2.rect.top = topPillar2.rect.bottom+135
            scoreIndicator.rect.top = topPillar.rect.bottom
            scoreIndicator2.rect.top = topPillar2.rect.bottom
            scoreIndicator.rect.left = topPillar.rect.centerx
            scoreIndicator2.rect.left = topPillar2.rect.centerx
            
            # if the window is closed the game will end
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                #user controls; if player presses space, the methods below will happen.
                #Space is the only control.
                if event.key == pygame.K_SPACE:
                    player.gravity()
                    player.fly()
                
        #if the player collides with the ground, all moving entities will stop.        
        if player.rect.colliderect (ground.rect):   
            topPillar.stop ()
            botPillar.stop ()
            topPillar2.stop()
            botPillar2.stop()
            ground.stop()
            scoreIndicator.stop()
            scoreIndicator2.stop()
            player.flightless()
            player.dead()
            #if dead is True, the death noise will play. if statement is used so death noise isnt continiously played; only played once.
            if dead:
                losefx.play()
                #blit the gameover message.
                screen.blit (gameoverLabelL, (140,200))
                dead = False
                keepGoing = False
                
        
        #if the player collides with first set of pillars, all moving entities will stop.    
        if player.rect.colliderect (topPillar.rect) or player.rect.colliderect (botPillar.rect):
            topPillar.stop ()
            botPillar.stop ()
            topPillar2.stop()
            botPillar2.stop()            
            ground.stop()
            scoreIndicator.stop()
            scoreIndicator2.stop()
            player.flightless()   
            player.dead()
            #if dead is True, the death noise will play. if statement is used so death noise isnt continiously played; only played once.
            if dead:
                losefx.play()
                #blit gameover msg.
                screen.blit (gameoverLabelL, (140,200))
                dead = False
                keepGoing = False
                
        #if the player collides with second set of pillars, all moving entities will stop.      
        if player.rect.colliderect (topPillar2.rect) or player.rect.colliderect (botPillar2.rect):
            topPillar.stop ()
            botPillar.stop ()
            topPillar2.stop()
            botPillar2.stop()            
            ground.stop()
            scoreIndicator.stop()
            scoreIndicator2.stop()
            player.flightless()
            player.dead()   
            #if dead is True, the death noise will play. if statement is used so death noise isnt continiously played; only played once.
            if dead:
                losefx.play()
                #blit the gameover message.
                screen.blit (gameoverLabelL, (140,200))
                dead = False
                keepGoing = False
        
        #Collision with the scoreIndicator and the player; if the player hits the scoreIndicator, points will be granted.
        if pygame.sprite.spritecollide(player, scoreIndicatorGroup, False):
            for point in pygame.sprite.spritecollide(player, scoreIndicatorGroup, False):
                point.hit()
                if not hit:
                    scoreKeeper.playerScore(timesPassed)
                    pointfx.play()
                    hit = True
                    
        
        # R - Refresh display
        allSprites.clear (screen,background)
        allSprites.update()
        allSprites.draw (screen)
        
        pygame.display.flip ()
    #Unhide mouse pointer
    pygame.mouse.set_visible (True)
    
    pygame.time.delay(3000)
    pygame.quit()
#call main()
main ()
        