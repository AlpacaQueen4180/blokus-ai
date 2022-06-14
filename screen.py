from PIL import ImageGrab
from PIL import Image
import time
from gamestate import *
# import numpy as np


# def get_screen():
#     img = ImageGrab.grab()
#     agent_id = check_id(img)
#     while True:
#         screen = ImageGrab.grab()
#         screen.save('screen.png')
#         if check_id('screen.png') == agent_id:
#             get_board()
#         time.sleep(5)


def get_board_from_screen(board: Board):
    """
    Updates the board in place with the screen content.
    """
    screen = ImageGrab.grab((590, 370, 1495, 1275))
    tile = (904 / (BOARD_COL - 1), 904 / (BOARD_ROW - 1))
    # agent_id = check_id(screen)
    for x in range(BOARD_COL):
        for y in range(BOARD_ROW):
            coord = (round(tile[0] * x), round(tile[1] * y))
            color = screen.getpixel(coord)
            # screen.putpixel(coord, (0, 0, 0))
            id = check_color(color)
            board.state[x][BOARD_ROW - 1 - y] = id
    # screen.show()


def check_color(color):
    if color == (68, 119, 198):
        player_id = 0  # blue
    elif color == (14, 168, 96):
        player_id = 1  # green
    elif color == (137, 13, 116):
        player_id = 2  # purple
    elif color == (255, 173, 51):
        player_id = 3  # orange
    else:
        player_id = '_'
    return player_id


def check_id():
    # img.convert('RGB')
    img = ImageGrab.grab()
    if img.getpixel((90, 785)) != ((237, 240, 247)): raise Exception("Not a Blokus screen")
    if img.getpixel((90, 340)) != (237, 240, 247):
        agent_id = 0    # blue
    elif img.getpixel((90, 870)) != (230, 246, 239):
        agent_id = 1    # green
    elif img.getpixel((1615, 870)) != (235, 230, 242):
        agent_id = 2    # purple
    elif img.getpixel((1615, 340)) != (254, 249, 231):
        agent_id = 3    # orange
    return agent_id
