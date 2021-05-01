# Intro to GameDev - main game file
import pgzrun
import random

WIDTH = 1000
HEIGHT = 600
SCOREBOARD_HEIGHT = 60

# define some colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BACKGROUND_TITLE = "background2"
BACKGROUND_LEVEL1 = "level1"
BACKGROUND_LEVEL2 = "level2"
BACKGROUND_LEVEL3 = "level3"

BACKGROUND_IMG = BACKGROUND_TITLE
PLAYER_IMG = "drawing6"
JUNK_IMG = "space_junk"
SATELLITE_IMG = "satellite_adv"
DEBRIS_IMG = "space_debris"
LASER_IMG = "laser_red"
START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"

start_button = Actor(START_IMG)
start_button.center = (WIDTH/2, 425)

instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 500)

# counter variables
score = 0
junk_speed = 5
satellite_speed = 3
debris_speed = 2
level = 0
level_screen = 0

junk_collect = 0
lvl2_LIMIT = 5  # collect 5 junk to move to Level 2
lvl3_LIMIT = 10

def on_mouse_down(pos):
    global level, level_screen

    # check start button
    if start_button.collidepoint(pos):
        level = 1
        level_screen = 1
        print("Start button pressed")

    # check instuctions button
    if instructions_button.collidepoint(pos):
        level = -1
        print("Instructions button pressed")

def init():
    global player, junks, satellite, debris, lasers 
    # initializing spaceship
    player = Actor(PLAYER_IMG)
    player.midright = (WIDTH-15, HEIGHT/2)

    # initializing junks
    junks = []
    for i in range(5):
        junk = Actor(JUNK_IMG)
        x_pos = random.randint(-700, -50)
        y_pos = random.randint(SCOREBOARD_HEIGHT, HEIGHT - junk.height)
        junk.topleft = (x_pos, y_pos)
        junks.append(junk)

    #initializing satellite
    satellite = Actor(SATELLITE_IMG)
    x_sat = random.randint(-500,-50)
    y_sat = random.randint(SCOREBOARD_HEIGHT, HEIGHT - satellite.height)
    satellite.topright = (x_sat, y_sat)

    #initialize debris
    debris = Actor(DEBRIS_IMG)
    x_deb = random.randint(-500,-50)
    y_deb = random.randint(SCOREBOARD_HEIGHT, HEIGHT - debris.height)
    debris.topright = (x_deb, y_deb)
    
    lasers=[]

    # background music
    music.play("spacelife")


init()

def draw():
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0,0))

    if level == 0:
        start_button.draw()
        instructions_button.draw()

    if level == -1:
        start_button.draw()

    if level >= 1:
        player.draw()
        for junk in junks:
            junk.draw()
    if level >= 2:
        satellite.draw()
    if level == 3:
        debris.draw()
        for laser in lasers:
            laser.draw()

    show_score = "Score: " + str(score)
    screen.draw.text(show_score, topleft=(650,15), fontsize=35, color='white')
    show_junk_collect = "Junk: " + str(junk_collect)
    screen.draw.text(show_junk_collect, topleft=(450,15), fontsize=35, color='white')

    if level == -1: # instructions screen
        start_button.draw()
        show_instructions = "Use UP and DOWN arrow keys to move your player\n\npress SPACEBAR to shoot"
        screen.draw.text(show_instructions, midtop=(WIDTH/2, 250), fontsize=35, color='white')       

    if level >= 1:
        show_level = "LEVEL " + str(level)
        screen.draw.text(show_level, topright=(375,15), fontsize=35, color='white')
    if level_screen == 1 or level_screen == 3 or level_screen == 5:
        show_transition = "LEVEL " + str(level) + "\nPress ENTER to continue..."
        screen.draw.text(show_transition, center=(WIDTH/2, HEIGHT/2), fontsize=70, color='white')
    if score < 0:  # game over
        show_game_over = "GAME OVER\npress ENTER to play again!"
        screen.draw.text(show_game_over, center=(WIDTH/2, HEIGHT/2), fontsize=70, color='white')

def update():
    global level, level_screen, BACKGROUND_IMG, junk_collect, score
    if level == -1: # Instructions screen
        BACKGROUND_IMG = BACKGROUND_LEVEL1
    if junk_collect == lvl2_LIMIT:  # Level 2
        level = 2
    if junk_collect == lvl3_LIMIT:  # Level 3
        level = 3

    if score >=0 and level>=1:
        if level_screen == 1:  # Level 1 Transition Screen
            BACKGROUND_IMG = BACKGROUND_LEVEL1
            if keyboard.RETURN == 1:
                level_screen = 2
                music.play("space_mysterious")
        if level_screen == 2:  # Level 1 Gameplay Screen
            playerUpdate()
            junkUpdate()
            # updateLasers()

        if level == 2 and level_screen <= 3:  
            level_screen = 3  # Level 2 Transition Screen
            BACKGROUND_IMG = BACKGROUND_LEVEL2
            if keyboard.RETURN == 1:
                level_screen = 4
                music.play("space_suspense")
        if level_screen == 4:  # Level 2 Gameplay Screen
            playerUpdate()
            junkUpdate()
            satelliteUpdate()

        if level == 3 and level_screen <= 5:
            level_screen = 5  # Level 3 Transition Screen
            BACKGROUND_IMG = BACKGROUND_LEVEL3
            if keyboard.RETURN == 1:
                level_screen = 6
                print("ENTER key is pressed")
        if level_screen == 6:  # Level 3 Gameplay Screen
            playerUpdate()
            junkUpdate()
            satelliteUpdate()
            debrisUpdate()
            updateLasers()

    if score < 0:  # Game Over
        music.stop()
        if keyboard.RETURN == 1:
            BACKGROUND_IMG = BACKGROUND_TITLE
            score = 0
            junk_collect = 0
            level = 0
            init()
    

def junkUpdate():
    global score, junk_speed, junk_collect
    for junk in junks:
        junk.x += junk_speed
        collision = player.colliderect(junk)
    
        if (junk.left > WIDTH or collision == 1):
        #junk_speed = random.randint(2,10)
            x_pos = -50
            y_pos = random.randint(SCOREBOARD_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)
        
        if (collision == 1):
            score += 1
            junk_collect += 1  # increase by 1 every time collision occurs
            sounds.collect_pep.play()

def playerUpdate():
    if (keyboard.up == 1 or keyboard.w == 1):
        player.y -= 5

    elif (keyboard.down == 1 or keyboard.s == 1):
        player.y += 5

    if (player.top < 60):
        player.top = 60
        
    if (player.bottom > HEIGHT):
        player.bottom = HEIGHT

    if (keyboard.space == 1) and level == 3:
        laser = Actor(LASER_IMG)
        laser.midright= (player.midleft)
        fireLasers(laser)

def satelliteUpdate():
    global score, satellite_speed
    satellite.x += satellite_speed
    collision = player.colliderect(satellite)

    if (satellite.left > WIDTH or collision==1):
        x_sat = random.randint(-500,-50)
        y_sat = random.randint(SCOREBOARD_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    if (collision == 1):
        score -= 10

def debrisUpdate():
    global score, debris_speed
    debris.x += debris_speed
    collision = player.colliderect(debris)

    if (debris.left > WIDTH or collision==1):
        x_deb = random.randint(-500,-50)
        y_deb = random.randint(SCOREBOARD_HEIGHT, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)

    if (collision == 1):
        score -= 10
        sounds.collect_pep.play()

LASER_SPEED = -5
def updateLasers():
    global score
    for laser in lasers:
        laser.x += LASER_SPEED
        collision_sat = satellite.colliderect(laser)
        collision_deb = debris.colliderect(laser)

        if laser.right < 0 or collision_sat == 1 or collision_deb == 1:
            lasers.remove(laser)

        # checking for collision with satellite
        if collision_sat == 1:
            x_sat = random.randint(-500,-50)
            y_sat = random.randint(SCOREBOARD_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score -= 5
            sounds.explosion.play()

        # checking for collision with debris
        if collision_deb:
            x_deb = random.randint(-500,-50)
            y_deb = random.randint(SCOREBOARD_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += 5

player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list

pgzrun.go()
