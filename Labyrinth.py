import tkinter as tk
import tkinter.messagebox as msg
import random
from numpy.random import choice
import time


class Gui:
    def __init__(self):
        self.window = root
        self.window.title("Generic Algorithm with Labyrinth")
        self.canvas_size = 700  # canvas
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, background="orange")
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
        size100 = tk.Radiobutton(self.frame, text='50x50', variable=self.size, value=100).grid(column=1, row=0)
        frame_ran = tk.Radiobutton(self.frame, text='Rastgele', variable=self.input_type, value="Random",
                                   command=self.obstacle_random).grid(column=0, row=1)
        frame_us = tk.Radiobutton(self.frame, text='Kullanıcı Girişi', variable=self.input_type, value="User",
                                  command=self.add_buttons).grid(column=1, row=1)
        button = tk.Button(self.frame, text="RUN", command=create_population).grid(column=1, row=3, sticky='nsew', padx=2)
        self.text = tk.Text(self.frame, width=20, height=10)
        self.text.grid(column=0, row=4)
        self.generation_label = tk.Label(self.window, font='Calibri 16 bold')
        self.generation_label.grid(column=1, row=1)

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
        self.text.delete('1.0', tk.END)
        self.buffer = (self.canvas_size - self.size.get()) / self.size.get()

        for j in range(0, self.size.get()):
            for i in range(0, self.size.get()):

                if i == 0 or i == self.size.get() - 1 or j == 0 or j == self.size.get() - 1:
                    self.canvas.create_rectangle(i * self.buffer + i, j * self.buffer + j, (i + 1) * self.buffer + i,
                                                 (j + 1) * self.buffer + j, fill="green", outline="brown")
                else:
                    self.canvas.create_rectangle(i * self.buffer + i, j * self.buffer + j, (i + 1) * self.buffer + i,
                                                 (j + 1) * self.buffer + j, fill="orange", outline="orange red")
        rect = self.canvas.find_closest(self.buffer + 2, self.buffer + 2)
        self.canvas.itemconfigure(rect, fill="light pink")
        rect = self.canvas.find_closest(self.buffer * (self.size.get() - 1) + self.size.get() - 3,
                                        self.buffer * (self.size.get() - 1) + self.size.get() - 3)
        self.canvas.itemconfigure(rect, fill="hot pink")

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
            x_pos = random.randint(0, int(self.canvas_size - (3 * self.buffer + 3)))
            y_pos = random.randint(0, int(self.canvas_size - (3 * self.buffer + 3)))
            self.obstacle_count += self.check_obstacle(x_dir, y_dir, x_pos, y_pos)


class Population:
    def __init__(self, pop_size, chr_size):
        self.pop_size = pop_size
        self.chr_size = chr_size
        self.total_fitness = 0
        self.population = []
        self.distributions = []


class Chromosome:
    def __init__(self, chr_size):
        self.chr_size = chr_size
        self.chromosome = []
        self.fitness = 0
        self.collide = 0
        self.first_collide = -1
        self.distance = 0
        self.traveled = 0
        self.path = []


def direction_finder(direction):
    if direction == 1:
        return -1, 0
    elif direction == 2:
        return 0, 1
    elif direction == 3:
        return 1, 0
    elif direction == 4:
        return 0, -1


def is_there_an_obstacle(x, y, move_x, move_y):
    x += move_x
    y += move_y
    rectangle = gui.canvas.find_overlapping(x * gui.buffer + x, y * gui.buffer + y,
                                            (x + 1) * gui.buffer + x, (y + 1) * gui.buffer + y)
    if gui.canvas.itemcget(rectangle, 'fill') == "green":  # obstacle
        return True, None
    else:
        return False, rectangle


def manhattan_distance(x, y, x_in, y_in):
    return abs(x_in - x) + abs(y_in - y)


def calculate_fitness(population):

    total_fitness = 0
    for j in range(population.pop_size):
        x = 1
        y = 1
        chromosome = population.population[j]
        i = 0
        for i in range(chromosome.chr_size):
            direction = chromosome.chromosome[i]
            # print(direction)
            move_x, move_y = direction_finder(direction)
            obstacle, rectangle = is_there_an_obstacle(x, y, move_x, move_y)

            if obstacle:
                chromosome.collide += 1
                if chromosome.first_collide == -1:
                    chromosome.first_collide = manhattan_distance(x, y, 1, 1)
            else:
                x += move_x
                y += move_y
                chromosome.path.append(rectangle)
        chromosome.traveled = manhattan_distance(x, y, 1, 1)  # şu ana kadar gittiği yol
        chromosome.distance = manhattan_distance(x, y, gui.size.get() - 2, gui.size.get() - 2)  # tahmini kalan yol
        if chromosome.distance == 0:
            chromosome.fitness = 1
        else:
            chromosome.fitness = 0.1 * (1 - chromosome.traveled / (gui.size.get() * 2)) \
                               + 0.9 * (1 - chromosome.distance / (gui.size.get() * 2)) \
                               + 0.0 * (1 - chromosome.collide / chromosome.chr_size) \
                               + 0.0 * (chromosome.first_collide / (gui.size.get() * 2))

        total_fitness += chromosome.fitness
    population.total_fitness = total_fitness

    for i in range(population.pop_size):
        population.distributions.append(population.population[i].fitness / population.total_fitness)


def roulette_wheel_selection(population):
    chromosomes = []
    for i in range(population.pop_size):
        chromosomes.append(i)
    index = choice(chromosomes, p=population.distributions)
    return population.population[index]


def uniform_crossover(parent1, parent2):
    child1 = []
    child2 = []
    for i in range(parent1.chr_size):
        temp = random.randint(0, 1)
        if temp == 0:
            child1.append(parent2.chromosome[i])
            child2.append(parent1.chromosome[i])
        else:
            child1.append(parent1.chromosome[i])
            child2.append(parent2.chromosome[i])
    temp = random.randint(0, 1)
    chromosome = Chromosome(parent1.chr_size)
    if temp == 0:
        chromosome.chromosome = child1
    else:
        chromosome.chromosome = child2
    return chromosome


def mutate(child):
    for i in range(int(child.chr_size/5)):
        index = random.randint(0, child.chr_size - 1)
        direction = random.randint(1, 4)
        child.chromosome[index] = direction
    return child


def find_best(population):
    max = 0
    max_index = 0
    for i in range(population.pop_size):
        if population.population[i].fitness > max:
            max = population.population[i].fitness
            max_index = i
    return population.population[max_index]


def genetic_algorithm(population, start):
    generation_number = 0
    populations = []
    best_child = Chromosome(population.chr_size)
    best_child.distance = 99

    while generation_number < 10 and best_child.distance > 0:
        print(generation_number)
        calculate_fitness(population)
        new_population = Population(20, 20)
        for i in range(population.pop_size):
            x = roulette_wheel_selection(population)
            y = roulette_wheel_selection(population)
            child = uniform_crossover(x, y)
            if random.randint(1, 5) == 1:
                child = mutate(child)
            new_population.population.append(child)
        best_child = find_best(population)
        populations.append(best_child)
        population = new_population
        generation_number += 1

    return populations


def visualize_populations(populations):
    index = len(populations) - 1
    path_size = len(populations[index].path)

    for j in range(path_size - 1):
        rectangle = populations[index].path[j]
        gui.canvas.itemconfigure(rectangle, fill="red")
    rectangle = populations[index].path[path_size - 1]
    gui.canvas.itemconfigure(rectangle, fill="blue")

    message = "Path Size: {}\nNumber of Collides: {}\nFirst Collide: {}\nDistance: {}".\
        format(path_size, populations[index].collide, populations[index].first_collide, populations[index].distance)
    generation_number = "{}".format(index)
    gui.text.insert(tk.END, message)
    gui.generation_label.config(text=generation_number)
    print("Path Size: ", path_size)
    print("Number of collides: ", populations[index].collide)
    print("First collide: ", populations[index].first_collide)
    print("Distance: ", populations[index].distance)


def create_population():
    start = time.time()
    pop = Population(gui.size.get()*gui.size.get(), int((gui.size.get()*gui.size.get()/4)))
    for i in range(pop.pop_size):
        chromosome = Chromosome(pop.chr_size)
        for j in range(chromosome.chr_size):
            chromosome.chromosome.append(random.randint(1, 4))
        pop.population.append(chromosome)
    populations = genetic_algorithm(pop, start)
    visualize_populations(populations)


if __name__ == "__main__":
    root = tk.Tk()
    gui = Gui()
    root.mainloop()


