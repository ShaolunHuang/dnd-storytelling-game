import cv2
import tkinter as tk


def edit_img():
    background = cv2.imread("resources/background.png")
    background = cv2.resize(background, (1280, 720))
    for i in range(10):
        background = cv2.GaussianBlur(background, (5, 5), cv2.BORDER_DEFAULT)
    cv2.imwrite("resources/background.png", background)


class DNDStorytellingGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('DND Storytelling Game')
        self.window.geometry('1280x720')
        self.window.resizable(False,False)
        self.show_home()
        
    def set_canvas(self):
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        self.background_img = tk.PhotoImage(file='resources/background.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)

        self.canvas.create_text(canvas_width/2, canvas_height/3.6, text='DND Storytelling Game', font=('Arial', 40), fill='white')

        start_button = tk.Button(self.window, text='Start', width=16, height=2, command=self.start)

        button_width = start_button.winfo_reqwidth()

        center_x = (canvas_width - button_width) / 2
        self.canvas.create_window(center_x, canvas_height/2, window=start_button, anchor=tk.NW)
        show_members_button = tk.Button(self.window, text='Show Members', width=16, height=2)
        self.canvas.create_window(center_x, canvas_height/72*42, window=show_members_button, anchor=tk.NW)
        show_img_button = tk.Button(self.window, text='Show Images', width=16, height=2)
        self.canvas.create_window(center_x, canvas_height/72*48, window=show_img_button, anchor=tk.NW)
        quit_button = tk.Button(self.window, text='Quit', width=16, height=2, command=self.window.quit)
        self.canvas.create_window(center_x, canvas_height/72*54, window=quit_button, anchor=tk.NW)


    def show_home(self):
        self.canvas = tk.Canvas(self.window, width=1280, height=720)
        self.canvas.pack(fill='both', expand=True)
        self.set_canvas()
        
    

        
    def start(self):
        self.canvas.delete('all')
        self.background_img = tk.PhotoImage(file='resources/old_book.png')
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tk.NW)
        self.canvas.create_text(640, 360, text='Start', font=('Arial', 40), fill='white')

    def mainloop(self):
        self.window.mainloop()


def main():
    # edit_img()
    game = DNDStorytellingGame()
    game.mainloop()


if __name__ == "__main__":
    main()
