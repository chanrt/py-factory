import pygame as pg

from constants import consts as c
from grid import grid as g


def game_loop():
    while True:
        keys_pressed = pg.key.get_pressed()
        played_moved = move_player(keys_pressed)
        cell_row, cell_col, cell_x, cell_y = get_pointer_params()

        if c.const_state == 1:
            left, _, right = pg.mouse.get_pressed()
            if left:
                g.update(c.conveyor_state, (cell_row, cell_col))
            if right:
                g.destroy((cell_row, cell_col))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                
                if event.key == pg.K_g:
                    c.toggle_gridlines()

                if event.key == pg.K_r:
                    g.toggle_rotation((cell_row, cell_col))
                    if c.const_state == 1:
                        c.cycle_conveyor_state()

        c.screen.fill(c.bg_color)

        if c.show_gridlines:
            draw_gridlines()

        pg.draw.rect(c.screen, c.highlight_color, (cell_x, cell_y, c.cell_length - 3, c.cell_length - 3))

        g.render()

        pg.display.flip()


def move_player(keys_pressed):
    moved = False

    if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
        c.player_y -= c.player_speed
        moved = True
        if c.player_y < 0:
            c.player_y = 0

    if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]:
        c.player_y += c.player_speed
        moved = True
        if c.player_y + c.sh > c.num_cells * c.cell_length:
            c.player_y = c.num_cells * c.cell_length - c.sh

    if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
        c.player_x -= c.player_speed
        moved = True
        if c.player_x < 0:
            c.player_x = 0

    if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
        c.player_x += c.player_speed
        moved = True
        if c.player_x + c.sw > c.num_cells * c.cell_length:
            c.player_x = c.num_cells * c.cell_length - c.sw

    return moved


def get_pointer_params():
    mouse_x, mouse_y = pg.mouse.get_pos()
    cell_row = (mouse_y + c.player_y) // c.cell_length
    cell_col = (mouse_x + c.player_x) // c.cell_length
    cell_x = cell_col * c.cell_length - c.player_x + 2
    cell_y = cell_row * c.cell_length - c.player_y + 2 

    return cell_row, cell_col, cell_x, cell_y


def draw_gridlines():
    for x in range(0, c.num_cells * c.cell_length, c.cell_length):
        pg.draw.line(c.screen, c.grid_color, (x - c.player_x, 0), (x - c.player_x, c.sh))
    for y in range(0, c.num_cells * c.cell_length, c.cell_length):
        pg.draw.line(c.screen, c.grid_color, (0, y - c.player_y), (c.sw, y - c.player_y))


if __name__ == '__main__':
    # this should directly lead to a game

    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen(screen)
    game_loop()