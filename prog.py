import tkinter as tk
import tkinter.messagebox
import random


class App:
    def __init__(self, root):
        # Setting title
        root.title("Sea Battle")
        # Setting window size
        width = 500
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        # root.resizable(width=False, height=False)

        grid_size = 10
        max_size = 250  # Half the size of the window
        button_size = max_size // grid_size
        start_x = (width - button_size * grid_size) // 2
        start_y = (height - button_size * grid_size) // 2

        self.buttons = []

        # Create the grid of buttons
        for row in range(grid_size):
            row_buttons = []
            for col in range(grid_size):
                btn = tk.Button(root, text="0", command=lambda r=row, c=col: self.grid_btn_onclick(r, c))
                btn.place(x=start_x + col * button_size, y=start_y + row * button_size, width=button_size,
                          height=button_size)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Create the start and stop buttons
        start_btn = tk.Button(root, text="Почати гру", command=self.start_btn_onclick)
        start_btn.place(x=400, y=460, width=70, height=25)

        start_btn = tk.Button(root, text="Почати", command=self.start_btn_onclick)
        start_btn.place(x=30, y=460, width=70, height=25)

        stop_btn = tk.Button(root, text="Наступна дія", command=self.stop_btn_onclick)
        stop_btn.place(x=200, y=460, width=100, height=25)

        self.is_active = False

        ###
        lbl1 = tk.Label(root, text="Морський Бій")
        lbl1.place(x=200, y=10)
        dictation = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j'}
        for col in range(1, 11):
            lbl1 = tk.Label(root, text=dictation[col])
            lbl1.place(x=start_x + col * button_size - button_size, y=start_y - button_size, width=button_size,
                       height=button_size)

        for row in range(1, 11):
            lbl1 = tk.Label(root, text=str(row))
            lbl1.place(x=start_x - button_size, y=start_y + row * button_size - button_size, width=button_size,
                       height=button_size)

    ###
    def grid_btn_onclick(self, row, col):
        btn = self.buttons[row][col]
        if btn["bg"] == "light blue":
            print(f"Button {row},{col} clicked - This is a special button")
            tk.messagebox.showinfo("Button Click", f"Button {row},{col} is special!")
        else:
            print(f"Button {row},{col} clicked")

    def start_btn_onclick(self):
        self.is_active = True
        lbl1 = tk.Label(root, text="Ready? START!")
        lbl1.place(x=200, y=10)

        # Вибір випадкової кнопки
        random_row = random.randint(0, 9)
        random_col = random.randint(0, 9)
        random_button = self.buttons[random_row][random_col]
        random_button.config(bg='lightblue', text="■")

    def stop_btn_onclick(self):
        if self.is_active:
            self.is_active = False
            lbl1 = tk.Label(root, text="First, let's place the ship of 4 cells")
            lbl1.place(x=200, y=10)
        else:
            lbl1 = tk.Label(root, text="Спочатку натисніть кнопку 'Почати'")
            lbl1.place(x=200, y=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
