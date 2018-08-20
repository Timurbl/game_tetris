import pygame
import random
 
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
 
WIDTH = 10
HEIGHT = 20
CELL_WIDTH = 30
CELL_HEIGHT = 30
 
AUTODOWN = pygame.USEREVENT + 1
 
O = [[1,1],
     [1,1]]
 
L = [[1,0],  
     [1,0],  
     [1,1]]
 
J = [[0,1],  
     [0,1],  
     [1,1]]
 
I = [[1,1,1,1]]
 
S = [[0,1,1],
     [1,1,0]]
 
Z = [[1,1,0],
     [0,1,1]]
 
T = [[1,1,1],
     [0,1,0]]
 
FORMS = (O, L, J, T, I, S, Z)
 
class Field:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.field = [[True] + [None] * self.width + [True] for i in range(self.height)] + [[True] * (self.width + 2)]
   
    def draw(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j + 1]:
                    pygame.draw.rect(screen, self.field[i][j + 1],
                                     [j * CELL_WIDTH, i * CELL_HEIGHT,
                                      CELL_WIDTH, CELL_HEIGHT])
    def capture(self, figure):
        for i in range(len(figure.form)):
            for j in range(len(figure.form[i])):
                if figure.form[i][j]:
                    self.field[figure.y + i][figure.x + j] = figure.form[i][j]
   
    def is_game_over(self, figure):
        return not figure._check_position(self, figure.x, figure.y)    
                   
    def _check_line(self, i):
        #for cell in self.field[i]:
            #if not cell:
                #return False
        #return True
        return all(self.field[i])
                   
    def remove_lines(self):
        removed = 0
        for i in range(self.height):
            if self._check_line(i):
                removed += 1
                self.field.pop(i)
                self.field.insert(0, [True] + [None] * self.width + [True])
        return removed
       
 
class Figure:
    def __init__(self, x, y, form):
        self.x = x
        self.y = y
        color = (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
        self.form = [[color if cell else None for cell in line] for line in form]
   
    def draw(self, screen):
        for i in range(len(self.form)):
            for j in range(len(self.form[i])):
                if self.form[i][j]:
                    pygame.draw.rect(screen, self.form[i][j],
                                     [(self.x - 1) * CELL_WIDTH + j * CELL_WIDTH,
                                      self.y * CELL_HEIGHT + i * CELL_HEIGHT,
                                      CELL_WIDTH, CELL_HEIGHT])  
                   
    def _check_position(self, field, new_x, new_y):
        for i in range(len(self.form)):
            for j in range(len(self.form[i])):
                if self.form[i][j] and field.field[new_y + i][new_x + j]:
                    return False
        return True
                   
    def can_move_down(self, field):
        return self._check_position(field, self.x, self.y + 1)
       
    def can_move_left(self, field):
        return self._check_position(field, self.x - 1, self.y)
 
    def can_move_right(self, field):
        return self._check_position(field, self.x + 1, self.y)
   
    def can_rotate(self, field):
        new_form = list(zip(*reversed(self.form)))
        new_x = self.x
        new_y = self.y
        for i in range(len(new_form)):
            for j in range(len(new_form[i])):
                if new_form[i][j] and (new_y + i < 0 or new_y + i >= field.height or
                                       new_x + j < 0 or new_x + j > field.width or
                                       field.field[new_y + i][new_x + j]):
                    return False
        return True
   
    def move_down(self):
        self.y += 1
       
    def move_left(self):
        self.x -= 1    
   
    def move_right(self):
        self.x += 1
       
    def rotate(self):
       self.form = list(zip(*reversed(self.form)))
 
def main():
    pygame.init()
 
    size = [WIDTH * CELL_WIDTH, HEIGHT * CELL_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Tetris")
    done = False
    clock = pygame.time.Clock()
    pygame.time.set_timer(AUTODOWN, 250)
   
    score = 0
   
    field = Field(WIDTH, HEIGHT)
    figure = Figure(field.width // 2, 0, random.choice(FORMS))
 
 
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pygame.time.set_timer(AUTODOWN, 10)
                elif event.key == pygame.K_LEFT and figure.can_move_left(field):
                    figure.move_left()
                elif event.key == pygame.K_RIGHT and figure.can_move_right(field):
                    figure.move_right()  
                elif event.key == pygame.K_SPACE and figure.can_rotate(field):
                    figure.rotate()          
                #elif event.key == K_ENTER:
                    #pygame.time.set_timer(AUTODOWN, 0)
            elif event.type == AUTODOWN:
                if figure.can_move_down(field): figure.move_down()
                else:
                    pygame.time.set_timer(AUTODOWN, 250)
                    # 1. сделать фигуру частью поля
                    field.capture(figure)
                    # 2. проверить заполнение рядов
                    removed = field.remove_lines()
                    score += removed**2 * 100
                    # 3. создать новую фигуру
                    figure = Figure(field.width // 2, 0, random.choice(FORMS))    
                    done = field.is_game_over(figure)                
       
        screen.fill(BLACK)
        label = pygame.font.SysFont("comicsansms", 36).render(str(score), True, RED)
        field.draw(screen)
        figure.draw(screen)
        screen.blit(label, (20, 20))
        pygame.display.flip()
        clock.tick(20)
   
    pygame.quit()
 
if __name__ == "__main__":
    main()