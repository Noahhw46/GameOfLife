import pygame
import sys
import random
from pygame.locals import *
import pygame_menu


class Grid():
    def __init__(self, width, height, cell_size, colors):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[0 for x in range(width)] for y in range(height)]
        self.colors = colors
        self.randomize = False
    
    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[y][x] == 0:
                    rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                    screen.fill((self.colors['Dead_Cell']), rect)
                    pygame.draw.rect(screen, (self.colors['Border']), rect, 1)
                    
                else:
                    rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, (self.colors['Alive_Cell']), rect)

    
    def get_neighbors(self, x, y):
        pseudoneighbors = []
        neighbors = []
        #get the values for the 8 surrounding cells: when i,j = 0,0, it is the cell itself, otherwise it is a neighbor
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                #check if the cell is on the grid
                if x + i >= 0 and x + i < self.width and y + j >= 0 and y + j < self.height:
                    pseudoneighbors.append((y+j, x+i))
        #check if the cell is alive
        for cell in pseudoneighbors:
            if self.grid[cell[0]][cell[1]] == 1:
                neighbors.append(cell)
        return neighbors
    
    def random_fill(self, percent):
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < percent:
                    self.grid[y][x] = 1
    
    def update(self):
        new_grid = [[0 for x in range(self.width)] for y in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                neighbors = self.get_neighbors(x, y)
                if self.grid[y][x] == 0:
                    if len(neighbors) == 3:
                        new_grid[y][x] = 1
                else:
                    if len(neighbors) < 2 or len(neighbors) > 3:
                        new_grid[y][x] = 0
                    else:
                        new_grid[y][x] = 1
        self.grid = new_grid
    
    def randomize_colors(self):
        self.colors['Dead_Cell'] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.colors['Alive_Cell'] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.colors['Border'] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        

class Menu():
    def __init__(self):
        self.set_percent(0.5)
        self.clock_speed = 60
        self.randomize = False
        self.colors = {'Dead_Cell': (0,0,0), 'Alive_Cell': (255,255,255), 'Border': (255,255,255)}
        self.menu = pygame_menu.Menu('Game of Life', width, height, theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Auto Play', self.start_the_game_automatic)
        self.menu.add.toggle_switch('Randomize colors', default=False, onchange=self.toggle_randomize)
        self.menu.add.range_slider('Clock speed', range_values=(1, 60), increment=1, default=30, onchange=self.set_clock_speed)
        self.menu.add.range_slider('Percent of cells alive', range_values=(0, .99), increment=0.1, default=0.2, onchange=self.set_percent)
        self.menu.add.selector('Dead cell color', [('Black', (0,0,0)), ('White', (255,255,255)), ('Red', (255,0,0)), ('Green', (0,255,0)), ('Blue', (0,0,255)), ('Yellow', (255,255,0)), ('Purple', (255,0,255)), ('Cyan', (0,255,255))], onchange=self.set_dead_cell_color, selector_id='Dead cell color', selection_effect=None, font_color=(0,0,0))
        self.menu.add.selector('Alive cell color', [('White', (255, 255, 255)), ('Black', (0, 0, 0)), ('Red', (255,0,0)), ('Green', (0,255,0)), ('Blue', (0,0,255)), ('Yellow', (255,255,0)), ('Purple', (255,0,255)), ('Cyan', (0,255,255))], onchange=self.set_alive_cell_color, selector_id='Alive cell color', selection_effect=None, font_color=(255,255,255))
        self.menu.add.selector('Border color', [('White', (255, 255, 255)), ('Black', (0, 0, 0)), ('Red', (255,0,0)), ('Green', (0,255,0)), ('Blue', (0,0,255)), ('Yellow', (255,255,0)), ('Purple', (255,0,255)), ('Cyan', (0,255,255))], onchange=self.set_border_color, selector_id='Border color', selection_effect=None, font_color=(255,255,255))
        self.menu.add.button('Quit', pygame_menu.events.EXIT, button_id='Quit')
        self.menu.mainloop(screen)
    
    def set_percent(self, percent):
        self.percent = percent
    def set_clock_speed(self, clock_speed):
        self.clock_speed = clock_speed
    def toggle_randomize(self, value):
        self.randomize = value
        dead_cell_selector = self.menu.get_widget('Dead cell color')
        alive_cell_selector = self.menu.get_widget('Alive cell color')
        border_selector = self.menu.get_widget('Border color')
        quit = self.menu.get_widget('Quit')
        if self.randomize == True:
            self.menu.remove_widget(dead_cell_selector)
            self.menu.remove_widget(alive_cell_selector)
            self.menu.remove_widget(border_selector)
            self.menu.remove_widget(quit)
            self.menu.add.selector('Dead cell color', [('Random', (255, 255, 255))], onchange=self.set_dead_cell_color, selector_id='Dead cell color', selection_effect=None, font_color=(255, 255, 255))
            self.menu.add.selector('Alive cell color', [('Random', (255, 255, 255))], onchange=self.set_alive_cell_color, selector_id='Alive cell color', selection_effect=None, font_color=(255,255,255))
            self.menu.add.selector('Border color', [('Random', (255, 255, 255))], onchange=self.set_border_color, selector_id='Border color', selection_effect=None, font_color=(255,255,255))
            self.menu.add.button('Quit', pygame_menu.events.EXIT, button_id='Quit')
        else:
            self.menu.remove_widget(dead_cell_selector)
            self.menu.remove_widget(alive_cell_selector)
            self.menu.remove_widget(border_selector)
            self.menu.remove_widget(quit)
            self.menu.add.selector('Dead cell color', [('Black', (0,0,0)), ('White', (255,255,255)), ('Red', (255,0,0)), ('Green', (0,255,0)), ('Blue', (0,0,255)), ('Yellow', (255,255,0)), ('Purple', (255,0,255)), ('Cyan', (0,255,255))], onchange=self.set_dead_cell_color, selector_id='Dead cell color', selection_effect=None, font_color=(0,0,0))
            self.menu.add.selector('Alive cell color', [('White', (255, 255, 255)), ('Black', (0, 0, 0)), ('Red', (255,0,0)), ('Green', (0,255,0)), ('Blue', (0,0,255)), ('Yellow', (255,255,0)), ('Purple', (255,0,255)), ('Cyan', (0,255,255))], onchange=self.set_alive_cell_color, selector_id='Alive cell color', selection_effect=None, font_color=(255,255,255))
            self.menu.add.selector('Border color', [('White', (255, 255, 255)), ('Black', (0, 0, 0)), ('Red', (255,0,0)), ('Green', (0,255,0)), ('Blue', (0,0,255)), ('Yellow', (255,255,0)), ('Purple', (255,0,255)), ('Cyan', (0,255,255))], onchange=self.set_border_color, selector_id='Border color', selection_effect=None, font_color=(255,255,255))
            self.menu.add.button('Quit', pygame_menu.events.EXIT, button_id='Quit')

    def set_dead_cell_color(self, *selected_colors):
        self.colors['Dead_Cell'] = selected_colors[1]
        dead_cell_selector = self.menu.get_widget('Dead cell color')
        if self.randomize == False:
            dead_cell_selector._font_color = selected_colors[1]
        else:
            dead_cell_selector._font_color = (0,0,0)


    def set_alive_cell_color(self, *color):
        self.colors['Alive_Cell'] = color[1]
        alive_cell_selector = self.menu.get_widget('Alive cell color')
        if self.randomize == False:
            alive_cell_selector._font_color = color[1]
        else:
            alive_cell_selector._font_color = (255,255,255)

    def set_border_color(self, *color):
        self.colors['Border'] = color[1]
        border_selector = self.menu.get_widget('Border color')
        if self.randomize == False:
            border_selector._font_color = color[1]
        else:
            border_selector._font_color = (255,255,255)
        
    

    def start_the_game(self):
        grid = Grid(30, 20, 40, self.colors)
        grid.random_fill(self.percent)
        if self.randomize == True:
            grid.randomize_colors()
        self.menu.disable()
        self.menu.clear()
        
        while True:
                for event in pygame.event.get():
                    keys = pygame.key.get_pressed()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()                     
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            x, y = event.pos
                            x = x // 40
                            y = y // 40
                            grid.grid[y][x] = 1
                        if event.button == 3:
                            x, y = event.pos
                            x = x // 40
                            y = y // 40
                            grid.grid[y][x] = 0
                    if keys[pygame.K_SPACE]:
                        grid.update()
                
                screen.fill((0,0,0))
                grid.draw(screen)
                pygame.display.flip()
                clock.tick(self.clock_speed)
        
    def start_the_game_automatic(self):
        grid = Grid(30, 20, 40, self.colors)
        grid.random_fill(self.percent)
        if self.randomize == True:
            grid.randomize_colors()
        self.menu.disable()
        self.menu.clear()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            grid.update()
            screen.fill((0,0,0))
            grid.draw(screen)
            pygame.display.flip()
            clock.tick(self.clock_speed)
            grid.update()


    



pygame.init()
width = 1200
height = 800
screen = pygame.display.set_mode((width, height))
#Set the title of the window
pygame.display.set_caption('Game of Life')
clock = pygame.time.Clock()
menu = Menu()


