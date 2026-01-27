import sys
import pygame
from pygame.event import Event
from time import sleep
from game_stats import GameStats

from bullet import Bullet
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from alien import Alien
from button import Button


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
        pygame.display.set_caption("外星人入侵小游戏    版本:V1.0.0   作者:cccgg")

        # 设置背景色
        self.bg_color = self.settings.bg_color
        self.ship = Ship(self)
        # print('游戏初始化时飞船位置:'+str(self.ship.rect))
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_aliens()

        #创建一个用于存储游戏统计信息的实例
        self.stats=GameStats(self)
        self.stats.getRecord()
        #创建一个Button按钮
        self.button=Button(self,'Play')
        #创建一个记分牌
        self.sb=Scoreboard(self)


    def run_game(self):
        '''开始游戏主循环'''
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
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
        #检查是否有子弹击中了外星人
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''响应子弹与外星人碰撞'''
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points*len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.aliens:
            # 删除现有子弹并创建一群新的外星人
            self.bullets.empty()
            self._create_aliens()
            self.settings.increase_speed()
            print('分数:'+str(self.settings.alien_points))
            print('外星人速度:'+str(self.settings.alien_speed))
            print('子弹速度:'+str(self.settings.bullet_speed))
            print('飞船速度:'+str(self.settings.ship_speed))

            #提高等级
            self.stats.level+=1
            self.sb.prep_level()

    def _check_events(self):
        '''响应按键和鼠标事件'''
        # 监听键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.saverecord()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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
            self.stats.saverecord()
            sys.exit()
        # 按esc键退出游戏
        elif event.key == pygame.K_ESCAPE:
            self.stats.saverecord()
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

        #绘制得分
        self.sb.show_score()
        #如果游戏处于非活动状态,就绘制Play按钮
        if not self.stats.game_active:
            self.button.draw_button()
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _create_aliens(self):
        '''创建外星人'''
        #创建一个外星人并计算一行可以容纳多个外星人

        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        #计算一行可以容纳多少外星人群
        available_space_x = self.settings.screen_width-3*alien_width
        number_aliens_x=available_space_x//(alien_width*2)
        #计算可以容纳几行外星人群
        ship_height=self.ship.rect.height
        available_space_y = (self.settings.screen_height-5*alien_height
                             -ship_height)
        number_rows=available_space_y//(alien_height*2)
        #创建外星人
        for number_row in range(number_rows):
            for alien_number in range(number_aliens_x):
                alien=Alien(self)
                alien.x=alien_width+2*alien_width*alien_number
                alien.y=alien_height*2+2*alien_height*number_row
                alien.rect.x=alien.x
                alien.rect.y=alien.y
                self.aliens.add(alien)

    def _update_aliens(self):
        '''更新外星人群中所有外星人的移动'''
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #检测是否有外星人到达屏幕底部
        self._check_aliens_bottom()

    def _ship_hit(self):
        '''响应飞船被外星人撞到'''
        if self.stats.ships_left>0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            #创建一群新的外星人,并将飞船放到屏幕底端中央
            self._create_aliens()
            self.ship.center_ship()
            # print('碰撞时飞船位置:'+str(self.ship.rect))
            #暂停
            sleep(0.2)
        else:
            self.stats.game_active=False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        '''有外星人到达边缘时采取相应的措施'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''将整行外星人下移,并改变他们的方向'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        '''检查是否有外星人到达了屏幕底部'''
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        '''在玩家单击Play按钮时开始游戏'''
        if (self.button.rect.collidepoint(mouse_pos)
                and self.stats.game_active==False):
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()
            self._create_aliens()
            self.ship.center_ship()
            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)



if __name__ == '__main__':
    # 创建游戏实例并运行
    ai = AlienInvasion()
    ai.run_game()
