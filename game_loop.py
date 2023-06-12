from numpy import cos, pi, sin
from time import time
import pygame as pg

from constants import consts as c
from structures import structure_manager as sm
from id_mapping import id_map
from items import item_manager as im
from images import img as i
from world import world as w


def game_loop():
    i.convert_alpha()

    while True:
        start = time()
        c.clock.tick(c.fps)

        keys_pressed = pg.key.get_pressed()
        move_player(keys_pressed)
        cell_row, cell_col, cell_x, cell_y = get_pointer_params()

        if c.const_state == 1:
            left, _, right = pg.mouse.get_pressed()
            if left:
                sm.add(cell_row, cell_col, id_map["conveyor"], c.rot_state)
            if right:
                sm.remove(cell_row, cell_col)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                if pg.K_0 < event.key < pg.K_6:
                    c.const_state = event.key - pg.K_0
                if event.key == pg.K_g:
                    c.toggle_gridlines()
                if event.key == pg.K_r or event.key == pg.K_l:
                    rotation = 1 if event.key == pg.K_r else -1
                    if sm.grid[cell_row][cell_col] != 0:
                        sm.rotate(cell_row, cell_col, rotation)
                    else:
                        c.cycle_rot_state(rotation)
                if event.key == pg.K_m or event.key == pg.K_n:
                    if event.key == pg.K_m:
                        c.cell_length += 5
                    else:
                        c.cell_length -= 5

                    i.reload_images()
                    sm.apply_zoom()
                    im.apply_zoom()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    sm.add(cell_row, cell_col, c.const_state - 1, c.rot_state)
                if event.button == 3:
                    if im.grid[cell_row][cell_col] != 0:
                        im.remove(cell_row, cell_col)
                    elif sm.grid[cell_row][cell_col] != 0:
                        sm.remove(cell_row, cell_col)

        c.screen.fill(c.bg_color)
        if c.show_gridlines:
            draw_gridlines()

        sm.update()
        im.update(sm)

        w.render()
        sm.render()
        im.render()

        if sm.grid[cell_row][cell_col] == 0:
            draw_action(cell_x, cell_y)
        else:
            sm.grid[cell_row][cell_col].render_tooltip()

        pg.display.flip()

        end = time()
        c.set_dt(end - start)


def move_player(keys_pressed):
    if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
        c.player_y -= c.player_speed * c.dt
        if c.player_y < 0:
            c.player_y = 0

    if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]:
        c.player_y += c.player_speed * c.dt
        if c.player_y + c.sh > c.num_cells * c.cell_length:
            c.player_y = c.num_cells * c.cell_length - c.sh

    if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
        c.player_x -= c.player_speed * c.dt
        if c.player_x < 0:
            c.player_x = 0

    if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
        c.player_x += c.player_speed * c.dt
        if c.player_x + c.sw > c.num_cells * c.cell_length:
            c.player_x = c.num_cells * c.cell_length - c.sw


def get_pointer_params():
    mouse_x, mouse_y = pg.mouse.get_pos()
    cell_row = int((mouse_y + c.player_y) / c.cell_length)
    cell_col = int((mouse_x + c.player_x) / c.cell_length)
    cell_x = cell_col * c.cell_length - c.player_x + 2
    cell_y = cell_row * c.cell_length - c.player_y + 2 

    return cell_row, cell_col, cell_x, cell_y


def draw_action(cell_x, cell_y):
    pg.draw.circle(c.screen, c.action_color, (cell_x + c.cell_length // 2, cell_y + c.cell_length // 2), 4 * c.cell_length // 5, 2)

    if c.const_state == 1:
        c.screen.blit(i.images[id_map["conveyor"]][c.rot_state], (cell_x - 1, cell_y - 1))

    elif c.const_state == 2:
        c.screen.blit(i.images[id_map["arm"]], (cell_x - 1, cell_y - 1))
        angle = ((1 - c.rot_state) * pi / 2) % (2 * pi)

        start_x = cell_x + c.cell_length // 2
        start_y = cell_y + c.cell_length // 2
        end_x = start_x + c.cell_length * cos(angle)
        end_y = start_y - c.cell_length * sin(angle)

        pg.draw.line(c.screen, c.arm_color, (start_x, start_y), (end_x, end_y), 2)
        draw_source(cell_x, cell_y, (c.rot_state + 2) % 4)
        draw_target(cell_x, cell_y, (c.rot_state + 2) % 4)

    elif c.const_state == 3:
        c.screen.blit(i.images[id_map["mine"]], (cell_x - 1, cell_y - 1))
        draw_target(cell_x, cell_y, c.rot_state)        
    elif c.const_state == 4:
        c.screen.blit(i.images[id_map["furnace"]], (cell_x - 1, cell_y - 1))
        draw_target(cell_x, cell_y, c.rot_state)
    elif c.const_state == 5:
        c.screen.blit(i.images[id_map["factory"]], (cell_x - 1, cell_y - 1))
        draw_target(cell_x, cell_y, c.rot_state)


def draw_target(cell_x, cell_y, state):
    translations = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    x = cell_x + translations[state][0] * c.cell_length - c.player_x
    y = cell_y + translations[state][1] * c.cell_length - c.player_y
    pg.draw.rect(c.screen, c.target_color, (x, y, c.cell_length, c.cell_length), 3)


def draw_source(source_x, source_y, state):
    translations = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    x = source_x + translations[state][0] * c.cell_length - c.player_x
    y = source_y + translations[state][1] * c.cell_length - c.player_y
    pg.draw.rect(c.screen, c.source_color, (x, y, c.cell_length, c.cell_length), 3)


def draw_gridlines():
    for x in range(0, c.num_cells * c.cell_length, c.cell_length):
        pg.draw.line(c.screen, c.grid_color, (x - c.player_x, 0), (x - c.player_x, c.sh))
    for y in range(0, c.num_cells * c.cell_length, c.cell_length):
        pg.draw.line(c.screen, c.grid_color, (0, y - c.player_y), (c.sw, y - c.player_y))


if __name__ == '__main__':
    # this should directly lead to a game
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()
    c.set_screen(screen)
    c.set_clock(clock)
    game_loop()