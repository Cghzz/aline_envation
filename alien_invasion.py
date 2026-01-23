import sys
import pygame
from settings import Settings
from ship import Ship
class AlienInvasion:
    '''管理游戏资源和行为的类'''
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        self.settings=Settings()
        self.screen=pygame.display.set_mode((self.settings.screen_width,
                                             self.settings.screen_height))
        pygame.display.set_caption("外星人入侵小游戏")
        #设置背景色
        self.bg_color=self.settings.bg_color
        self.ship = Ship(self)

    def run_game(self):
        '''开始游戏主循环'''
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        '''响应按键和鼠标事件'''
        # 监听键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if (event.key==pygame.K_RIGHT
                        and self.ship.rect.x
                        < self.settings.screen_width-self.ship.rect.width-1):
                    #向右移动飞船
                    self.ship.moving_right=True
                elif (event.key==pygame.K_LEFT
                      and self.ship.rect.x>0):
                    #向左移动飞船
                    self.ship.moving_left=True
                elif (event.key==pygame.K_UP
                      and self.ship.rect.y>0):
                    #向上移动飞船
                    self.ship.moving_up=True
                elif (event.key==pygame.K_DOWN
                      and self.ship.rect.y
                      <self.settings.screen_height-self.ship.rect.height-1):
                    #向下移动飞船
                    self.ship.moving_down=True
            elif event.type==pygame.KEYUP:
                if (event.key==pygame.K_RIGHT
                        and self.ship.rect.x
                        < self.settings.screen_width-self.ship.rect.width-1):
                    #向右移动飞船
                    self.ship.moving_right=False
                elif (event.key==pygame.K_LEFT
                      and self.ship.rect.x>0):
                    #向左移动飞船
                    self.ship.moving_left=False
                elif (event.key==pygame.K_UP
                      and self.ship.rect.y>0):
                    #向上移动飞船
                    self.ship.moving_up=False
                elif (event.key==pygame.K_DOWN
                      and self.ship.rect.y<self.settings.screen_height
                      -self.ship.rect.height):
                    #向下移动飞船
                    self.ship.moving_down=False



    def _update_screen(self):
        '''更新屏幕上的图像,并切换到新屏幕'''
        # 填充屏幕颜色
        self.screen.fill(self.settings.bg_color)
        # 绘制飞船
        self.ship.blitme()
        # 让最近绘制的屏幕可见
        pygame.display.flip()

if __name__=='__main__':
    #创建游戏实例并运行
    ai=AlienInvasion()
    ai.run_game()