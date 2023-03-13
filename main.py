import sys, pygame, random, copy
pygame.init()

CYAN = 0, 240, 240
BLUE = 0, 0, 240
ORANGE = 240, 161, 0
YELLOW = 240, 240, 0
GREEN = 0, 240, 0
PURPLE = 161, 0, 240
RED = 240, 0, 0
BLACK = 0, 0, 0

EMPTY, IN_PLACE, MOVING = 0, 1, 2
EMPTY_PIECE = [EMPTY, (0, 0, 0)]

PIECE_LEN = 20
PIECES = [
    [[[0, 5], [1, 5], [2, 5], [3, 5]], CYAN],
    [[[0, 5], [1, 5], [2, 5], [2, 4]], BLUE],
    [[[0, 4], [1, 4], [2, 4], [2, 5]], ORANGE],
    [[[0, 4], [1, 4], [0, 5], [1, 5]], YELLOW],
    [[[1, 4], [1, 5], [0, 5], [0, 6]], GREEN],
    [[[0, 4], [0, 5], [1, 5], [0, 6]], PURPLE],
    [[[0, 4], [0, 5], [1, 5], [1, 6]], RED],
]

class Game:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.grid = self.generate_empty_grid()
        self.piece = self.create_piece()
        self.finished = False
        self.score = 0

    def generate_empty_grid(self):
        return [[EMPTY_PIECE for j in range(self.width // PIECE_LEN)] for i in range(self.height // PIECE_LEN)]
    
    def reset(self):
        if not self.finished:
            return 
        
        self.grid = self.generate_empty_grid()
        self.piece = self.create_piece()
        self.finished = False
        self.score = 0
    
    def create_piece(self):
        piece_id = random.randint(0, len(PIECES) - 1)
        pieces, color = copy.deepcopy(PIECES[piece_id])
        for py, px in pieces:
            if self.grid[py][px][0] != EMPTY:
                self.finished = True
            self.grid[py][px] = [MOVING, color]
        return [pieces, color, piece_id]
    
    def draw(self, screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                state, color = self.grid[i][j]
                if state != EMPTY:
                    pygame.draw.rect(screen, color, (j * PIECE_LEN, i * PIECE_LEN, PIECE_LEN, PIECE_LEN))
    
    def update(self, pieces, color, dy, dx):
        for ind in range(len(pieces)):
            py, px = pieces[ind]
            self.grid[py][px] = copy.deepcopy(EMPTY_PIECE)
            pieces[ind][0] += dy
            pieces[ind][1] += dx
        self.piece[0] = pieces
        for py, px in pieces:
            self.grid[py][px] = [MOVING, color]

    def move(self):
        if self.finished or self.piece == None:
            return
        
        pieces, color = self.piece
        for py, px in pieces:
            if py == 19 or self.grid[py + 1][px][0] == IN_PLACE:
                for _py, _px in pieces:
                    self.grid[_py][_px][0] = IN_PLACE
                self.piece = self.create_piece()
                return
        
        self.update(pieces, color, 1, 0)
        self.remove_lines()
    
    def move_left(self):
        if self.finished or self.piece == None:
            return
    
        pieces, color = self.piece
        for py, px in pieces:
            if px == 0 or self.grid[py][px - 1][0] == IN_PLACE:
                return

        self.update(pieces, color, 0, -1)

    def move_right(self):
        if self.finished or self.piece == None:
            return
    
        pieces, color = self.piece
        for py, px in pieces:
            if px == 9 or self.grid[py][px + 1][0] == IN_PLACE:
                return

        self.update(pieces, color, 0, 1)
    
    def move_down(self):
        if self.finished or self.piece == None:
            return
    
        pieces, color = self.piece
        for py, px in pieces:
            if py == 19 or self.grid[py + 1][px][0] == IN_PLACE:
                return

        self.update(pieces, color, 1, 0)

    def empty_line(self, py):
        for px in range(len(self.grid[py])):
            self.grid[py][px] = copy.deepcopy(EMPTY_PIECE)

    def remove_lines(self):
        to_be_removed = []
        for py in range(len(self.grid)):
            all_in_place = True
            for px in range(len(self.grid[py])):
                all_in_place = all_in_place and self.grid[py][px][0] == IN_PLACE
            if all_in_place:
                to_be_removed.append(py)

        while to_be_removed:
            r = [to_be_removed.pop()]
            while to_be_removed and to_be_removed[-1] + 1 == r[-1]:
                r.append(to_be_removed.pop())
            
            self.score += (2 ** (len(r) - 1)) * 100
            for py in r:
                self.empty_line(py)
            
            for py in range(r[0], len(r) - 1, -1):
                self.grid[py], self.grid[py - len(r)] = self.grid[py - len(r)], self.grid[py]
        
    def rotate_counter_clockwise(self):
        # TODO: solve rotations
        if self.finished or self.piece == None:
            return
        
        pieces, color, piece_id = self.piece

    def rotate_clockwise(self):
        # TODO: solve rotations
        if self.finished or self.piece == None:
            return
    
width, height = 200, 400

game = Game(width, height)

screen = pygame.display.set_mode((width + 200, height))
clock = pygame.time.Clock()

font = pygame.font.SysFont('chalkduster.ttf', 30)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_left()
            if event.key == pygame.K_RIGHT:
                game.move_right()
            if event.key == pygame.K_DOWN:
                game.move_down()
            if event.key == pygame.K_r:
                game.reset()
            if event.key == pygame.K_a:
                game.rotate_counter_clockwise()
            if event.key == pygame.K_d:
                game.rotate_clockwise()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        game.move_left()
    if keys[pygame.K_RIGHT]:
        game.move_right()
    if keys[pygame.K_DOWN]:
        game.move_down()

    screen.fill(BLACK)

    game.draw(screen)
    game.move()
    
    pygame.draw.rect(screen, (194, 197, 204), (200, 0, 200, 400))

    score_img = font.render(f'Score: {game.score}', True, BLACK)
    score_img_width = score_img.get_width()
    screen.blit(score_img, (300 - score_img_width // 2, 10))

    pygame.display.flip()

    clock.tick(5)