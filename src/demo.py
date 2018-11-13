#encode:utf-8
'''
demo
'''
# import random
import os.path
import pygame
from pygame.locals import *

#
# constant
#
SCREENRECT = Rect(0, 0, 640, 480)
# 设置背景颜色和线条颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (128, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

main_dir = os.path.split(os.path.abspath(__file__))[0]

#
# global
#
begin_point = 0 # touch begin point
move_point = 0 # touch move point
end_point = 0 # touch end point
screen = 0 # screen
mouse = 0 # mouse icon
points = [] # mouse click, add circle

def distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return pow(dx*dx + dy*dy, 0.5)

def load_image(file):
    '''load image'''
    file = os.path.join(main_dir, '..', 'res', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def handle_event():
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if not on_key_up(event.dict):
                return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            touch_begin(event.dict)
        if event.type == pygame.MOUSEMOTION:
            touch_move(event.dict)
        if event.type == pygame.MOUSEBUTTONUP:
            touch_end(event.dict)
    return True

def on_key_down(e):

    pass

def on_key_up(e):
    if e['key'] == pygame.K_ESCAPE:
        pygame.quit()
        return False
    return True

def touch_begin(e):
    if e['button'] != 1:
        return
    global begin_point
    begin_point = e['pos']
    pass

def touch_move(e):
    global move_point, mouse
    mouse = e['pos']
    if e['buttons'] != (1, 0, 0):#left button NOT clicked
        return
    if begin_point != 0:
        move_point = e['pos']
    pass

def touch_end(e):
    if e['button'] != 1:
        return
    global begin_point, move_point
    begin_point = 0
    move_point = 0
    points.append(e['pos'])
    pass

def draw_mouse():
    global screen, mouse
    if mouse != 0:
        pygame.draw.circle(screen, RED, mouse, 3, 3)

def update_game(updates):
    global screen
    screen.fill(GRAY)
    draw_mouse()
    pos = 0
    if begin_point != 0:
        pos = begin_point
    if move_point != 0:
        pos = move_point
    if pos != 0:# temp circle
        pygame.draw.circle(screen, PINK, pos, 10, 1)
        for p in points:
            if distance(p, pos) < 100:
                pygame.draw.line(screen, RED, p, pos, 1)
    for point in points:# sure circle
        pygame.draw.circle(screen, RED, point, 10, 1)
    for i in range(len(points)):
        for j in range(i, len(points)):
            if i == j:
                continue
            p1 = points[i]
            p2 = points[j]
            if distance(p1, p2) < 100:
                pygame.draw.line(screen, RED, p1, p2, 1)
    for p in points:
        if distance(mouse, p) < 30:
            pygame.draw.circle(screen, RED, p, 10, 3)
    pygame.display.flip()
    dirty = updates.draw(screen)
    pygame.display.update(dirty)

def start_game():
    '''start game'''
    global screen
    pygame.init()

    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    pygame.display.flip()
    updates = pygame.sprite.RenderUpdates()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Test')
    pygame.mouse.set_visible(0)
    while True:
        if not handle_event():
            return
        updates.clear(screen, screen)
        updates.update()
        update_game(updates)
        clock.tick(60)
    pygame.time.wait(1000)
    pygame.quit()

if __name__ == '__main__':
    start_game()
