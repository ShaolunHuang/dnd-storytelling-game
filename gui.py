import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from main import main
from player import Character
from player_attribute import PlayerAttribute, PlayerInventory


def edit_img():
    background = cv2.imread("resources/background.png")
    background = cv2.resize(background, (1280, 720))
    for i in range(10):
        background = cv2.GaussianBlur(background, (5, 5), cv2.BORDER_DEFAULT)
    cv2.imwrite("resources/background_blurred.png", background)


def check_string(string, name):
    if string == "":
        raise ValueError(f"{name} cannot be empty")


def check_int(integer, name):
    if integer == "":
        raise ValueError(f"{name} cannot be empty")
    try:
        int(integer)
    except:
        raise ValueError(f"{name} must be an integer")


class DNDStorytellingGame:
    def __init__(self):
        self.canvas = None
        self.background_img = None
        self.window = tk.Tk()
        self.window.title('DND Storytelling Game')
        self.window.geometry('1280x720')
        self.window.resizable(False, False)
        self.show_home()

    def set_canvas(self):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        for child in self.canvas.winfo_children():
            child.destroy()
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/background_blurred.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)

        self.canvas.create_text(
            canvas_width / 2,
            canvas_height / 3.6,
            text='DND Storytelling Game',
            font=('Arial', 40),
            fill='white')

        start_button = tk.Button(self.window, text='Single Player', width=16, height=2, command=self.start)

        button_width = start_button.winfo_reqwidth()

        center_x = (canvas_width - button_width) / 2
        self.canvas.create_window(center_x, canvas_height / 2, window=start_button, anchor=tk.NW)
        show_members_button = tk.Button(
            self.window,
            text='Display Production Team',
            width=16,
            height=2,
            command=self.show_members)
        self.canvas.create_window(center_x, canvas_height / 72 * 42, window=show_members_button, anchor=tk.NW)
        show_img_button = tk.Button(
            self.window,
            text='Show Encounter Images',
            width=16,
            height=2,
            command=self.show_images)
        self.canvas.create_window(center_x, canvas_height / 72 * 48, window=show_img_button, anchor=tk.NW)
        quit_button = tk.Button(self.window, text='Quit', width=16, height=2, command=self.window.quit)
        self.canvas.create_window(center_x, canvas_height / 72 * 54, window=quit_button, anchor=tk.NW)

    def show_members(self):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        for child in self.canvas.winfo_children():
            child.destroy()
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/background_blurred.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)
        self.canvas.create_text(
            canvas_width / 2,
            canvas_height / 3.6,
            text='Production Team',
            font=('Arial', 40),
            fill='white')
        self.canvas.create_text(
            canvas_width / 2,
            canvas_height / 2.8,
            text='Names in Alphabetical Order',
            font=('Arial', 20),
            fill='white')
        self.canvas.create_text(
            canvas_width / 4,
            canvas_height / 1.8 - 50,
            text='Alan Huang',
            font=('Arial', 20),
            fill='white')
        self.canvas.create_text(
            canvas_width / 4,
            canvas_height / 1.8 + 50,
            text='James Jiang',
            font=('Arial', 20),
            fill='white')
        self.canvas.create_text(
            canvas_width / 4 * 3,
            canvas_height / 1.8 - 50,
            text='John Wang',
            font=('Arial', 20),
            fill='white')
        self.canvas.create_text(
            canvas_width / 4 * 3,
            canvas_height / 1.8 + 50,
            text='Ricky Tian',
            font=('Arial', 20),
            fill='white')
        back_button = tk.Button(self.window, text='Last Page', width=10, height=2, command=self.set_canvas)
        self.canvas.create_window(canvas_width / 7 * 1.1, canvas_height / 10 * 8.5, window=back_button,
                                  anchor=tk.CENTER)

    def show_images(self):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        for child in self.canvas.winfo_children():
            child.destroy()
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/background_blurred.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)
        self.canvas.create_text(
            canvas_width / 2,
            canvas_height / 3.6,
            text='Encounter Images',
            font=('Arial', 40),
            fill='white')
        self.canvas.create_text(
            canvas_width / 2,
            canvas_height / 3.6 + 50,
            text='No Images Available',
            font=('Arial', 20),
            fill='white')
        back_button = tk.Button(self.window, text='Last Page', width=10, height=2, command=self.set_canvas)
        self.canvas.create_window(canvas_width / 7 * 1.1, canvas_height / 10 * 8.5, window=back_button,
                                  anchor=tk.CENTER)

    def show_home(self):
        self.canvas = tk.Canvas(self.window, width=1280, height=720)
        self.canvas.pack(fill='both', expand=True)
        self.set_canvas()

    def start(self):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        field_font = ('Algerian', 15)

        for child in self.canvas.winfo_children():
            child.destroy()
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/old_book.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)
        self.canvas.create_text(canvas_width/2, 100, text='Enter the Game Settings', font=('Arial', 40), fill='black')

        # First Page
        self.canvas.create_text(canvas_width/2, canvas_height/4, text='Enter the keywords for this game background', font=field_font, fill='black') # Text
        self.canvas.create_text(canvas_width/2, canvas_height/4+50, text='Box left blank will be generated automatically', font=('Arial', 10), fill='black')

        text_widget = tk.Text(self.window, width=40, height=8)
        # text_widget.insert('end', text)
        text_widget_window = self.canvas.create_window(canvas_width/2, canvas_height/2, window=text_widget)

        def get_info():
            text = text_widget.get('1.0', 'end')
            text = text.strip()
            if text == '':
                text = ["Cyberpunk", "desert", "city", "lava"]
            else:
                text = text.split(',')
            self.make_player(text)

        back_button = tk.Button(self.window, text='Last Page', width=10, height=2, command=self.set_canvas)
        self.canvas.create_window(canvas_width / 7 * 1.1, canvas_height / 10 * 8.5, window=back_button,
                                  anchor=tk.CENTER)

        next_button = tk.Button(self.window, text='Next Page', width=10, height=2, command=get_info)
        self.canvas.create_window(canvas_width / 7 * 6, canvas_height / 10 * 8.5, window=next_button, anchor=tk.CENTER)


    def make_player(self, story_background):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        field_font = ('Algerian', 15)
        for child in self.canvas.winfo_children():
            child.destroy()
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/old_book.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)
        # ---------------------------- Second Page of Player Settings ---------------------------- #
        # Player Name
        self.canvas.create_text(canvas_width / 6, canvas_height / 10 * 2, text='Your Name', font=field_font,
                                fill='black')  # Text
        name = tk.Text(self.canvas, height=1, width=20)
        self.canvas.create_window(canvas_width / 6 * 2, canvas_height / 10 * 2, window=name, anchor=tk.CENTER)

        # Sex
        self.canvas.create_text(canvas_width / 6, canvas_height / 10 * 3, text='Sex', font=field_font,
                                fill='black')  # List of Choice
        var = tk.StringVar()
        male = tk.Radiobutton(self.canvas, text="Male", font=field_font, variable=var, value='male')
        self.canvas.create_window(canvas_width / 6 * 1.8, canvas_height / 10 * 3, window=male, anchor=tk.CENTER)
        female = tk.Radiobutton(self.canvas, text="Female", font=field_font, variable=var, value='female')
        self.canvas.create_window(canvas_width / 6 * 2.3, canvas_height / 10 * 3, window=female, anchor=tk.CENTER)

        # Age
        self.canvas.create_text(canvas_width / 6, canvas_height / 10 * 4, text='Age', font=field_font,
                                fill='black')  # Text
        age = tk.Text(self.canvas, height=1, width=5)
        self.canvas.create_window(canvas_width / 6 * 2, canvas_height / 10 * 4, window=age, anchor=tk.CENTER)

        # Race
        self.canvas.create_text(canvas_width / 6, canvas_height / 10 * 5, text='Race', font=field_font,
                                fill='black')  # Text
        race = tk.Text(self.canvas, height=1, width=20)
        self.canvas.create_window(canvas_width / 6 * 2, canvas_height / 10 * 5, window=race, anchor=tk.CENTER)

        # Level
        self.canvas.create_text(canvas_width / 6, canvas_height / 10 * 6, text='Level', font=field_font,
                                fill='black')  # Text
        level = tk.Text(self.canvas, height=1, width=20)
        self.canvas.create_window(canvas_width / 6 * 2, canvas_height / 10 * 6, window=level, anchor=tk.CENTER)

        # Class
        self.canvas.create_text(canvas_width / 6, canvas_height / 10 * 7, text='Class', font=field_font,
                                fill='black')  # Text
        player_class = tk.Text(self.canvas, height=1, width=20)
        self.canvas.create_window(canvas_width / 6 * 2, canvas_height / 10 * 7, window=player_class, anchor=tk.CENTER)

        ### Player Attributes ###
        values = list(range(11))
        self.canvas.create_text(canvas_width / 6 * 3.7, canvas_height / 10 * 2, text='Constitution', font=field_font,
                                fill='black')  # 6 drop down range from 0-20
        cons_drop = ttk.Combobox(self.window, values=values, height=12, width=5, state='readonly')
        cons_drop.current(0)
        self.canvas.create_window(canvas_width / 6 * 4.5, canvas_height / 10 * 2, window=cons_drop, anchor=tk.CENTER)

        self.canvas.create_text(canvas_width / 6 * 3.7, canvas_height / 10 * 2.5, text='Strength', font=field_font,
                                fill='black')
        stren_drop = ttk.Combobox(self.window, values=values, height=12, width=5, state='readonly')
        stren_drop.current(0)
        self.canvas.create_window(canvas_width / 6 * 4.5, canvas_height / 10 * 2.5, window=stren_drop, anchor=tk.CENTER)

        self.canvas.create_text(canvas_width / 6 * 3.7, canvas_height / 10 * 3, text='Dexterity', font=field_font,
                                fill='black')
        dex_drop = ttk.Combobox(self.window, values=values, height=12, width=5, state='readonly')
        dex_drop.current(0)
        self.canvas.create_window(canvas_width / 6 * 4.5, canvas_height / 10 * 3, window=dex_drop, anchor=tk.CENTER)

        self.canvas.create_text(canvas_width / 6 * 3.7, canvas_height / 10 * 3.5, text='Intelligence', font=field_font,
                                fill='black')
        intel_drop = ttk.Combobox(self.window, values=values, height=12, width=5, state='readonly')
        intel_drop.current(0)
        self.canvas.create_window(canvas_width / 6 * 4.5, canvas_height / 10 * 3.5, window=intel_drop, anchor=tk.CENTER)

        self.canvas.create_text(canvas_width / 6 * 3.7, canvas_height / 10 * 4, text='Wisdom', font=field_font,
                                fill='black')
        wis_drop = ttk.Combobox(self.window, values=values, height=12, width=5, state='readonly')
        wis_drop.current(0)
        self.canvas.create_window(canvas_width / 6 * 4.5, canvas_height / 10 * 4, window=wis_drop, anchor=tk.CENTER)

        self.canvas.create_text(canvas_width / 6 * 3.7, canvas_height / 10 * 4.5, text='Charisma', font=field_font,
                                fill='black')
        char_drop = ttk.Combobox(self.window, values=values, height=12, width=5, state='readonly')
        char_drop.current(0)
        self.canvas.create_window(canvas_width / 6 * 4.5, canvas_height / 10 * 4.5, window=char_drop, anchor=tk.CENTER)

        self.canvas.create_text(canvas_width / 6 * 3.7, canvas_height / 10 * 5.5, text='Inventory', font=field_font,
                                fill='black')  # Text
        inventory = tk.Text(self.canvas, height=4, width=30)
        self.canvas.create_window(canvas_width / 6 * 4.7, canvas_height / 10 * 5.5, window=inventory, anchor=tk.CENTER)

        self.canvas.create_text(canvas_width / 6 * 3.7, canvas_height / 10 * 7, text='Background',
                                font=field_font,
                                fill='black')  # Text
        background = tk.Text(self.canvas, height=4, width=30)
        self.canvas.create_window(canvas_width / 6 * 4.7, canvas_height / 10 * 7, window=background, anchor=tk.CENTER)

        def get_info():
            player_name = name.get("1.0", "end-1c")
            player_sex = var.get()
            player_age = age.get("1.0", "end-1c")
            player_race = race.get("1.0", "end-1c")
            player_level = level.get("1.0", "end-1c")
            nonlocal player_class
            player_class_str = player_class.get("1.0", "end-1c")
            player_inventory = inventory.get("1.0", "end-1c")
            player_background = background.get("1.0", "end-1c")
            player_con = cons_drop.get()
            player_str = stren_drop.get()
            player_dex = dex_drop.get()
            player_int = intel_drop.get()
            player_wis = wis_drop.get()
            player_char = char_drop.get()
            try:
                check_string(player_name, 'Name')
                check_string(player_sex, 'Sex')
                check_int(player_age, 'Age')
                check_string(player_race, 'Race')
                check_int(player_level, 'Level')
                check_string(player_class_str, 'Class')
                check_string(player_background, 'Background')
            except ValueError as e:
                messagebox.showerror('Error!', e)
                return None
            ret = [player_name, player_sex, player_age, player_race, player_level, player_class_str, player_inventory,
                   player_background, player_con, player_str, player_dex, player_int, player_wis, player_char]
            print(", ".join(ret))
            return ret

        def generatePlayer():
            info = get_info()
            if info is None:
                return
            player = Character()
            player.create(
                info[0],
                info[1],
                int(info[2]),
                info[3],
                int(info[4]),
                info[5],
                PlayerAttribute(constitution=int(info[8]), strength=int(info[9]), dexterity=int(info[10]),
                                intelligence=int(info[11]), wisdom=int(info[12]), charisma=int(info[13])),
                PlayerInventory([], [], [], [], [], [], []),
                info[7],
            )
            main([player], story_background)

        # Flip the book
        back_button = tk.Button(self.window, text='Last Page', width=10, height=2, command=self.start)
        self.canvas.create_window(canvas_width / 7 * 1.1, canvas_height / 10 * 8.5, window=back_button,
                                  anchor=tk.CENTER)

        next_button = tk.Button(self.window, text='Next Page', width=10, height=2, command=generatePlayer)
        self.canvas.create_window(canvas_width / 7 * 6, canvas_height / 10 * 8.5, window=next_button, anchor=tk.CENTER)

    # def generatePlayer(self):

    def mainloop(self):
        self.window.mainloop()


def start_game():
    edit_img()
    game = DNDStorytellingGame()
    game.mainloop()


if __name__ == "__main__":
    start_game()
