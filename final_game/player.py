import pygame

TILE = 40

class Player:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, TILE, TILE)

        self.__speed = 4
        self.direction = "right"

        self.spawn_x = x
        self.spawn_y = y
        self.has_checkpoint = False

        self.checkpoint_data = None

        self.moving = False
        self.target_x = x
        self.target_y = y
        self.score = 0
        self.keys = []
        self.coin_sound = None

        self.__lives = 3
        self.invincible = False
        self.timer = 0

        self.is_attacking = False
        self.attack_timer = 0

        self.ammo = 10

        self.is_reloading = False
        self.reload_timer = 0
        

    def get_lives(self):
        return self.__lives

    def set_lives(self, lives):
        self.__lives = lives

    def move(self, walls,
    bushes,
    rocks,
    coins,
    switch_doors,key_doors,
    checkpoints,
    zombies,
    treasures,
    coin_sound=None):

        keys = pygame.key.get_pressed()

        if not self.moving:

            dx = 0
            dy = 0

            if keys[pygame.K_LEFT]:
                self.direction = "left"
                dx = TILE - TILE
            if keys[pygame.K_RIGHT]:
                self.direction = "right"
                dx = TILE - TILE
            if keys[pygame.K_UP]:
                self.direction = "up"
                dy = TILE - TILE
            if keys[pygame.K_DOWN]:
                self.direction = "down"
                dy = TILE - TILE

            if keys[pygame.K_a]:
                self.direction = "left"
                dx = -TILE
            elif keys[pygame.K_d]:
                self.direction = "right"
                dx = TILE
            elif keys[pygame.K_w]:
                dy = -TILE
                self.direction = "up"
            elif keys[pygame.K_s]:
                dy = TILE
                self.direction = "down"

            if dx != 0 or dy != 0:

                future = pygame.Rect(
                    self.rect.x + dx,
                    self.rect.y + dy,
                    TILE,
                    TILE
                )

                blocked = False

                # cek rock
                for rock in rocks:

                    if future.colliderect(rock.rect):

                        if dx != 0 and rock.can_move(dx, 0, walls,bushes, rocks,switch_doors,key_doors,zombies,treasures,coins):

                            pushed = rock.push(dx, 0, walls,bushes, rocks,switch_doors,key_doors,zombies,treasures,coins)
                            if not pushed:
                                blocked = True

                        else:
                            blocked = True

                for checkpoint in checkpoints:
                    if future.colliderect(checkpoint.rect):
                        self.spawn_x = checkpoint.rect.x
                        self.spawn_y = checkpoint.rect.y
                        self.has_checkpoint = True

                for switch_door in switch_doors:

                    if future.colliderect(switch_door.rect):

                        switch_door.on_player_touch(self)

                        if not switch_door.get_is_open():
                            blocked = True
                            break

                for key_door in key_doors:

                    if future.colliderect(key_door.rect):

                        key_door.on_player_touch(self)

                        if not key_door.get_is_open():
                            blocked = True
                            break

                for treasure in treasures:
                    if self.rect.colliderect(treasure.rect):
                        treasure.on_player_touch(self)

                # cek wall
                if not blocked:

                    for wall in walls:
                        if wall._solid and future.colliderect(wall.rect):
                            blocked = True
                            break

                for coin in coins:
                    if future.colliderect(coin.rect):
                        coins.remove(coin)
                        self.score += 1
                        if coin_sound:
                            coin_sound.play()

                if not blocked:

                    self.target_x = self.rect.x + dx
                    self.target_y = self.rect.y + dy
                    self.moving = True


        if self.moving:

            if self.rect.x < self.target_x:
                self.rect.x += self.__speed

            if self.rect.x > self.target_x:
                self.rect.x -= self.__speed

            if self.rect.y < self.target_y:
                self.rect.y += self.__speed

            if self.rect.y > self.target_y:
                self.rect.y -= self.__speed


            if self.rect.x == self.target_x and self.rect.y == self.target_y:
                self.moving = False

    def hit(self):
        if not self.invincible:
            self.__lives -= 1
            self.invincible = True
            self.timer = pygame.time.get_ticks()

    def update(self):
        if self.invincible:
            if pygame.time.get_ticks() - self.timer > 1000:
                self.invincible = False