#encode:utf-8
'''
test
'''
# import random
import os.path
import pygame
from pygame.locals import *

SCREENRECT = Rect(0, 0, 640, 480)
# 设置背景颜色和线条颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
points = [(200, 75), (300, 25), (400, 75)]

main_dir = os.path.split(os.path.abspath(__file__))[0]
def load_image(file):
    '''load image'''
    file = os.path.join(main_dir, '..', 'res', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def start_game():
    '''start game'''
    pygame.init()

    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    background = load_image('bg.png')
    background = pygame.transform.scale(background, (32, 32))
    screen.blit(background, (100, 100))
    pygame.display.flip()
    alls = pygame.sprite.RenderUpdates()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Test')
    # pygame.mouse.set_visible(0)
    while True:
        for event in pygame.event.get():
            '''
            event.type == 2     key down    {'unicode': 'a', 'key': 97, 'mod': 0, 'scancode': 0}
            event.type == 3     key up      {'key': 97, 'mod': 0, 'scancode': 0}
                event.dict.key      97
                event.dict.unicode  'a'
            event.type == 4     mouse move
                event.dict.pos      x,y
                event.dict.rel      cur_pos - pre_pos
                event.dict.buttons  pressed button
                                    1   left button pressed while moving
                                    2   middle wheel
                                    3   right button
            event.type == 5     mouse down  {'pos': (499, 417), 'button': 1} 5
            event.type == 6     mouse up    {'pos': (499, 417), 'button': 1} 6
                event.dict.pos      x,y
                event.dict.button   1   mouse left button
                                    2   mouse middle wheel
                                    3   mouse right button
            '''
            if event.type == 3:
                if event.dict['key'] == 27: # key.escape
                    return

        # keystate = pygame.key.get_pressed()
        ''' 按键表，按下的键，对应位置的0变为1
        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,...) # total: 323
        '''
        alls.clear(screen, background)
        alls.update()
        screen.fill(WHITE)

        # 画不封闭的两条直线
        pygame.draw.lines(screen, GREEN, 0, points, 1)

        # 画不抗锯齿的一条直线
        pygame.draw.line(screen, BLUE, (100, 200), (540, 250), 1)

        # 画抗锯齿的一条直线
        pygame.draw.aaline(screen, BLUE, (100, 250), (540, 300), 1)
        pygame.display.flip()


        dirty = alls.draw(screen)
        pygame.display.update(dirty)
        clock.tick(60)
    pygame.time.wait(1000)
    pygame.quit()

if __name__ == '__main__':
    start_game()
