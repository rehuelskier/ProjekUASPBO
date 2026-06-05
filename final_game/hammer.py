import pygame
from abc import ABC, abstractmethod

TILE = 40

class Weapon(ABC):

    def __init__(self, x, y, speed, width=TILE, height=TILE, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self._speed = speed
        self._spawn = True
        self._target_x = 0
        self._target_y = 0
        self._image = image

    def move(self):
        pass

    def attack(self):
        pass

    def update(self):
        return False

    def draw(self, screen, camera_x, camera_y):
        if self._image:
            screen.blit(self._image, (self.rect.x - camera_x, self.rect.y - camera_y))
        else:
            pygame.draw.rect(
                screen,
                (255, 200, 0),
                (
                    self.rect.x - camera_x,
                    self.rect.y - camera_y,
                    self.rect.width,
                    self.rect.height,
                )
            )

class Hammer(Weapon):

    def __init__(self, player, image=None):

        self.direction = player.direction
        size = TILE

        if self.direction == "up":
            x, y = player.rect.x, player.rect.y - size
        elif self.direction == "down":
            x, y = player.rect.x, player.rect.y + size
        elif self.direction == "left":
            x, y = player.rect.x - size, player.rect.y
        else:  # right
            x, y = player.rect.x + size, player.rect.y

        super().__init__(x, y, speed=0, width=size, height=size, image=image)

        self.timer = pygame.time.get_ticks()
        self.duration = 200
        self.damage = 10

    def move(self):
        pass

    def attack(self):
        pass

    def update(self):
        if pygame.time.get_ticks() - self.timer > self.duration:
            return False
        return True

class Pistol(Weapon):

    def __init__(self, player, bullet_image=None):
        bullet_size = 10 // 2
        self.direction = player.direction

        if self.direction == "up":
            x = player.rect.centerx - bullet_size // 2
            y = player.rect.y - bullet_size
            dx, dy = 0, -4
        elif self.direction == "down":
            x = player.rect.centerx - bullet_size // 2
            y = player.rect.bottom
            dx, dy = 0, 4
        elif self.direction == "left":
            x = player.rect.x - bullet_size
            y = player.rect.centery - bullet_size // 2
            dx, dy = -4, 0
        else:
            x = player.rect.right
            y = player.rect.centery - bullet_size // 2
            dx, dy = 4, 0

        scaled_bullet = None
        if bullet_image is not None:
            scaled_bullet = pygame.transform.scale(bullet_image, (bullet_size, bullet_size))

        super().__init__(x, y, speed=4, width=bullet_size, height=bullet_size, image=scaled_bullet)

        self.dx = dx
        self.dy = dy
        self.timer = pygame.time.get_ticks()
        self.duration = 1000
        self.damage = 15

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def update(self, walls,bushes,coins,rocks,switch_doors,key_doors):
        self.move()

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                return False

        for rock in rocks:
            if self.rect.colliderect(rock.rect):
                return False

        for bushes in bushes:
            if self.rect.colliderect(bushes.rect):
                return False


        for coins in coins:
            if self.rect.colliderect(coins.rect):
                return False

        for switch_doors in switch_doors:
            if self.rect.colliderect(switch_doors.rect):
                return False

        for key_doors in key_doors:
            if self.rect.colliderect(key_doors.rect):
                return False

        if pygame.time.get_ticks() - self.timer > self.duration:
            return False

        return True
