import pygame

def handle_events(stage, stage_clear, game_over):

    running = True
    spawn_attack = False
    selected_weapon = None
    load_checkpoint = False


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_over:

                if event.key == pygame.K_r:
                    game_over = False
                    stage = 1

            elif not stage_clear:

                if event.key == pygame.K_1:
                    selected_weapon = "hammer"

                if event.key == pygame.K_2:
                    selected_weapon = "pistol"

                if event.key == pygame.K_SPACE:
                    spawn_attack = True

                if event.key == pygame.K_l:
                    load_checkpoint = True

            else:

                if event.key == pygame.K_RETURN:
                    stage += 1
                    stage_clear = False

    return running, spawn_attack, selected_weapon, load_checkpoint, stage, stage_clear, game_over

