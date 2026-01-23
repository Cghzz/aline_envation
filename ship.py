import pygame

from settings import Settings


class Ship:
    '''管理飞船的类'''

    def __init__(self, ai_game):
        '''初始化飞船并设置其初始位置'''
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings=Settings();
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('./images/飞船.bmp')
        self.rect = self.image.get_rect()
        # 对于每艘新飞船,都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 设置一个连续移动标志,如果该标志位False,飞船不会移动
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        #在飞船的属性x y中存储小数值
        self.x=float(self.rect.x)
        self.y=float(self.rect.y)

    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        '''根据移动标准来调整飞船位置'''
        if self.moving_right and self.rect.x<self.screen_rect.width-self.rect.width:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.x>0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.y>0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.y<self.screen_rect.height-self.rect.height:
            self.y += self.settings.ship_speed

        #根据self.x更新rect对象
        self.rect.x=self.x
        self.rect.y=self.y
