from PIL import Image, ImageTk
from tkinter import Tk, Label 
import threading
import time

# The square size of the window.
WINDOW_SIZE = 900

# The number of width-wise pixels each rod will have.
ROD_WIDTH = 10

# The number of disks in the game.
DISK_COUNT = 6

# The number of width-wise pixels the smallest disk will have.
DISK_MINWIDTH = 40

# The number of height-wise pixels each disk will have.
DISK_THICKNESS = 30

# The RGB color value used to represent the disks.
DISK_COLOR = (255, 0, 0)

# The number of pixels which represents how much wider each disk is.
DISK_WIDTH_INCREMENT = 30

root = Tk()
root.title("Towers of Hanoi Visual Representation")

class Towers:
    def __init__(self, disks):
        self.disks = disks
        self.rods = [[],[],[]]
        self.rods[0] = [(x + 1) for x in range(disks)]
    
    def size(self, rod):
        return len(self.rods[rod])
    
    def peek(self, rod):
        if not self.rods[rod]:
            return None
        return self.rods[rod][0]
    
    def pop(self, rod):
        val = self.peek(rod)
        if val:
            del self.rods[rod][0]
        return val
    
    def push(self, rod, val):
        self.rods[rod].insert(0, val)

    def valid_move(self, source_rod, dest_rod):
        if not self.peek(source_rod):
            return False
        if not self.peek(dest_rod):
            return True
        return self.peek(source_rod) < self.peek(dest_rod)

    def make_move(self, source_rod, dest_rod):
        val = self.pop(source_rod)
        self.push(dest_rod, val)

class Game:
    def __init__(self):
        self.towers = Towers(DISK_COUNT)
        self.panel = Label(root)
        self.panel.grid(column=0, row=0)
        self.panel.pack()
        game_th = threading.Thread(target=self.game)
        game_th.daemon = True
        game_th.start() 

    def game(self):
        self.render_towers()
        parity = self.towers.disks % 2
        time.sleep(1)

        while self.towers.size(2) != self.towers.disks:
            if parity == 0:
                # A - B
                self.make_valid_move(0, 1)

                # A - C
                self.make_valid_move(0, 2)

                # B - C
                self.make_valid_move(1, 2)
            else:
                # A - C
                self.make_valid_move(0, 2)

                # A - B
                self.make_valid_move(0, 1)

                # B - C
                self.make_valid_move(1, 2)

    def make_valid_move(self, rod1, rod2):
        if self.towers.valid_move(rod1, rod2):
            self.game_move(rod1, rod2)
        elif self.towers.valid_move(rod2, rod1):
            self.game_move(rod2, rod1)

    def game_move(self, source, dest):
        self.towers.make_move(source, dest)
        self.render_towers()
        time.sleep(1)

    def render_towers(self):
        img = Image.new("RGB", (WINDOW_SIZE, WINDOW_SIZE))
        
        # Render the rods.
        for i in range((WINDOW_SIZE // 3) // 2, WINDOW_SIZE, WINDOW_SIZE // 3):
            for j in range((WINDOW_SIZE // 4), WINDOW_SIZE):
                for k in range(i - ROD_WIDTH // 2, i + ROD_WIDTH // 2):
                    img.putpixel((k, j), (255, 255, 255))
        
        # Render the disks.
        for i in range(3):
            rod_location = ((WINDOW_SIZE // 3) // 2) + ((WINDOW_SIZE // 3) * i)
            rod_disks = self.towers.rods[i]
            pixel_level = WINDOW_SIZE - 1

            if len(rod_disks) != 0:
                for disk_number in reversed(rod_disks):
                    for j in range(pixel_level, pixel_level - DISK_THICKNESS, -1):
                        width = DISK_MINWIDTH + (disk_number * DISK_WIDTH_INCREMENT)
                        for k in range(rod_location - (width // 2), rod_location + (width // 2)):
                            img.putpixel((k, j), DISK_COLOR)
                    pixel_level -= DISK_THICKNESS

        photo_image = ImageTk.PhotoImage(img)
        self.panel.configure(image=photo_image)
        self.panel.photo = photo_image
        self.panel.pack()

game = Game()
root.mainloop() 
