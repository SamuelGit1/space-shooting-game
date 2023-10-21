import pgzrun
from random import *
from pgzhelper import *

WIDTH = 890                 # The width of the game window
HEIGHT = 560                # The height of the game window
SPAWN_ENEMY_PESENTAGE = 30  # The spawn rate of the enemy per tick
ENEMY_LIMIT = 200           # The maximum number of enemie on the screen

enemies = []
lasers = []
enemy_lasers = []

player = Actor('playership2_blue')
player.x, player.bottom = WIDTH / 2, HEIGHT
player.hp = float('inf')

def keyboard_input():
    if keyboard.w or keyboard.up:
        player.y -= 5
    if keyboard.a or keyboard.left:
        player.x -= 5
    if keyboard.s or keyboard.down:
        player.y += 5
    if keyboard.d or keyboard.right:
        player.x += 5
    if keyboard.b and keyboard.a and keyboard.c and keyboard.k:
        player.x, player.bottom = WIDTH / 2, HEIGHT

def check_pos():
    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH
    if player.top < 0:
        player.top = 0
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT

def spawn_enemy():
    if len(enemies) < ENEMY_LIMIT and randint(1, 100) <= SPAWN_ENEMY_PESENTAGE:
        enemy = Actor('enemies/enemyblack1')
        enemy.x = randint(0, WIDTH)
        enemies.append(enemy)

def update_lasers():
    for laser in lasers:
        laser.move_forward(15)
        if laser.bottom < 0:
            lasers.remove(laser)
            continue

        for enemy in enemies:
            if laser.collide_pixel(enemy):
                lasers.remove(laser)
                enemies.remove(enemy)
                break

    for enemy_laser in enemy_lasers:
        enemy_laser.angle = 270
        enemy_laser.move_forward(15)
        if enemy_laser.top > HEIGHT:
                enemy_lasers.remove(enemy_laser)
                continue
        elif enemy_laser.collide_pixel(player):
            enemy_lasers.remove(enemy_laser)
            player.hp -= 1
            if keyboard.m:
                player.hp -= player.hp / 100


    if keyboard.space:
        laser = Actor('lasers/laserblue01')
        laser.bottom = player.bottom
        laser.x = player.x

        if len(enemies) > 0:
            enemy = choice(enemies)
            laser.angle = laser.angle_to(enemy)
        else:
            laser.angle = 90

        lasers.append(laser)

def update_enemies():
    for enemy in enemies:
        if randint(1, 100) <= 5:
            enemy_laser = Actor('lasers/lasergreen02')
            enemy_laser.top = enemy.bottom
            enemy_laser.x = enemy.x
            enemy_lasers.append(enemy_laser)

def update():
    keyboard_input()
    check_pos()
    spawn_enemy()
    update_lasers()
    update_enemies()


def draw():
    screen.clear()

    hp_bar = Rect(0, 0, player.hp / 100 * WIDTH, 30)
    screen.draw.filled_rect(hp_bar, (255, 0, 0))

    player.draw()

    for enemy in enemies:
        enemy.draw()
    for laser in lasers:
        laser.draw()
    for enemy_laser in enemy_lasers:
        enemy_laser.draw()
    
    


pgzrun.go()