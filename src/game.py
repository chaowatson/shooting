import time
from os import path


import pygame
import cProfile

from mlgame.gamedev.game_interface import PaiaGame, GameResultState, GameStatus
from mlgame.view.test_decorator import check_game_progress, check_game_result
from mlgame.view.view_model import create_text_view_data, create_asset_init_data, create_image_view_data, create_line_view_data , Scene
from mlgame.view.view import PygameView
from .game_object import *
from .param import *
from .map import *
from .moving_enemy_path import *

ASSET_PATH = path.join(path.dirname(__file__), "../asset")
MAP_PATH = path.join(ASSET_PATH, "map/map1.tmx")


class Shooting(PaiaGame):
    """
    This is a Interface of a game
    """

    def __init__(self, time_to_play, game_mode):
        super().__init__()
        self.game_result_state = GameResultState.FAIL
        self.scene = Scene(width=WIDTH, height=HEIGHT, color="#FFFFFF", bias_x=0, bias_y=0)
        self.map = TiledMap(MAP_PATH)
        self.setup()
        self.score = 0
        self._begin_time = time.time()
        self._timer = 0
        self.frame_count = 0
        self.time_limit = time_to_play

    def setup(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.healthbars = pygame.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'Player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'Enemy':
                EnemyFactory.create_enemy('enemy', self, tile_object.x, tile_object.y)
            if tile_object.name == 'MovingEnemy':
                EnemyFactory.create_enemy('moving enemy', self, tile_object.x, tile_object.y, ENEMY1PATH, 16)
            if tile_object.name == 'ShootingEnemy':
                EnemyFactory.create_enemy('shooting enemy', self, tile_object.x, tile_object.y)
            if tile_object.name == 'Wall':
                Wall(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)

    def update(self, commands):
        # handle command
        ai_1p_cmd = commands[self.ai_clients()[0]["name"]]
        self.player.update(ai_1p_cmd)
        self.enemies.update()
        self.bullets.update()
        self._timer = round(time.time() - self._begin_time, 3)
        self.frame_count += 1
        # self.draw()

        if not self.is_running:
            return "QUIT"

    def game_to_player_data(self):
        """
        send something to game AI
        we could send different data to different ai
        """
        to_players_data = {}
        data_to_1p = {
            "frame": self.frame_count,
            "player_x": self.player.rect.centerx,
            "player_y": self.player.rect.centery,
            "score": self.score,
            "status": self.get_game_status(),
            "north_detection": self.player.north_distance,
            "south_detection": self.player.south_distance,
            "west_detection": self.player.west_distance,
            "east_detection": self.player.east_distance,

        }

        for ai_client in self.ai_clients():
            to_players_data[ai_client['name']] = data_to_1p
        # should be equal to config. GAME_SETUP["ml_clients"][0]["name"]

        return to_players_data

    def get_game_status(self):

        if self.is_running:
            status = GameStatus.GAME_ALIVE
        elif self.score > 0: #self.score_to_win:
            status = GameStatus.GAME_PASS
        else:
            status = GameStatus.GAME_OVER
        return status

    def reset(self):
        pass


    @property
    def is_running(self):
        return self.frame_count < self.time_limit

    def get_scene_init_data(self):
        """
        Get the initial scene and object information for drawing on the web
        """
        # TODO add music or sound
        map1_path = path.join(ASSET_PATH, "img/map1.png")
        map1 = create_asset_init_data("map1", WIDTH, HEIGHT, map1_path, "url")
        player_path = path.join(ASSET_PATH, "img/player.png")
        player = create_asset_init_data("player", 32, 32, player_path, "url")
        enemy_path = path.join(ASSET_PATH, "img/enemy.png")
        enemy = create_asset_init_data("enemy", 32, 32, enemy_path, "url")
        bullet_path = path.join(ASSET_PATH, "img/bullet.png")
        bullet = create_asset_init_data("bullet", 32, 32, bullet_path, "url")
        scene_init_data = {"scene": self.scene.__dict__,
                           "assets": [
                                map1,
                                player,
                                enemy,
                                bullet
                           ],
                           # "audios": {}
                           }
        return scene_init_data

    @check_game_progress
    def get_scene_progress_data(self):
        """
        Get the position of game objects for drawing on the web
        """
        map1 = create_image_view_data("map1", 0, 0, WIDTH, HEIGHT)
        game_obj_list = [map1]
        game_obj_list.extend([self.player.game_object_data])
        bullets_data = []
        for bullet in self.bullets:
            bullets_data.append(bullet.game_object_data)
        game_obj_list.extend(bullets_data)
        enemies_data = []
        for enemy in self.enemies:
            enemies_data.append(enemy.game_object_data)
        game_obj_list.extend(enemies_data)
        healthbar_data = []
        for healthbar in self.healthbars:
            healthbar_data.append(healthbar.game_object_data)
        game_obj_list.extend(healthbar_data)
        player_angle = create_text_view_data("player's angle = " + str(int(self.player.display_angle)), 12.5*TILESIZE, TILESIZE, "#000000")
        top_distance = create_text_view_data("north distance = " + str(int(self.player.north_distance)), 12.5*TILESIZE, 0, "#000000")
        down_distance = create_text_view_data("south distance = " + str(int(self.player.south_distance)), 12.5*TILESIZE, 0.5*TILESIZE,  "#000000")
        left_distance = create_text_view_data("west distance = " + str(int(self.player.west_distance)), 16.5 *TILESIZE, 0, "#000000")
        right_distance = create_text_view_data("east distance = " + str(int(self.player.east_distance)), 16.5*TILESIZE, 0.5 * TILESIZE, "#000000")
        scene_progress = {
            # background view data will be draw first
            "background": [


            ],
            # game object view data will be draw on screen by order , and it could be shifted by WASD
            "object_list": game_obj_list,
            "toggle": [down_distance, top_distance, left_distance, right_distance, player_angle],
            "foreground": [

            ],
            # other information to display on web
            "user_info": [],
            # other information to display on web
            "game_sys_info": {}
        }
        return scene_progress

    @check_game_result
    def get_game_result(self):
        """
        send game result
        """
        if self.get_game_status() == GameStatus.GAME_PASS:
            self.game_result_state = GameResultState.FINISH
        return {"frame_used": self.frame_count,
                "state": self.game_result_state,
                "attachment": [

                    {"player": self.ai_clients()[0]["name"],
                     "score": "score",
                     "remain_hp": 1,
                     "remain_time": 1
                     }
                ]

                }

        pass

    def get_keyboard_command(self):
        """
        Define how your game will run by your keyboard
        """
        cmd_1p = []
        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_w]:
            cmd_1p.append("UP")
        if key_pressed_list[pygame.K_s]:
            cmd_1p.append("DOWN")
        if key_pressed_list[pygame.K_a]:
            cmd_1p.append("LEFT_TURN")
        if key_pressed_list[pygame.K_d]:
            cmd_1p.append("RIGHT_TURN")
        if key_pressed_list[pygame.K_SPACE]:
            cmd_1p.append("SHOOT")
        ai_1p = self.ai_clients()[0]["name"]
        return {ai_1p: cmd_1p}


    @staticmethod
    def ai_clients():
        """
        let MLGame know how to parse your ai,
        you can also use this names to get different cmd and send different data to each ai client
        """
        return [
            {"name": "1P"},
            {"name": "2P"}
        ]
