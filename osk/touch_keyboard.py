'''Touch keyboard class module. will display list of keys/buttons
returns the string compiled by the key presses.'''

from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from adafruit_button import Button
from displayio import Group
from terminalio import FONT
from collections import namedtuple
import board, time
from adafruit_pyportal import PyPortal

from colors import *
from display_setup import display, ts, splash, screen_height, screen_width

font = FONT
font2 = bitmap_font.load_font("/fonts/Roboto-Medium-16.bdf")
glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: '
font2.load_glyphs(glyphs)


class TouchKeys:
    '''Touch keyboard for pyportal usage.'''

    # Settings
    BUTTON_WIDTH, BUTTON_HEIGHT = 48, 40
    BUTTON_COLOR, BUTTON_TEXT_COLOR = LIGHT_GRAY, BLACK
    BUTTON_MARGIN, PADDING = 0, 0
    MAX_CHARS = 300
    LEFT_START, TOP_START = 1, 114
    CAPITALIZED = True

    Coords = namedtuple("Point", "x y")
    buttons = []

    alpha_keys_caps = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'DEL',
        'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/',
        'CAPS', 'SYM', ' ', 'RETURN', '???'
    ]

    alpha_keys_lower = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'DEL',
        'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',
        'CAPS', 'SYM', ' ', 'RETURN', '???'
    ]

    symbol_keys = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        '`', '~', '!', '@', '#', '$', '%', '^', '&', '*',
        '(', ')', '-', '=', '_', '+', '{', '}', '[', ']',
        ';', "'", ':', '"', '<', '>', '?', ',', '.', '/',
        '\\', '|', 'ABC', 'RETURN', '???'
    ]

    key_sets = [
        alpha_keys_caps,
        alpha_keys_lower,
        symbol_keys
    ]

    # draw rectangle to hold the text stuff.
    text_area = Rect(0, 2, screen_width - 0, 108, fill=DARK_GRAY, outline=PINK_ISH)
    # create label area for text to show in.
    text_box = Label(font2, text="", color=LIGHT_GRAY, max_glyphs=MAX_CHARS, x=10, y=16)

    # define all the groups for the OSK for each key set:
    main_group = Group( max_size=( len(alpha_keys_caps) + 4 ) )

    main_group.append(text_area)
    main_group.append(text_box)

    def __init__(self):
        '''load the parts and display the keyboard and text entry box'''
        print('Loading keyboard')
        self.load_buttons(self.key_sets[0])
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        splash.pop()
        
    def edit_text(self):
        pass

    # Some button functions
    def button_grid(self, row, col):
        return self.Coords(self.BUTTON_MARGIN * (row + self.PADDING) + self.BUTTON_WIDTH * row + self.LEFT_START,
                    self.BUTTON_MARGIN * (col + self.PADDING) + self.BUTTON_HEIGHT * col + self.TOP_START)
    
    def add_button(self, row, col, label, width=1, color=LIGHT_GRAY, text_color=BLACK):
        pos = self.button_grid(row, col)
        new_button = Button(x=pos.x, y=pos.y,
                            width=self.BUTTON_WIDTH * width + self.BUTTON_MARGIN * (width - 1),
                            height=self.BUTTON_HEIGHT, label=label, label_font=font,
                            label_color=text_color, fill_color=color, style=Button.SHADOWRECT)
        self.buttons.append(new_button)
        return new_button
    
    def find_button(self, label):
        result = None
        for _, btn in enumerate(self.buttons):
            if btn.label == label:
                result = btn
        return result

    def load_buttons(self, key_set):
        x, y = 0, 0
        btn_width = 1
        for char in key_set:
            if y == 4:
                btn_width = 2
                if x > 0:
                    x += 1
            self.add_button(x, y, char, width=btn_width)
            x += 1
            if x == 10:
                x = 0
                y += 1
        for btn in self.buttons:
            self.main_group.append(btn.group)

    def switch_alpha_symbol(self, input_char):
        # print('SWITCH TO ALPHA or SYMBOL KEY SET!')
        if input_char == 'ABC':
            if self.CAPITALIZED:
                cap = 0
            elif not self.CAPITALIZED:
                cap = 1
            # print(f'Cap setting: {cap}')
            for b, btn in enumerate(self.buttons):
                btn.label = self.key_sets[cap][b]
        elif input_char == 'SYM':
            for b, btn in enumerate(self.buttons):
                btn.label = self.key_sets[2][b]
        time.sleep(0.75)

    def delete_text_char(self):
        # print('THIS NEEDS TO DELETE SOMETHING')
        if len(self.text_box.text) > 0:
            self.text_box.text = self.text_box.text[:-1]

    def switch_capitalization(self):
        if self.CAPITALIZED:
            # print('Switch to Lower Case set')
            for b, btn in enumerate(self.buttons):
                # print(self.key_sets[0][b])
                btn.label = self.key_sets[1][b]
        elif not self.CAPITALIZED:
            # print('Switch to Upper Case Set')
            for b, btn in enumerate(self.buttons):
                # print(self.key_sets[1][b])
                btn.label = self.key_sets[0][b]
        self.CAPITALIZED = not self.CAPITALIZED
        time.sleep(0.75)

    def update_text(self, text_from_buttons):
        self.text_box.text += text_from_buttons

    def show(self, target_group):
        '''Get the keyboard to show on the display :crosses fingers:'''
        # print('SHOW ME THE KEYBOARD!')
        target_group.append(self.main_group)
        text_input = ''
        touched = False
        while True:
            touch = ts.touch_point
            if touch:
                # print(touch)
                for btn in self.buttons:
                    if btn.contains(touch) and touched == False:
                        touched = True
                        input_char = btn.label
                        # print(input_char)
                        if input_char == 'DEL':
                            # remove the last char added.
                            text_input = text_input[:-1]
                            self.delete_text_char()
                            # print(text_input)
                        elif input_char == 'CAPS':
                            self.switch_capitalization()
                        elif input_char == 'SYM' or input_char == 'ABC':
                            self.switch_alpha_symbol(input_char)
                        elif input_char == 'RETURN':
                            # return the typed shit to the outside world!
                            return text_input  
                        elif input_char == '???':
                            print('Uhh.....')
                        else:
                            self.update_text(input_char)
                            text_input += input_char
                            # print(text_input)
                    elif touched and not btn.contains(touch):
                        # print('buttons released')
                        touched = False
                time.sleep(0.05)
