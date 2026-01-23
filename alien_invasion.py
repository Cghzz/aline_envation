import sys
import pygame
from pygame.event import Event

from bullet import Bullet
from settings import Settings
from ship import Ship
from alien import Alien

class AlienInvasion:
    '''管理游戏资源和行为的类'''

    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        # self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width=self.screen.get_rect().width
        # self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("外星人入侵小游戏")
        # 设置背景色
        self.bg_color = self.settings.bg_color
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
    def run_game(self):
        '''开始游戏主循环'''
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()


            self._create_aliens()
            self._update_aliens()
            self._update_screen()

    def _update_bullets(self):
        '''更新子弹位置并删除消失的子弹'''
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

    def _check_events(self):
        '''响应按键和鼠标事件'''
        # 监听键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_keyup_event(self, event: Event):
        if (event.key == pygame.K_RIGHT
        ):
            # 向右移动飞船
            self.ship.moving_right = False
        elif (event.key == pygame.K_LEFT
        ):
            # 向左移动飞船
            self.ship.moving_left = False
        elif (event.key == pygame.K_UP
        ):
            # 向上移动飞船
            self.ship.moving_up = False
        elif (event.key == pygame.K_DOWN
        ):
            # 向下移动飞船
            self.ship.moving_down = False

    def _check_keydown_event(self, event: Event):
        if (event.key == pygame.K_RIGHT
        ):
            # 向右移动飞船
            self.ship.moving_right = True
        elif (event.key == pygame.K_LEFT
        ):
            # 向左移动飞船
            self.ship.moving_left = True
        elif (event.key == pygame.K_UP
        ):
            # 向上移动飞船
            self.ship.moving_up = True
        elif (event.key == pygame.K_DOWN
        ):
            # 向下移动飞船
            self.ship.moving_down = True
        # 按q键退出游戏
        elif event.key == pygame.K_q:
            sys.exit()
        # 按esc键退出游戏
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        '''创建一颗子弹,并将其加入编组bullets中'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        '''更新屏幕上的图像,并切换到新屏幕'''
        # 填充屏幕颜色
        self.screen.fill(self.settings.bg_color)
        # 绘制飞船
        self.ship.blitme()
        # 绘制子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #绘制外星人
        self.aliens.draw(self.screen)
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _create_aliens(self):
        '''创建外星人'''
        #创建一个外星人并计算一行可以容纳多个外星人

        alien=Alien(self)
        alien_width,aline_height=alien.rect.size
        #计算一行可以容纳多少外星人群
        available_space_x = self.settings.screen_width-2*alien_width
        number_aliens_x=available_space_x//(alien_width*2)
        #计算可以容纳几行外星人群
        ship_height=self.ship.rect.height
        available_space_y = (self.settings.screen_height-3*ship_height
                             -ship_height)
        number_rows=available_space_y//(aline_height*2)
        #创建第一行外星人
        for number_row in range(number_rows):
            for alien_number in range(number_aliens_x):
                alien=Alien(self)
                alien.x=alien_width+2*alien_width*alien_number
                alien.y=aline_height+2*aline_height*number_row
                alien.rect.x=alien.x
                alien.rect.y=alien.y
                self.aliens.add(alien)

    def _update_aliens(self):
        '''更新外星人群中所有外星人的移动'''
        self.aliens.update()


if __name__ == '__main__':
    # 创建游戏实例并运行
    ai = AlienInvasion()
    ai.run_game()
