import pygame as pg

from constants import consts as c


def game_loop():
    

    while True:
        keys_pressed = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                
            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                cell_row = (mouse_y + c.player_y) // c.cell_length
                cell_col = (mouse_x + c.player_x) // c.cell_length
                print(cell_row, cell_col)
                
        move_player(keys_pressed)

        c.screen.fill(c.bg_color)

        draw_grid()

        pg.display.flip()


def move_player(keys_pressed):
    if keys_pressed[pg.K_UP]:
            c.player_y -= c.player_speed
            if c.player_y < 0:
                c.player_y = 0

    if keys_pressed[pg.K_DOWN]:
        c.player_y += c.player_speed
        if c.player_y + c.sh > c.num_cells * c.cell_length:
            c.player_y = c.num_cells * c.cell_length - c.sh

    if keys_pressed[pg.K_LEFT]:
        c.player_x -= c.player_speed
        if c.player_x < 0:
            c.player_x = 0

    if keys_pressed[pg.K_RIGHT]:
        c.player_x += c.player_speed
        if c.player_x + c.sw > c.num_cells * c.cell_length:
            c.player_x = c.num_cells * c.cell_length - c.sw


def draw_grid():
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