import pygame
import copy

def update_game(player, zombies, rocks,coins,weapons, walls,bushes, switch_doors,key_doors,switches,treasures,checkpoints, Hammer,
                coin_sound,
                rock_sound, hit_sound, checkpoint_sound, open_door_sound, take_key_sound,
                trap_active, room_zombies, exit_door,
                stage_clear, game_over,
                camera_x, camera_y,
                MAP_X, MAP_Y, WIDTH, HEIGHT):

    if not game_over and not stage_clear:

        # =================
        # PLAYER MOVE
        # =================
        player.move(walls,bushes, rocks,coins,switch_doors,key_doors,checkpoints,zombies,treasures,coin_sound)
        player.update()

        for bush in bushes[:]:
            if player.rect.colliderect(bush.rect):
                bushes.remove(bush)

        for checkpoint in checkpoints:

            if player.rect.colliderect(checkpoint.rect):

                if not checkpoint.get_active():
                    checkpoint.activate(player)

                    player.checkpoint_data = {

                        "zombies": copy.deepcopy(zombies),
                        "treasures": copy.deepcopy(treasures),
                        "rocks": copy.deepcopy(rocks),
                        "coins": copy.deepcopy(coins),
                        "bushes": copy.deepcopy(bushes),
                        "key_doors": copy.deepcopy(key_doors),

                        "keys": copy.deepcopy(player.keys)

                    }

        # =================
        # WEAPON UPDATE
        # =================
        for w in weapons[:]:
            if isinstance(w,Hammer):
                alive = w.update()
            else:
                alive = w.update(walls,bushes,coins,rocks,switch_doors,key_doors)

            if not alive:
                weapons.remove(w)
                

        # =================
        # WEAPON HIT
        # =================
        for w in weapons[:]:
            for i, zombie in enumerate(zombies):
                if w.rect.colliderect(zombie.rect):

                    if hasattr(zombie, "hammer_hit"):
                        zombies[i] = zombie.hammer_hit(player.direction)

                    if not isinstance(w, Hammer):
                        weapons.remove(w)

                    break

        if player.is_reloading:
            if pygame.time.get_ticks() - player.reload_timer >= 2000:
                player.ammo = 6
                player.is_reloading = False

        if player.get_lives() <= 0:

            if player.has_checkpoint:

                player.rect.x = player.spawn_x
                player.rect.y = player.spawn_y

                player.target_x = player.spawn_x
                player.target_y = player.spawn_y

                if player.checkpoint_data:
                    zombies[:] = copy.deepcopy(
                        player.checkpoint_data["zombies"]
                    )

                    treasures[:] = copy.deepcopy(
                        player.checkpoint_data["treasures"]
                    )

                    rocks[:] = copy.deepcopy(
                        player.checkpoint_data["rocks"]
                    )

                    coins[:] = copy.deepcopy(
                        player.checkpoint_data["coins"]
                    )

                    bushes[:] = copy.deepcopy(
                        player.checkpoint_data["bushes"]
                    )

                    key_doors[:] = copy.deepcopy(
                        player.checkpoint_data["key_doors"]
                    )

                    player.keys = copy.deepcopy(
                        player.checkpoint_data["keys"]
                    )

                player.set_lives(3)
                player.invincible = False

            else:
                game_over = True

        # =================
        # ROCK UPDATE (gravity)
        # =================
        for rock in rocks:
            rock.update(walls,bushes, rocks,switch_doors,key_doors, zombies,treasures,coins,player)

        for switch in switches:
            switch.update(rocks)

        for coin in coins:
            coin.update(walls,bushes, rocks,switch_doors,key_doors, zombies,treasures,coins,player)


        # ZOMBIE UPDATE
        # =================
        for zombie in zombies:

            zombie.update(player, walls, bushes, treasures,
                          rocks,coins, switch_doors, key_doors, zombies)

            if zombie.is_dead():
                continue

            if zombie.is_stunned():
                continue

            if player.rect.colliderect(zombie.rect):
                # play hit sound then apply hit
                if hit_sound:
                    hit_sound.play()
                player.hit()
                break

        # player.update_attack()
        # player.update_reload()

        # =================
        # EXIT DOOR
        # =================
        if player.rect.colliderect(exit_door.rect):
            stage_clear = exit_door.on_player_touch(player)


    # =================
    # CAMERA
    # =================
    camera_x = player.rect.centerx - WIDTH // 2
    camera_y = player.rect.centery - HEIGHT // 2

    camera_x = max(0, min(camera_x, MAP_X - WIDTH))
    camera_y = max(0, min(camera_y, MAP_Y - HEIGHT))


    return weapons, trap_active, room_zombies, stage_clear, game_over, camera_x, camera_y