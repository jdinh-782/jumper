# For Education Purposes Only
import pygame as p
import sys
import random


p.init()

width = 400
height = 600
screen = p.display.set_mode(size=(width, height))
p.display.set_caption("Jump")

background = p.image.load("background.png")
game_over_screen = p.image.load("game over.png")
game_over_screen = p.transform.scale(game_over_screen, (width, height))

# create an event for when to add another platform
ADD_PLATFORM_EVENT = p.USEREVENT + 1


class Platform(p.sprite.Sprite):
    def __init__(self, x, y):
        super(Platform, self).__init__()

        self._image = p.image.load("platform.png")
        self._image = p.transform.scale(self._image, (60, 15))
        self._rect = self._image.get_rect(topleft=(x, y))

        self._scored = False

    def get_rect(self):
        return self._rect

    def update(self):
        self._rect.y += 1

        if self._rect.y < -50:
            self.kill()
            return True
        return False

    def hit(self, temp):
        self._scored = temp

    def scored(self):
        return self._scored

    def draw(self, surface):
        surface.blit(self._image, self._rect)


class Doodler(p.sprite.Sprite):
    def __init__(self, doodler_x, doodler_y):
        super(Doodler, self).__init__()

        self._doodler = p.image.load("doodler.png")
        self._doodler = p.transform.scale(self._doodler, (65, 65))
        self._doodler_rect = self._doodler.get_rect()
        self._doodler_rect.x = 170
        self._doodler_rect.y = 500
        self._pos = (doodler_x, doodler_y)
        self._speed = [0, 5]

        self._top = 100
        self._bottom = height

        self._temp = 0

    def continuous_move(self):
        self._doodler_rect = self._doodler_rect.move(self._speed)

        # change doodler velocity when it goes up/down
        if self._doodler_rect.top < self._top or self._doodler_rect.bottom > self._bottom:
            self._speed[1] = -self._speed[1]

    # track key press for left/right movement
    def key_move(self):
        key = p.key.get_pressed()

        self._doodler_rect.x = min(max(1, self._doodler_rect.x), 665)

        if key[p.K_RIGHT]:
            self._doodler_rect.x += 3
        elif key[p.K_LEFT]:
            self._doodler_rect.x -= 3

        # check if doodler goes out of bounds
        if self._doodler_rect.x > width:
            self._doodler_rect.x = 0
        if self._doodler_rect.x < 0:
            self._doodler_rect.x = width

    def get_rect(self):
        return self._doodler_rect

    def change_position(self):
        self._speed[1] = -self._speed[1]

    def draw(self, surface):
        surface.blit(self._doodler, (self._doodler_rect.x, self._doodler_rect.y))


def add_platforms():
    x = random.randint(5, 300)
    # y = random.randint(5, 500)
    return Platform(x, 0)


platforms = list()
platforms.append(add_platforms())

score_label_font = p.font.Font('freesansbold.ttf', 20)
score_label_text = score_label_font.render('Score: ', True, (0, 0, 0))

score = 0
score_font = score_label_font

d = Doodler(170, 500)

# instantiate a time for when the ADD_PLATFORM_EVENT should occur
clock = p.time.Clock()
p.time.set_timer(ADD_PLATFORM_EVENT, 3000)

bounces = 0
game_over = False

while True:
    score_text = score_font.render(f" {score} ", True, (0, 0, 0))

    for event in p.event.get():
        if event.type == p.QUIT:
            sys.exit()
        elif event.type == ADD_PLATFORM_EVENT:
            platforms.append(add_platforms())

    screen.fill([0, 0, 0])
    screen.blit(background, background.get_rect())

    for platform in platforms:
        platform.update()
        platform.draw(screen)

        point = d.get_rect()
        collide = platform.get_rect().colliderect(point)

        # check if doodler collides with a platform
        if collide == 1:
            if platform.scored() is False:
                score += 1
                platform.hit(True)
            # print(score)
            d.change_position()

    d.continuous_move()
    d.key_move()
    d.draw(screen)

    # check when doodler goes below the screen (after a certain number of bounces)
    if d.get_rect().y == 525:
        bounces += 1
        if bounces >= 5:
            game_over = True

    if game_over is True:
        screen.blit(game_over_screen, game_over_screen.get_rect())

        # find a more sufficient way to end the game
        if d.get_rect().y <= 500:
            p.time.wait(3500)
            p.quit()
            sys.exit()

    screen.blit(score_label_text, (5, 15))
    screen.blit(score_text, (65, 15))

    p.display.flip()
    clock.tick(60)
