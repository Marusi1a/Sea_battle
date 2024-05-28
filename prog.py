import tkinter as tk
import tkinter.messagebox
import random


class App:

    def __init__(self, root):
        # Setting title
        root.title("Sea Battle")
        # Setting window size
        width = 900
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
        self.buttons_ships = []

        # Create the grid of buttons
        for row in range(grid_size):
            row_buttons = []
            for col in range(grid_size):
                btn = tk.Button(root, text="0", command=lambda r=row, c=col: self.on_button_click(r, c))
                btn.place(x=start_x * 1.5 + col * button_size, y=start_y + row * button_size, width=button_size,
                          height=button_size)
                row_buttons.append(btn)
            self.buttons_ships.append(row_buttons)

        for row in range(grid_size):
            row_buttons = []
            for col in range(grid_size):
                btn = tk.Button(root, text="0", command=lambda r=row, c=col: self.on_button_click(r, c))
                btn.place(x=start_x * 0.5 + col * button_size, y=start_y + row * button_size, width=button_size,
                          height=button_size)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        self.ship_orientation = tk.BooleanVar()
        self.ship_orientation.set(True)  # Початкове значення - горизонтальна орієнтація

        self.radio_horizontal = tk.Radiobutton(root, text="Горизонтально", variable=self.ship_orientation, value=True)
        self.radio_horizontal.place(x=30, y=400)

        self.radio_vertical = tk.Radiobutton(root, text="Вертикально", variable=self.ship_orientation, value=False)
        self.radio_vertical.place(x=30, y=430)
        start_btn1 = tk.Button(root, text="Почати гру", command=self.start_bnt_onclick1)
        start_btn1.place(x=700, y=460, width=70, height=25)
        start_btn = tk.Button(root, text="Почати", command=self.start_btn_onclick)
        start_btn.place(x=450, y=460, width=70, height=25)
        stop_btn = tk.Button(root, text="Наступна дія", command=self.stop_btn_onclick)
        stop_btn.place(x=550, y=460, width=100, height=25)
        final_btn1 = tk.Button(root, text="В бій", command=self.finding_enemy)
        final_btn1.place(x=780, y=460, width=70, height=25)
        self.is_active = False
        self.actions = ["", "Розтавляємо корабель по 4", "Розтавляємо корабель по 3", "Розтавляємо корабелі по 2",
                        "Розтавляємо корабелі по 1"]
        self.current_action_index = 0

        self.lbl1 = tk.Label(root, text="Морський Бій")
        self.lbl1.place(x=500, y=10)

        dictation = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j'}
        for col in range(1, 11):
            lbl1 = tk.Label(root, text=dictation[col])
            lbl1.place(x=start_x * 1.5 + col * button_size - button_size, y=start_y - button_size, width=button_size,
                       height=button_size)

        for row in range(1, 11):
            lbl1 = tk.Label(root, text=str(row))
            lbl1.place(x=start_x * 1.5 - button_size, y=start_y + row * button_size - button_size, width=button_size,
                       height=button_size)

        dictation = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j'}
        for col in range(1, 11):
            lbl1 = tk.Label(root, text=dictation[col])
            lbl1.place(x=start_x * 0.5 + col * button_size - button_size, y=start_y - button_size, width=button_size,
                       height=button_size)

        for row in range(1, 11):
            lbl1 = tk.Label(root, text=str(row))
            lbl1.place(x=start_x * 0.5 - button_size, y=start_y + row * button_size - button_size, width=button_size,
                       height=button_size)

        self.ship_counts = {4: 1, 3: 2, 2: 3, 1: 4}
        self.placed_ships = {4: 0, 3: 0, 2: 0, 1: 0}
        self.previous_state = None  # Додай змінну для збереження попереднього стану

    def right_side_ship(self, col, len_ship):
        return col + len_ship <= 10

    def down_ship(self, row, len_ship):
        return row + len_ship <= 10

    def can_place_ship_row(self, row, col, len_ship):
        for i in range(len_ship):
            if self.buttons[row][col + i].cget("text") == "x":
                return False
        return True

    def can_place_ship_col(self, row, col, len_ship):
        for i in range(len_ship):
            if self.buttons[row + i][col].cget("text") == "x":
                return False
        return True

    def take_ship_row(self, row, col, len_ship):
        if not self.can_place_ship_row(row, col, len_ship):
            tk.messagebox.showwarning("Помилка", "Неможливо розташувати корабель тут!")
            return

        for i in range(len_ship):
            self.buttons_ships[row][col + i].config(bg='lightblue', text="■")
            self.buttons_ships[row][col + i].config(state="disabled")
            if row != 0:
                self.buttons_ships[row - 1][col + i].config(state="disabled", text="x")
            if row != 9:
                self.buttons_ships[row + 1][col + i].config(state="disabled", text="x")

        if col + len_ship < 10:
            if row != 0:
                self.buttons_ships[row - 1][col + len_ship].config(state="disabled", text="x")
            if row != 9:
                self.buttons_ships[row + 1][col + len_ship].config(state="disabled", text="x")
            self.buttons_ships[row][col + len_ship].config(state="disabled", text="x")
        if col - 1 >= 0:
            if row != 0:
                self.buttons_ships[row - 1][col - 1].config(state="disabled", text="x")
            if row != 9:
                self.buttons_ships[row + 1][col - 1].config(state="disabled", text="x")
            self.buttons_ships[row][col - 1].config(state="disabled", text="x")

        self.placed_ships[len_ship] += 1

    def take_ship_col(self, row, col, len_ship):
        if not self.can_place_ship_col(row, col, len_ship):
            tk.messagebox.showwarning("Помилка", "Неможливо розташувати корабель тут!")
            return

        for i in range(len_ship):
            self.buttons_ships[row + i][col].config(bg='lightblue', text="■")
            self.buttons_ships[row + i][col].config(state="disabled")
            if col != 0:
                self.buttons_ships[row + i][col - 1].config(state="disabled", text="x")
            if col != 9:
                self.buttons_ships[row + i][col + 1].config(state="disabled", text="x")

        if row + len_ship < 10:
            if col != 0:
                self.buttons_ships[row + len_ship][col - 1].config(state="disabled", text="x")
            if col != 9:
                self.buttons_ships[row + len_ship][col + 1].config(state="disabled", text="x")
            self.buttons_ships[row + len_ship][col].config(state="disabled", text="x")
        if row - 1 >= 0:
            if col != 0:
                self.buttons_ships[row - 1][col - 1].config(state="disabled", text="x")
            if col != 9:
                self.buttons_ships[row - 1][col + 1].config(state="disabled", text="x")
            self.buttons_ships[row - 1][col].config(state="disabled", text="x")
            self.placed_ships[len_ship] += 1

    def on_button_click(self, row, col):
        if self.current_action_index == 1:
            len_ship = 4
        elif self.current_action_index == 2:
            len_ship = 3
        elif self.current_action_index == 3:
            len_ship = 2
        elif self.current_action_index == 4:
            len_ship = 1
        else:
            return
        if self.placed_ships[len_ship] >= self.ship_counts[len_ship]:
            tk.messagebox.showwarning("Помилка", f"Ви вже розмістили всі кораблі довжиною {len_ship} клітинки!")
            return

        if self.ship_orientation.get():  # Горизонтальне розміщення
            if self.right_side_ship(col, len_ship):
                self.take_ship_row(row, col, len_ship)
        else:  # Вертикальне розміщення
            if self.down_ship(row, len_ship):
                self.take_ship_col(row, col, len_ship)


    def can_place_ship(self, grid, row, col, length, direction):
        if direction == 'horizontal':
            if col + length > 10:
                return False
            for i in range(length):
                if grid[row][col + i]['text'] == '■':
                    return False
            for i in range(max(0, row - 1), min(10, row + 2)):
                for j in range(max(0, col - 1), min(10, col + length + 1)):
                    if grid[i][j]['text'] == '■':
                        return False
        elif direction == 'vertical':
            if row + length > 10:
                return False
            for i in range(length):
                if grid[row + i][col]['text'] == '■':
                    return False
            for i in range(max(0, row - 1), min(10, row + length + 1)):
                for j in range(max(0, col - 1), min(10, col + 2)):
                    if grid[i][j]['text'] == '■':
                        return False
        return True

    def place_ship(self, grid, row, col, length, direction):
        if direction == 'horizontal':
            for i in range(length):
                grid[row][col + i].config(bg='lightblue', text='■')
        elif direction == 'vertical':
            for i in range(length):
                grid[row + i][col].config(bg='lightblue', text='■')

    def place_random_ship(self, grid, length):
        direction = random.choice(['horizontal', 'vertical'])
        row, col = random.randint(0, 9), random.randint(0, 9)
        while not self.can_place_ship(grid, row, col, length, direction):
            direction = random.choice(['horizontal', 'vertical'])
            row, col = random.randint(0, 9), random.randint(0, 9)
        self.place_ship(grid, row, col, length, direction)

    def place_all_ships(self, grid):
        for length in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
            self.place_random_ship(grid, length)

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
        self.place_all_ships(self.buttons)
        self.update_label("Гра почалась!")

    def place_ship_randomly_col(self, row, col, len_ship):
        if self.down_ship(row, len_ship):
            if self.ship_orientation.get():
                col_ship = col
                row_ship = row
            else:
                col_ship = row
                row_ship = col
            self.take_ship_col(row_ship, col_ship, len_ship)

    def save_previous_state(self):
        self.previous_state = []
        for row in self.buttons:
            row_state = []
            for btn in row:
                row_state.append((btn.cget("bg"), btn.cget("text"), btn["state"]))
            self.previous_state.append(row_state)
        self.undo_stack.append(self.previous_state)

    def finding_enemy(self):
        for row in range(len(self.buttons)):
            for col in range(len(self.buttons[row])):
                btn = self.buttons[row][col]
                if btn['state'] == 'normal':  # Перевіряємо, чи кнопка активована користувачем
                    if self.buttons_ships[row][col]['text'] == '■':  # Влучення в корабель ворога
                        btn.config(bg='red')
                    else:
                        btn.config(bg='pink')
                    btn.config(state='disabled')  # Деактивуємо кнопку після натискання
                    return


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()