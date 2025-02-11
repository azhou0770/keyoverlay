import tkinter as tk
from datetime import datetime, timedelta
from PIL import Image, ImageTk, ImageDraw
from pynput import keyboard
from pynput.keyboard import Key
import cv2
import numpy as np

## SETTINGS
CLEAR_ROW_MILLIS = 2250
NEW_ROW_MILLIS = 1380
ROW_HEIGHT_PX = 60
MAGIC_FILE = 'magic.png'
BINDINGS_FILE = 'bindings.png'
ARROWS_FILE = 'arrows.png'
DISTANCE_BETWEEN_LABELS = 45
FONT = 'Verdana 12'
HOLD_MS_THRESHOLD = 75
##
# RESOLUTION:
ROW_WIDTH_PX = 410
HEIGHT = 900

class LabelRow:
    """
    A class to represent a row of labels in the overlay.

    Attributes:
        labels (list): A list of labels in the row.
        last_active (datetime): The timestamp of the last label added to the row.
    """
    def __init__(self, now):
        """
        Initializes a new LabelRow.

        Args:
            now (datetime): The current timestamp.
        """
        self.labels = []
        self.prev_label = None
        self.prev_key = None
        self.last_active = now

    def add_label(self, label, now, key):
        """
        Add a label to the row.

        Args:
            label: The label to be added.
            now (datetime): The current timestamp.
        """
        # Change the label if the previous label was a hold down
        # if self.prev_key and key != self.prev_key:
        #     current_fg_color = self.prev_label.cget('fg')
        #     if (current_fg_color == 'white'):
        #         self.prev_label.config(fg='#FFFF00')

        if self.prev_key and key == self.prev_key and now - self.last_active < timedelta(milliseconds=HOLD_MS_THRESHOLD):
            self.prev_label.config(fg='blue')
            # we end up not updating the self.labels list to reflect the change when modifying the prev_label
        else:
            time_diff_ms = int((now - self.last_active).total_seconds() * 1000)
            label_text = f"{time_diff_ms}ms" # Probably not necessary
            self.labels.append((label, now, label_text, time_diff_ms))
            self.prev_label = label
            self.prev_key = key
        self.last_active = now

    def destroy(self):
        """Destroy all labels in the row."""
        for label, _, _, _ in self.labels:
            label.destroy()
        self.labels = []
        self.prev_label = None
        self.prev_key = None
    def reposition(self, y, wraparound):
        """
        Reposition the labels in the row.

        Args:
            y (int): The vertical position for the labels.
            fixed_horizontal_distance (int): The horizontal distance between labels.
            wraparound (int): The maximum horizontal position before wrapping to the next row.

        Returns:
            int: The new vertical position after repositioning.
        """
        xpos = 0

        for label, _, _, _ in self.labels:
            label.place(x=xpos, y=y)
            xpos += DISTANCE_BETWEEN_LABELS

            # if xpos > wraparound:
            #     print("this shouldn't happpen")
            #     y += ROW_HEIGHT_PX
            #     xpos = 0

        return y + ROW_HEIGHT_PX

class LabelGrid:
    """
    A class to represent a grid of labels in the overlay.

    Attributes:
        last_active (int): The timestamp of the last label added to the grid.
        rows (list): A list of LabelRow instances.
    """
    def __init__(self):
        """Initialize an empty LabelGrid."""
        self.last_active = 0

        self.rows = []

    def add_label(self, root, img, now, key):
        """
        Add a label to the grid.

        Args:
            root: The Tkinter root window.
            img: The image to be displayed in the label.
            now (datetime): The current timestamp.
        """
        if len(self.rows) == 0 or \
           now - self.last_active > timedelta(milliseconds=NEW_ROW_MILLIS):
            self.rows.append(LabelRow(now))
        label_row = self.rows[-1]
        max_labels = ROW_WIDTH_PX//(ICON_SIZE + (DISTANCE_BETWEEN_LABELS - ICON_SIZE))
        if len(label_row.labels) == max_labels:
            self.rows.append(LabelRow(now))
            label_row = self.rows[-1]

        if not self.last_active:
            label = tk.Label(root, image=img, borderwidth=0, compound='top', font = FONT)
        else:
            time_diff_ms = int((now - self.last_active).total_seconds() * 1000)
            label = tk.Label(root, image=img, borderwidth=0, text=f"{time_diff_ms}", compound='top', font = FONT, bg = '#000000', fg = '#FFFF00')
        label_row.add_label(label, now, key)
        self.last_active = now

    def add_label_release(self, root, img, now, key):
        """
        Add a label to the grid.

        Args:
            root: The Tkinter root window.
            img: The image to be displayed in the label.
            now (datetime): The current timestamp.
        """

        if len(self.rows) == 0 or \
           now - self.last_active > timedelta(milliseconds=NEW_ROW_MILLIS):
            self.rows.append(LabelRow(now))
        label_row = self.rows[-1]
        max_labels = ROW_WIDTH_PX//(ICON_SIZE + (DISTANCE_BETWEEN_LABELS - ICON_SIZE))
        if len(label_row.labels) == max_labels:
            self.rows.append(LabelRow(now))
            label_row = self.rows[-1]
        if self.last_active:
            time_diff_ms = int((now - self.last_active).total_seconds() * 1000)
            label = tk.Label(root, image=img, borderwidth=0, text=f"{time_diff_ms}", compound='top', font = FONT, bg = '#000000', fg = '#FF0000')
        else:
            label = tk.Label(root, image=img, borderwidth=0, compound='top', font = FONT)
        label_row.add_label(label, now, key)
        self.last_active = now

    def reposition(self, now, wraparound):
        """
        Reposition labels in the grid and clear old rows.

        Args:
            now (datetime): The current timestamp.
            wraparound (int): The maximum horizontal position before wrapping to the next row.
        """
        kept_rows = []
        for row in self.rows:
            if now - row.last_active > timedelta(milliseconds=CLEAR_ROW_MILLIS):
                row.destroy()
            else:
                kept_rows.append(row)
        self.rows = kept_rows
        y = 0
        for row in self.rows:
            y = row.reposition(y=y, wraparound=wraparound)

def find_origin():
    """
    Find the origin (starting point) for key icons on the overlay.

    Returns:
        tuple: A tuple of (row, column) representing the origin point.
    """
    magic = cv2.imread(MAGIC_FILE)
    bindings = cv2.imread(BINDINGS_FILE)
    res = cv2.matchTemplate(bindings, magic, cv2.TM_SQDIFF)
    return np.unravel_index(res.argmin(), res.shape)

keys = {}

keys['Key.esc'] = (0, 0)
keys['Key.f1'] = (0, 2)
keys['Key.f2'] = (0, 3)
keys['Key.f3'] = (0, 4)
keys['Key.f4'] = (0, 5)
keys['Key.f5'] = (0, 6.5)
keys['Key.f6'] = (0, 7.5)
keys['Key.f7'] = (0, 8.5)
keys['Key.f8'] = (0, 9.5)
keys['Key.f9'] = (0, 11)
keys['Key.f10'] = (0, 12)
keys['Key.f11'] = (0, 13)
keys['Key.f12'] = (0, 14)

keys[192] = (1, 0) # `
keys[49] = (1, 1) # 1
keys[50] = (1, 2) # 2
keys[51] = (1, 3) # 3
keys[52] = (1, 4) # 4
keys[53] = (1, 5) # 5
keys[54] = (1, 6) # 6
keys[55] = (1, 7) # 7
keys[56] = (1, 8) # 8
keys[57] = (1, 9) # 9
keys[48] = (1, 10) # 0
keys[189] = (1, 11) # -
keys[187] = (1, 12) # =

keys[81] = (2, 1.5) # q
keys[87] = (2, 2.5) # w
keys[69] = (2, 3.5) # e
keys[82] = (2, 4.5) # r
keys[84] = (2, 5.5) # t
keys[89] = (2, 6.5) # y
keys[85] = (2, 7.5) # u
keys[73] = (2, 8.5) # i
keys[79] = (2, 9.5) # o
keys[80] = (2, 10.5) # p
keys[219] = (2, 11.5) # [
keys[221] = (2, 12.5) # ]
keys[220] = (2, 13.75) # \

keys[65] = (3, 2) # a
keys[83] = (3, 3) # s
keys[68] = (3, 4) # d
keys[70] = (3, 5) # f
keys[71] = (3, 6) # g
keys[72] = (3, 7) # h
keys[74] = (3, 8) # j
keys[75] = (3, 9) # k
keys[76] = (3, 10) # l
keys[186] = (3, 11) # ;
keys[222] = (3, 12) # '

keys['Key.shift'] = (4, 0.75)
keys['Key.shift_l'] = (4, 0.75)
keys['Key.shift_r'] = (4, 0.75)
keys[90] = (4, 2.5) # z
keys[88] = (4, 3.5) # x
keys[67] = (4, 4.5) # c
keys[86] = (4, 5.5) # v
keys[66] = (4, 6.5) # b
keys[78] = (4, 7.5) # n
keys[77] = (4, 8.5) # m
keys[188] = (4, 9.5) # ,
keys[190] = (4, 10.5) # .

keys['Key.ctrl'] = (5, 0.25)
keys['Key.ctrl_l'] = (5, 0.25)
keys['Key.ctrl_r'] = (5, 0.25)
keys['Key.alt'] = (5, 3.25)
keys['Key.alt_l'] = (5, 3.25)
keys['Key.alt_r'] = (5, 3.25)
keys['Key.alt_gr'] = (5, 3.25)
keys['Key.space'] = (5, 7)

keys['Key.scroll_lock'] = (0, 16.25)
keys['Key.insert'] = (1, 15.25)
keys['Key.home'] = (1, 16.25)
keys['Key.page_up'] = (1, 17.25)
keys['Key.delete'] = (2, 15.25)
keys['Key.end'] = (2, 16.25)
keys['Key.page_down'] = (2, 17.25)

keys[37] = (0, 228) # left
keys[38] = (239, 0) # up
keys[39] = (0, 0) # right
keys[40] = (239, 228) # down

origin = find_origin()

ICON_SIZE = 32
ICON_MARGIN = 1
OFFSET_X = -1
OFFSET_Y = -104

def crop_key(kid):
    """
    Crop the key icon from the bindings image based on its position.

    Args:
        kid: The identifier of the key.

    Returns:
        tuple: A tuple of (x1, y1, x2, y2) representing the cropping coordinates.
    """
    oy, ox = origin
    r, c = keys[kid]
    x = int(ox + c * (ICON_SIZE + ICON_MARGIN) + OFFSET_X + 1e-3)
    y = int(oy + r * (ICON_SIZE + ICON_MARGIN) + OFFSET_Y + 1e-3)
    if r == 0:
        y -= 5
    if r == 0 and c > 6 and c < 10:
        x += 1
    if c > 14:
        if r > 3:
            x += 1
        x += 1
    if r == 2 and c == 13.75:
        x += 1
    if r == 3 or r == 4 or (r == 5 and c != 0.25):
        x -= 1
    return (x, y, x + ICON_SIZE, y + ICON_SIZE)


def crop_key_arrows(kid):
    x, y = keys[kid]
    SIZE = 172
    return (x, y, x + SIZE, y + SIZE)


def key_tkimage(bindings, kid):
    """
    Create a Tkinter PhotoImage from a cropped key image.

    Args:
        bindings: The bindings image.
        kid: The identifier of the key.

    Returns:
        ImageTk.PhotoImage: A Tkinter PhotoImage of the cropped key image.
    """
    img = bindings.crop(crop_key(kid))
    green = (0, 255, 0)
    ImageDraw.floodfill(img, (0            , 0), green)
    ImageDraw.floodfill(img, (ICON_SIZE - 1, 0), green)
    ImageDraw.floodfill(img, (0            , ICON_SIZE - 1), green)
    ImageDraw.floodfill(img, (ICON_SIZE - 1, ICON_SIZE - 1), green)
    return ImageTk.PhotoImage(img)

def key_tkimage_arrows(arrows, kid):
    img = arrows.crop(crop_key_arrows(kid))
    img = img.resize((ICON_SIZE, ICON_SIZE), Image.NEAREST)
    return ImageTk.PhotoImage(img)

def keyid(key):
    """
    Get the identifier of a pressed key.

    Args:
        key: The pressed key object.

    Returns:
        str or int: The identifier of the key.
    """
    if hasattr(key, 'vk'):
        return key.vk
    elif hasattr(key, 'name') and key.name in ['left', 'right', 'up', 'down']:
        return key.name
    else:
        return str(key)


def suppress_alt(event):
    return "break"  # Suppresses the default behavior of the Alt key

def suppress_ctrl_c(event):
    return "break"  # Suppresses the default behavior of Ctrl+C

if __name__ == "__main__":

    root = tk.Tk()
    root.title('Overlay')
    root.geometry(str(ROW_WIDTH_PX) + "x" + str(HEIGHT))
    root.configure(background='#00ff00')
    grid = LabelGrid()
    bindings = Image.open(BINDINGS_FILE)
    arrows = Image.open(ARROWS_FILE)
    
    root.bind("<KeyRelease-Alt_L>", suppress_alt)
    root.bind("<KeyRelease-Alt_R>", suppress_alt)
    root.bind("<KeyPress-Control_L>", suppress_alt)
    root.bind("<KeyRelease-Control_L>", suppress_alt)
    root.bind("<KeyPress-Control_R>", suppress_alt)
    root.bind("<KeyRelease-Control_R>", suppress_alt)
    root.bind("<Control-c>", suppress_ctrl_c)


    tk_keys = {kid: key_tkimage(bindings, kid) for kid in keys}

    tk_keys[Key.left.name] = key_tkimage_arrows(arrows, 37)
    tk_keys[Key.up.name] = key_tkimage_arrows(arrows, 38)
    tk_keys[Key.right.name] = key_tkimage_arrows(arrows, 39)
    tk_keys[Key.down.name] = key_tkimage_arrows(arrows, 40)

    for key, value in tk_keys.items():
        print(f"Key: {key}, Value: {value}")

    def on_press(key):
        """
        Callback function when a key is pressed.

        Args:
            key: The pressed key.
        """
        kid = keyid(key)

        if kid is None or kid not in tk_keys:
            return

        now = datetime.now()

        img = tk_keys[kid]
        grid.add_label(root, img, now=now, key=key)
        grid.reposition(now=now, wraparound=ROW_WIDTH_PX - ICON_SIZE)


    def on_release(key):
        """
        Callback function when a key is released.

        Args:
            key: The released key.
        """
        kid = keyid(key)

        if not hasattr(key, 'name') and not hasattr(key, 'vk'):
            return

        if kid is None or kid not in tk_keys:
            # print(f"Key {key} with keyid {kid} is not in tk_keys")
            return

        now = datetime.now()

        img = tk_keys[kid]
        grid.add_label_release(root, img, now=now, key=kid)
        grid.reposition(now=now, wraparound=ROW_WIDTH_PX - ICON_SIZE)

    listener = keyboard.Listener(on_press = on_press, on_release = on_release)
    listener.start()
    root.mainloop()