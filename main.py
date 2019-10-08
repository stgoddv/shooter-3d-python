
import time
import math
import tkinter
from tkinter import Label
from tkinter import ttk

def Screen2Text(screen, nScreenWidth):
    screen = ''.join(screen)
    return '\n'.join([screen[i:i+nScreenWidth] for i in range(0, len(screen), nScreenWidth)])

def draw_text(Canvas, text, px_x, px_y, args = None):
    l = Label(Canvas, text=text, **args) if args else Label(Canvas, text=text)
    l.place(x=px_x, y=px_y, anchor='nw')
    l.config(font='TkFixedFont')

def draw_screen(Canvas, screen, nScreenWidth, args = None):
    draw_text(Canvas, Screen2Text(screen, nScreenWidth), 0, 0, args=args)

nScreenHeight = 25
nScreenWidth = 80

pxByHeight = 17
pxByWidth = 8

HEIGHT = nScreenHeight * pxByHeight
WIDTH = int(nScreenWidth * pxByWidth)

screen = [' ' for i in range(nScreenHeight*nScreenWidth)]

k_down = 0
k_code = set()

def k_down_e(e):
    global k_down
    global k_code
    k_code.add(e.keycode)
    k_down += 1

def k_up_e(e):
    global k_down
    global k_code
    k_code.remove(e.keycode)
    k_down -= 1

top = tkinter.Tk()
top.bind('<KeyPress>', k_down_e)
top.bind('<KeyRelease>', k_up_e)

top.title('First Person Shooter 3D')
C = tkinter.Canvas(top, bg="white", height=HEIGHT, width=WIDTH)
theme = {'fg':'white', 'bg':'black'}

player_x = 8.
player_y = 8.
player_a = 0.
n_map_width = 16
n_map_height = 16
map = ''

map += "################"
map += "#..............#"
map += "#..............#"
map += "#..#...........#"
map += "#..#####.......#"
map += "#..#...........#"
map += "#..#...........#"
map += "#..............#"
map += "#..............#"
map += "#.........######"
map += "#..............#"
map += "#..............#"
map += "#..............#"
map += "#..............#"
map += "#..............#"
map += "################"

fov = 3.14159 / 4.
f_depth = 16.

tp1 = time.time()
tp2 = time.time()

elapsed = 0
def timeChanged():
    global elapsed, theme, nScreenWidth, fov, f_depth, k_down, k_code, player_a, player_x, player_y
    global tp1, tp2
    C.delete("all")

    tp2 = time.time()
    elapsed_time = tp2 - tp1
    tp1 = tp2

    # Rotate
    if k_down and 113 in k_code: player_a -= 1. * elapsed_time
    if k_down and 114 in k_code: player_a += 1. * elapsed_time

    # Forward Backwards
    if k_down and 111 in k_code:
        player_x += math.sin(player_a) * 1. * elapsed_time
        player_y += math.cos(player_a) * 1. * elapsed_time
    if k_down and 116 in k_code:
        player_x -= math.sin(player_a) * 1. * elapsed_time
        player_y -= math.cos(player_a) * 1. * elapsed_time

    # Lateral
    if k_down and 38 in k_code:
        player_x += -math.cos(player_a) * 1. * elapsed_time
        player_y += math.sin(player_a) * 1. * elapsed_time
    if k_down and 40 in k_code:
        player_x -= -math.cos(player_a) * 1. * elapsed_time
        player_y -= math.sin(player_a) * 1. * elapsed_time

    for x in range(nScreenWidth):
        ray_angle = (player_a - fov / 2.) + (x / nScreenWidth) * fov

        distance_2_wall = 0
        hit_wall = False

        eye_x = math.sin(ray_angle)
        eye_y = math.cos(ray_angle)

        while not hit_wall and distance_2_wall < f_depth:
            distance_2_wall += 0.5

            n_test_x = int(player_x + eye_x * distance_2_wall)
            n_test_y = int(player_y + eye_y * distance_2_wall)

            if (n_test_x < 0 or n_test_x >= n_map_width or n_test_y < 0 or n_test_y >= n_map_height):
                # Outbounds
                hit_wall = True
                distance_2_wall = f_depth
            else:
                # Inbounds
                if (map[n_test_y * n_map_width + n_test_x] == '#'): hit_wall = True

        # Calculate distance to ceiling and floor
        n_ceiling = (nScreenHeight / 2.) - nScreenHeight / distance_2_wall
        n_floor = nScreenHeight - n_ceiling

        n_shade = ' '
        if (distance_2_wall <= f_depth / 4.): n_shade = u"\u2588"
        elif (distance_2_wall <= f_depth / 3.): n_shade = u"\u2593"
        elif (distance_2_wall <= f_depth / 2.): n_shade = u"\u2592"
        elif (distance_2_wall <= f_depth): n_shade = u"\u2591"
        else: n_shade = ' '

        for y in range(nScreenHeight):
            if (y < n_ceiling):
                screen[y * nScreenWidth + x] = ' '
            elif (y > n_ceiling and y <= n_floor):
                screen[y * nScreenWidth + x] = n_shade
            else:
                screen[y * nScreenWidth + x] = ' '

    draw_screen(C, screen, nScreenWidth, args=theme)
    C.pack()
    elapsed += 1
    if elapsed < 100000: top.after(100, timeChanged)

timeChanged()
top.mainloop()
