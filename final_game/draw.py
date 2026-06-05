import pygame

from zombie import BossZombie, ZombieHorizontal, ZombieVertical
TILE = 40

def draw_game(screen, player, zombies, rocks, walls, traps, switch_doors, key_doors, switches, checkpoints, treasures, bushes,
              weapons, coins, exit_door,
              camera_x, camera_y,
              stage, high_stage,
              stage_clear, game_over,
              font, small_font,
              player_images, ghost_images,
               coin_image, wall_image, door_image, open_door_image,
              keydoor1_image, keydoor2_image, open_keydoor1_image, open_keydoor2_image,
              treasure1_image, treasure2_image, bush_image, switch_image,
              portal_image,checkpoint_image, checkpoint_off_image,rock_image, overlay_alpha=0):

    screen.fill((20, 20, 20))

    for wall in walls:
        screen.blit(wall_image, (wall.rect.x - camera_x, wall.rect.y - camera_y))

    for switch_door in switch_doors:
        image = open_door_image if switch_door.get_is_open() else door_image
        screen.blit(image, (switch_door.rect.x - camera_x, switch_door.rect.y - camera_y))

    for key_door in key_doors:
        if key_door.get_is_open():
            image = open_keydoor1_image if key_door.door_id == 1 else open_keydoor2_image
        else:
            image = keydoor1_image if key_door.door_id == 1 else keydoor2_image
        screen.blit(image, (key_door.rect.x - camera_x, key_door.rect.y - camera_y))

    for checkpoint in checkpoints:
        screen.blit(checkpoint_image if checkpoint.get_active() else checkpoint_off_image, (checkpoint.rect.x - camera_x, checkpoint.rect.y - camera_y))

    for treasure in treasures:
        if not treasure.get_opened():
            image = treasure1_image if treasure.key_id == 1 else treasure2_image
            screen.blit(image, (treasure.rect.x - camera_x, treasure.rect.y - camera_y))

    for bush in bushes:
        screen.blit(bush_image, (bush.rect.x - camera_x, bush.rect.y - camera_y))

    for switch in switches:
        screen.blit(switch_image, (switch.rect.x - camera_x, switch.rect.y - camera_y))

    if exit_door:
        screen.blit(portal_image, (exit_door.rect.x - camera_x, exit_door.rect.y - camera_y))

    player_surface = player_images.get(player.direction, player_images["right"])
    # blinking when invincible
    draw_player = True
    if getattr(player, "invincible", False):
        elapsed = pygame.time.get_ticks() - getattr(player, "timer", 0)
        if ((elapsed // 100) % 2) == 0:
            draw_player = False

    if draw_player:
        screen.blit(player_surface, (player.rect.x - camera_x, player.rect.y - camera_y))

    for zombie in zombies:
        if zombie.is_stunned():
            image = ghost_images["stun"]
        elif isinstance(zombie, ZombieHorizontal):
            image = ghost_images["left"] if zombie.get_direction() < 0 else ghost_images["right"]
        elif isinstance(zombie, ZombieVertical):
            image = ghost_images["idle"]
        else:
            image = ghost_images["idle"]

        screen.blit(image, (zombie.rect.x - camera_x, zombie.rect.y - camera_y))

    for w in weapons:
        w.draw(screen, camera_x, camera_y)

    for coin in coins:
        screen.blit(coin_image, (coin.rect.x - camera_x, coin.rect.y - camera_y))

    for rock in rocks:
        screen.blit(rock_image, (rock.rect.x - camera_x, rock.rect.y - camera_y))

    score_text = small_font.render("Coin: "+str(player.score),True,(255,255,255))
    screen.blit(score_text,(10,100))

    lives_text = small_font.render("Lives: "+str(player.get_lives()),True,(255,255,255))
    screen.blit(lives_text,(10,10))

    stage_text = small_font.render("Stage "+str(stage),True,(255,255,255))
    screen.blit(stage_text,(10,40))

    high_text = small_font.render("High Stage "+str(high_stage),True,(255,255,255))
    screen.blit(high_text,(10,70))


    if stage_clear:

        text = font.render("STAGE CLEAR",True,(255,255,0))
        screen.blit(text,(300-150,200-50))

    if game_over:

        text = font.render("GAME OVER",True,(255,0,0))
        screen.blit(text,(300-140,200-50))

    # overlay (start fade / death fade)
    try:
        if overlay_alpha and overlay_alpha > 0:
            overlay = pygame.Surface(screen.get_size())
            overlay.fill((0, 0, 0))
            overlay.set_alpha(int(max(0, min(255, overlay_alpha))))
            screen.blit(overlay, (0, 0))
    except Exception:
        pass

    # show on-touch message (set by objects like Treasure)
    try:
        if getattr(player, 'message_text', None):
            msg = player.message_text
            msg_surf = small_font.render(msg, True, (255, 255, 200))
            px = player.rect.x - camera_x
            py = player.rect.y - camera_y
            # draw above player
            screen.blit(msg_surf, (px, py - 30))
    except Exception:
        pass
