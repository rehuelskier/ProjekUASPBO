import pygame
from abc import ABC, abstractmethod

TILE = 40
STUN_DURATION_MS = 2000
TURN_DELAY_MS = 500

class BaseZombie(ABC):

    player_speed: int
    zombie_speed: int
    frames_per_tile: int
    _dir: int

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, TILE, TILE)
        self._dead = False
        self.target_x = x
        self.target_y = y
        self.is_moving = False
        self._stunned = False
        self._stun_time = 0
        self._waiting_turn = False
        self._turn_wait_time = 0

    def get_direction(self):
        return self._dir

    def set_direction(self, direction):
        if direction in (-1, 1):
            self._dir = direction

    def reverse_direction(self):
        self._dir *= -1

    def is_stunned(self):
        return self._stunned

    def set_stunned(self, status):
        self._stunned = status

    def is_dead(self):
        return self._dead

    def set_dead(self, status):
        self._dead = status

    def is_waiting_turn(self):
        return self._waiting_turn

    def set_waiting_turn(self, status):
        self._waiting_turn = status

    @abstractmethod
    def update(self, player, walls, bushes, treasures,
               rocks,coins, switch_doors, key_doors, zombies):
        pass

    def hammer_hit(self, direction):

        self.set_stunned(True)
        self._stun_time = pygame.time.get_ticks()
        return self

    def can_move(self, dx, dy, walls, bushes, treasures,
                 rocks,coins, switch_doors, key_doors, zombies):

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
            if future.colliderect(switch_door):
                return False

        for key_door in key_doors:
            if future.colliderect(key_door):
                return False

        for rock in rocks:
            if future.colliderect(rock.rect):
                return False

        for coin in coins:
            if future.colliderect(coin.rect):
                return False

        for zombie in zombies:
            if zombie is self:
                continue

            if future.colliderect(zombie.rect):
                return False

            if zombie.is_moving:
                target_rect = pygame.Rect(zombie.target_x, zombie.target_y, TILE, TILE)
                if future.colliderect(target_rect):
                    return False

        return True

    def _process_stun(self):

        if not self.is_stunned():
            return False

        if pygame.time.get_ticks() - self._stun_time >= STUN_DURATION_MS:
            self.set_stunned(False)

        return self.is_stunned()

    def _process_turn_wait(self):

        if not self.is_waiting_turn():
            return False

        if pygame.time.get_ticks() - self._turn_wait_time >= TURN_DELAY_MS:
            self.reverse_direction()
            self.set_waiting_turn(False)

        return self.is_waiting_turn()

    def _apply_smooth_move(self):

        if (not self.is_moving or self.is_stunned() or
                self.is_waiting_turn()):
            return

        if self.rect.x < self.target_x:
            self.rect.x = min(self.rect.x + self.zombie_speed, self.target_x)
        elif self.rect.x > self.target_x:
            self.rect.x = max(self.rect.x - self.zombie_speed, self.target_x)

        if self.rect.y < self.target_y:
            self.rect.y = min(self.rect.y + self.zombie_speed, self.target_y)
        elif self.rect.y > self.target_y:
            self.rect.y = max(self.rect.y - self.zombie_speed, self.target_y)

        if self.rect.x == self.target_x and self.rect.y == self.target_y:
            self.is_moving = False

    def _start_move(self, dx, dy):

        self.target_x  = self.rect.x + dx
        self.target_y  = self.rect.y + dy
        self.is_moving = True


class ZombieHorizontal(BaseZombie):

    def __init__(self, x, y, player_speed=4):

        self.player_speed = player_speed
        self.zombie_speed = max(1, player_speed // 2)
        self.frames_per_tile = TILE // self.zombie_speed
        self._dir = 1

        super().__init__(x, y)

    def update(self, player, walls, bushes, treasures,
               rocks,coins, switch_doors, key_doors, zombies):

        self._apply_smooth_move()

        if self._process_turn_wait():
            return

        if self._process_stun():
            return

        if self.is_moving:
            return

        dx = TILE * self.get_direction()

        if self.can_move(dx, 0, walls, bushes, treasures,
                         rocks,coins, switch_doors, key_doors, zombies):
            self._start_move(dx, 0)
        else:
            if not self.is_waiting_turn():
                self.set_waiting_turn(True)
                self._turn_wait_time = pygame.time.get_ticks()


class ZombieVertical(BaseZombie):

    def __init__(self, x, y, player_speed=4):

        self.player_speed = player_speed
        self.zombie_speed = max(1, player_speed // 2)
        self.frames_per_tile = TILE // self.zombie_speed
        self._dir = 1

        super().__init__(x, y)

    def update(self, player, walls, bushes, treasures,
               rocks,coins, switch_doors, key_doors, zombies):

        self._apply_smooth_move()

        if self._process_turn_wait():
            return

        if self._process_stun():
            return

        if self.is_moving:
            return

        dy = TILE * self.get_direction()

        if self.can_move(0, dy, walls, bushes, treasures,
                         rocks,coins, switch_doors, key_doors, zombies):
            self._start_move(0, dy)
        else:
            if not self.is_waiting_turn():
                self.set_waiting_turn(True)
                self._turn_wait_time = pygame.time.get_ticks()


class BossZombie(BaseZombie):

    def __init__(self, x, y, stage, player_speed=3):

        self.player_speed = player_speed
        self.zombie_speed = max(1, player_speed // 2)
        self.frames_per_tile = TILE // self.zombie_speed
        self._dir = 1

        super().__init__(x, y)

        self.hp = 5 + (stage // 5) * 2


    def update(self, player, walls, bushes, treasures,
               rocks,coins, switch_doors, key_doors, zombies):
        pass


    def hit(self):
        self.hp -= 1
        return self.hp <= 0