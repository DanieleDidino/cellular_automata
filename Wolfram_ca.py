import pygame
import numpy as np

# Setting
rule_n = 99  # Set the rule (must be between 0 and 256), try: 22, 30, 99
central_point = True  # start from a single central point?
size = width, height = 600, 300  # window size
col = (255, 255, 255)  # color living cells
col_back = 0, 0, 0  # background color
time_int = 1  # interval between screen update (in ms)


class Cells:
    def __init__(self, n_cells):
        self.n_cells = n_cells
        self.cell_states = np.zeros(n_cells)
        self.previous_states = np.zeros(n_cells)

    def set_cell_states(self, new_state):
        self.cell_states = new_state

    def set_previous_state(self):
        self.previous_states = self.get_cell_states()

    def get_cell_states(self):
        return self.cell_states

    def get_neighs(self, cell):
        left = self.previous_states[(cell - 1) % self.n_cells]
        middle = self.previous_states[cell]
        right = self.previous_states[(cell + 1) % self.n_cells]
        # Convert "left, middle, right" (which are binary) to a base 10 number,
        # and subtract is from 7. This result is used to select the outcome of
        # the rule, which is described in a 8-element array.
        return 7 - int((4 * left) + (2 * middle) + right)

    def rule_n(self, rule):
        # Convert "rule" to a 8-digit binary number
        rule_bin = ('0' * (8 - len(bin(rule)[2:]))) + bin(rule)[2:]
        self.set_previous_state()
        next_gen = np.empty(0)
        for i in range(self.n_cells):
            neigh = self.get_neighs(i)
            next_gen = np.append(next_gen, int(rule_bin[neigh]))
        return next_gen


class Grid:
    def __init__(self, n_cells, nrows):
        self.n_cells = n_cells
        self.cells = []
        for r in range(nrows):
            cell_line = Cells(n_cells)
            self.cells.append(cell_line)
        if central_point:
            first_gen = np.zeros(n_cells)
            first_gen[int(n_cells / 2)] = 1
            self.cells[nrows - 1].set_cell_states(first_gen)
        else:
            first_gen = np.random.randint(0, 2, n_cells)
            self.cells[nrows - 1].set_cell_states(first_gen)

    def next_generation(self, rule):
        self.cells.pop(0)
        n_cells = len(self.cells)
        for i in range(n_cells):
            if i == (n_cells - 1):
                new_gen = self.cells[i].rule_n(rule)
                c_new = Cells(self.n_cells)
                c_new.set_cell_states(new_gen)
                self.cells.append(c_new)


# define a main function
def main(rule):

    # initialize the pygame module
    pygame.init()

    # initialize clock object
    clock = pygame.time.Clock()

    # Define cells and grid
    n_cells = width
    cell_auto = Grid(n_cells=n_cells, nrows=height)

    # create a surface on screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(f"Wolfram Cellular Automata - Rule {rule}")

    # define a variable to control the main loop
    running = True

    # main loop
    while running:

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        cell_auto.next_generation(rule)

        for r in range(len(cell_auto.cells)):
            line = cell_auto.cells[r].get_cell_states()
            for nc in range(n_cells):
                if line[nc] == 1:
                    # col = (255, 255, 255)
                    screen.set_at((nc, r), col)

        pygame.display.update()
        screen.fill(col_back)

        # Wait
        clock.tick(int(1000/time_int))


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main(rule_n)
