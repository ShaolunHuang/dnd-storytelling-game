import cv2
import tkinter as tk

def edit_img():
    background = cv2.imread("resources/background.png")
    background = cv2.resize(background, (1280, 720))
    for i in range(10):
        background = cv2.GaussianBlur(background, (5, 5), cv2.BORDER_DEFAULT)
    cv2.imwrite("resources/background_blurred.png", background)


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

        self.background_img = tk.PhotoImage(file='resources/background_blurred.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)

        self.canvas.create_text(
            canvas_width / 2,
            canvas_height / 3.6,
            text='DND Storytelling Game',
            font=('Arial', 40),
            fill='white')

        start_button = tk.Button(self.window, text='Start', width=16, height=2, command=self.start)

        button_width = start_button.winfo_reqwidth()

        center_x = (canvas_width - button_width) / 2
        self.canvas.create_window(center_x, canvas_height / 2, window=start_button, anchor=tk.NW)
        show_members_button = tk.Button(self.window, text='Show Members', width=16, height=2)
        self.canvas.create_window(center_x, canvas_height / 72 * 42, window=show_members_button, anchor=tk.NW)
        show_img_button = tk.Button(self.window, text='Show Images', width=16, height=2)
        self.canvas.create_window(center_x, canvas_height / 72 * 48, window=show_img_button, anchor=tk.NW)
        quit_button = tk.Button(self.window, text='Quit', width=16, height=2, command=self.window.quit)
        self.canvas.create_window(center_x, canvas_height / 72 * 54, window=quit_button, anchor=tk.NW)

    def show_home(self):
        self.canvas = tk.Canvas(self.window, width=1280, height=720)
        self.canvas.pack(fill='both', expand=True)
        self.set_canvas()

    def start(self):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        field_font = ('Algerian', 15)
        
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/old_book.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)
        #self.canvas.create_text(640, 100, text='Enter the Game Settings', font=('Arial', 40), fill='white') 

        # First Page
        # self.canvas.create_text(100, 50, text='Enter the keywords for this game background', font=field_font, fill='black' # Text
        # self.canvas.create_text(100, 50, text='Box left blank will be generated automatically', font=('Arial', 10), fill='white')
        
        # text_widget = tk.Text(self.window, width=20, height=4)
        # text_widget.insert('end', text)
        # text_widget_window = canvas.create_window(150, 150, window=text_widget)


        # Second Page
        self.canvas.create_text(canvas_width / 3, canvas_height / 9 * 2, text='Your Name', font=field_font, fill='black') # Text
        name = tk.Text(self.canvas, height = 1, width = 20)
        self.canvas.create_window(canvas_width / 3 * 2, canvas_height / 9 * 2, window=name, anchor=tk.CENTER)

        self.canvas.create_text(canvas_width / 3, canvas_height / 9 * 3, text='Sex', font=field_font, fill='black') # List of Choice
        var = tk.StringVar()
        male = tk.Radiobutton(self.canvas, text="Male", font=field_font, variable=var, value='male')
        self.canvas.create_window(canvas_width / 3 * 1.85, canvas_height / 9 * 3, window=male, anchor=tk.CENTER)
        female = tk.Radiobutton(self.canvas, text="Female", font=field_font, variable=var, value='female')
        self.canvas.create_window(canvas_width / 3 * 2.2, canvas_height / 9 * 3, window=female, anchor=tk.CENTER)

        self.canvas.create_text(canvas_width / 3, canvas_height / 9 * 4, text='Age', font=field_font, fill='black')  # Text
        age = tk.Text(self.canvas, height = 1, width = 5)
        self.canvas.create_window(canvas_width / 3 * 2, canvas_height / 9 * 4, window=age, anchor=tk.CENTER)
        
        self.canvas.create_text(canvas_width / 3, canvas_height / 9 * 5, text='Race', font=field_font, fill='black') # Text
        race = tk.Text(self.canvas, height = 1, width = 20)
        self.canvas.create_window(canvas_width / 3 * 2, canvas_height / 9 * 5, window=race, anchor=tk.CENTER)

        self.canvas.create_text(canvas_width / 3, canvas_height / 9 * 6, text='Level', font=field_font, fill='black') # Text
        level = tk.Text(self.canvas, height = 1, width = 20)
        self.canvas.create_window(canvas_width / 3 * 2, canvas_height / 9 * 6, window=level, anchor=tk.CENTER)

        self.canvas.create_text(canvas_width / 3, canvas_height / 9 * 7, text='Class', font=field_font, fill='black') # Text
        player_class = tk.Text(self.canvas, height = 1, width = 20)
        self.canvas.create_window(canvas_width / 3 * 2, canvas_height / 9 * 7, window=player_class, anchor=tk.CENTER)

        back_button = tk.Button(self.window, text='Last Page', width=10, height=2)
        self.canvas.create_window(canvas_width / 7 * 1.1, canvas_height / 9 * 7.5, window=back_button, anchor=tk.CENTER)

        next_button = tk.Button(self.window, text='Next Page', width=10, height=2)
        self.canvas.create_window(canvas_width / 7 * 6, canvas_height / 9 * 7.5, window=next_button, anchor=tk.CENTER)

        # self.canvas.create_text(100, 50, text='Attributes', font=field_font, fill='black') # 6 drop down range from 0-20: str, dex, int, con, app, pow
        # self.canvas.create_text(100, 50, text='Inventory', font=field_font, fill='black') # Text
        # self.canvas.create_text(100, 50, text='Background', font=field_font, fill='black') # Text

        # inputtxt = tk.Text(self.canvas, height = 2, width = 5)
        # self.canvas.create_window(100, 100, window=inputtxt, anchor=tk.NW)
        
    # def generatePlayer(self):
        



    def mainloop(self):
        self.window.mainloop()


def main():
    edit_img()
    game = DNDStorytellingGame()
    game.mainloop()


if __name__ == "__main__":
    main()
