class Settings:
    '''存储游戏中所有设置的类'''

    def __init__(self):
        '''初始化游戏的设置'''
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (255, 255, 255)
        # 飞船设置
        self.ship_speed = 1
        self.ship_limit = 3
        # 子弹设置
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 6
        self.bullet_color = (200, 0, 0)
        self.bullets_allowed = 500

        # 外星人设置
        self.alien_speed = 0.2

        self.fleet_drop_speed = 1
        self.fleet_direction = 1

        # 加快游戏节奏的速度
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        # 音频文件
        self.bgm_music='./music/bgm.mp3'
        self.bump_music='./music/bump.mp3'
        self.hit_music='./music/hit.mp3'
        self.shoot_music='./music/shoot.mp3'
        # 音量
        self.volume=0.5

    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.ship_speed = 1.0
        self.bullet_speed = 2.0
        self.alien_speed = 0.2
        # fleet_direction为1表示右移,-1表示左移
        self.fleet_direction = 1
        self.fleet_drop_speed = 10
        # 计分
        self.alien_points = 50

    def increase_speed(self):
        '''提高速度设置'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.speedup_scale)
