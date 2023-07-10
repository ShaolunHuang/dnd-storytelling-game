import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from main import background_generator, text_to_speech
from player import Character
from player_attribute import PlayerAttribute, PlayerInventory
from tkinter import scrolledtext
from radar_image import radar_factory
import matplotlib.pyplot as plt
from image_generator import ImageGenerator
from story_generation import Generator
import os
import re
import pygame

def edit_img():
    radar = cv2.imread("resources/images/radar.png")
    radar = cv2.resize(radar, (300, 300))
    cv2.imwrite("resources/images/radar.png", radar)


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
        self.encounter_num = 1
        self.show_home()

    def set_canvas(self):
        self.stop()
        self.encounter_num = 1
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

        start_button = tk.Button(self.window, text='Single Player', width=20, height=2, command=self.start)

        button_width = start_button.winfo_reqwidth()

        center_x = (canvas_width - button_width) / 2
        self.canvas.create_window(center_x, canvas_height / 2, window=start_button, anchor=tk.NW)
        show_members_button = tk.Button(
            self.window,
            text='Display Production Team',
            width=20,
            height=2,
            command=self.show_members)
        self.canvas.create_window(center_x, canvas_height / 72 * 42, window=show_members_button, anchor=tk.NW)
        show_img_button = tk.Button(
            self.window,
            text='Show Encounter Images',
            width=20,
            height=2,
            command=lambda: self.show_images(0))
        self.canvas.create_window(center_x, canvas_height / 72 * 48, window=show_img_button, anchor=tk.NW)
        quit_button = tk.Button(self.window, text='Quit', width=20, height=2, command=self.window.quit)
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

    def show_images(self, pt):
        self.img_files = [f for f in os.listdir("resources/images/") if os.path.isfile(os.path.join("resources/images/", f))]
        if pt < 0:
            self.set_canvas()
            return
        if pt >= len(self.img_files):
            self.set_canvas()
            return
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        for child in self.canvas.winfo_children():
            child.destroy()
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/background_blurred.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)
        self.canvas.create_text(
            canvas_width / 2,
            canvas_height / 10,
            text='Encounter Images',
            font=('Arial', 40),
            fill='white')
        if len(self.img_files) == 0:
            self.canvas.create_text(
                canvas_width / 2,
                canvas_height / 3.6 + 50,
                text='No Images Available',
                font=('Arial', 20),
                fill='white')
        else:
            self.generated_img = tk.PhotoImage(file=f'resources/images/{self.img_files[pt]}')
            self.canvas.create_image(canvas_width / 2, canvas_height / 2, image=self.generated_img, anchor=tk.CENTER)
            next_button = tk.Button(self.window, text='Next Page', width=10, height=2, command=lambda: self.show_images(pt + 1))
            self.canvas.create_window(canvas_width / 7 * 6, canvas_height / 10 * 8.5, window=next_button, anchor=tk.CENTER)
        back_button = tk.Button(self.window, text='Last Page', width=10, height=2, command=lambda: self.show_images(pt - 1))
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
        #self.canvas.create_text(canvas_width / 2, 100, text='Enter the Game Settings', font=('Arial', 40), fill='black')

        # First Page
        self.canvas.create_text(canvas_width / 3*0.95, canvas_height / 3*1.5, text='Enter the keywords for this \n game background',
                                font=field_font, fill='black', justify="center")  # Text

        text_widget = tk.Text(self.window, width=40, height=8)
        # text_widget.insert('end', text)
        text_widget_window = self.canvas.create_window(canvas_width / 3*2.17, canvas_height /3*1.47, window=text_widget)

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
            self.player = Character()
            self.player.create(
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
            self.narrater, self.story_response = background_generator([self.player], story_background)
            self.story_begin()


        # Flip the book
        back_button = tk.Button(self.window, text='Last Page', width=10, height=2, command=self.start)
        self.canvas.create_window(canvas_width / 7 * 1.1, canvas_height / 10 * 8.5, window=back_button,
                                  anchor=tk.CENTER)

        next_button = tk.Button(self.window, text='Next Page', width=10, height=2, command=generatePlayer)
        self.canvas.create_window(canvas_width / 7 * 6, canvas_height / 10 * 8.5, window=next_button, anchor=tk.CENTER)

    def story_begin(self):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        field_font = ('Algerian', 15)
        for child in self.canvas.winfo_children():
            child.destroy()
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/old_book.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)

        # Generated Image
        self.generated_img = tk.PhotoImage(file='resources/images/img_generated_1.png')
        self.canvas.create_image(canvas_width / 3.3, canvas_height / 2.3, image=self.generated_img, anchor=tk.CENTER)

        # Scrollable wordlsetting, region, background
        text_area = scrolledtext.ScrolledText(self.window, wrap = tk.WORD, width = 30,
                                              height = 15, background= "#FAEED2", font = ("Times New Roman", 15))
        worldsetting = self.narrater.world.worldsetting.to_narrative()
        region = self.narrater.world.worldregion.to_narrative()
        background = self.narrater.background.to_narrative()
        input = f"""World Setting:\n{worldsetting}\n\nRegion:\n{region}\n\nBackground:\n{background.strip("}")}"""
        text_area.insert(tk.END, input)
        text_area.configure(state='disabled')

        self.canvas.create_window(canvas_width / 4 * 2.9, canvas_height / 2.5, window=text_area,
                                  anchor=tk.CENTER)

        back_button = tk.Button(self.window, text='Home', width=10, height=2, command=self.set_canvas)
        self.canvas.create_window(canvas_width / 7 * 1.1, canvas_height / 10 * 8.5, window=back_button,
                                  anchor=tk.CENTER)

        next_button = tk.Button(self.window, text='Next Page', width=10, height=2, command=self.encounter_loop)
        self.canvas.create_window(canvas_width / 7 * 6, canvas_height / 10 * 8.5, window=next_button, anchor=tk.CENTER)

        play_worldsetting = tk.Button(self.window, text='Play World Setting', width=15, height=2,  command=self.play_worldsetting)
        self.canvas.create_window(canvas_width / 7 * 4.2, canvas_height / 10 * 7.5, window=play_worldsetting, anchor=tk.CENTER)

        play_region = tk.Button(self.window, text='Play Region', width=10, height=2,  command=self.play_region)
        self.canvas.create_window(canvas_width / 7 * 4.9, canvas_height / 10 * 7.5, window=play_region, anchor=tk.CENTER)

        play_background = tk.Button(self.window, text='Play Background', width=15, height=2,  command=self.play_background)
        self.canvas.create_window(canvas_width / 7 * 5.6, canvas_height / 10 * 7.5, window=play_background, anchor=tk.CENTER)

    def play_worldsetting(self):
        pygame.mixer.init()
        pygame.mixer.music.load(f"resources/audios/output_worldsetting.wav")
        pygame.mixer.music.play()

    def play_region(self):
        pygame.mixer.init()
        pygame.mixer.music.load(f"resources/audios/output_region.wav")
        pygame.mixer.music.play()

    def play_background(self):
        pygame.mixer.init()
        pygame.mixer.music.load(f"resources/audios/output_background.wav")
        pygame.mixer.music.play()

    def play_story(self):
        pygame.mixer.init()
        pygame.mixer.music.load(f"resources/audios/output_story.wav")
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.init()
        pygame.mixer.music.unload()

    def image_generator(self):
        img_generate = ImageGenerator()
        text = self.story_response
        
    
    def encounter_loop(self):
        self.stop()
        # self.story_response is first suggestion
        response = self.story_response
        
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        field_font = ('Times New Roman', 15)
        for child in self.canvas.winfo_children():
            child.destroy()
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/old_book.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)

        def next(player_choice,response):
            self.stop()
            if(response.text.find('"END"') != -1) or (response.text.find("END") != -1) or (response.text.find("End") != -1):
                self.set_canvas()
            # self.encounter_num += 1
            choice = player_choice.get("1.0", "end-1c")
            if(choice == ""):
                messagebox.showwarning("Warning", "Please make your choice.")
            else:
                choice = self.player.get_name() + ": " + choice
                self.story_response = self.narrater.next(choice, "")
                print(f"{self.story_response.text}\n")
                text_to_speech(self.story_response.text, "story")
                keywords_generator = Generator("?")
                keyword = keywords_generator.generate_keywords(self.story_response.text)
                
                print(f"{keyword}\n")
                
                keyword = keyword.text
                
                start_tag = '<'
                end_tag = '>'
                close_tag = '</'
                keywords = []
                
                start = 0
                while True:
                    if start >=len(keyword): 
                        break
                    start = keyword.find(start_tag, start)
                    if start == -1:  # No more tags
                        break
                    end = keyword.find(end_tag, start)
                    if(end == -1):
                        break
                    close = keyword.find(close_tag, end)
                    if(close == -1):
                        break
                    tag_content = keyword[end+1:close].strip()
                    keywords.append(tag_content)
                    start = close+1
                
                main_char = str(self.player.age) + " years old "+ str(self.player.sex) + " " + str(self.player.race) + " " + str(self.player.c_class)
                print(f"{main_char}\n")
                
                keywords[0] = main_char
                
                out_keywords = ""
                for words in keywords:
                    if(words != ""):
                        out_keywords += words + ", "
                    
                print(f"{out_keywords}\n")
                image_gen = ImageGenerator()
                self.encounter_num += 1
                
                image_gen.get_image("".join(out_keywords),str(self.encounter_num))
                self.encounter_loop()
          
        if not os.path.exists(f'resources/images/img_generated_{self.encounter_num}.png'):  
            self.encounter_num = self.encounter_num - 1
            
        self.generated_img = tk.PhotoImage(file=f'resources/images/img_generated_{self.encounter_num}.png')
        self.canvas.create_image(canvas_width / 3.3, canvas_height / 2.3, image=self.generated_img, anchor=tk.CENTER)
        
        text_area = scrolledtext.ScrolledText(self.window, wrap = tk.WORD, width = 30,
                                              height = 16, background= "#FAEED2", font = field_font)
        input = f"""{response}\n"""
        text_area.insert(tk.END, input)
        text_area.configure(state='disabled')

        self.canvas.create_window(canvas_width / 4 * 2.9, canvas_height / 2.8, window=text_area,
                                  anchor=tk.CENTER)
        
        player_response = tk.Text(self.canvas, height=8, width=45)
        self.canvas.create_window(canvas_width / 4 * 2.9, canvas_height / 3*2.1, window=player_response, anchor=tk.CENTER)

        back_button = tk.Button(self.window, text='Home', width=10, height=2, command=self.set_canvas)
        self.canvas.create_window(canvas_width / 7 * 1.1, canvas_height / 10 * 8.5, window=back_button,
                                  anchor=tk.CENTER)
        
        inventory_button = tk.Button(self.window, text='Check Status', width=10, height=2, command=self.inventory_page)
        self.canvas.create_window(canvas_width / 7 * 3.6, canvas_height / 10 * 8.5, window=inventory_button, anchor=tk.CENTER)

        next_button = tk.Button(self.window, text='Next Page', width=10, height=2, command=lambda: next(player_response,response))
        self.canvas.create_window(canvas_width / 7 * 6, canvas_height / 10 * 8.5, window=next_button, anchor=tk.CENTER)
        
        play_story = tk.Button(self.window, text='Play Story', width=10, height=2,  command=self.play_story)
        self.canvas.create_window(canvas_width / 7 * 5, canvas_height / 10 * 8.5, window=play_story, anchor=tk.CENTER)
        
    
    def inventory_page(self):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        field_font = ('Algerian', 15)
        for child in self.canvas.winfo_children():
            child.destroy()
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/old_book.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)
        strength, constitution, dexterity, intelligence, wisdom, charisma = self.player.get_all_attributes()
        data = [['Strength', 'Constitution', 'Dexterity', 'Intelligence', 'Wisdom', 'Charisma'],
        ('Player Attributes', [
            [strength, constitution, dexterity, intelligence, wisdom, charisma]])]

        N = len(data[0])
        theta = radar_factory(N, frame='polygon')

        spoke_labels = data.pop(0)
        title, case_data = data[0]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
        fig.subplots_adjust(top=0.85, bottom=0.05)

        ax.set_rgrids([4, 6, 8, 10])
        ax.set_title(title,  position=(0.5, 1.1), ha='center')

        for d in case_data:
            line = ax.plot(theta, d)
            ax.fill(theta, d,  alpha=0.25)
        ax.set_varlabels(spoke_labels)

        plt.savefig('resources/images/radar.png')
        plt.close()
        edit_img()
        
        p_name, p_sex, p_background, p_race, p_age, p_level, p_class = self.player.get_all_info()
        # Player Name
        self.canvas.create_text(canvas_width / 6+10, canvas_height / 10 * 2, text='Name', font=field_font,
                                fill='black')  # Text
        self.canvas.create_text(canvas_width / 6 * 2+10, canvas_height / 10 * 2, text=p_name, font=field_font,
                                fill='black')

        # Sex
        self.canvas.create_text(canvas_width / 6+10, canvas_height / 10 * 3, text='Sex', font=field_font,
                                fill='black')  # List of Choice
        self.canvas.create_text(canvas_width / 6 * 2+10, canvas_height / 10 * 3, text=p_sex, font=field_font,
                                fill='black')

        # Age
        self.canvas.create_text(canvas_width / 6+10, canvas_height / 10 * 4, text='Age', font=field_font,
                                fill='black')  # Text
        self.canvas.create_text(canvas_width / 6 * 2+10, canvas_height / 10 * 4, text=p_age, font=field_font,
                                fill='black')

        # Race
        self.canvas.create_text(canvas_width / 6+10, canvas_height / 10 * 5, text='Race', font=field_font,
                                fill='black')  # Text
        self.canvas.create_text(canvas_width / 6 * 2+10, canvas_height / 10 * 5, text=p_race, font=field_font,
                                fill='black')

        # Level
        self.canvas.create_text(canvas_width / 6+10, canvas_height / 10 * 6, text='Level', font=field_font,
                                fill='black')  # Text
        self.canvas.create_text(canvas_width / 6 * 2+10, canvas_height / 10 * 6, text=p_level, font=field_font,
                                fill='black')

        # Class
        self.canvas.create_text(canvas_width / 6+10, canvas_height / 10 * 7, text='Class', font=field_font,
                                fill='black')  # Text
        self.canvas.create_text(canvas_width / 6 * 2+10, canvas_height / 10 * 7, text=p_class, font=field_font,
                                fill='black')
        
        self.generated_img = tk.PhotoImage(file='resources/images/radar.png')
        self.canvas.create_image(canvas_width / 6*4.5, canvas_height / 10*4, image=self.generated_img, anchor=tk.CENTER)

        # Flip the book
        back_button = tk.Button(self.window, text='Back', width=10, height=2, command=self.encounter_loop)
        self.canvas.create_window(canvas_width / 7 * 1.1, canvas_height / 10 * 8.5, window=back_button, anchor=tk.CENTER)


    def mainloop(self):
        self.window.mainloop()


def start_game():
    game = DNDStorytellingGame()
    game.mainloop()


if __name__ == "__main__":
    start_game()
