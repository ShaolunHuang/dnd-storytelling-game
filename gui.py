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
        
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/old_book.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)
        #self.canvas.create_text(640, 100, text='Enter the Game Settings', font=('Arial', 40), fill='white') 

        # First Page
        # self.canvas.create_text(100, 50, text='Enter the keywords for this game background', font=('Arial', 20), fill='white') # Text
        # self.canvas.create_text(100, 50, text='Box left blank will be generated automatically', font=('Arial', 10), fill='white')
        
        # text_widget = tk.Text(self.window, width=20, height=4)
        # text_widget.insert('end', text)
        # text_widget_window = canvas.create_window(150, 150, window=text_widget)
        
        
        

        # Second Page
        self.canvas.create_text(canvas_width / 3, canvas_height / 7, text='Your Name', font=('Algerian', 15), fill='black') # Text
        name = tk.Text(self.canvas, height = 1, width = 20)
        self.canvas.create_window(canvas_width / 3 * 2, canvas_height / 7, window=name, anchor=tk.NW)

        # self.canvas.create_text(100, 50, text='Sex', font=('Arial', 20), fill='white') # List of Choice
        # var = tk.IntVar()
        # male = tk.Radiobutton(self.canvas, text="Male", variable=var, value=1)
        # female = tk.Radiobutton(self.canvas, text="Female", variable=var, value=1)


        # self.canvas.create_text(100, 50, text='Age', font=('Arial', 20), fill='white')  # Text
        # age = tk.Text(self.canvas, height = 2, width = 5)
        # self.canvas.create_window(100, 100, window=inputtxt, anchor=tk.NW)
        
        # self.canvas.create_text(100, 50, text='Race', font=('Arial', 20), fill='white') # Text
        # race = tk.Text(self.canvas, height = 2, width = 5)
        # self.canvas.create_window(100, 100, window=inputtxt, anchor=tk.NW)

        # self.canvas.create_text(100, 50, text='Level', font=('Arial', 20), fill='white') # Text
        # self.canvas.create_text(100, 50, text='Player_Class', font=('Arial', 20), fill='white') # Text
        # self.canvas.create_text(100, 50, text='Attributes', font=('Arial', 20), fill='white') # 6 drop down range from 0-20: str, dex, int, con, app, pow
        # self.canvas.create_text(100, 50, text='Inventory', font=('Arial', 20), fill='white') # Text
        # self.canvas.create_text(100, 50, text='Background', font=('Arial', 20), fill='white') # Text

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
