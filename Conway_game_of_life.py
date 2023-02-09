import numpy as np
import pygame

# setting
prob_cell = 0.4  # 0.4  # probability tha a cell is alive at the beginning
cell_size = 4  # increase this value if the computer is slow
size = width, height = 500, 500  # must be a multiple of cell_size (decrease if the computer is slow)
col_live = (50, 255, 50)  # living cells color
col_back = (0, 0, 0)  # background color
time_int = 100  # interval between screen update (in ms)
from_centre = 0  # 0 = draw everywhere on the screen; 1 = draw only in the centre of the screen


class Board:
    def __init__(self, b_height, b_width):
        self.h = int(b_height / cell_size)
        self.w = int(b_width / cell_size)
        self.world = np.zeros((self.h, self.w), dtype=int)
        self.prev_gen = np.zeros((self.h, self.w), dtype=int)

    def copy_board(self):
        self.prev_gen = self.world.copy()

    def set_state(self, i, j, state):
        self.world[i][j] = state

    def get_cur_state(self, i, j):
        # get the current state
        return self.world[i][j]

    def get_prev_state(self, i, j):
        # get the state of the previous generation (used to create a new generation)
        return self.prev_gen[i][j]

    def get_neigh(self, i, j):
        n_neigh = 0
        for y in [-1, 0, 1]:
            for x in [-1, 0, 1]:
                if not ((y == 0) and (x == 0)):
                    r = (i + y) % self.h  # row
                    c = (j + x) % self.w  # column
                    n_neigh += self.get_prev_state(r, c)
        return n_neigh

    def rule(self, i, j):
        n_neigh = self.get_neigh(i, j)
        state = self.get_prev_state(i, j)
        if (state == 1) and ((n_neigh < 2) or (n_neigh > 3)):
            new_state = 0
        elif (state == 0) and (n_neigh == 3):
            new_state = 1
        else:
            new_state = state
        self.set_state(i, j, new_state)

    def set_rand_states(self):
        # draw only in the centre of the screen
        if from_centre:
            y_from = int(self.h * 0.45)
            y_to = int(self.h * 0.65)
            x_from = int(self.w * 0.45)
            x_to = int(self.w * 0.65)
            for y in range(y_from, y_to):
                for x in range(x_from, x_to):
                    if (np.random.uniform(low=0, high=1, size=1)) > (1 - prob_cell):
                        self.set_state(y, x, 1)
        # draw everywhere on the screen
        elif not from_centre:
            for y in range(self.h):
                for x in range(self.w):
                    if (np.random.uniform(low=0, high=1, size=1)) > (1 - prob_cell):
                        self.set_state(y, x, 1)

    def new_gen(self):
        self.copy_board()
        for h in range(self.h):
            for w in range(self.w):
                self.rule(h, w)


# define a main function
def main():
    # initialize the pygame module
    pygame.init()

    # initialize clock object
    clock = pygame.time.Clock()

    # Define cells and grid
    grid = Board(b_height=height, b_width=width)

    # set the cells to a random state
    grid.set_rand_states()

    # create a surface on screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(f"Conway's game of life")

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

        for r in range(grid.h):
            for c in range(grid.w):
                cur_state = grid.get_cur_state(r, c)
                if cur_state == 1:
                    pygame.draw.rect(screen, col_live, pygame.Rect(c*cell_size, r*cell_size, cell_size, cell_size))

        pygame.display.update()
        screen.fill(col_back)

        grid.new_gen()

        # Wait
        clock.tick(int(1000/time_int))


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
