import pygame

TILE = 40


class Wall:
    def __init__(self, x, y, solid=True, color=(120,120,120)):
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self._solid = solid
        self._color = color

    def draw(self, screen, camera_x=0, camera_y=0):
        pygame.draw.rect(
            screen,
            self._color,
            (
                self.rect.x - camera_x,
                self.rect.y - camera_y,
                TILE,
                TILE
            )
        )

    def collide(self, obj):
        return self._solid and self.rect.colliderect(obj.rect)

    def on_player_touch(self, player):
        pass

# module-level sfx (set from main)
open_door_sound = None
take_key_sound = None
checkpoint_sound = None


class Bush(Wall):
    def __init__(self, x, y):
        super().__init__(x, y, solid=True, color=(30,160,30))

    def on_player_touch(self, player):
        pass


class Door(Wall):

    def __init__(self, x, y, door_id):
        super().__init__(x, y, solid=True, color=(139,69,19))

        self.door_id = door_id
        self._is_open = False

    def get_is_open(self):
        return self._is_open

    def open(self):
        # Only perform actions when transitioning from closed -> open
        if self._is_open:
            return
        self._is_open = True
        self._solid = False
        self._color = (200,170,120)
        # play open door sound if available (play once on transition)
        try:
            if open_door_sound:
                open_door_sound.play()
        except Exception:
            pass

    def close(self):
        self._is_open = False
        self._solid = True
        self._color = (139,69,19)

class KeyDoor(Door):

    def on_player_touch(self, player):

        if self.get_is_open():
            return

        if self.door_id in player.keys:

            player.keys.remove(self.door_id)

            self.open()

class SwitchDoor(Door):

    pass

class Switch:

    def __init__(self, x, y, door_id):
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.__active = False
        self.door_id = door_id
        self.door = None

    def get_active(self):
        return self.__active

    def update(self, rocks):

        active_now = False

        for rock in rocks:
            if self.rect.colliderect(rock.rect):
                active_now = True
                break

        self.__active = active_now

        if self.door:
            if self.__active:
                self.door.open()

    def draw(self, screen, camera_x=0, camera_y=0):

        color = (255, 255, 0)

        if self.__active:
            color = (255, 150, 0)

        pygame.draw.rect(
            screen,
            color,
            (
                self.rect.x - camera_x,
                self.rect.y - camera_y,
                TILE,
                TILE
            )
        )


class Exit(Wall):
    def __init__(self, x, y):
        super().__init__(x, y, solid=False, color=(0,200,0))
        self.active = True

    def on_player_touch(self, player):
        return True


class Checkpoint(Wall):
    def __init__(self, x, y):
        super().__init__(x, y, solid=False, color=(50,50,220))
        self.__active = False

    def get_active(self):
        return self.__active

    def activate(self, player):
        self.__active = True

        player.has_checkpoint = True
        player.spawn_x = self.rect.x
        player.spawn_y = self.rect.y
        # play checkpoint sound if available
        try:
            if checkpoint_sound:
                checkpoint_sound.play()
        except Exception:
            pass

    def on_player_touch(self, player):
        if not self.__active:
            self.activate(player)

class Treasure(Wall):
    def __init__(self,x,y,key_id, hint=None):
        super().__init__(x,y,solid=False,color=(70,20,60))
        self.__opened = False
        self.key_id = key_id
        # hint shown to player when touching this treasure
        self.hint = hint if hint is not None else f"Key for door {key_id}"

    def get_opened(self):
        return self.__opened

    def open(self):
        self.__opened = True
        self._color = (200, 170, 120)

    def on_player_touch(self, player):

        if not self.__opened:
            self.open()
            player.keys.append(self.key_id)
            print(player.keys)
            # play take-key sound if available
            try:
                if take_key_sound:
                    take_key_sound.play()
            except Exception:
                pass


