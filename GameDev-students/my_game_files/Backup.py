# Intro to GameDev - main game file
import pgzrun
import random

WIDTH = 1000
HEIGHT = 600
SCOREBOARD_HEIGHT = 60

BACKGROUND_IMG = "new_level_1"
PLAYER_IMG = "drawing6"
JUNK_IMG = "space_junk"
SATELLITE_IMG = "satellite_adv"
DEBRIS_IMG = "space_debris"
LASER_IMG = "laser_red"

def init():
    global player, junks, satellite, debris, lasers
    player = Actor(PLAYER_IMG)
    player.midright = (WIDTH-15, HEIGHT/2)

    junks = []
    for i in range(5):
        junk = Actor(JUNK_IMG)
        x_pos = random.randint(-500, -50)
        y_pos = random.randint(SCOREBOARD_HEIGHT, HEIGHT - junk.height)
        junk.topleft = (x_pos, y_pos)
        junks.append(junk)
        
        
    satellite = Actor(SATELLITE_IMG)
    x_sat = random.randint(-500,-50)
    y_sat = random.randint(SCOREBOARD_HEIGHT, HEIGHT - satellite.height)
    satellite.topright = (x_sat, y_sat)

    debris = Actor(DEBRIS_IMG)
    x_deb = random.randint(-500,-50)
    y_deb = random.randint(SCOREBOARD_HEIGHT, HEIGHT - debris.height)
    debris.topright = (x_deb, y_deb)

    lasers=[]

score = 0
junk_speed = 5
satellite_speed = 3
debris_speed = 2

init()

def draw():
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0,0))
    player.draw()

    for junk in junks:
        junk.draw()

    satellite.draw()
    debris.draw()

    show_score = "Score: " + str(score)
    screen.draw.text(show_score, topleft=(750, 15), fontsize=35, color="white")

    for laser in lasers:
        laser.draw()

def update():
    playerUpdate()
    junkUpdate()
    satelliteUpdate()
    debrisUpdate()
    updateLasers()

def junkUpdate():
    global score, junk_speed
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

def playerUpdate():
    if (keyboard.up == 1 or keyboard.w == 1):
        player.y -= 5

    elif (keyboard.down == 1 or keyboard.s == 1):
        player.y += 5

    if (player.top < 60):
        player.top = 60
    if (player.bottom > HEIGHT):
        player.bottom = HEIGHT

    if keyboard.space == 1:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
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
        
LASER_SPEED = -5
LASER_SPEED = -5
def updateLasers():
    global score
    for laser in lasers:
        laser.x += LASER_SPEED

        if laser.right < 0:
            lasers.remove(laser)

        # checking for collision with satellite
        if satellite.colliderect(laser) == 1:
            lasers.remove(laser)
            x_sat = random.randint(-500,-50)
            y_sat = random.randint(SCOREBOARD_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score -= 5

        # checking for collision with debris
        if debris.colliderect(laser) == 1:
            lasers.remove(laser)
            x_deb = random.randint(-500,-50)
            y_deb = random.randint(SCOREBOARD_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += 5

player.laserActive = 1  # add laserActive status to the player

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
