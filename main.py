import os
import sys
from random import choice

import pygame
from pygame import Surface
from pygame.locals import *
from pygame.sprite import Sprite

from settings import *

pygame.mixer.pre_init()
pygame.init()
channel = pygame.mixer.find_channel(True)
channel.set_volume(100.0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
test_player = Surface((50, 100))
test_player.fill(GREEN)
player_sprite = pygame.image.load('resources/sprites/hero.png').convert_alpha()
sounds = [pygame.mixer.Sound('resources/music/' + file) for file in os.listdir('resources/music')]
ZOOM = 3


class Knife(Sprite):
    def __init__(self, player, x, y, ang=0, vx=500, vy=100, vang=3):
        super(Knife, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load('resources/sprites/knife.png').convert_alpha(), (20, 50))
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.player = player
        self.ang = ang
        self.vang = vang
        self.vy = vy
        self.vx = vx

    def step(self, dt):
        x, y = self.rect.bottomleft
        x += self.vx * dt
        y += self.vy * dt
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.vy += g * dt
        self.ang += self.vang * dt
        if not self.rect.colliderect(screen.get_rect()):
            self.player.kill_bullet()
            return False
        return True

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class Player(Sprite):
    def __init__(self, sprite, x, y, rect=None):
        super(Player, self).__init__()
        self.image = sprite
        self.rect = rect if rect is not None else self.image.get_rect(topleft=(x, y))
        self.speed = 300
        self.bullet = None

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def move_h(self, dt):
        self.move(dt * self.speed, 0)

    def move_v(self, dt):
        self.move(0, dt * self.speed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def kill_bullet(self):
        self.bullet = None

    def shoot(self):
        if self.bullet is None:
            self.bullet = Knife(self, *self.rect.topright)
            return self.bullet
        return None


class App:
    def __init__(self):
        self.FPS = 10000
        self.screen = screen
        self.bg = pygame.image.load('resources/pictures/bg.jpg').convert()
        self.clock = pygame.time.Clock()
        self.player = Player(pygame.transform.scale(player_sprite, (100, 170)), 100, 600)
        self.controller = PlayerController(self, self.player)
        self.objects = []

    def draw(self):
        # self.screen.blit(pygame.transform.scale(self.bg, (WIDTH, HEIGHT)), (0, 0))
        self.screen.fill((255, 255, 255))
        self.player.draw(self.screen)
        for obj in self.objects:
            obj.draw(self.screen)

    def run(self):
        while True:
            self.screen.fill(BLACK)
            self.controller.keydownhandler(pygame.key.get_pressed(), self.clock.get_time() / 1000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.controller.clickhandler(event.pos, event.button)

            for number, object in enumerate(self.objects):
                if object is None:
                    self.objects.pop(number)
                    continue
                if not object.step(self.clock.get_time() / 1000):
                    self.objects.pop(number)
            pygame.display.set_caption(str(self.clock.get_fps()))
            self.draw()
            pygame.display.update()
            self.clock.tick(self.FPS)


class PlayerController:
    def __init__(self, app: App, player: Player, l_key=K_LEFT, r_key=K_RIGHT, up_key=K_UP, down_key=K_DOWN):
        self.app = app
        self.down_key = down_key
        self.up_key = up_key
        self.r_key = r_key
        self.l_key = l_key
        self.player = player

    def keydownhandler(self, pressed, delta_t):
        if pressed[self.l_key]:
            self.player.move_h(-delta_t)
        if pressed[self.r_key]:
            self.player.move_h(delta_t)
        if pressed[self.down_key]:
            self.player.move_v(delta_t)
        if pressed[self.up_key]:
            self.player.move_v(-delta_t)
        if pressed[K_SPACE]:
            self.app.objects.append(self.player.shoot())

    def clickhandler(self, pos, button):
        if self.player.rect.collidepoint(*pos):
            print("YEEE")
            channel.play(choice(sounds))
            return True

        return False


print(sys.platform)
app = App()
app.run()
