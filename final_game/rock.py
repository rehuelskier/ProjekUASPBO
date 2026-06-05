import pygame

TILE = 40

# module-level sfx (set from main)
rock_sound = None


class Rock:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.__speed = 4
        self.moving = False
        self.target_x = x
        self.target_y = y
        self.falling = False
        self.roll_delay = 50
        self.roll_wait = 0


    def can_move(self, dx, dy,walls,bushes, rocks,switch_doors,key_doors, zombies=None,treasures=None, coins=None, ignore_zombies=False):

        future = self.rect.move(dx, dy)

        for wall in walls:
            if future.colliderect(wall):
                return False

        for bush in bushes:
            if future.colliderect(bush.rect):
                return False

        for treasure in treasures:
            if future.colliderect(treasure.rect):
                return False

        for switch_door in switch_doors:
            if not switch_door.get_is_open():
                if future.colliderect(switch_door.rect):
                    return False

        for key_door in key_doors:
            if not key_door.get_is_open():
                if future.colliderect(key_door.rect):
                    return False

        for rock in rocks:
            if rock != self and future.colliderect(rock.rect):
                return False

        if coins is not None:
            for coin in coins:
                if future.colliderect(coin.rect):
                    return False

        if zombies is not None and not ignore_zombies:
            for zombie in zombies:
                if future.colliderect(zombie.rect):
                    return False

        return True


    def push(self, dx, dy, walls,bushes, rocks,switch_doors,key_doors, zombies,treasures, coins):
        # Prevent pushing while the rock is already moving, falling,
        # or in the roll-delay countdown before it rolls down.
        if self.moving or self.falling or (self.roll_wait > 0 and self.roll_wait < self.roll_delay):
            return False

        # If space below is free, start falling immediately.
        if self.can_move(
                0, TILE,
                walls, bushes, rocks,
                switch_doors, key_doors,
                zombies,
                treasures,
                coins,
                ignore_zombies=True
        ):
            self.target_y = self.rect.y + TILE
            self.moving = True
            self.falling = True
            self.roll_wait = 0
            return False

        # Otherwise, allow pushing horizontally if destination is free.
        if self.can_move(dx, dy, walls, bushes, rocks, switch_doors, key_doors, zombies, treasures, coins):
            self.target_x = self.rect.x + dx
            self.target_y = self.rect.y + dy
            self.moving = True
            # play push sound if available
            try:
                if rock_sound:
                    rock_sound.play()
            except Exception:
                pass
            return True

        return False


    def update(self, walls,bushes, rocks,switch_doors,key_doors, zombies,treasures, coins,player):

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

                if self.falling:
                    self.falling = False

            if self.falling:
                for zombie in zombies[:]:
                    if self.rect.colliderect(zombie.rect):
                        zombies.remove(zombie)
                        self.falling = False
            return

        # ========================
        # GRAVITY - FALL DOWN
        # ========================

        future = self.rect.move(0, TILE)

        if player is not None:
            if future.colliderect(player.rect):
                return

        if self.can_move(0, TILE, walls,bushes, rocks,switch_doors,key_doors, zombies,treasures, coins, ignore_zombies=True):
            self.target_y = self.rect.y + TILE
            self.moving = True
            self.falling = True
            self.roll_wait = 0
            return
        else:
            self.falling = False

        # ========================
        # CHECK OBSTACLE BELOW
        # ========================
        below_rect = self.rect.move(0, TILE)

        obstacle_below = False
        for rock in rocks:
            if rock != self and below_rect.colliderect(rock.rect):
                obstacle_below = True
                break

        if not obstacle_below:
            for coin in coins:
                if below_rect.colliderect(coin.rect):
                    obstacle_below = True
                    break

        if obstacle_below:
            left_rect = self.rect.move(-TILE, 0)
            down_left_rect = self.rect.move(-TILE, TILE)
            right_rect = self.rect.move(TILE, 0)
            down_right_rect = self.rect.move(TILE, TILE)

            left_blocked = False
            right_blocked = False

            for wall in walls:
                if left_rect.colliderect(wall) or down_left_rect.colliderect(wall):
                    left_blocked = True
                if right_rect.colliderect(wall) or down_right_rect.colliderect(wall):
                    right_blocked = True
                if left_blocked and right_blocked:
                    break

            for bush in bushes:
                if left_rect.colliderect(bush) or down_left_rect.colliderect(bush):
                    left_blocked = True
                if right_rect.colliderect(bush) or down_right_rect.colliderect(bush):
                    right_blocked = True
                if left_blocked and right_blocked:
                    break

            if player is not None:
                if left_rect.colliderect(player.rect) or down_left_rect.colliderect(player.rect):
                    left_blocked = True

                if right_rect.colliderect(player.rect) or down_right_rect.colliderect(player.rect):
                    right_blocked = True

            for rock in rocks:
                if rock != self:
                    if left_rect.colliderect(rock.rect) or down_left_rect.colliderect(rock.rect):
                        left_blocked = True
                    if right_rect.colliderect(rock.rect) or down_right_rect.colliderect(rock.rect):
                        right_blocked = True
                    if left_blocked and right_blocked:
                        break

            if not left_blocked:
                for coin in coins:
                    if left_rect.colliderect(coin.rect) or down_left_rect.colliderect(coin.rect):
                        left_blocked = True
                        break

            if not right_blocked:
                for coin in coins:
                    if right_rect.colliderect(coin.rect) or down_right_rect.colliderect(coin.rect):
                        right_blocked = True
                        break

            if not left_blocked or not right_blocked:

                if self.roll_wait < self.roll_delay:
                    self.roll_wait += 1
                    return

                self.roll_wait = 0

            if not left_blocked:
                self.target_x = self.rect.x - TILE
                self.target_y = self.rect.y + TILE
                self.moving = True
                return

            if not right_blocked:
                self.target_x = self.rect.x + TILE
                self.target_y = self.rect.y + TILE
                self.moving = True
                return

        else:
            self.roll_wait = 0


class Coin(Rock):

    def __init__(self, x, y):
        super().__init__(x, y)

    def push(self, dx, dy, walls,bushes, rocks,switch_doors,key_doors, zombies,treassures, coins):
        return False