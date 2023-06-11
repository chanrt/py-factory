from numpy import cos, pi, sin
from time import time
import pygame as pg


from arms import arm_manager as am
from constants import consts as c
from grid import grid_manager as gm
from items import item_manager as im
from images import img as i
from world import world as w


def game_loop():
    i.convert_alpha()

    im.add_item(5, 5, 3)
    im.add_item(7, 5, 4)
    im.add_item(8, 5, 5)
    im.add_item(9, 5, 6)

    while True:
        start = time()
        c.clock.tick(c.fps)

        keys_pressed = pg.key.get_pressed()
        played_moved = move_player(keys_pressed)
        cell_row, cell_col, cell_x, cell_y = get_pointer_params()

        if c.const_state == 1:
            left, _, right = pg.mouse.get_pressed()
            if left:
                gm.update(c.conveyor_state, (cell_row, cell_col))
            if right:
                gm.destroy((cell_row, cell_col))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                
                if pg.K_0 < event.key < pg.K_6:
                    c.const_state = event.key - pg.K_0
                
                # toggles
                if event.key == pg.K_g:
                    c.toggle_gridlines()
                if event.key == pg.K_r:
                    gm.toggle_rotation((cell_row, cell_col))
                    am.toggle_rotation(cell_row, cell_col)

                    if c.const_state == 1:
                        c.cycle_conveyor_state()
                    if c.const_state == 2:
                        c.cycle_arm_state()
                    if c.const_state == 3:
                        c.cycle_mine_state()
                if event.key == pg.K_l:
                    gm.toggle_rotation((cell_row, cell_col), -1)
                    am.toggle_rotation(cell_row, cell_col, -1)

                    if c.const_state == 1:
                        c.cycle_conveyor_state(-1)
                    if c.const_state == 2:
                        c.cycle_arm_state(-1)
                    if c.const_state == 3:
                        c.cycle_mine_state(-1)

                # zoom in/out
                if event.key == pg.K_m or event.key == pg.K_n:
                    if event.key == pg.K_m:
                        c.cell_length += 5
                    else:
                        c.cell_length -= 5

                    i.reload_images()
                    am.apply_zoom()
                    im.apply_zoom()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if c.const_state == 2:
                        gm.update(6, (cell_row, cell_col))
                        am.add_arm(cell_row, cell_col, c.arm_state)
                    if c.const_state == 3:
                        gm.update(10, (cell_row, cell_col))
                    if c.const_state == 4:
                        gm.update(11, (cell_row, cell_col))
                    if c.const_state == 5:
                        gm.update(12, (cell_row, cell_col))
                if event.button == 3:
                    im.remove_item(cell_row, cell_col)
                    gm.destroy((cell_row, cell_col))
                    am.remove_arm(cell_row, cell_col)

        c.screen.fill(c.bg_color)

        if c.show_gridlines:
            draw_gridlines()

        im.update()
        am.update()

        w.render()
        gm.render()
        im.render()
        am.render()

        if gm.grid[cell_row, cell_col] == 0:
            draw_action(cell_x, cell_y)

        pg.display.flip()

        end = time()
        c.set_dt(end - start)


def move_player(keys_pressed):
    moved = False

    if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
        c.player_y -= c.player_speed * c.dt
        moved = True
        if c.player_y < 0:
            c.player_y = 0

    if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]:
        c.player_y += c.player_speed * c.dt
        moved = True
        if c.player_y + c.sh > c.num_cells * c.cell_length:
            c.player_y = c.num_cells * c.cell_length - c.sh

    if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
        c.player_x -= c.player_speed * c.dt
        moved = True
        if c.player_x < 0:
            c.player_x = 0

    if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
        c.player_x += c.player_speed * c.dt
        moved = True
        if c.player_x + c.sw > c.num_cells * c.cell_length:
            c.player_x = c.num_cells * c.cell_length - c.sw

    return moved


def get_pointer_params():
    mouse_x, mouse_y = pg.mouse.get_pos()
    cell_row = int((mouse_y + c.player_y) / c.cell_length)
    cell_col = int((mouse_x + c.player_x) / c.cell_length)
    cell_x = cell_col * c.cell_length - c.player_x + 2
    cell_y = cell_row * c.cell_length - c.player_y + 2 

    return cell_row, cell_col, cell_x, cell_y


def draw_action(cell_x, cell_y):
    pg.draw.circle(c.screen, c.action_color, (cell_x + c.cell_length // 2, cell_y + c.cell_length // 2), c.cell_length, 2)

    if c.const_state == 1:
        c.screen.blit(i.images[c.conveyor_state], (cell_x - 1, cell_y - 1))
    elif c.const_state == 2:
        c.screen.blit(i.images[6], (cell_x - 1, cell_y - 1))
        start_x = cell_x + c.cell_length // 2
        start_y = cell_y + c.cell_length // 2

        if c.arm_state == 1:
            angle = pi / 2
        elif c.arm_state == 2:
            angle = 0
        elif c.arm_state == 3:
            angle = 3 * pi / 2
        elif c.arm_state == 4:
            angle = pi

        end_x = start_x + c.cell_length * cos(angle)
        end_y = start_y - c.cell_length * sin(angle)

        pg.draw.line(c.screen, c.arm_color, (start_x, start_y), (end_x, end_y), 2)
    elif c.const_state == 3:
        c.screen.blit(i.images[10], (cell_x - 1, cell_y - 1))
        translations = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        x = cell_x + translations[c.mine_state - 1][0] * c.cell_length - c.player_x + c.cell_length // 2
        y = cell_y + translations[c.mine_state - 1][1] * c.cell_length - c.player_y + c.cell_length // 2
        pg.draw.circle(c.screen, c.sink_color, (x, y), c.cell_length // 3)
            
    elif c.const_state == 4:
        c.screen.blit(i.images[11], (cell_x - 1, cell_y - 1))
    elif c.const_state == 5:
        c.screen.blit(i.images[12], (cell_x - 1, cell_y - 1))


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