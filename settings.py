class Settings:
    '''存储游戏中所有设置的类'''
    def __init__(self):
        '''初始化游戏的设置'''
        self.screen_width=1200
        self.screen_height=900
        self.bg_color=(255,255,255)
        #飞船设置
        self.ship_speed=2
        self.ship_limit=3
        #子弹设置
        self.bullet_speed=5
        self.bullet_width=300
        self.bullet_height=6
        self.bullet_color=(200,0,0)
        self.bullets_allowed=500

        #外星人设置
        self.alien_speed=0.3
        self.fleet_drop_speed=10
        #fleet_direction为1表示右移,-1表示左移
        self.fleet_direction=0.2
