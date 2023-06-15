from math import cos, pi, sin
import pygame as pg

from constants import consts as c
from id_mapping import id_map
from images import img as i
from ui.game_ui import ui


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
        ui.render_text("Place Conveyor: (L/R) to rotate")

    if c.const_state == 2:
        c.screen.blit(i.images[id_map["conveyor_underground"]][c.rot_state], (cell_x - 1, cell_y - 1))
        translations = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        x = cell_x + translations[c.rot_state][0] * c.ug_state * c.cell_length
        y = cell_y - translations[c.rot_state][1] * c.ug_state * c.cell_length
        c.screen.blit(i.images[id_map["conveyor_underground"]][c.rot_state + 4], (x, y))
        pg.draw.circle(c.screen, c.action_color, (x + c.cell_length // 2, y + c.cell_length // 2), 4 * c.cell_length // 5, 2)
        ui.render_text("Place Underground Conveyor: (L/R) to rotate (Shift/Ctrl) to change length")

    elif c.const_state == 3:
        c.screen.blit(i.images[id_map["splitter"]][c.rot_state], (cell_x - 1, cell_y - 1))
        translations = [[(-1, 1), (1, 1)], [(1, -1), (1, 1)], [(1, -1), (-1, -1)], [(-1, 1), (-1, -1)]]
        x1 = cell_x + translations[c.rot_state][0][0] * c.cell_length
        y1 = cell_y - translations[c.rot_state][0][1] * c.cell_length
        x2 = cell_x + translations[c.rot_state][1][0] * c.cell_length
        y2 = cell_y - translations[c.rot_state][1][1] * c.cell_length
        pg.draw.rect(c.screen, c.target_color, (x1, y1, c.cell_length, c.cell_length), 3)
        pg.draw.rect(c.screen, c.target_color, (x2, y2, c.cell_length, c.cell_length), 3)
        ui.render_text("Place Splitter: (L/R) to rotate")

    elif c.const_state == 4:
        c.screen.blit(i.images[id_map["arm"]], (cell_x - 1, cell_y - 1))
        angle = ((1 - (c.rot_state + 2) % 4) * pi / 2) % (2 * pi)

        start_x = cell_x + c.cell_length // 2
        start_y = cell_y + c.cell_length // 2
        end_x = start_x + c.cell_length * cos(angle)
        end_y = start_y - c.cell_length * sin(angle)

        pg.draw.line(c.screen, c.arm_color, (start_x, start_y), (end_x, end_y), 2)
        draw_source(cell_x, cell_y, c.rot_state)
        draw_target(cell_x, cell_y, c.rot_state)
        ui.render_text("Place Arm: (L/R) to rotate")

    elif c.const_state == 5:
        c.screen.blit(i.images[id_map["mine"]], (cell_x - 1, cell_y - 1))
        draw_target(cell_x, cell_y, c.rot_state) 
        ui.render_text("Place Mine: (L/R) to rotate") 

    elif c.const_state == 6:
        c.screen.blit(i.images[id_map["furnace"]], (cell_x - 1, cell_y - 1))
        draw_target(cell_x, cell_y, c.rot_state)
        ui.render_text("Place Furnace: (L/R) to rotate")

    elif c.const_state == 7:
        c.screen.blit(i.images[id_map["factory"]], (cell_x - 1, cell_y - 1))
        draw_target(cell_x, cell_y, c.rot_state)
        ui.render_text("Place Factory: (L/R) to rotate")


def draw_target(cell_x, cell_y, state):
    translations = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    x = cell_x + translations[state][0] * c.cell_length
    y = cell_y + translations[state][1] * c.cell_length
    pg.draw.rect(c.screen, c.target_color, (x, y, c.cell_length, c.cell_length), 3)


def draw_source(source_x, source_y, state):
    translations = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    x = source_x + translations[state][0] * c.cell_length
    y = source_y + translations[state][1] * c.cell_length
    pg.draw.rect(c.screen, c.source_color, (x, y, c.cell_length, c.cell_length), 3)


def draw_gridlines():
    for x in range(0, c.num_cells * c.cell_length, c.cell_length):
        pg.draw.line(c.screen, c.grid_color, (x - c.player_x, 0), (x - c.player_x, c.sh))
    for y in range(0, c.num_cells * c.cell_length, c.cell_length):
        pg.draw.line(c.screen, c.grid_color, (0, y - c.player_y), (c.sw, y - c.player_y))