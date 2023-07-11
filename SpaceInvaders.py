import pygame
from pygame.locals import *
import random
import json
import pygame_gui as pg_gui

pygame.init()
pygame.font.init()
pygame.mixer.init()

#  [DEFINITION][REGION]~~(START)~~>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#--------@{CONSTANTS}
WINDOW_ICON=pygame.image.load('.\\src\\window\\window_icon_001.png')
WINDOW_NAME="[S P A C E - I N V A D E R S]"
TEXT_FONT=pygame.font.Font('freesansbold.ttf', 32)
SCORE_BOARD_FONT=pygame.font.Font('freesansbold.ttf', 24)
ADD_SCORE_FONT= pygame.font.Font('freesansbold.ttf', 18)
GAME_OVER_FONT= pygame.font.Font('freesansbold.ttf', 64)
FRAME_RATE=90
PLAYER_HP = 5
ENEMY_SPAWN_INTERVAL = 2000
LOSE_HP_EVENT = USEREVENT + 1
ADD_SCORE_EVENT = USEREVENT + 2
ENEMY_SPAWN_EVENT = USEREVENT + 3
PLAYER_DEFAULT_NAME="UNKNOWN"

#--------@{META-CLASSES}
class RGB_Color():
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    blue = (0,0,255)
    green = (0,255,0)

class Scene():
    scenes=["start_window","game_window","game_over_scene"]
    current=0

    @staticmethod
    def init():
        Scene.current = 0
        pygame.mixer.music.load('.\\src\\background\\music\\8bit_menu.mp3')
        pygame.mixer.music.play(-1)

    @staticmethod
    def get_scene(id=None):
        if id == None:
            id = Scene.current

        return Scene.scenes[id]

    @staticmethod
    def go_to_next():
        if Scene.current == int(len(Scene.scenes) - 1):
            Scene.current = 0
        else:
            Scene.current += 1

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        if Scene.current == 0:
            #game_window.player_name_input_box.show()
            game_window.player_name_input_box.visible = 1
            #game_window.player_name_input_box
            pygame.mixer.music.load('.\\src\\background\\music\\8bit_menu.mp3')
            pygame.mixer.music.play(-1)

        elif Scene.current == 1:
            #game_window.player_name_input_box.hide()
            game_window.player_name_input_box.visible = 0
            pygame.mixer.music.load('.\\src\\background\\music\\faster_tempo_arcade_kid.mp3')
            pygame.mixer.music.play(-1)
        elif Scene.current == 2:
            pygame.mixer.music.load('.\\src\\background\\music\\slow_8bit_nostalgia.mp3')
            pygame.mixer.music.play(-1)
    
class game_window():
    screen=None
    width=None
    height=None
    clock=pygame.time.Clock()
    game_background_img = None
    game_background = None
    highscore_data=None
    ui_manager=None
    player_name_input_box=None

    @staticmethod
    def init():
        game_window.screen = pygame.display.set_mode((0,0), FULLSCREEN)
        game_window.width, game_window.height = pygame.display.get_surface().get_size()
        pygame.display.set_icon(WINDOW_ICON)
        pygame.display.set_caption(WINDOW_NAME)
        game_window.ui_manager = pg_gui.UIManager((game_window.width,game_window.height))
        game_window.game_background_img = pygame.image.load('.\\src\\background\\background.jpg').convert()
        game_window.game_background = pygame.transform.scale(game_window.game_background_img, (game_window.width, game_window.height))
        game_window.player_name_input_box = pg_gui.elements.UITextEntryLine(relative_rect=Rect(((game_window.width / 2) - 100), (game_window.height - ((game_window.height / 2) / 2) - 20), 200, 50), manager=game_window.ui_manager)
        game_window.player_name_input_box.set_text(str(game_manager.player_name))
        #game_window.player_name_input_box
        game_window.load_scene()

    @staticmethod
    def update():
        game_clock_tick = game_window.clock.tick(FRAME_RATE)
        game_window.ui_manager.update(game_clock_tick/1000.0)
        game_window.ui_manager.draw_ui(game_window.screen)
        pygame.display.update()
        pygame.display.flip()

    @staticmethod
    def close():
        pygame.quit()

    @staticmethod
    def load_scene():
        if Scene.current == 0:
            header_img = pygame.image.load('.\\src\\background\\start_screen.png').convert_alpha()
            game_window.player_name_input_box.visible = 1


            with open('.\\src\\data\\highscore.json') as json_file:
                game_window.highscore_data = json.load(json_file)

            highscore_text01 = TEXT_FONT.render(f"[HIGHSCORE]", True, RGB_Color.white,RGB_Color.black)
            highscore_text04 = TEXT_FONT.render(f" ", True, RGB_Color.white,RGB_Color.black)
            highscore_text05 = TEXT_FONT.render(f"PLAYER:  {game_window.highscore_data['player']}", True, RGB_Color.white,RGB_Color.black)
            highscore_text02 = TEXT_FONT.render(f" LEVEL:   {game_window.highscore_data['level']}", True, RGB_Color.white,RGB_Color.black)
            highscore_text03 = TEXT_FONT.render(f" SCORE:   {game_window.highscore_data['score']}", True, RGB_Color.white,RGB_Color.black)

            body_text = TEXT_FONT.render("Press {ENTER} to start...     OR     {ESC} to quit...", True, RGB_Color.white,RGB_Color.black)

            header_rect = header_img.get_rect()
            header_rect.center = ((game_window.width / 2),((header_img.get_height() / 2) + 10))

            highscore_rect01 = highscore_text01.get_rect()
            highscore_rect01.center = ((game_window.width / 2), 0)
            highscore_rect01.top = (header_rect.bottom + 50)

            highscore_rect04 = highscore_text04.get_rect()
            highscore_rect04.center = ((game_window.width / 2), 0)
            highscore_rect04.top = highscore_rect01.bottom

            highscore_rect05 = highscore_text05.get_rect()
            highscore_rect05.center = ((game_window.width / 2), 0)
            highscore_rect05.top = highscore_rect04.bottom

            highscore_rect02 = highscore_text02.get_rect()
            highscore_rect02.center = ((game_window.width / 2), 0)
            highscore_rect02.top = highscore_rect05.bottom

            highscore_rect03 = highscore_text03.get_rect()
            highscore_rect03.center = ((game_window.width / 2), 0)
            highscore_rect03.top = highscore_rect02.bottom

            body_rect = body_text.get_rect()
            body_rect.center = ((game_window.width / 2), ((game_window.height - body_text.get_height()) - 10))

            game_window.load(game_window.game_background, rect=(0,0))
            game_window.load(header_img, rect=header_rect)
            game_window.load(highscore_text01, rect=highscore_rect01)
            game_window.load(highscore_text04, rect=highscore_rect04)
            game_window.load(highscore_text05, rect=highscore_rect05)
            game_window.load(highscore_text02, rect=highscore_rect02)
            game_window.load(highscore_text03, rect=highscore_rect03)
            game_window.load(body_text, rect=body_rect)

        elif Scene.current == 1:
            game_window.load(level_handler.background_img, rect=(0,0))
            score_board.show()

        elif Scene.current == 2:
            with open('.\\src\\data\\highscore.json') as json_file:
                game_window.highscore_data = json.load(json_file)

            ply_score = 0

            if game_manager.player_score > 0 and not game_manager.player_score == None:
                ply_score = game_manager.player_score

            game_window.load(game_window.game_background, rect=(0,0))
            game_window.screen.fill(RGB_Color.black)
            header_text = GAME_OVER_FONT.render(f"[GAME OVER]", True, RGB_Color.red, RGB_Color.black)
            body_text = TEXT_FONT.render("Press {ENTER} to restart...    OR     {ESC} to quit...", True, RGB_Color.white,RGB_Color.black)
            score_text01 = TEXT_FONT.render("[SCORE]", True, RGB_Color.white,RGB_Color.black)
            score_text02 = TEXT_FONT.render("", True, RGB_Color.white,RGB_Color.black)
            score_text03 = TEXT_FONT.render(f"{game_manager.player_name}", True, RGB_Color.white,RGB_Color.black)
            score_text04 = TEXT_FONT.render(f"{game_manager.level}", True, RGB_Color.white,RGB_Color.black)
            score_text05 = TEXT_FONT.render(f"{ply_score}", True, RGB_Color.white,RGB_Color.black)

            highscore_text01 = TEXT_FONT.render("[HIGHSCORE]", True, RGB_Color.white,RGB_Color.black)
            highscore_text02 = TEXT_FONT.render("", True, RGB_Color.white,RGB_Color.black)
            highscore_text03 = TEXT_FONT.render(f"{game_window.highscore_data['player']}", True, RGB_Color.white,RGB_Color.black)
            highscore_text04 = TEXT_FONT.render(f"{game_window.highscore_data['level']}", True, RGB_Color.white,RGB_Color.black)
            highscore_text05 = TEXT_FONT.render(f"{game_window.highscore_data['score']}", True, RGB_Color.white,RGB_Color.black)

            score_classifier_text01 = TEXT_FONT.render("PLAYER:", True, RGB_Color.white,RGB_Color.black)
            score_classifier_text02 = TEXT_FONT.render("LEVEL:", True, RGB_Color.white,RGB_Color.black)
            score_classifier_text03 = TEXT_FONT.render("SCORE:", True, RGB_Color.white,RGB_Color.black)

            header_rect = header_text.get_rect()
            header_rect.center = ((game_window.width / 2), (game_window.height / 4))

            score_text01_rect = score_text01.get_rect()
            score_text01_rect.center = (((game_window.width / 8) * 3),(game_window.height / 2))

            score_text02_rect = score_text02.get_rect()
            score_text02_rect.center = (((game_window.width / 8) * 3),(game_window.height / 2))
            score_text02_rect.top = score_text01_rect.bottom

            score_text03_rect = score_text03.get_rect()
            score_text03_rect.center = (((game_window.width / 8) * 3),(game_window.height / 2))
            score_text03_rect.top = score_text02_rect.bottom

            score_text04_rect = score_text04.get_rect()
            score_text04_rect.center = (((game_window.width / 8) * 3),(game_window.height / 2))
            score_text04_rect.top = score_text03_rect.bottom

            score_text05_rect = score_text05.get_rect()
            score_text05_rect.center = (((game_window.width / 2) - (game_window.width / 8)),(game_window.height / 2)) #
            score_text05_rect.top = score_text04_rect.bottom




            highscore_text01_rect = highscore_text01.get_rect()
            highscore_text01_rect.center = ((game_window.width - ((game_window.width / 8) * 3)),(game_window.height / 2))

            highscore_text02_rect = highscore_text02.get_rect()
            highscore_text02_rect.center = ((game_window.width - ((game_window.width / 8) * 3)),(game_window.height / 2))
            highscore_text02_rect.top = highscore_text01_rect.bottom

            highscore_text03_rect = highscore_text03.get_rect()
            highscore_text03_rect.center = ((game_window.width - ((game_window.width / 8) * 3)),(game_window.height / 2))
            highscore_text03_rect.top = highscore_text02_rect.bottom

            highscore_text04_rect = highscore_text04.get_rect()
            highscore_text04_rect.center = ((game_window.width - ((game_window.width / 8) * 3)),(game_window.height / 2))
            highscore_text04_rect.top = highscore_text03_rect.bottom

            highscore_text05_rect = highscore_text05.get_rect()
            highscore_text05_rect.center = ((game_window.width - ((game_window.width / 8) * 3)),(game_window.height / 2))
            highscore_text05_rect.top = highscore_text04_rect.bottom


            score_classifier_text01_rect = score_classifier_text01.get_rect()
            score_classifier_text01_rect.center = score_text03_rect.center
            score_classifier_text01_rect.left = 0

            score_classifier_text02_rect = score_classifier_text02.get_rect()
            score_classifier_text02_rect.center = score_text04_rect.center
            score_classifier_text02_rect.left = 0

            score_classifier_text03_rect = score_classifier_text03.get_rect()
            score_classifier_text03_rect.center = score_text05_rect.center
            score_classifier_text03_rect.left = 0

            body_rect = body_text.get_rect()
            body_rect.center = ((game_window.width / 2), ((game_window.height - body_text.get_height()) - 10))

            game_window.load(header_text, rect=header_rect)
            game_window.load(score_text01, rect=score_text01_rect)
            game_window.load(score_text02, rect=score_text02_rect)
            game_window.load(score_text03, rect=score_text03_rect)
            game_window.load(score_text04, rect=score_text04_rect)
            game_window.load(score_text05, rect=score_text05_rect)
            game_window.load(highscore_text01, rect=highscore_text01_rect)
            game_window.load(highscore_text02, rect=highscore_text02_rect)
            game_window.load(highscore_text03, rect=highscore_text03_rect)
            game_window.load(highscore_text04, rect=highscore_text04_rect)
            game_window.load(highscore_text05, rect=highscore_text05_rect)
            game_window.load(score_classifier_text01, rect=score_classifier_text01_rect)
            game_window.load(score_classifier_text02, rect=score_classifier_text02_rect)
            game_window.load(score_classifier_text03, rect=score_classifier_text03_rect)
            game_window.load(body_text, rect=body_rect)

    @staticmethod
    def load(obj_surface, rect=None):
        if rect == None:
            rect = obj_surface.get_rect()

        game_window.screen.blit(obj_surface, rect)

    @staticmethod
    def load_objects(game_objects):
        for g_obj in game_objects:
            game_window.load(g_obj.surface, rect=g_obj.rect)

class game_manager():
    game_over=False
    quit_game=False
    restart_game=False
    start_game=False
    player_score = 0
    player_hp = PLAYER_HP
    player_name = PLAYER_DEFAULT_NAME
    all_sprites=pygame.sprite.Group()
    players = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemy_spawn_count = 1
    enemy_count = 0
    #pygame.time.set_timer(ENEMY_SPAWN_EVENT, ENEMY_SPAWN_INTERVAL)
    level = 1

    @staticmethod
    def reset():
        game_manager.game_over = False
        game_manager.quit_game = False
        game_manager.restart_game = False
        game_manager.start_game = False
        game_manager.all_sprites = pygame.sprite.Group()
        game_manager.players = pygame.sprite.Group()
        game_manager.bullets = pygame.sprite.Group()
        game_manager.enemies = pygame.sprite.Group()
        game_manager.player_score = 0
        game_manager.enemy_spawn_count = 1
        game_manager.enemy_count = 0
        game_manager.level = 1
        game_manager.player_hp = PLAYER_HP
        game_manager.player_name = str(game_manager.player_name)

    @staticmethod
    def update():
        if game_manager.player_score > 0 and game_manager.enemy_count <= 0:
            game_manager.enemy_spawn_count += 1
            game_manager.level += 1

        if game_manager.enemy_count <= 0:
            pygame.event.post(pygame.event.Event(ENEMY_SPAWN_EVENT))

class event_handler():
    pressed_keys=pygame.key.get_pressed()
    events=pygame.event.get()

    @staticmethod
    def handle():
        for event in event_handler.get_events():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if Scene.current == int(len(Scene.scenes) - 1) or Scene.current == 0:
                        game_manager.quit_game = True
                    elif Scene.current == 1:
                        game_manager.game_over = True

                    break

                if event.key == K_RETURN:
                    if Scene.current == int(len(Scene.scenes) - 1):
                        game_manager.restart_game = True
                    elif Scene.current == 0:
                        game_manager.start_game = True
                        game_manager.player_name = game_window.player_name_input_box.get_text()
                        
                        if len(game_manager.player_name) <= 0:
                            game_manager.player_name = PLAYER_DEFAULT_NAME

                    break

            if event.type == QUIT:
                game_manager.quit_game = True
                game_manager.game_over = True
                    
                break

            game_window.ui_manager.process_events(event)

            if event.type == ADD_SCORE_EVENT:
                game_manager.player_score += 1

                break

            if event.type == LOSE_HP_EVENT:
                game_manager.player_hp -= 1

                if game_manager.player_hp == 0:
                    game_manager.game_over = True

            if Scene.current == 1 and event.type == ENEMY_SPAWN_EVENT:
                for i in range(0, game_manager.enemy_spawn_count):
                    new_enemy = Enemy()
                    game_manager.enemies.add(new_enemy)
                    game_manager.all_sprites.add(new_enemy)
                    game_manager.enemy_count += 1
                
        if not game_manager.game_over:
            event_handler.get_keys_pressed()

    @staticmethod
    def get_events():
        event_handler.events = pygame.event.get()
        return event_handler.events

    @staticmethod
    def get_keys_pressed():
        event_handler.pressed_keys = pygame.key.get_pressed()
        return event_handler.pressed_keys

    @staticmethod
    def update():
        event_handler.get_events()
        event_handler.get_keys_pressed()

class score_board():
    @staticmethod
    def show():
        player_text = SCORE_BOARD_FONT.render(f"PLAYER:  {game_manager.player_name}", True, RGB_Color.white, RGB_Color.black)
        level_text = SCORE_BOARD_FONT.render(f"LEVEL:  {game_manager.level}", True, RGB_Color.white, RGB_Color.black)
        score_text = SCORE_BOARD_FONT.render(f"SCORE:  {game_manager.player_score}", True, RGB_Color.white, RGB_Color.black)
        hp_text = SCORE_BOARD_FONT.render(f"HP:  {game_manager.player_hp}", True, RGB_Color.white, RGB_Color.black)

        player_rect = player_text.get_rect()
        level_rect = level_text.get_rect()
        score_rect = score_text.get_rect()
        hp_rect = hp_text.get_rect()

        player_rect.left = 0
        player_rect.top = 0
        level_rect.top = player_rect.bottom
        level_rect.left = 0
        score_rect.top = level_rect.bottom
        score_rect.left = 0
        hp_rect.top = score_rect.bottom
        hp_rect.left = 0

        game_window.load(player_text, rect=player_rect)
        game_window.load(level_text, rect=level_rect)
        game_window.load(score_text, rect=score_rect)
        game_window.load(hp_text, rect=hp_rect)

class level_handler():
    background_img = None
    change_ambiente = False
    last_change_level = 0

    @staticmethod
    def reset():
        level_handler.background_img = pygame.transform.scale(pygame.image.load('.\\src\\background\\background.jpg').convert(), (game_window.width, game_window.height))
        level_handler.last_change_level = 0

    @staticmethod
    def handle():
        if (game_manager.level % 10) == 0 and game_manager.level > 0 and game_manager.level > level_handler.last_change_level:
            level_handler.last_change_level = game_manager.level
            game_manager.player_hp += 1
            level_handler.change_ambiente = True
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            if game_manager.level >= 10 and game_manager.level < 20:
                player.speed += (player.speed / 4)
                pygame.mixer.music.load('.\\src\\background\\music\\retro_plattforming.mp3')

            elif game_manager.level >= 20 and game_manager.level < 30:
                player.speed += (player.speed / 4)
                player.bullet_cooldown -= (player.bullet_cooldown / 8)
                pygame.mixer.music.load('.\\src\\background\\music\\a_bit_of_hope.mp3')

            elif game_manager.level >= 30: # and game_manager.level < 40:
                pygame.mixer.music.load('.\\src\\background\\music\\boss_time.mp3')

                if not player.bullet_cooldown <= 50:
                    player.bullet_cooldown -= (player.bullet_cooldown / 8)

            else:
                pygame.mixer.music.load('.\\src\\background\\music\\faster_tempo_arcade_kid.mp3')

                
            pygame.mixer.music.play(-1)
            level_handler.change_ambiente = False

            


#--------@{OBJECT-CLASSES}
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.image = pygame.image.load('.\\src\\ship\\ship_64px_002.png').convert_alpha()
        self.active_image = pygame.image.load('.\\src\\ship\\ship_64px_002_active.png').convert_alpha()
        self.surface = self.image
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect()
        self.speed = 7
        self.start_pos = ((game_window.width / 2), ((game_window.height - self.surface.get_height()) - 10))
        self.rect.center = self.start_pos

        self.bullet_speed = 14
        self.bullet_cooldown = 200
        self.bullet_cooldown_tracker = 0

        self.hp = PLAYER_HP

    def set_active_image(self):
        old_top = self.rect.top
        old_center = self.rect.center
        self.surface = self.active_image
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect()
        self.rect.center = old_center
        self.rect.top = old_top

    def set_passive_image(self):
        old_top = self.rect.top
        old_center = self.rect.center
        self.surface = self.image
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect()
        self.rect.center = old_center
        self.rect.top = old_top

    def reset(self):
        self.rect.center = self.start_pos
        self.speed = 7
        self.bullet_speed = 14
        self.hp = PLAYER_HP

    def shoot(self):
        new_shot = Bullet(self.bullet_speed, self.rect.center, self.rect.top)
        game_manager.all_sprites.add(new_shot)
        game_manager.bullets.add(new_shot)

    def move_up(self, speed=None):
        if speed == None:
            speed = -self.speed

        self.rect.move_ip(0, speed)

        if self.rect.top <= 0:
            self.rect.top = 0

    def move_down(self, speed=None):
        if speed == None:
            speed = self.speed

        self.rect.move_ip(0, speed)

        if self.rect.bottom >= game_window.height:
            self.rect.bottom = game_window.height

    def move_left(self):
        self.rect.move_ip(-self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.move_ip(self.speed, 0)

        if self.rect.right > game_window.width:
            self.rect.right = game_window.width

    def update(self):
        passive_img = True
        self.hp = game_manager.player_hp

        self.bullet_cooldown_tracker += game_window.clock.get_time()
        if self.bullet_cooldown_tracker > self.bullet_cooldown:
            self.bullet_cooldown_tracker = 0
        
        if event_handler.pressed_keys[K_UP] or event_handler.pressed_keys[K_w]:
            passive_img = False
            self.set_active_image()
            self.move_up()

        if event_handler.pressed_keys[K_DOWN] or event_handler.pressed_keys[K_s]:
            #self.set_passive_image()
            self.move_down()

        if event_handler.pressed_keys[K_LEFT] or event_handler.pressed_keys[K_a]:
            passive_img = False
            self.set_active_image()
            self.move_left()

        if event_handler.pressed_keys[K_RIGHT] or event_handler.pressed_keys[K_d]:
            passive_img = False
            self.set_active_image()
            self.move_right()

        if event_handler.pressed_keys[K_SPACE] and self.bullet_cooldown_tracker == 0:
            self.shoot()

        if passive_img:
            self.set_passive_image()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, player_center, player_top):
        super(Bullet,self).__init__()
        self.spawn_image = pygame.image.load('.\\src\\Bullet\\bullet_spawn.png').convert_alpha()
        self.image = pygame.image.load('.\\src\\Bullet\\bullet.png').convert_alpha()
        self.surface = self.spawn_image
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect()
        self.is_first = 0
        self.speed = speed
        self.player_center = player_center
        self.player_top = player_top
        self.rect.center = self.player_center
        self.rect.bottom = self.player_top
        self.dead = False
        

    def update(self):
        if self.is_first == 0:
            self.is_first = 1
        elif self.is_first == 1:
            self.is_first = 2
            self.surface = self.image
            self.surface.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surface.get_rect()
            self.rect.center = self.player_center
            self.rect.bottom = self.player_top
            self.rect.move_ip(0, -self.speed)
        else:
            self.rect.move_ip(0, -self.speed)

        if self.dead:
            self.kill()

        if pygame.sprite.spritecollideany(self, game_manager.enemies):
            self.dead = True

        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.image = pygame.image.load('.\\src\\enemy\\enemy_64px_001.png').convert_alpha()
        self.surface = self.image
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect()
        # (self.surface.get_width() / 2)
        self.rect.center = (random.randint(0, (game_window.width - (self.surface.get_width() / 2))), random.randint(0,self.surface.get_height()))

        self.speed = round(random.uniform(0.5,2.0), 1) #randint(0.5,2)

        self.dead = False
        self.death_animation_frames = [pygame.image.load('.\\src\\enemy\\enemy_death_64px_001.png').convert_alpha(),pygame.image.load('.\\src\\enemy\\enemy_death_64px_002.png').convert_alpha(),pygame.image.load('.\\src\\enemy\\enemy_death_64px_003.png').convert_alpha(),pygame.image.load('.\\src\\enemy\\enemy_death_64px_004.png').convert_alpha(),pygame.image.load('.\\src\\enemy\\enemy_death_64px_005.png').convert_alpha()]
        self.death_animation_frame = 0
        self.death_animation_frame_cooldown = 100
        self.death_animation_frame_cooldown_tracker = 0


    def death_animation(self):
        old_center = self.rect.center
        self.surface = self.death_animation_frames[self.death_animation_frame]
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect()
        self.rect.center = old_center
        self.death_animation_frame += 1

    def update(self):
        self.speed = round(random.uniform(0.5,2.0), 1) #randint(0.5,2)
        if self.dead:
            self.death_animation_frame_cooldown_tracker += game_window.clock.get_time()
            if self.death_animation_frame_cooldown_tracker > self.death_animation_frame_cooldown:
                self.death_animation_frame_cooldown_tracker = 0

            if self.death_animation_frame == int(len(self.death_animation_frames) - 1):
                game_manager.enemy_count -= 1
                self.kill()
            else:
                if self.death_animation_frame_cooldown_tracker == 0:
                    #if self.death_animation_frame <= 4:
                    #    add_score_text = ADD_SCORE_FONT.render("+1",True,RGB_Color.white)
                    #    add_score_rect = add_score_text.get_rect()
                    #    add_score_rect = self.rect.center

                    #    game_window.load(add_score_text,rect=add_score_rect)

                    self.death_animation()
        else:
            self.rect.move_ip(random.randint(-10,10), self.speed)

            if pygame.sprite.spritecollideany(self, game_manager.bullets):
                pygame.event.post(pygame.event.Event(ADD_SCORE_EVENT))
                self.dead = True

            if pygame.sprite.spritecollideany(self, game_manager.players):
                pygame.event.post(pygame.event.Event(LOSE_HP_EVENT))
                self.dead = True

            if self.rect.top > game_window.height:
                pygame.event.post(pygame.event.Event(LOSE_HP_EVENT))
                self.dead = True

            if self.rect.right > game_window.width:
                self.rect.right = game_window.width

            if self.rect.left < 0:
                self.rect.left = 0


#  [DEFINITION][REGION]~~(END)~~<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#  [EXECUTION][REGION]~~(START)~~>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#--------@{PREPARATION}
game_window.init()
#game_ui.init()
player = Player()

#--------@{MAIN}
while not game_manager.quit_game:
    Scene.init()
    game_manager.reset()
    player.reset()
    level_handler.reset()
    game_manager.all_sprites.add(player)
    game_manager.players.add(player)
    game_window.update()

    while not game_manager.start_game:
        game_manager.update()
        event_handler.handle()
        if game_manager.start_game or game_manager.quit_game:
            break

        game_window.load_scene()
        game_window.update()

    Scene.go_to_next()

    while not game_manager.game_over and not game_manager.quit_game:
        level_handler.handle()
        # >>> [FRAME]~~~(START)
        event_handler.handle()
        game_manager.update()

        if game_manager.game_over:
            break

        game_window.load_scene()
        player.update()
        game_manager.bullets.update()
        game_manager.enemies.update()
        
        # <<< [FRAME]~~(END)
        game_window.load_objects(game_manager.all_sprites)
        game_window.update()

    Scene.go_to_next()
    if game_manager.level > game_window.highscore_data['level'] or game_manager.player_score > game_window.highscore_data['score']:
        game_window.highscore_data['level'] = game_manager.level
        game_window.highscore_data['score'] = game_manager.player_score
        game_window.highscore_data['player'] = game_manager.player_name

        json_string = json.dumps(game_window.highscore_data)
        with open('.\\src\\data\\highscore.json', 'w') as outfile:
            outfile.write(json_string)

    while not game_manager.quit_game and not game_manager.restart_game:
        event_handler.handle()
        if game_manager.quit_game or game_manager.restart_game:
            break

        game_window.load_scene()
        game_window.update()

    #Scene.go_to_next()

#--------@{END}
game_window.close()

#  [EXECUTION][REGION]~~(END)~~<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<