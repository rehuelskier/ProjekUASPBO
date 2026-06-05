import pygame
import copy
import os
import rock as rock_module
import obstacle as obstacle_module

from player import Player
from hammer import Hammer,Pistol
from map import load_map, all_maps

from loop import handle_events
from update import update_game
from draw import draw_game

pygame.init()

WIDTH = 600
HEIGHT = 400
TILE = 40
MAX_LIVES = 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crypth of Ghost")
current_path = os.path.dirname(__file__)
asset_path = os.path.join(current_path, "assets")


def load_image(name, size=None, alpha=True):
    path = os.path.join(asset_path, name)
    image = pygame.image.load(path)
    image = image.convert_alpha() if alpha else image.convert()
    return pygame.transform.scale(image, size) if size else image


coin_image = load_image("coin.png", (TILE, TILE))
wall_image = load_image("wall.png", (TILE, TILE))
door_image = load_image("door.png", (TILE, TILE))
open_door_image = load_image("open_door.png", (TILE, TILE))
portal_image = load_image("portal.png", (TILE, TILE))
bush_image = load_image("bush.png", (TILE, TILE))
switch_image = load_image("switch.png", (TILE, TILE))
keydoor1_image = load_image("keydoor1.png", (TILE, TILE))
keydoor2_image = load_image("keydoor2.png", (TILE, TILE))
open_keydoor1_image = load_image("open_keydoor1.png", (TILE, TILE))
open_keydoor2_image = load_image("open_keydoor2.png", (TILE, TILE))
treasure1_image = load_image("treasure1.png", (TILE, TILE))
treasure2_image = load_image("treasure2.png", (TILE, TILE))
checkpoint_image = load_image("checkpoint_on.png", (TILE, TILE))
checkpoint_off_image = load_image("checkpoint.off.png", (TILE, TILE))
rock_image = load_image("rock.png", (TILE, TILE))
menu_bg_image = load_image("menu_bg.png", (WIDTH, HEIGHT), alpha=False)

player_images = {
    "up": load_image("player_north.png", (TILE, TILE)),
    "down": load_image("player_south.png", (TILE, TILE)),
    "left": load_image("player_west.jpeg", (TILE, TILE)),
    "right": load_image("player_east.png", (TILE, TILE)),
}

weapon_images = {
    "hammer": {
        "up": load_image("hammer_top.png", (TILE, TILE)),
        "down": load_image("hammer_bottom.png", (TILE, TILE)),
        "left": load_image("hammer_left.png", (TILE, TILE)),
        "right": load_image("hammer_right.png", (TILE, TILE)),
    },
    "pistol": {
        "up": load_image("gun_top.png", (TILE, TILE)),
        "down": load_image("gun_bottom.png", (TILE, TILE)),
        "left": load_image("gun_left.png", (TILE, TILE)),
        "right": load_image("gun_right.png", (TILE, TILE)),
    }
}

ghost_images = {
    "idle": load_image("ghost_idle.png", (TILE, TILE)),
    "left": load_image("ghost_left.png", (TILE, TILE)),
    "right": load_image("ghost_right.png", (TILE, TILE)),
    "stun": load_image("ghost_stun.png", (TILE, TILE)),
}

bullet_image = load_image("peluru.png", (TILE // 2, TILE // 2))

def load_sound(filename, volume=0.5):
    path = os.path.join(asset_path, filename)
    try:
        s = pygame.mixer.Sound(path)
        s.set_volume(volume)
        return s
    except Exception:
        return None

coin_sound = load_sound("Coin.mp3", 0.4)
gun_sound = load_sound("sfx_gun.mp3", 0.5)
hammer_sound = load_sound("sfx_hammer.mp3", 0.5)
rock_sound = load_sound("batu_geser.mp3", 0.5)
checkpoint_sound = load_sound("sfx checkpoint.mp3", 0.5) or load_sound("checkpoint.mp3", 0.5) or load_sound("sfx_checkpoint.mp3", 0.5)
death_sound = load_sound("death.mp3", 0.6)
hit_sound = load_sound("hit.mp3", 0.6)
open_door_sound = load_sound("open_door.mp3", 0.5)
take_key_sound = load_sound("take_key.mp3", 0.6)
menu_backsound = load_sound("menu_backsound.mp3", 0.4)

rock_module.rock_sound = rock_sound
obstacle_module.open_door_sound = open_door_sound
obstacle_module.take_key_sound = take_key_sound
obstacle_module.checkpoint_sound = checkpoint_sound

clock = pygame.time.Clock()

MAP_X = 2000
MAP_Y = 1300

font = pygame.font.SysFont(None,50)
small_font = pygame.font.SysFont(None,35)

stage = 0
high_stage = 1
weapons = []
current_weapon = "hammer"

walls, bushes, zombies, coins, traps, rocks, spawn, switch_doors, key_doors, switches, treasures, checkpoints, exit_door = load_map(
    all_maps[stage - 1]
)

player = Player(spawn[0], spawn[1])

trap_active = False
room_zombies = []

stage_clear = False
game_over = False

camera_x = 0
camera_y = 0

running = True
game_state = "menu"
current_stage = stage
menu_channel = None
menu_playing = False
overlay_alpha = 255
start_fade = True
death_fade = False

while running:

    clock.tick(60)

    if game_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "play"

        screen.blit(menu_bg_image, (0, 0))
        pygame.display.flip()
        continue

    # start menu/back sound when entering play
    if game_state == "play" and not menu_playing:
        try:
            menu_channel = menu_backsound.play(-1)
            menu_playing = True
        except Exception:
            menu_channel = None
            menu_playing = False
        # start with dark overlay then fade
        overlay_alpha = 255
        start_fade = True
        death_fade = False

    # LOOP (INPUT)
    running, spawn_attack, selected_weapon, load_checkpoint, stage, stage_clear, game_over = handle_events(
        stage, stage_clear, game_over
    )

    if stage != current_stage:
        if stage <= len(all_maps):
            walls, bushes, zombies, coins, traps, rocks, spawn, switch_doors, key_doors, switches, treasures, checkpoints, exit_door = load_map(
                all_maps[stage - 1]
            )
            player.rect.x = spawn[0]
            player.rect.y = spawn[1]
            player.target_x = spawn[0]
            player.target_y = spawn[1]
            player.has_checkpoint = False
            player.checkpoint_data = None
            current_stage = stage
            stage_clear = False
            game_over = False
        else:
            game_over = True

    if stage > high_stage:
        high_stage = stage

    if load_checkpoint and player.has_checkpoint:

        player.rect.x = player.spawn_x
        player.rect.y = player.spawn_y

        player.target_x = player.spawn_x
        player.target_y = player.spawn_y

        if player.checkpoint_data:
            zombies[:] = copy.deepcopy(player.checkpoint_data["zombies"])
            treasures[:] = copy.deepcopy(player.checkpoint_data["treasures"])
            rocks[:] = copy.deepcopy(player.checkpoint_data["rocks"])
            coins[:] = copy.deepcopy(player.checkpoint_data["coins"])
            bushes[:] = copy.deepcopy(player.checkpoint_data["bushes"])
            key_doors[:] = copy.deepcopy(player.checkpoint_data["key_doors"])

            player.keys = copy.deepcopy(
                player.checkpoint_data["keys"]
            )

    if selected_weapon:
        current_weapon = selected_weapon

    if spawn_attack:

        if current_weapon == "hammer":
            hammer_sound.play()
            player.is_attacking = True
            player.attack_timer = pygame.time.get_ticks()
            weapon_image = weapon_images["hammer"][player.direction]
            weapons.append(Hammer(player, weapon_image))

        elif current_weapon == "pistol":

            if player.is_reloading:
                print("LAGI RELOAD")

            elif player.ammo > 0:
                player.ammo -= 1
                gun_sound.play()
                weapons.append(Pistol(player, bullet_image))

            else:
                print("RELOAD!")
                player.is_reloading = True
                player.reload_timer = pygame.time.get_ticks()


    # UPDATE (LOGIC)
    (weapons, trap_active, room_zombies, stage_clear, game_over, camera_x, camera_y)= update_game(
        player, zombies, rocks, coins, weapons, walls, bushes, switch_doors,key_doors,switches,treasures, checkpoints, Hammer,
        coin_sound,
        rock_sound, hit_sound, checkpoint_sound, open_door_sound, take_key_sound,
        trap_active, room_zombies, exit_door,
        stage_clear, game_over,
        camera_x, camera_y,
        MAP_X, MAP_Y, WIDTH, HEIGHT
    )

    # DRAW (RENDER)
    # handle start/death overlay fades and menu music stop on death
    if game_over and menu_playing:
        try:
            if menu_channel:
                menu_channel.stop()
        except Exception:
            pass
        menu_playing = False
        try:
            death_sound.play()
        except Exception:
            pass
        death_fade = True

    if start_fade:
        overlay_alpha = max(0, overlay_alpha - 10)
        if overlay_alpha == 0:
            start_fade = False

    if death_fade:
        overlay_alpha = min(255, overlay_alpha + 10)
        if overlay_alpha == 255:
            death_fade = False

    draw_game(
        screen, player, zombies, rocks, walls, traps, switch_doors, key_doors, switches, checkpoints, treasures, bushes,
        weapons, coins, exit_door,
        camera_x, camera_y,
        stage, high_stage,
        stage_clear, game_over,
        font, small_font,
        player_images, ghost_images,
         coin_image, wall_image, door_image, open_door_image,
        keydoor1_image, keydoor2_image, open_keydoor1_image, open_keydoor2_image,
        treasure1_image, treasure2_image, bush_image, switch_image,
        portal_image,checkpoint_image, checkpoint_off_image,rock_image,
        overlay_alpha
    )
    # UI TEXT
    weapon_text = small_font.render("Weapon: " + current_weapon, True, (255, 255, 255))
    screen.blit(weapon_text, (10, 130))

    if current_weapon== "pistol":
        ammo_text = small_font.render("Ammo: " + str(player.ammo), True, (255, 255, 255))
        screen.blit(ammo_text, (10, 160))
    pygame.display.flip()
pygame.quit()