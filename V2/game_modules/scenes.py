from typing import Text
import pygame
from pygame.locals import *
import pygame_gui as pg_gui
import json
from game_modules import mytools

SCENES_CONFIGS_JSON_PATH = '.\\config\\scenes.json'
WINDOW_CONFIG_JSON_PATH = '.\\config\\window.json'
HIGHSCORE_DATA_JSON_PATH = '..\\src\\data\\highscore.json'

SCENES_CONFIGS = mytools.read_json_file(SCENES_CONFIGS_JSON_PATH)
WINDOW_CONFIG = mytools.read_json_file(WINDOW_CONFIG_JSON_PATH)

class game_window():
    config=None
    screen=None
    width=None
    height=None
    clock=pygame.time.Clock()
    icon=None
    caption=None
    frame_rate=None
    ui_manager=None

    @staticmethod
    def init():
        game_window.config = WINDOW_CONFIG
        game_window.icon = pygame.image.load(game_window.config['paths']['icon'])
        game_window.caption = game_window.config['caption']
        game_window.screen = pygame.display.set_mode((0,0), FULLSCREEN)
        game_window.width, game_window.height = pygame.display.get_surface().get_size()
        pygame.display.set_icon(game_window.icon)
        pygame.display.set_caption(game_window.caption)
        game_window.frame_rate = game_window.config['frame_rate']
        game_window.ui_manager = pg_gui.UIManager((game_window.width,game_window.height))

    @staticmethod
    def update():
        game_clock_tick = game_window.clock.tick(game_window.frame_rate)
        game_window.ui_manager.update(game_clock_tick/1000.0)
        game_window.ui_manager.draw_ui(game_window.screen)
        pygame.display.update()
        pygame.display.flip()

    @staticmethod
    def close():
        pygame.quit()

class start_screen():
    active = False
    config = None
    background_img = None
    header_img = None
    header = None
    background = None
    highscore=None
    highscore_data=None

    @staticmethod
    def init():
        start_screen.config = SCENES_CONFIGS['start_screen']
        start_screen.background_img = pygame.image.load(start_screen.config['paths']['background_img']).convert()
        start_screen.background = pygame.transform.scale(start_screen.game_background_img, (game_window.width, game_window.height))
        start_screen.header_img = pygame.image.load(start_screen.config['paths']['header_img']).convert_alpha()
        start_screen.highscore_data = mytools.read_json_file(HIGHSCORE_DATA_JSON_PATH)

        start_screen.config["UI_elements"]['header']['relative_rect'][2] = start_screen.header_img.get_width()
        start_screen.config["UI_elements"]['header']['relative_rect'][3] = start_screen.header_img.get_height()

        start_screen.header = pg_gui.elements.UIImage(
                                                        relative_rect=pygame.Rect(start_screen.config["UI_elements"]['header']['relative_rect']),
                                                        image_surface=start_screen.header_img,
                                                        manager=game_window.ui_manager
                                                    )

        start_screen.highscore = pg_gui.elements.UILabel(
                                                            relative_rect=pygame.Rect(start_screen.config["UI_elements"]["highscore"]["relative_rect"]),
                                                            text=f"""
[HIGHSCORE]
PLAYER:  {start_screen.highscore_data['player']}
LEVEL:   {start_screen.highscore_data['level']}
SCORE:   {start_screen.highscore_data['score']}
""",
                                                            manager=game_window.ui_manager
                                                        )

        start_screen.player_name_input_field = pg_gui.elements.UITextEntryLine(
                                                            relative_rect=
                                                        )
        
        

    @staticmethod
    def update():
        if start_screen.active:
            pass

    @staticmethod
    def hide():
        pass
        

class game_screen():
    active = False

    @staticmethod
    def init():
        pass

    @staticmethod
    def update():
        pass

class game_over_screen():
    active = False

    @staticmethod
    def init():
        pass

    @staticmethod
    def update():
        pass

class pause_screen():
    active = False

    @staticmethod
    def init():
        pass

    @staticmethod
    def update():
        pass

class Scene():
    config = None
    scenes = {
        "start_screen": start_screen,
        "game_screen": game_screen,
        "game_over_screen": game_over_screen,
        "pause_screen": pause_screen
    }

    current=None
    current_name=None

    @staticmethod
    def init():
        Scene.config = SCENES_CONFIGS
        Scene.current_name = Scene.config['initial_scene']
        Scene.current = Scene.scenes[Scene.current_name]

    def go_to(scene_name):
        Scene.current.active = False
        Scene.current_name = scene_name
        Scene.current = Scene.scenes[Scene.current_name]
        Scene.current.active = True

