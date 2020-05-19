'''the main display, 
set up and control of images/text/menus on the screen'''

from adafruit_touchscreen import Touchscreen
from displayio import Group
import displayio
import board
import time
# from adafruit_pyportal import PyPortal

# pyportal display set up
display = board.DISPLAY
display.rotation = 0

# Touchscreen setup
screen_width = display.width
screen_height = display.height

# if display rotation = 270:
if display.rotation == 0:
    ts = Touchscreen(   board.TOUCH_XL, board.TOUCH_XR,
                        board.TOUCH_YD, board.TOUCH_YU,
                        calibration=(   (5200, 59000), 
                                        (5800, 57000) ),
                        size=(screen_width, screen_height) )

elif display.rotation == 90:
    ts = Touchscreen(   board.TOUCH_YU, board.TOUCH_YD,
                        board.TOUCH_XL, board.TOUCH_XR, 
                        calibration=(   (5200, 59000), 
                                        (5800, 57000) ),
                        size=(240, 320) )

elif display.rotation == 180:
    ts = Touchscreen(   board.TOUCH_XR, board.TOUCH_XL,
                        board.TOUCH_YU, board.TOUCH_YD,
                        calibration=(   (5200, 59000), 
                                        (5800, 57000) ),
                        size=(320, 240) )

elif display.rotation == 270:
    ts = Touchscreen(   board.TOUCH_YD, board.TOUCH_YU,
                        board.TOUCH_XR, board.TOUCH_XL,
                        calibration=(   (5200, 59000), 
                                        (5800, 57000) ),
                        size=(240, 320) )

splash = Group(max_size=10)