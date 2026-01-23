import pygame


class Ship:
    '''管理飞船的类'''

    def __init__(self, ai_game):
        '''初始化飞船并设置其初始位置'''
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
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

    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        '''根据移动标准来调整飞船位置'''
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1
        if self.moving_up:
            self.rect.y -= 1
        if self.moving_down:
            self.rect.y += 1
