import pygame
import os
import sys
import random
import time
import sqlite3


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


class Dust(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.dust_anim = ['sprites/dust/dust1.png',
                          'sprites/dust/dust2.png',
                          'sprites/dust/dust3.png']
        self.rect = pygame.Rect(x, y, 12, 12)
        self.curr_frame = 0
        self.play_anim()

    def play_anim(self):
        self.image = pygame.transform.scale(load_image(self.dust_anim[int(self.curr_frame)]), (48, 48))
        self.curr_frame += 0.1
        if self.curr_frame >= 3:
            self.kill()

    def draw(self, dest, camera):
        dest.blit(self.image, camera.move(self.rect))


class Item(pygame.sprite.Sprite):
    helmet_sprites = [load_image(f"sprites/helmets/Item__{i}.png") for i in range(44, 48)]
    acces_sprites = [load_image(f"sprites/accessories/Item__{i}.png") for i in range(40, 44)]
    weapons_sprites = [load_image(f"sprites/weapons/common/Item__{str(i).rjust(2, '0')}.png") for i in range(16)]
    weapons_rare_sprites = [load_image(f"sprites/weapons/rare/Item{i}.png") for i in range(1, 13)]
    armor_sprites = [load_image(f"sprites/armor/Item__{i}.png") for i in range(56, 60)]
    shield_sprites = [load_image(f"sprites/shields/Item__{i}.png") for i in range(24, 28)]

    def __init__(self, group, type, rarity, lvl):
        super().__init__(group)
        self.type = type
        self.level = lvl
        self.rank = rarity
        self.rank_int = ['common', 'uncommon', 'rare', 'epic', 'legendary'].index(self.rank) + 1
        if self.type == 'weap':

            self.dmg_avg = 10 + self.level * self.rank_int ** 1.5
            self.end_dmg = random.randint((self.dmg_avg * 0.85) // 1, (self.dmg_avg * 1.15) // 1)
            self.random_stat = 0

            if self.rank in ['epic', 'legendary']:
                self.image = random.choice(self.weapons_rare_sprites)
                self.image = pygame.transform.scale(self.image, (40, 40))
                self.random_stat = self.level * self.rank_int // 4
                self.stat_type = random.choice(['Strength', 'Agility'])
            else:
                self.image = random.choice(self.weapons_sprites)
                self.image = pygame.transform.scale(self.image, (40, 40))

        elif self.type == 'accs':
            self.image = random.choice(self.acces_sprites)
            self.image = pygame.transform.scale(self.image, (40, 40))

        elif self.type == 'helm':
            self.image = random.choice(self.helmet_sprites)
            self.image = pygame.transform.scale(self.image, (40, 40))

        elif self.type == 'shld':
            self.image = random.choice(self.shield_sprites)
            self.image = pygame.transform.scale(self.image, (40, 40))

        elif self.type == 'armr':
            self.image = random.choice(self.armor_sprites)
            self.image = pygame.transform.scale(self.image, (40, 40))

        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = pygame.Rect(440, 145, 48, 48)  # X: + 51, Y: + 54

    def draw(self, dest, row, col):
        r_t_d = self.rect.copy()
        r_t_d.x += col * 51
        r_t_d.y += row * 54
        dest.blit(self.image, r_t_d)

    def get_desc(self):
        if self.type == 'weap':
            info_lst = [f"Damage: {self.end_dmg}"]
            if self.random_stat != 0:
                info_lst.append(f"{self.stat_type}: {self.random_stat}")
        elif self.type == 'armr':
            info_lst = [f"asdasdas"]
        elif self.type == 'accs':
            info_lst = [f"негры"]
        elif self.type == 'shld':
            info_lst = [f"zxczxc"]
        elif self.type == 'helm':
            info_lst = [f"zxczxc13123"]
        return info_lst


class Camera:
    def __init__(self, player):
        self.max_height = 1600
        self.max_width = 1600
        self.rect = pygame.Rect(0, 0, 1600, 1600)
        self.player = player

    def move(self, obj):
        if isinstance(obj, pygame.Rect):
            return obj.move(self.rect.topleft)
        return obj.rect.move(self.rect.topleft)

    def update(self):
        left, top, _, _ = self.player.rect
        _, _, w, h = self.rect
        left, top = -left + WIDTH / 2, -top + HEIGHT / 2

        left = min(0, left)
        left = max(-(self.rect.width - WIDTH), left)
        top = max(-(self.rect.height - HEIGHT), top)
        top = min(0, top)

        self.rect = pygame.Rect(left, top, w, h)


class Ground(pygame.sprite.Sprite):
    image = load_image('sprites/ground/grass.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(self.image, (1600, 1600))
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
        self.animate()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def animate(self):
        self.image = load_image(self.image_lst[int(self.curr_frame)] + '.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.curr_frame += 0.1
        if self.curr_frame >= len(self.image_lst):
            self.curr_frame = 0


class Fence(pygame.sprite.Sprite):
    images = [f'sprites/fences/fence{i}' for i in range(1, 17)]

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
    images = [f'sprites/paths/path{i}' for i in range(1, 17)]

    def __init__(self, group, lft, rght, tp, bt, x, y):
        super().__init__(group, lft, rght, tp, bt, x, y)

    def draw(self, dest):
        dest.blit(self.image, self.rect)


class Chest(pygame.sprite.Sprite):
    golden_image = load_image('sprites/chest_anim/golden_chest/chest1.png')
    silver_image = load_image('sprites/chest_anim/silver_chest/chest1.png')

    def __init__(self, group, x, y, rank):
        super().__init__(group)
        self.curr_frame = 0
        self.x = x
        self.y = y
        self.closed = True
        self.opening = False
        self.rank = rank
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
            self.animate()

    def open(self):
        if self.closed:
            self.closed = False
            self.opening = True
            self.animate()

    def animate(self):
        if self.opening:
            if self.rank == 0:
                self.image = load_image(self.silver_anim[int(self.curr_frame)] + '.png')
            else:
                self.image = load_image(self.gold_anim[int(self.curr_frame)] + '.png')
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.curr_frame += 0.2
            if self.curr_frame >= 4:
                self.opening = False


class StatusBar(pygame.sprite.Sprite):
    def __init__(self, group, pl):
        super().__init__(group)
        self.player = pl
        self.max_hp = self.player.max_hp
        self.max_mana = self.player.max_mana
        self.curr_mana = self.player.curr_mana
        self.curr_hp = self.player.curr_hp
        self.hp_border = pygame.transform.scale(load_image('sprites/bars/hp_border.png'), (200, 16))
        self.mana_border = pygame.transform.scale(load_image('sprites/bars/mana_border.png'), (200, 16))
        self.hp_bar = pygame.transform.scale(load_image('sprites/bars/hp_bar.png'), (200, 12))
        self.mana_bar = pygame.transform.scale(load_image('sprites/bars/mana_bar.png'), (200, 12))
        self.hp_border_rect = pygame.Rect(50, 10, 300, 24)
        self.hp_bar_rect = self.hp_border_rect.copy()
        self.hp_bar_rect.y += 2
        self.mana_border_rect = pygame.Rect(50, 33, 300, 24)
        self.mana_bar_rect = self.mana_border_rect.copy()
        self.mana_bar_rect.y += 2

    def update(self):
        self.max_hp = self.player.max_hp
        self.max_mana = self.player.max_mana
        self.curr_mana = self.player.curr_mana
        self.curr_hp = self.player.curr_hp
        self.curr_mana = min(self.curr_mana, self.max_mana)
        self.curr_hp = min(self.curr_hp, self.max_hp)
        percent_hp = (self.curr_hp / self.max_hp * 100) // 1
        percent_mana = (self.curr_hp / self.max_hp * 100) // 1
        self.hp_bar = pygame.transform.scale(self.hp_bar, (percent_hp * 2, 12))
        self.mana_bar = pygame.transform.scale(self.mana_bar, (percent_mana * 2, 12))

    def draw(self, dest):
        dest.blit(self.hp_bar, self.hp_bar_rect)
        dest.blit(self.hp_border, self.hp_border_rect)
        dest.blit(self.mana_bar, self.mana_bar_rect)
        dest.blit(self.mana_border, self.mana_border_rect)


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
    def __init__(self, group, gr, blocks, chests, x, y, level=1):
        super().__init__(group)
        self.col = self.row = 0
        self.font = pygame.font.Font('font/m6x11.ttf', 20)
        self.level = level
        self.ground = gr
        self.inventory = pygame.sprite.Group()
        self.inv_lst = []
        self.prev_dust = time.time()
        self.weapon = self.armor = self.accessory = self.shield = self.helmet = None
        self.weap_r = pygame.Rect(440, 480 ,31 ,31)
        self.armr_r = pygame.Rect(542, 480, 31, 31)
        self.accs_r = pygame.Rect(644, 480, 31, 31)
        self.shld_r = pygame.Rect(491, 480, 31, 31)
        self.helm_r = pygame.Rect(593, 480, 31, 31)
        itm = Item(self.inventory, 'weap', 'common', 10)
        itm2 = Item(self.inventory, 'armr', 'legendary', 10)
        self.inv_lst.append(itm)
        self.inv_lst.append(itm2)
        self.rect = pygame.Rect(300, 300, 25, 25)
        self.prev_y_change = time.time()
        self.prev_x_change = time.time()
        self.selection_line = load_image('sprites/outline/outline.png', colorkey=(255, 255, 255))
        self.selection_line = pygame.transform.scale(self.selection_line, (48, 48))
        self.sel_rect = pygame.Rect(435, 142, 70, 70)
        self.curr_hp = 100
        self.prev_enter_press = time.time()
        self.curr_mana = 100
        self.prev_esc_press = time.time()
        self.max_hp = 100
        self.curr_choice = 0
        self.two_choices = False
        self.max_mana = 100
        self.blocks = blocks
        self.chests = chests
        self.is_idle = True
        self.is_running = False
        self.is_sprinting = False
        self.inventory_opened = False
        self.inventory_image = load_image('sprites/inv/inventory.png', colorkey= (255, 255, 255))
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

    def draw(self, dest, camera):
        dest.blit(self.image, camera.move(self.rect))
        if self.inventory_opened:
            self.inventory_rect.right = min(camera.move(self.inventory_rect).right, 1600)
            dest.blit(self.inventory_image, self.inventory_rect)


    def update(self, lft, rght, tp, bt, shift, opening, inv, c_i):
        if not self.inventory_opened:

            self.prev = [self.is_running, self.is_idle]

            if inv:
                self.open_inventory()
                self.inventory_opened = True
                self.col = self.row = 0
                return

            self.is_sprinting = False
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

            if self.rect.bottom > 1600:
                self.rect.bottom = 1600
                ys = 0
            elif self.rect.top < 0:
                self.rect.top = 0
                ys = 0
            if self.rect.left < 0:
                self.rect.left = 0
                xs = 0
            elif self.rect.right > 1600:
                self.rect.right = 1600
                xs = 0

            if shift:
                self.is_sprinting = True

            if xs == ys == 0:
                self.is_idle = True
                self.is_running = False

            else:
                self.is_idle = False
                self.is_running = True

            if opening:
                self.check_rect = self.rect.copy()
                self.check_rect.x -= 5
                self.check_rect.y -= 5
                self.check_rect.width += 10
                self.check_rect.height += 10

                for chest in chests:
                    if chest.hitbox.colliderect(self.check_rect):
                        chest.open()
        else:
            if c_i and time.time() - self.prev_esc_press > 0.3:
                if self.two_choices:
                    self.two_choices = False
                    self.selection_line = load_image('sprites/outline/outline.png', colorkey=(255, 255, 255))
                    self.selection_line = pygame.transform.scale(self.selection_line, (48, 48))
                    self.row = self.col = 0
                else:
                    self.inventory_opened = False
                    self.close_inventory()
                self.prev_esc_press = time.time()

            xs = ys = 0
            if tp:
                if self.two_choices:
                    if time.time() - self.prev_y_change >= 0.3:
                        self.row = max(self.row - 1, 0)
                        self.prev_y_change = time.time()
                elif time.time() - self.prev_y_change > 0.3:
                    self.row = max(self.row - 1, 0)
                    self.prev_y_change = time.time()
                    if len(self.inv_lst) - 1 >= self.col + self.row * 5:
                        self.curr_item_info = self.inv_lst[self.col + self.row * 5].get_desc()
                    else:
                        self.curr_item_info = []

            if bt:
                if self.two_choices:
                    if time.time() - self.prev_y_change >= 0.3:
                        self.row = min(self.row + 1, 1)
                        self.prev_y_change = time.time()
                elif time.time() - self.prev_y_change > 0.3:
                    self.row = min(self.row + 1, 2)
                    self.prev_y_change = time.time()
                    if len(self.inv_lst) - 1 >= self.col + self.row * 5:
                        self.curr_item_info = self.inv_lst[self.col + self.row * 5].get_desc()
                    else:
                        self.curr_item_info = []

            if lft:
                if self.two_choices:
                    pass
                else:
                    if time.time() - self.prev_x_change > 0.3:
                        self.col = max(self.col - 1, 0)
                        self.prev_x_change = time.time()
                        if len(self.inv_lst) - 1 >= self.col + self.row * 5:
                            self.curr_item_info = self.inv_lst[self.col + self.row * 5].get_desc()
                        else:
                            self.curr_item_info = []


            if rght:
                if self.two_choices:
                    pass
                else:
                    if time.time() - self.prev_x_change > 0.3:
                        self.col = min(self.col + 1, 4)
                        self.prev_x_change = time.time()
                        if len(self.inv_lst) - 1 >= self.col + self.row * 5:
                            self.curr_item_info = self.inv_lst[self.col + self.row * 5].get_desc()
                        else:
                            self.curr_item_info = []

            if opening:
                if self.two_choices:
                    if time.time() - self.prev_enter_press >= 0.3:
                        if self.row == 1:
                            self.inv_lst.remove(self.inv_lst[self.sel_r * 5 + self.sel_c])
                            self.two_choices = False
                            self.selection_line = load_image('sprites/outline/outline.png', colorkey=(255, 255, 255))
                            self.selection_line = pygame.transform.scale(self.selection_line, (48, 48))
                            self.row = self.col = 0
                            if len(self.inv_lst):
                                self.curr_item_info = self.inv_lst[0].get_desc()
                            else:
                                self.curr_item_info = []

                        elif self.row == 0:
                            tmp = self.inv_lst[self.sel_r * 5 + self.sel_c]
                            if tmp.type == 'weap':
                                if self.weapon is None:
                                    self.weapon = tmp
                                    self.inv_lst.remove(tmp)
                                else:
                                    mem = self.weapon
                                    self.weapon = tmp
                                    self.inv_lst[self.sel_r * 5 + self.sel_c] = mem
                            elif tmp.type == 'accs':
                                if self.accessory is None:
                                    self.accessory = tmp
                                    self.inv_lst.remove(tmp)
                                else:
                                    mem = self.accessory
                                    self.accessory = tmp
                                    self.inv_lst[self.sel_r * 5 + self.sel_c] = mem
                            elif tmp.type == 'armr':
                                if self.armor is None:
                                    self.armor = tmp
                                    self.inv_lst.remove(tmp)
                                else:
                                    mem = self.armor
                                    self.armor = tmp
                                    self.inv_lst[self.sel_r * 5 + self.sel_c] = mem
                            elif tmp.type == 'helm':
                                if self.helmet is None:
                                    self.helmet = tmp
                                    self.inv_lst.remove(tmp)
                                else:
                                    mem = self.helmet
                                    self.helmet = tmp
                                    self.inv_lst[self.sel_r * 5 + self.sel_c] = mem
                            elif tmp.type == 'shld':
                                if self.shield is None:
                                    self.shield = tmp
                                    self.inv_lst.remove(tmp)
                                else:
                                    mem = self.shield
                                    self.shield = tmp
                                    self.inv_lst[self.sel_r * 5 + self.sel_c] = mem
                            self.two_choices = False
                            self.selection_line = load_image('sprites/outline/outline.png', colorkey=(255, 255, 255))
                            self.selection_line = pygame.transform.scale(self.selection_line, (48, 48))
                            self.row = self.col = 0
                            if len(self.inv_lst):
                                self.curr_item_info = self.inv_lst[0].get_desc()
                            else:
                                self.curr_item_info = []

                        self.prev_enter_press = time.time() + 0.2
                elif time.time() - self.prev_enter_press > 0.3 and len(self.inv_lst) - 1 >= self.col + self.row * 5:
                    self.selection_line = load_image('sprites/outline/bot_outline.png', colorkey=(255, 255, 255))
                    self.selection_line = pygame.transform.scale(self.selection_line, (70, 35))
                    self.two_choices = True
                    self.prev_enter_press = time.time()
                    self.sel_r = self.row
                    self.sel_c = self.col
                    self.row = 0
                    self.col = 0

            self.text_rect = pygame.Rect(400, 400, 400, 400)

            if self.two_choices:
                self.sel_rect = pygame.Rect(622, 335 + 34 * self.row, 70, 70)
            else:
                self.sel_rect = pygame.Rect(435 + 51 * self.col, 142 + 54 * self.row, 70, 70)
            self.is_sprinting = False
            self.prev = [self.is_running, self.is_idle]

            if xs == ys == 0:
                self.is_idle = True
                self.is_running = False

            else:
                self.is_idle = False
                self.is_running = True
        if self.is_sprinting and self.is_running:
            if time.time() - self.prev_dust > 0.15:
                x_of_rect = self.rect.left - 8 if self.direction == 1 else self.rect.right - 8
                dust = Dust(self.ground, x_of_rect, a.rect.bottom - 12)
                self.prev_dust = time.time()

        self.play_anim()

    def play_anim(self):
        self.curr_frame = 0 if [self.is_running, self.is_idle] != self.prev else self.curr_frame

        if self.is_idle:
            self.image = pygame.transform.scale(load_image(self.idle_anim[int(self.curr_frame)] + '.png'), (48, 48))
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.curr_frame += 0.1
            if self.curr_frame >= len(self.idle_anim):
                self.curr_frame = 0

        if self.is_running:
            self.image = pygame.transform.scale(load_image(self.running_anim[int(self.curr_frame)] + '.png'), (48, 48))
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.curr_frame += 0.1 * (1.5 if self.is_sprinting else 1)
            if self.curr_frame >= len(self.running_anim):
                self.curr_frame = 0

    def open_inventory(self):
        self.two_choices = False
        self.inventory_rect = pygame.Rect(400, 0, 312, 500)
        self.inventory_image = pygame.transform.scale(self.inventory_image, (330, 550))
        if len(self.inv_lst):
            self.curr_item_info = self.inv_lst[0].get_desc()

    def close_inventory(self):
        self.inventory_rect = None
        self.inventory_opened = False

    def draw_desc(self, dest):
        if self.curr_item_info:
            text_coord = 320
            for line in self.curr_item_info:
                string_rendered = self.font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 440
                text_coord += intro_rect.height
                dest.blit(string_rendered, intro_rect)


class GroundDecor(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 16, 16)
        self.img = [f'sprites/ground_decor/decor{i}.png' for i in range(1, 17)]
        self.image = load_image(random.choice(self.img))
        self.image = pygame.transform.scale(self.image, (32, 32))

    def draw(self, dest):
        dest.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, x, y, name):
        super(Enemy, self).__init__(group)
        self.rect = pygame.Rect(x, y, 72, 72)
        self.hitbox = self.rect.copy()
        self.hitbox.y += 48
        self.hitbox.x += 16
        self.hitbox.height -= 48
        self.hitbox.width -= 16
        self.curr_frame = 0
        if name == 'skeleton':
            self.frames = [load_image(f"sprites/skeleton/skeleton{i}.png") for i in range(1, 7)]
            self.image = self.frames[self.curr_frame]
        self.image = pygame.transform.scale(self.image, (96, 96))

    def animate(self):
        self.image = self.frames[int(self.curr_frame)]
        self.curr_frame += 0.1
        if self.curr_frame >= len(self.frames):
            self.curr_frame = 0
        self.image = pygame.transform.scale(self.image, (96, 96))

    def draw(self, dest):
        dest.blit(self.image, self.rect)


if __name__ == '__main__':
    blocks = []
    chests = []
    all_groups = []
    is_intro = True
    player = pygame.sprite.Group()
    ground = pygame.sprite.Group()
    entities = pygame.sprite.Group()
    g = Ground(ground)
    with open('data/plain.txt', 'r', encoding='utf-8') as file:
        file = file.readlines()
        for i in range(len(file)):
            for j in range(len(file[i].rstrip('\n'))):
                if file[i][j] == '#':
                    tree = Block(entities, j * 32, i * 32)
                    blocks.append(tree)
                elif file[i][j] == '*':
                    chest = Chest(entities, j * 32, i * 32, 0)
                    blocks.append(chest)
                    chests.append(chest)
                elif file[i][j] == '&':
                    chest = Chest(entities, j * 32, i * 32, 1)
                    blocks.append(chest)
                    chests.append(chest)
                elif file[i][j] == '(':
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
                elif file[i][j] == '%':
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
                elif file[i][j] == '-':
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
                elif file[i][j] == '.':
                    if random.randint(1, 100) < 16:
                        decor = GroundDecor(ground, j * 32, i * 32)
                elif file[i][j] == '$':
                    skelet = Enemy(entities, j * 32, i * 32, 'skeleton')
                    blocks.append(skelet)

    running = True
    a = Player(player, ground, blocks, chests, 50, 70)
    c = Camera(a)
    gui = pygame.sprite.Group()
    hpbar = StatusBar(gui, a)
    all_groups.append(player)
    all_groups.append(entities)
    blocks.sort(key=lambda x: x.hitbox.bottom)
    while running:
        for event in pygame.event.get():
            if event.type == FRAME:
                order = []
                bot = right = left = top = accel = openn = inventory = close_inv = False
                pressed_keys = pygame.key.get_pressed()
                for sprite in ground:
                    if isinstance(sprite, Dust):
                        sprite.play_anim()
                        sprite.draw(screen, c)
                    else:
                        screen.blit(sprite.image, c.move(sprite))
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
                if pressed_keys[pygame.K_i]:
                    inventory = True
                if pressed_keys[pygame.K_ESCAPE]:
                    close_inv = True
                player.update(left, right, top, bot, accel, openn, inventory, close_inv)
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
                for sprite in ground:
                    screen.blit(sprite.image, c.move(sprite))
                for sprite in order:
                    screen.blit(sprite.image, c.move(sprite))
                c.update()
                for sprite in entities:
                    try:
                        sprite.animate()
                    except:
                        pass
                for sprite in gui:
                    sprite.update()
                    sprite.draw(screen)
                if a.inventory_opened:
                    screen.blit(a.inventory_image, a.inventory_rect)
                    for num, item in enumerate(a.inv_lst):
                        item.draw(screen, num // 5, num % 5)
                    screen.blit(a.selection_line, a.sel_rect)
                    if a.weapon is not None:
                        screen.blit(a.weapon.image, a.weap_r)
                    if a.shield is not None:
                        screen.blit(a.shield.image, a.shld_r)
                    if a.accessory is not None:
                        screen.blit(a.accessory.image, a.accs_r)
                    if a.armor is not None:
                        screen.blit(a.armor.image, a.armr_r)
                    if a.helmet is not None:
                        screen.blit(a.helmet.image, a.helm_r)
                    a.draw_desc(screen)
                pygame.display.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
