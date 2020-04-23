import tkinter as tk
import tkinter.messagebox as msg
import random


class Gui:
    def __init__(self, window):
        self.window = window
        self.window.title("Generic Algorithm with Labyrinth")
        self.canvas = tk.Canvas(window, width=700, height=700, background="orange")
        self.canvas.grid(column=1, row=0)
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=0, column=0, sticky="n")
        self.size = tk.IntVar()
        self.input_type = tk.StringVar()
        self.direction = tk.IntVar()
        self.buffer = 0
        self.k = 0
        self.obstacle_count = 0
        size20 = tk.Radiobutton(self.frame, text='20x20', variable=self.size, value=20).grid(column=0, row=0)
        size100 = tk.Radiobutton(self.frame, text='100x100', variable=self.size, value=100).grid(column=1, row=0)
        frame_ran = tk.Radiobutton(self.frame, text='Rastgele', variable=self.input_type, value="Random",
                                   command=self.obstacle_random).grid(column=0, row=1)
        frame_us = tk.Radiobutton(self.frame, text='Kullanıcı Girişi', variable=self.input_type, value="User",
                                  command=self.add_buttons).grid(column=1, row=1)

    def add_buttons(self):
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.obstacle_user)
        self.obstacle_count = 0
        vertical = tk.Radiobutton(self.frame, text="Dikey", variable=self.direction, value=0).grid(column=0, row=2)
        horizontal = tk.Radiobutton(self.frame, text="Yatay", variable=self.direction, value=1).grid(column=1, row=2)
        msg.showinfo(title="Bilgi", message="Engel koymak istediğiniz kutuların üzerine tıklayınız.")

    def draw_grid(self):
        if self.size.get() == 0:
            return
        elif self.size.get() == 20:
            self.k = 10
        elif self.size.get() == 100:
            self.k = 100
        self.canvas.delete("all")
        self.buffer = (700 - self.size.get()) / self.size.get()

        for j in range(0, self.size.get()):
            for i in range(0, self.size.get()):
                self.canvas.create_rectangle(i * self.buffer + i, j * self.buffer + j, (i + 1) * self.buffer + i,
                                             (j + 1) * self.buffer + j, fill="orange", outline="orange red")
        rect = self.canvas.find_closest(1, 1)
        self.canvas.itemconfigure(rect, fill="purple")
        rect = self.canvas.find_closest(699, 699)
        self.canvas.itemconfigure(rect, fill="purple")

    def check_obstacle(self, x_dir, y_dir, x_pos, y_pos):
        x = x_pos
        y = y_pos

        rect1 = self.canvas.find_closest(x, y)
        rect2 = self.canvas.find_closest(x + x_dir * self.buffer * 1, y + y_dir * self.buffer * 1)
        rect3 = self.canvas.find_closest(x + x_dir * self.buffer * 2, y + y_dir * self.buffer * 2)
        rect4 = self.canvas.find_closest(x + x_dir * self.buffer * 3, y + y_dir * self.buffer * 3)

        if (self.canvas.itemcget(rect1, 'fill') == "orange" and self.canvas.itemcget(rect2, 'fill') == "orange"
                and self.canvas.itemcget(rect3, 'fill') == "orange" and self.canvas.itemcget(rect4, 'fill')
                == "orange"):
            if rect1 != rect2 and rect2 != rect3 and rect3 != rect4:
                self.canvas.itemconfigure(rect1, fill="green", outline="brown")
                self.canvas.itemconfigure(rect2, fill="green", outline="brown")
                self.canvas.itemconfigure(rect3, fill="green", outline="brown")
                self.canvas.itemconfigure(rect4, fill="green", outline="brown")
                return 1
            elif self.input_type == "User":
                msg.showwarning(title="Uyarı", message="Engel koymak istediğiniz kutuların sınır bölgelerine değil, "
                                                       "orta noktalarına tıklayınız.")
        return 0

    def obstacle_user(self, event):
        if self.obstacle_count < self.k:
            x_dir = self.direction.get()
            y_dir = 1 - x_dir
            print(event.x, event.y)
            x_pos = event.x
            y_pos = event.y
            self.obstacle_count += self.check_obstacle(x_dir, y_dir, x_pos, y_pos)
        else:
            msg.showinfo(title="Bilgi", message="Maksimum engel sayısına ulaşıldı.")

    def obstacle_random(self):
        self.draw_grid()
        self.obstacle_count = 0
        while self.obstacle_count < self.k:
            x_dir = random.randint(0, 1)  # 0: horizontal, 1: vertical
            y_dir = 1 - x_dir
            x_pos = random.randint(0, 700 - (3 * self.buffer + 3))
            y_pos = random.randint(0, 700 - (3 * self.buffer + 3))
            self.obstacle_count += self.check_obstacle(x_dir, y_dir, x_pos, y_pos)


if __name__ == "__main__":
    root = tk.Tk()
    gui = Gui(root)

    root.mainloop()
