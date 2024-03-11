import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random


class RandomBoardTicTacToe:
    def __init__(self, size = (600, 800)):

        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 153, 0)
        self.RED = (255, 0, 0)
        self.GREY = (181, 176, 176)
        self.NAVY = (0, 0, 102)
        self.BLUE = (113, 206, 246)

        # Grid Size
        self.GRID_SIZE = 4
        self.OFFSET = 5

        self.gridStartX = 0
        self.gridStartY = 0
        self.cellSize = 0
        self.cellTotal = 0
        self.grid_rect = None

        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = self.size[0]/self.GRID_SIZE - self.OFFSET
        self.HEIGHT = self.size[1]/self.GRID_SIZE - self.OFFSET

        # This sets the margin between each cell
        self.MARGIN = 5

        #Placeholder initialization for dropdown
        self.dropdown_expanded = False
        self.current_selection = "3x3"
        self.dropdown_options = ["3x3", "4x4", "5x5"]
        #The actual position and size will be calculatesd in draw_game
        self.dropdown_rect = pygame.Rect(0, 0, 0, 0)  #Placeholder values for now
        
        
        #Initalize variables for scores and winners
        self.human_score = 0
        self.computer_score = 0
        self.winner = None 


        #initialize values for select options 
        self.nought_selected = False
        self.cross_selected = False
        self.human_vs_human_selected = False
        self.human_vs_computer_selected = False


        self.minimax_selected = True  # No algorithm selected by default
        self.minimax_rect = None  # Will be defined in draw_game
        self.negamax_rect = None  # Will be defined in draw_game

        self.game_state = GameStatus( turn_O=self.nought_selected)

        self.start_game = False # This will be used to start the game once the user selects the options

        self.start_game_rect = None  # Will be defined in draw_game

        self.grid_rects = []

        self.mode = "player_vs_ai"  # Default mode is player vs AI

        
        
        
        # Initialize pygame
        pygame.init()

        self.screen = pygame.display.set_mode(self.size)

        # self.game_reset()

    def draw_game(self):
        # Create a 2 dimensional array using the column and row variables
        # pygame.init()
        # self.screen = pygame.display.set_mode(self.size)
        #window name
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.WHITE)
        """
        YOUR CODE HERE TO DRAW THE GRID OTHER CONTROLS AS PART OF THE GUI
        """
        self.grid_rects = []  # Reset the grid rectangles

        #DRAWING THE OUTER RECTANGLE AND CAPTION RECTANGLE:---------------
        outer_rect = pygame.Rect(self.MARGIN, self.MARGIN, self.size[0] - self.MARGIN*2, self.size[1]-self.MARGIN*2)
        pygame.draw.rect(self.screen, self.BLACK, outer_rect, 5)
        caption_rect = pygame.Rect(self.MARGIN, self.MARGIN, self.size[0] - self.MARGIN*2, self.HEIGHT/4)
        pygame.draw.rect(self.screen, self.BLACK, caption_rect, 5)



        #SETTING THE TEXT WITHIN THE CAPTION RECTANGLE-----------------
        #Set the center of textRect to be the same as the center of caption_rect. 
        #This centers the text within caption_rect.
        #Blitting the text surface onto the screen
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('TIC-TAC-TOE MEGA BOARD', True, self.BLACK, self.WHITE)
        textRect = text.get_rect()
        textRect.center = caption_rect.center
        self.screen.blit(text, textRect)



        #CONTENT/TEXT WITHIN THE INNER BOX--------
        #Align horizontally with the caption
        #Position just below the caption with a 10 pixel margin 
        #Blit text onto the screen at the specified position
        inner_font = pygame.font.Font('freesansbold.ttf', 24)
        inner_text = inner_font.render('Select human player symbol below: ', True, self.BLACK, self.WHITE)
        text_rect = inner_text.get_rect()
        text_rect.centerx = caption_rect.centerx
        text_rect.top = caption_rect.bottom + 10  
        self.screen.blit(inner_text, text_rect)



        #CONTENT/TEXT WITHIN THE INNENR BOX. These are the select options:----------------------
        #Draw the options text with appropriate font size
        #Draw the circle for the nought option
        option_height = 50  # Set the height for the option areas
        font = pygame.font.Font(None, 24)
        circle_padding = 10
        

        #THESE ARE THE NOUGHT AND CROSS BUTTONS------------------------
        #Draw the text onto the screen at the specified position for circle and cross
        text_nought = font.render('Nought (O)', True, self.BLACK)
        self.screen.blit(text_nought, (self.MARGIN * 8, 120))
        text_cross = font.render('Cross (X)', True, self.BLACK)
        self.screen.blit(text_cross, (self.MARGIN * 8, 150 ))


        nought_color_option = self.BLUE if self.nought_selected else self.NAVY
        circle_radius = option_height //6
        nought_circle_center_x = self.MARGIN *5
        nought_circle_center_y = 120 + option_height // 5.7
        self.nought_rect = pygame.Rect(
        nought_circle_center_x - circle_radius - circle_padding, 
        nought_circle_center_y - circle_radius - circle_padding, 
        2 * (circle_radius + circle_padding), 
        2 * (circle_radius + circle_padding))
        #self.nought_rect = pygame.Rect(self.MARGIN, 120, self.size[0] - self.MARGIN*2, option_height)
        self.screen.blit(text_nought, (self.MARGIN * 8, 120))
        circle_center = (self.MARGIN * 5, 120 + option_height // 5.7) # Calculate the center position for the circle
        pygame.draw.circle(self.screen, nought_color_option, circle_center, option_height // 6, 0)         #Draw the circle for the nought option
        
        
        cross_color_option = self.BLUE if self.cross_selected else self.NAVY
        cross_circle_center = (self.MARGIN * 5, 150 + option_height // 5.7) #Calculate the center position for the circle
        #self.cross_rect = pygame.Rect(self.MARGIN, 180 + option_height, self.size[0] - self.MARGIN*2, option_height)
        self.cross_rect = pygame.Rect(
        cross_circle_center[0] - option_height // 6 - circle_padding,
        cross_circle_center[1] - option_height // 6 - circle_padding,
        2 * (option_height // 6 + circle_padding),
        2 * (option_height // 6 + circle_padding))
        pygame.draw.circle(self.screen, cross_color_option, cross_circle_center, option_height // 6, 0)

        
        
        
        
        #THESE ARE THE HUMAN VS HUMAN AND HUMAN VS COMPUTER OPTIONs AND BUTTONS------------------------
        #Define the x-coordinate for the start of the "Human vs" options, 
        #which will be to the right of the "Nought (O)" and "Cross (X)" options.
        second_col_x = self.MARGIN * 20 + max(text_nought.get_width(), text_cross.get_width()) + self.MARGIN


        #Render the "Human vs" options text
        #Calculate the y-coordinate for the "Human vs" options
        #Define rectangles for clickable areas with the correct height for "Human vs" options
        text_human_human = font.render('Human vs Human', True, self.BLACK)
        text_human_computer = font.render('Human vs Computer', True, self.BLACK)
        self.screen.blit(text_human_human, (second_col_x, 120)) # Draw the "Human vs" human text onto the screen
        self.screen.blit(text_human_computer, (second_col_x, 150))# Draw the "Human vs" computer onto the screen


        #Draw the "Human vs Human" option circle and clickable rectangle
        #self.human_human_rect = pygame.Rect(second_col_x, 120, self.size[0] - second_col_x - self.MARGIN, option_height)
        human_human_circle_center = (self.MARGIN * 35, 120 + option_height // 5.7)  # Centered inss the option area
        self.human_human_rect = pygame.Rect(
        human_human_circle_center[0] - option_height // 6 - circle_padding,
        human_human_circle_center[1] - option_height // 6 - circle_padding,
        2 * (option_height // 6 + circle_padding),
        2 * (option_height // 6 + circle_padding))
        self.human_human_color = self.BLUE if self.human_vs_human_selected else self.NAVY
        pygame.draw.circle(self.screen, self.human_human_color, human_human_circle_center, option_height // 6, 0)
        

        #Draw the "Human vs Computer" option circle and clickable retangle
        #self.human_computer_rect = pygame.Rect(second_col_x, 150, self.size[0] - second_col_x - self.MARGIN, option_height)
        human_computer_circle_center = (self.MARGIN * 35, 150 + option_height // 5.7)  # Centered in the option area
        self.human_computer_rect = pygame.Rect(
        human_computer_circle_center[0] - option_height // 6 - circle_padding,
        human_computer_circle_center[1] - option_height // 6 - circle_padding,
        2 * (option_height // 6 + circle_padding),
        2 * (option_height // 6 + circle_padding))
        self.human_computer_color = self.BLUE if self.human_vs_computer_selected else self.NAVY
        pygame.draw.circle(self.screen, self.human_computer_color, human_computer_circle_center, option_height // 6, 0)
        



        #BOARD SIZE DROP DOWN BUTTON UI---------------------------------------
        # Draw the dropdown box
        font = pygame.font.Font(None, 24)

        #Determine the position for the "Board Size" label and dropdown
        label_text = font.render('Board Size:', True, self.BLACK)
        label_x = second_col_x + 200  # The x-coordinate where the "Human vs Human" text starts
        label_y = 120  # The y-coordinate to align with the "Nought (O)" option

        # Calculate the x position for the dropdown box based on the label
        dropdown_x = label_x + label_text.get_width() + self.MARGIN  # Add some space after the label
        dropdown_y = label_y
        dropdown_width = 100  # or however wide you want the dropdown to be
        dropdown_height = option_height  # the height of your option buttons for consistency

        # Update the dropdown_rect with the actual position and size
        self.dropdown_rect.update(dropdown_x, dropdown_y, dropdown_width, dropdown_height)

        # Draw the "Board Size" label
        self.screen.blit(label_text, (label_x, label_y))

        # Draw the dropdown box
        pygame.draw.rect(self.screen, self.GREY, self.dropdown_rect)
        # ... (rest of the dropdown drawing code)


       # Draw the dropdown arrow
        arrow_size = 10  # The size of the triangle
        arrow_center_x = self.dropdown_rect.right - arrow_size  # Position the arrow inside the dropdown rectangle
        arrow_center_y = self.dropdown_rect.centery
        # Draw an upside-down triangle (arrow) indicating a dropdown
        pygame.draw.polygon(self.screen, self.BLUE, [
            (arrow_center_x - arrow_size, arrow_center_y - arrow_size // 2),
            (arrow_center_x, arrow_center_y + arrow_size // 2),
            (arrow_center_x + arrow_size, arrow_center_y - arrow_size // 2)
        ])

        # Render the current selection in red text within the dropdown box
        current_selection_text_surface = font.render(self.current_selection, True, self.RED)
        current_selection_text_rect = current_selection_text_surface.get_rect(center=self.dropdown_rect.center)
        self.screen.blit(current_selection_text_surface, current_selection_text_rect.topleft)

        #If the dropdown is expanded, draw the options
        if self.dropdown_expanded:
            for i, option in enumerate(self.dropdown_options):
                #Calculate the position for each option
                option_rect = self.dropdown_rect.copy()
                option_rect.y += (i + 1) * self.dropdown_rect.height  # Stacking options below the current selection
                #Draw the rectangle for the option
                pygame.draw.rect(self.screen, self.GREY, option_rect)
                #Render the text for the option in red
                option_text_surface = font.render(option, True, self.RED)
                #Blit the text for the option
                option_text_rect = option_text_surface.get_rect(center=option_rect.center)
                self.screen.blit(option_text_surface, option_text_rect.topleft)

        
        
        
        #DRAWING OF THE MINIMAX OR NEGAMAX OPTION TEXT-------------------------
        font = pygame.font.Font(None, 22)
        if self.human_vs_computer_selected:
            minimax_negamax_x = label_x  # Align the left edge with the BOARD SIZE text
            minimax_negamax_y = label_y + 25  # Some space below the "BOARD SIZE" TEXT

            #Define colors based on selection
            minimax_color = self.BLUE if self.minimax_selected else self.NAVY
            negamax_color = self.NAVY if self.minimax_selected else self.BLUE  # If minimax is not selected, negamax is assumed

            #Draw the "Minimax?" and "Negamax?" option text
            text_minimax = font.render('Minimax?', True, self.BLACK)
            text_negamax = font.render('Negamax?', True, self.BLACK)

            #Calculate positions for text and circles
            minimax_text_position = (minimax_negamax_x, minimax_negamax_y)
            negamax_text_position = (minimax_negamax_x, minimax_negamax_y + option_height - 25)  # Add some vertical space

            #Update rectangles for clickable areas
            self.minimax_rect = pygame.Rect(minimax_text_position[0], minimax_text_position[1], 100, option_height)
            self.negamax_rect = pygame.Rect(negamax_text_position[0], negamax_text_position[1], 100, option_height)

            #Draw text onto the screen
            self.screen.blit(text_minimax, minimax_text_position)
            self.screen.blit(text_negamax, negamax_text_position)

            #Draw the selection circles for "Minimax" and "Negamax"
            pygame.draw.circle(self.screen, minimax_color, (minimax_text_position[0] + text_minimax.get_width() + 10, minimax_text_position[1] + text_minimax.get_height() // 2), option_height // 6, 0)
            pygame.draw.circle(self.screen, negamax_color, (negamax_text_position[0] + text_negamax.get_width() + 10, negamax_text_position[1] + text_negamax.get_height() // 2), option_height // 6, 0)


        

        


        #START BUTTON -------------------------------------
        # Assuming you've already calculated 'board_top', the top y-coordinate of the board
        # Button dimensions and position
        button_width = 200
        button_height = 20
        board_top = self.size[1]
        button_offset = 10  # Distance above the board
        button_x = (self.size[0] - button_width) // 2  # Centered horizontally
        button_y = board_top/3 - button_offset - button_height

        # Draw the button rectangle
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        if not self.start_game:
            pygame.draw.rect(self.screen, self.GREEN, button_rect)
            self.start_game_rect = button_rect  # Save the rectangle for later use

            # Create the button label
            button_text = font.render('Start Game', True, self.BLACK, self.GREEN)

            # Get the rectangle of the button label and center it
            text_rect = button_text.get_rect()
            text_rect.center = button_rect.center

            # Blit the button label onto the screen
            self.screen.blit(button_text, text_rect)
        # Draw the button rectangle with restart text
        elif self.start_game:
            pygame.draw.rect(self.screen, self.RED, button_rect)
            self.start_game_rect = button_rect
            button_text = font.render('Restart Game', True, self.BLACK, self.RED)
            text_rect = button_text.get_rect()
            text_rect.center = button_rect.center
            self.screen.blit(button_text, text_rect)



        #DISPLAY WINNER, AND SCORES ----------------------------
        display_y = button_y - 60  # Adjust this based on your layout
        score_font = pygame.font.Font(None, 24)  # Font for the scores
        
        # Render the winner, human score, and computer score
        #if self.winner:
        winner_text = score_font.render(f"Winner: {self.winner}", True, self.BLACK)
        self.screen.blit(winner_text, (self.MARGIN + 400, display_y + 20))
        
        human_score_text = score_font.render(f"Human Score: {self.human_score}", True, self.BLACK)
        computer_score_text = score_font.render(f"Computer Score: {self.computer_score}", True, self.BLACK)
        # Calculate positions based on your layout. Here's an example:
        self.screen.blit(human_score_text, (self.MARGIN + 5, display_y + 20))  # Adjust spacing as needed
        self.screen.blit(computer_score_text, (self.MARGIN + 200, display_y + 20))  # Adjust spacing and positioning


        #CODE FOR GRID ----------------------------------------------
        grid_top_left_x = self.MARGIN
        self.gridStartX = grid_top_left_x
        grid_top_left_y = button_rect.bottom + self.MARGIN  # Start just below the 'Start Game' button
        self.gridStartY = grid_top_left_y

        #CALCULATE THE AVAILABLE SPACE
        available_width = self.size[0] - (2 * self.MARGIN)
        available_height = self.size[1] - grid_top_left_y - self.MARGIN  # Space below the 'Start Game' button
        # Calculate the size of each grid cell based on the selected board size
        GRID_SIZE = int(self.current_selection[0])  # Assuming the selection is like "3x3", "4x4", etc.
        self.cellTotal = GRID_SIZE
        cell_size = min((available_width // GRID_SIZE), (available_height // GRID_SIZE))
        self.cellSize = cell_size
        self.grid_rect = pygame.Rect(grid_top_left_x, grid_top_left_y, cell_size * GRID_SIZE, cell_size * GRID_SIZE)

        # Calculate the total grid width and height based on cell size
        total_grid_width = cell_size * GRID_SIZE
        total_grid_height = cell_size * GRID_SIZE

        # Calculate the starting x and y positions to center the grid
        grid_start_x = (self.size[0] - total_grid_width) // 2
        grid_start_y = button_rect.bottom + (self.size[1] - button_rect.bottom - total_grid_height) // 2

        # Draw the grid
        for row in range(int(self.current_selection[0])):
            # print("ROW: ", row)
            self.grid_rects.append([])  # Create a new row
            for col in range(int(self.current_selection[0])):
                # print("COL: ", col)
                cell_rect = pygame.Rect(
                    grid_start_x + (col * cell_size),
                    grid_start_y + (row * cell_size),
                    cell_size,
                    cell_size
                )
                # print("board_state: ", self.game_state.board_state)
                # print("row: ", row)
                # print("col: ", col)
                if self.game_state.board_state[row][col] == 1:
                    pygame.draw.circle(self.screen, self.CIRCLE_COLOR, cell_rect.center, cell_size // 3, 10)
                    # self.draw_circle(cell_rect.centerx, cell_rect.centery)
                elif self.game_state.board_state[row][col] == -1:
                    pygame.draw.line(self.screen, self.CROSS_COLOR, cell_rect.topleft, cell_rect.bottomright, 10)
                    pygame.draw.line(self.screen, self.CROSS_COLOR, cell_rect.bottomleft, cell_rect.topright, 10)
                self.grid_rects[row].append(cell_rect)  # Save the rectangle for later use
                pygame.draw.rect(self.screen, self.BLACK, cell_rect, 1)  # 1 for the line thickness

    
        # pygame.display.update()

    def draw_circle(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CIRCLE FOR THE NOUGHTS PLAYER AT THE CELL THAT IS SELECTED VIA THE gui
        """
        #Calculate the center of the cell
        center_x = (x * (self.WIDTH + self.MARGIN)) + (self.WIDTH // 2) + self.MARGIN
        center_y = (y * (self.HEIGHT + self.MARGIN)) + (self.HEIGHT // 2) + self.MARGIN

        #Draw the circle
        pygame.draw.circle(self.screen, self.CIRCLE_COLOR, (center_x, center_y), self.WIDTH // 4, 0)
        

    def draw_cross(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CROSS FOR THE CROSS PLAYER AT THE CELL THAT IS SELECTED VIA THE gui
        """
        #Calculate the top left and bottom right points of the cell
        top_left_x = x * (self.WIDTH + self.MARGIN) + self.MARGIN
        top_left_y = y * (self.HEIGHT + self.MARGIN) + self.MARGIN
        bottom_right_x = top_left_x + self.WIDTH
        bottom_right_y = top_left_y + self.HEIGHT

        #Calculate the top right and bottom left points of the cell for the cross
        top_right_x = bottom_right_x
        top_right_y = top_left_y
        bottom_left_x = top_left_x
        bottom_left_y = bottom_right_y

        #Set the line thickness
        line_thickness = 2

        #Draw the two lines of the cross
        pygame.draw.line(self.screen, self.CROSS_COLOR, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), line_thickness)
        pygame.draw.line(self.screen, self.CROSS_COLOR, (top_right_x, top_right_y), (bottom_left_x, bottom_left_y), line_thickness)

    def play_game(self, mode="player_vs_ai"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click was inside the dropdown rectangle
                if self.dropdown_rect.collidepoint(event.pos):
                    self.dropdown_expanded = not self.dropdown_expanded
                # Check if the mouse click was inside the dropdown options
                if self.dropdown_expanded:
                    for i, option in enumerate(self.dropdown_options):
                        option_rect = self.dropdown_rect.copy()
                        option_rect.y += (i + 1) * self.dropdown_rect.height
                        if option_rect.collidepoint(event.pos):
                            self.current_selection = option
                            self.dropdown_expanded = False
                            # Update the game state based on the selected board size
                            if int(option[0]) == 3:
                                self.game_state = GameStatus(turn_O=self.nought_selected)
                            elif int(option[0]) == 4:
                                self.game_state = GameStatus([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], self.nought_selected)
                            elif int(option[0]) == 5:
                                self.game_state = GameStatus([[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]], self.nought_selected)
                            # self.game_state = GameStatus(,self.nought_selected)
                            self.start_game = False
                            self.winner = None
                            self.human_score = 0
                            self.computer_score = 0
                            self.minimax_selected = True
                            self.negamax_selected = None
                            self.grid_rects = []
                            self.mode = mode
                if self.nought_rect.collidepoint(event.pos):
                    self.nought_selected = True
                    self.cross_selected = False
                    self.game_state.turn_O = self.nought_selected
                if self.cross_rect.collidepoint(event.pos):
                    self.nought_selected = False
                    self.cross_selected = True
                    self.game_state.turn_O = self.nought_selected
                if self.human_human_rect.collidepoint(event.pos):
                    self.human_vs_human_selected = True
                    self.human_vs_computer_selected = False
                    self.mode = "player_vs_player"
                if self.human_computer_rect.collidepoint(event.pos):
                    self.human_vs_computer_selected = True
                    self.human_vs_human_selected = False
                    self.mode = "player_vs_ai"
                if self.minimax_rect and self.minimax_rect.collidepoint(event.pos):
                    self.minimax_selected = True
                    self.negamax_selected = False
                if self.negamax_rect and self.negamax_rect.collidepoint(event.pos):
                    self.minimax_selected = False
                    self.negamax_selected = True
                if self.start_game_rect.collidepoint(event.pos):
                    if self.start_game:
                        self.current_selection = "3x3"
                        self.game_state = GameStatus(turn_O=self.nought_selected)
                        self.start_game = False
                        self.winner = None
                        self.human_score = 0
                        self.computer_score = 0
                        self.minimax_selected = True
                        self.negamax_selected = None
                        self.grid_rects = []
                    else:
                        self.start_game = True
                        # self.game_state = GameStatus(turn_O=self.nought_selected)
                        self.winner = None
                        self.human_score = 0
                        self.computer_score = 0
                        # self.minimax_selected = None
                        # self.negamax_selected = None
                        self.grid_rects = [] 
                if self.grid_rect and self.grid_rect.collidepoint(event.pos):
                    if self.start_game:
                        print("cell total: ", self.cellTotal)
                        # print("game board", self.game_state.board_state)
                        for row in range(self.cellTotal):
                            for col in range(self.cellTotal):
                                if self.grid_rects[row][col].collidepoint(event.pos) and self.game_state.is_terminal()[0] == False:
                                    if self.game_state.board_state[row][col] == 0:
                                        # print("grid rectangle: ", self.grid_rects)
                                        if self.game_state.turn_O:
                                            self.game_state.board_state[row][col] = 1
                                            self.game_state.turn_O = False
                                            if self.mode == "player_vs_ai":
                                                if self.minimax_selected:
                                                    val, move = minimax(self.game_state, 3, False)
                                                    print("move: ", move)
                                                    print("val: ", val)
                                                    if move:
                                                        self.game_state.board_state[move[0]][move[1]] = -1
                                                        self.game_state.turn_O = True
                                                    else:
                                                        for i in range(self.cellTotal):
                                                            for j in range(self.cellTotal):
                                                                if self.game_state.board_state[i][j] == 0:
                                                                    self.game_state.board_state[i][j] = -1
                                                                    self.game_state.turn_O = True
                                                                    break
                                                        # self.game_state.board_state[row][col] = -1
                                                        self.game_state.turn_O = True
                                                    # self.game_state.board_state[move[0]][move[1]] = -1
                                                    self.game_state.turn_O = True
                                            # print("game board", self.game_state.board_state)
                                        else:
                                            # print("game board", self.game_state.board_state)
                                            self.game_state.board_state[row][col] = -1
                                            self.game_state.turn_O = True
                                            # print("game board", self.game_state.board_state)
                                        
                                        self.human_score, self.computer_score = self.game_state.get_scores()
                                        if self.game_state.is_terminal()[0]:
                                            self.winner = self.game_state.is_terminal()[1]
                                        print("scores: ", self.human_score, self.computer_score)
                              


tictactoegame = RandomBoardTicTacToe()

clock = pygame.time.Clock()
while True:

    # Process inputs
    tictactoegame.play_game()

    # Draw the game
    tictactoegame.draw_game()

    pygame.display.update()
    clock.tick(60)