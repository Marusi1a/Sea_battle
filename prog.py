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
        max_size = 250
        button_size = max_size // grid_size
        start_x = (width - button_size * grid_size) // 2
        start_y = (height - button_size * grid_size) // 2

        self.buttons = []

        # Create the grid of buttons
        for row in range(grid_size):
            row_buttons = []
            for col in range(grid_size):
                btn = tk.Button(root, text="0", command=lambda r=row, c=col: self.on_button_click(r, c))
                btn.place(x=start_x + col * button_size, y=start_y + row * button_size, width=button_size,
                          height=button_size)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        start_btn1 = tk.Button(root, text="Почати гру", command=self.start_bnt_onclick1)
        start_btn1.place(x=400, y=460, width=70, height=25)

        start_btn = tk.Button(root, text="Почати", command=self.start_btn_onclick)
        start_btn.place(x=30, y=460, width=70, height=25)
        stop_btn = tk.Button(root, text="Наступна дія", command=self.stop_btn_onclick)
        stop_btn.place(x=200, y=460, width=100, height=25)

        self.is_active = False
        self.actions = ["", "Розтавляємо корабель по 4", "Розтавляємо корабель по 3", "Розтавляємо корабелі по 2",
                        "Розтавляємо корабелі по 1"]
        self.current_action_index = 0

        self.lbl1 = tk.Label(root, text="Морський Бій")
        self.lbl1.place(x=200, y=10)

        dictation = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j'}
        for col in range(1, 11):
            lbl1 = tk.Label(root, text=dictation[col])
            lbl1.place(x=start_x + col * button_size - button_size, y=start_y - button_size, width=button_size,
                       height=button_size)

        for row in range(1, 11):
            lbl1 = tk.Label(root, text=str(row))
            lbl1.place(x=start_x - button_size, y=start_y + row * button_size - button_size, width=button_size,
                       height=button_size)

    def right_side_ship(self, col, len_ship):
        return col + len_ship <= 10

    def take_ship_row(self, row, col, len_ship):
        for i in range(len_ship):
            self.buttons[row][col + i].config(bg='lightblue', text="■")
            self.buttons[row][col + i].config(state="disabled")
            if row != 0:
                self.buttons[row - 1][col + i].config(state="disabled", text="x")
            if row != 9:
                self.buttons[row + 1][col + i].config(state="disabled", text="x")
        if col + len_ship < 10:
            self.buttons[row - 1][col + len_ship].config(state="disabled", text="x")
            self.buttons[row + 1][col + len_ship].config(state="disabled", text="x")
            self.buttons[row][col + len_ship].config(state="disabled", text="x")
        if col - 1 >= 0:
            self.buttons[row - 1][col - 1].config(state="disabled", text="x")
            self.buttons[row + 1][col - 1].config(state="disabled", text="x")
            self.buttons[row][col - 1].config(state="disabled", text="x")

    def on_button_click(self, row, col):
        if self.current_action_index == 1:
            len_ship = 4
            if self.right_side_ship(col, len_ship):
                self.take_ship_row(row, col, len_ship)
        elif self.current_action_index == 2:
            len_ship = 3
            self.take_ship_row(row, col, len_ship)
        elif self.current_action_index == 3:
            len_ship = 2
            self.take_ship_row(row, col, len_ship)
        elif self.current_action_index == 4:
            len_ship = 1
            self.take_ship_row(row, col, len_ship)

    def grid_btn_onclick(self, row, col):
        btn = self.buttons[row][col]
        if btn["bg"] == "light blue":
            print(f"Button {row},{col} clicked - This is a special button")
            tk.messagebox.showinfo("Button Click", f"Button {row},{col} is special!")
        else:
            print(f"Button {row},{col} clicked")

    def start_btn_onclick(self):
        self.is_active = True
        self.current_action_index = max(0, self.current_action_index - 1)
        self.update_label(self.actions[self.current_action_index])

    # lbl1 = tk.Label(root, text="Ready? START!")
    #  lbl1.place(x=200, y=10)

    def stop_btn_onclick(self):
        if not self.is_active:
            self.update_label("Спочатку натисніть кнопку 'Почати'")
            return

        self.current_action_index += 1
        if self.current_action_index >= len(self.actions):
            self.update_label("Всі кораблі розміщені")
            return

        self.update_label(self.actions[self.current_action_index])

    def update_label(self, text):

        self.lbl1.config(text=text)

    def start_bnt_onclick1(self):
        self.is_active = True

        random_row = random.randint(0, 9)
        random_col = random.randint(0, 9)
        random_button = self.buttons[random_row][random_col]
        random_button.config(bg='lightblue', text="■")
        lbl1 = tk.Label(root, text="Гра почалась!")
        lbl1.place(x=200, y=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()