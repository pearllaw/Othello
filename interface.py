import pygame 

class Gui:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (60, 179, 113)
        self.YELLOW = (255, 255, 153)
        # Measurements for board spaces and disk pieces
        self.WIDTH = 55
        self.HEIGHT = 55
        self.MARGIN = 5
        self.RADIUS = 20
        self.SCREEN_SIZE = (485, 485)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Othello Game")
    
    def show_screen(self, state):
        """Display the initial board."""
        node = lambda x, y: "%s" % (state.board.get((x, y)))
        coordinates = [[node(x, y) for x in range(8)] for y in range(8)]
        self.screen.fill(self.BLACK)
        self.draw_board(coordinates)
        # Update the screen
        pygame.display.flip()

    def draw_board(self, board):
        for row in range(8):
            for col in range(8):
                x_coord = (self.MARGIN + self.WIDTH) * row + self.MARGIN
                y_coord = (self.MARGIN + self.HEIGHT) * col + self.MARGIN
                pygame.draw.rect(self.screen, self.GREEN, [x_coord, y_coord, self.WIDTH, self.HEIGHT])
                player = board[row][col]
                if player != None:
                    self.draw_disk(player, row, col)

    def draw_disk(self, player, x, y):
        x_coord = (self.MARGIN + self.WIDTH) * x + self.MARGIN + 25
        y_coord = (self.MARGIN + self.HEIGHT) * y + self.MARGIN + 25
        if player == 'B':
            pygame.draw.circle(self.screen, self.BLACK, (x_coord, y_coord), self.RADIUS)
        elif player == 'W':
            pygame.draw.circle(self.screen, self.WHITE, (x_coord, y_coord), self.RADIUS)

    def get_mouse_event(self):
        """Detect user clicks."""
        done = False
        # Loop until user clicks close button
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Change x, y screen coordinates to grid coordinates
                    column = pos[0] // (self.WIDTH + self.MARGIN)
                    row = pos[1] // (self.HEIGHT + self.MARGIN)
                    return (row, column)
        pygame.quit()  

    def reset_square(self, pos):
        """Reset squares back to original color."""
        x = (self.MARGIN + self.WIDTH) * pos[0] + self.MARGIN
        y = (self.MARGIN + self.WIDTH) * pos[1] + self.MARGIN 
        pygame.draw.rect(self.screen, self.GREEN, [x, y, self.WIDTH, self.HEIGHT])
        pygame.display.flip()

    def update(self, board):
        """Update the screen."""
        for i in range(8):
            for j in range(8):
                self.reset_square((j, i)) 
                if board.get((i, j)) != None:
                    self.draw_disk(board.get((i, j)), j, i)         
        pygame.display.flip()
    
    def show_valid_moves(self, moves):
        """Display valid squares current player can move to in yellow.""" 
        for move in moves:
            x = (self.MARGIN + self.WIDTH) * move[1] + self.MARGIN
            y = (self.MARGIN + self.WIDTH) * move[0] + self.MARGIN
            pygame.draw.rect(self.screen, self.YELLOW, [x, y, self.WIDTH, self.HEIGHT])
        pygame.display.flip()
    
    def score(self, player):
        """Display the score and keep the screen open until user closes it."""
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True 
            self.screen.fill(self.BLACK)
            font = pygame.font.SysFont('Arial', 20)
            if player == 'B':
                display = font.render("You won!", True, self.WHITE)
            elif player == 'W':
                display = font.render("White won!", True, self.WHITE)
            else:
                display = font.render("Tie!", True, self.WHITE)
            self.screen.blit(display, 
                display.get_rect(
                    center=(self.screen.get_width()/2, self.screen.get_height()/2)))
            pygame.display.flip()
        pygame.quit()