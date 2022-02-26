import pygame
import os
import sys
import random

pygame.init()
FPS = 60
FRAME = pygame.USEREVENT + 3
pygame.time.set_timer(FRAME, 1000 // FPS)
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ННП')

"""
. - трава
# - дерево
* - сундук(серебро)
& - сундук (золото)
@ - персонаж
% - вода
( - забор
"""


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Ground(pygame.sprite.Sprite):
    image = load_image('sprites/ground/grass.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(self.image, (800, 600))
        self.rect = pygame.Rect(0, 0, 800, 600)

    def draw(self, dest):
        dest.blit(self.image, self.rect)


class Pond(pygame.sprite.Sprite):
    images_mid = ['sprites/water/watermid1']
    images_top = ['sprites/water/watertop1']
    images_bot = ['sprites/water/waterbot1']
    images_left = ['sprites/water/waterleft1']
    images_right = ['sprites/water/waterright1']
    images_topleft = ['sprites/water/waterlefttop1']
    images_topright = ['sprites/water/waterrighttop1']
    images_botleft = ['sprites/water/waterleftbot1']
    images_botright = ['sprites/water/waterrightbot1']

    def __init__(self, group, lft, rght, tp, bt, x, y):
        self.image_lst = []
        self.curr_frame = 0
        super().__init__(group)
        if lft and rght and tp and bt:
            self.image_lst = self.images_mid
        elif bt and rght and not (lft or tp):
            self.image_lst = self.images_topleft
        elif lft and rght and bt and not tp:
            self.image_lst = self.images_top
        elif bt and lft and not (rght or tp):
            self.image_lst = self.images_topright
        elif tp and bt and rght and not lft:
            self.image_lst = self.images_left
        elif lft and tp and bt and not rght:
            self.image_lst = self.images_right
        elif tp and rght and not (lft or bt):
            self.image_lst = self.images_botleft
        elif tp and lft and rght and not bt:
            self.image_lst = self.images_bot
        else:
            self.image_lst = self.images_botright
        self.image = load_image(self.image_lst[int(self.curr_frame)] + '.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = pygame.Rect(x, y, 32, 32)
        self.hitbox = self.rect.copy()
        self.hitbox.x -= 16
        self.hitbox.width += 8
        self.hitbox.y -= 16
        self.hitbox.height -= 8
        self.play_anim()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def play_anim(self):
        self.image = load_image(self.image_lst[int(self.curr_frame)] + '.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.curr_frame += 0.1
        if self.curr_frame >= len(self.image_lst):
            self.curr_frame = 0


class Fence(pygame.sprite.Sprite):
    images = ['sprites/fences/fence1',
              'sprites/fences/fence2',
              'sprites/fences/fence3',
              'sprites/fences/fence4',
              'sprites/fences/fence5',
              'sprites/fences/fence6',
              'sprites/fences/fence7',
              'sprites/fences/fence8',
              'sprites/fences/fence9',
              'sprites/fences/fence10',
              'sprites/fences/fence11',
              'sprites/fences/fence12',
              'sprites/fences/fence13',
              'sprites/fences/fence14',
              'sprites/fences/fence15',
              'sprites/fences/fence16']

    def __init__(self, group, lft, rght, up, bt, x, y):
        super().__init__(group)
        if bt and not (lft or rght or up):
            self.image = load_image(self.images[0] + '.png')
        elif bt and rght and not up and not lft:
            self.image = load_image(self.images[1] + '.png')
        elif lft and rght and not up and bt:
            self.image = load_image(self.images[2] + '.png')
        elif lft and bt and not (up or rght):
            self.image = load_image(self.images[3] + '.png')
        elif up and bt and not (lft or rght):
            self.image = load_image(self.images[4] + '.png')
        elif up and bt and rght and not lft:
            self.image = load_image(self.images[5] + '.png')
        elif lft and rght and up and bt:
            self.image = load_image(self.images[6] + '.png')
        elif up and lft and bt and not rght:
            self.image = load_image(self.images[7] + '.png')
        elif up and not (lft or rght or bt):
            self.image = load_image(self.images[8] + '.png')
        elif up and rght and not (lft or bt):
            self.image = load_image(self.images[9] + '.png')
        elif lft and rght and up and not bt:
            self.image = load_image(self.images[10] + '.png')
        elif lft and up and not (bt or rght):
            self.image = load_image(self.images[11] + '.png')
        elif not (lft or rght or up or bt):
            self.image = load_image(self.images[12] + '.png')
        elif rght and not (up or bt or lft):
            self.image = load_image(self.images[13] + '.png')
        elif lft and rght and not (up or bt):
            self.image = load_image(self.images[14] + '.png')
        else:
            self.image = load_image(self.images[15] + '.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = pygame.Rect(x, y, 32, 32)
        self.hitbox = self.rect.copy()
        self.hitbox.x -= 8
        self.hitbox.height -= 24

    def draw(self, dest):
        dest.blit(self.image, self.rect)


class Path(Fence):
    images = ['sprites/paths/path1',
              'sprites/paths/path2',
              'sprites/paths/path3',
              'sprites/paths/path4',
              'sprites/paths/path5',
              'sprites/paths/path6',
              'sprites/paths/path7',
              'sprites/paths/path8',
              'sprites/paths/path9',
              'sprites/paths/path10',
              'sprites/paths/path11',
              'sprites/paths/path12',
              'sprites/paths/path13',
              'sprites/paths/path14',
              'sprites/paths/path15',
              'sprites/paths/path16']

    def __init__(self, group, lft, rght, up, bt, x, y):
        super().__init__(group, lft, rght, up, bt, x, y)

    def draw(self, dest):
        dest.blit(self.image, self.rect)


class Chest(pygame.sprite.Sprite):
    golden_image = load_image('sprites/chest_anim/golden_chest/chest1.png')
    silver_image = load_image('sprites/chest_anim/silver_chest/chest1.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.curr_frame = 0
        self.x = x
        self.y = y
        self.closed = True
        self.opening = False
        self.rank = 1
        self.silver_anim = [
            'sprites/chest_anim/silver_chest/chest1',
            'sprites/chest_anim/silver_chest/chest2',
            'sprites/chest_anim/silver_chest/chest3',
            'sprites/chest_anim/silver_chest/chest4'
        ]
        self.gold_anim = [
            'sprites/chest_anim/golden_chest/chest1',
            'sprites/chest_anim/golden_chest/chest2',
            'sprites/chest_anim/golden_chest/chest3',
            'sprites/chest_anim/golden_chest/chest4'
        ]
        self.image = self.golden_image if self.rank == 1 else self.silver_image
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = pygame.Rect(x, y, 32, 32)
        self.hitbox = self.rect.copy()
        self.hitbox.height = 1
        self.hitbox.x -= 10

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.opening:
            self.play_anim()

    def open(self):
        if self.closed:
            self.closed = False
            self.opening = True
            self.play_anim()

    def play_anim(self):
        if self.opening:
            if self.rank == 0:
                self.image = load_image(self.silver_anim[int(self.curr_frame)] + '.png')
            else:
                self.image = load_image(self.gold_anim[int(self.curr_frame)] + '.png')
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.curr_frame += 0.2
            if self.curr_frame >= 4:
                self.opening = False


class Block(pygame.sprite.Sprite):
    tree_img = pygame.transform.scale(load_image('sprites/trees/tree.png'), (96, 128))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.x = x
        self.y = y
        self.image = self.tree_img
        self.rect = pygame.Rect(x, y, 96, 128)
        self.hitbox = pygame.Rect(x + 16, y + 80, 45, 14)

    def draw(self, dest):
        dest.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, group, blocks, chests, x, y):
        super().__init__(group)
        self.rect = pygame.Rect(300, 300, 25, 25)
        self.blocks = blocks
        self.chests = chests
        self.is_idle = True
        self.is_running = False
        self.curr_frame = 0
        self.x = x
        self.y = y
        self.direction = 1
        self.running_anim = ['sprites/running_anim/moving1',
                             'sprites/running_anim/moving2',
                             'sprites/running_anim/moving3',
                             'sprites/running_anim/moving4',
                             'sprites/running_anim/moving5',
                             'sprites/running_anim/moving6']

        self.idle_anim = ['sprites/idle_anim/idle1',
                          'sprites/idle_anim/idle2',
                          'sprites/idle_anim/idle3',
                          'sprites/idle_anim/idle4',
                          'sprites/idle_anim/idle5',
                          'sprites/idle_anim/idle6']

    def draw(self, dest):
        dest.blit(self.image, self.rect)

    def update(self, lft, rght, tp, bt, shift, opening):
        xs, ys = 0, 0
        if lft:
            xs -= 2

        if rght:
            xs += 2

        if tp:
            ys -= 2

        if bt:
            ys += 2

        self.rect.x += xs * (2 if shift else 1)
        for block in blocks:
            if block.hitbox.colliderect(self.rect):
                self.rect.x -= xs * (2 if shift else 1)
                xs = 0

        self.rect.y += ys * (2 if shift else 1)
        for block in blocks:
            if block.hitbox.colliderect(self.rect):
                self.rect.y -= ys * (2 if shift else 1)
                ys = 0

        if xs < 0:
            self.direction = -1
        elif xs > 0:
            self.direction = 1

        if opening:
            self.check_rect = self.rect.copy()
            self.check_rect.x -= 5
            self.check_rect.y -= 5
            self.check_rect.width += 10
            self.check_rect.height += 10

            for chest in chests:
                if chest.hitbox.colliderect(self.check_rect):
                    chest.open()

        self.prev = [self.is_running, self.is_idle]

        if xs == ys == 0:
            self.is_idle = True
            self.is_running = False

        else:
            self.is_idle = False
            self.is_running = True
        self.play_anim()

    def play_anim(self):

        if self.is_idle:
            self.curr_frame = 0 if [self.is_running, self.is_idle] != self.prev else self.curr_frame
            self.image = pygame.transform.scale(load_image(self.idle_anim[int(self.curr_frame)] + '.png'), (48, 48))
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.curr_frame += 0.1
            if self.curr_frame >= len(self.idle_anim):
                self.curr_frame = 0

        if self.is_running:
            self.curr_frame = 0 if [self.is_running, self.is_idle] != self.prev else self.curr_frame
            self.image = pygame.transform.scale(load_image(self.running_anim[int(self.curr_frame)] + '.png'), (48, 48))
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.curr_frame += 0.1
            if self.curr_frame >= len(self.running_anim):
                self.curr_frame = 0


if __name__ == '__main__':
    blocks = []
    chests = []
    all_groups = []
    player = pygame.sprite.Group()
    ground = pygame.sprite.Group()
    entities = pygame.sprite.Group()
    g = Ground(ground)
    with open('data/town.txt', 'r', encoding='utf-8') as file:
        file = file.readlines()
        for i in range(len(file)):
            for j in range(len(file[i].rstrip('\n'))):
                if file[i][j] == '#':
                    tree = Block(entities, j * 32, i * 32)
                    blocks.append(tree)
                if file[i][j] == '*':
                    chest = Chest(entities, j * 32, i * 32)
                    blocks.append(chest)
                    chests.append(chest)
                if file[i][j] == '(':
                    up = down = left = right = False
                    if i > 0 and file[i - 1][j] == '(':
                        up = True
                    if i < len(file) - 1 and file[i + 1][j] == '(':
                        down = True
                    if j > 0 and file[i][j - 1] == '(':
                        left = True
                    if j < len(file[i]) and file[i][j + 1] == '(':
                        right = True
                    fence = Fence(entities, left, right, up, down, j * 32, i * 32)
                    blocks.append(fence)
                if file[i][j] == '%':
                    up = down = left = right = False
                    if i > 0 and file[i - 1][j] == '%':
                        up = True
                    if i < len(file) - 1 and file[i + 1][j] == '%':
                        down = True
                    if j > 0 and file[i][j - 1] == '%':
                        left = True
                    if j < len(file[i]) and file[i][j + 1] == '%':
                        right = True
                    pond = Pond(entities, left, right, up, down, j * 32, i * 32)
                    blocks.append(pond)
                if file[i][j] == '-':
                    up = down = left = right = False
                    if i > 0 and file[i - 1][j] == '-':
                        up = True
                    if i < len(file) - 1 and file[i + 1][j] == '-':
                        down = True
                    if j > 0 and file[i][j - 1] == '-':
                        left = True
                    if j < len(file[i]) and file[i][j + 1] == '-':
                        right = True
                    path = Path(ground, left, right, up, down, j * 32, i * 32)

    running = True
    a = Player(player, blocks, chests, 50, 70)
    all_groups.append(player)
    all_groups.append(entities)
    blocks.sort(key=lambda x: x.hitbox.bottom)
    while running:
        for event in pygame.event.get():
            if event.type == FRAME:
                order = []
                bot = right = left = top = accel = openn = False
                pressed_keys = pygame.key.get_pressed()
                ground.draw(screen)
                if pressed_keys[pygame.K_LEFT]:
                    left = True
                if pressed_keys[pygame.K_UP]:
                    top = True
                if pressed_keys[pygame.K_RIGHT]:
                    right = True
                if pressed_keys[pygame.K_DOWN]:
                    bot = True
                if pressed_keys[pygame.K_LSHIFT]:
                    accel = True
                if pressed_keys[pygame.K_RETURN]:
                    openn = True
                player.update(left, right, top, bot, accel, openn)
                for chest in chests:
                    chest.update()
                for block in blocks:
                    if block.hitbox.bottom <= a.rect.bottom:
                        order.append(block)
                    else:
                        order.append(a)
                        order.append(block)
                cnt = order.count(a)
                if cnt == 0:
                    order.append(a)
                elif cnt != 1:
                    new_lst = []
                    first = order.index(a)
                    for elem in order:
                        if elem == a and a in new_lst:
                            pass
                        else:
                            new_lst.append(elem)
                    order = new_lst
                for sprite in order:
                    sprite.draw(screen)
                pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
