class Settings:
    '''存储游戏中所有设置的类'''
    def __init__(self):
        '''初始化游戏的设置'''
        self.screen_width=1200
        self.screen_height=900
        self.bg_color=(255,255,255)
        self.ship_speed=5
        #子弹设置
        self.bullet_speed=3
        self.bullet_width=3
        self.bullet_height=6
        self.bullet_color=(200,0,0)
        self.bullets_allowed=500

        #外星人设置
        self.alien_speed=2.0

