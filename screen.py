import PIL
from PIL import ImageGrab
from PIL import Image
import time
from gamestate import board
import numpy as np


def get_screen() : 
    start = ImageGrab.grab()
    start.save('start.png')
    agent_id = check_id()
    while True :
        screen = ImageGrab.grab()
        screen.save('screen.png')
        if check_id('screen.png') == agent_id :
            get_board()
        time.sleep(5)
def get_board() :
    screen = Image.open("screen.png")
    screen.convert('RGB')
    for x in range(20):
        for y in range(20):
            color = screen.getpixel(360 + 32*x, 805 + 32*y)
            id = check_color(color)
            if id == 0 : board.state[x][y] = '_'
            else : board.state[x][y] = id
def check_color(color) :
    if color == (35, 121, 198) : player = 1      #blue
    if color == (255, 169, 37) : player = 2      #green
    if color == (152, 0, 113) : player = 3       #purple
    if color == (0, 171, 102) : player = 4       #orange
    if color == (203, 213, 223) : player = 0
    return player
def check_id(picname) : 
    start = Image.open(picname)
    start.convert('RGB')
    if start.getpixel(50, 225) != (236, 240, 247) : agent_id = 1   #blue
    elif start.getpixel(50, 555) != (226, 247, 240) : agent_id = 2 #green
    elif start.getpixel(1000, 555) != (236, 230 ,242) : agent_id = 3    #purple
    elif start.getpixel(1000, 225) != (255, 249, 231) : agent_id = 4    #orange
    return agent_id
    
