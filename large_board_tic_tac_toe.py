"""
PLEASE READ THE COMMENTS BELOW AND THE HOMEWORK DESCRIPTION VERY CAREFULLY BEFORE YOU START CODING

 The file where you will need to create the GUI which should include (i) drawing the grid, (ii) call your Minimax/Negamax functions
 at each step of the game, (iii) allowing the controls on the GUI to be managed (e.g., setting board size, using 
                                                                                 Minimax or Negamax, and other options)
 In the example below, grid creation is supported using pygame which you can use. You are free to use any other 
 library to create better looking GUI with more control. In the __init__ function, GRID_SIZE (Line number 36) is the variable that
 sets the size of the grid. Once you have the Minimax code written in multiAgents.py file, it is recommended to test
 your algorithm (with alpha-beta pruning) on a 3x3 GRID_SIZE to see if the computer always tries for a draw and does 
 not let you win the game. Here is a video tutorial for using pygame to create grids http://youtu.be/mdTeqiWyFnc
 
 
 PLEASE CAREFULLY SEE THE PORTIONS OF THE CODE/FUNCTIONS WHERE IT INDICATES "YOUR CODE BELOW" TO COMPLETE THE SECTIONS
 
"""
import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random

mode = "player_vs_ai" # default mode for playing the game (player vs AI)

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
        self. OFFSET = 5

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

        #Initialize the dropdown rectangle with x, y, width, and height
        # Initialize pygame
        pygame.init()
        self.game_reset()

    def draw_game(self):
        # Create a 2 dimensional array using the column and row variables
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        #window name
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.WHITE)
        """
        YOUR CODE HERE TO DRAW THE GRID OTHER CONTROLS AS PART OF THE GUI
        """


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



        #CONTENT/TEXT WITHIN THE INNENR BOX--------
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
        font = pygame.font.Font(None, 24)
        text_nought = font.render('Nought (O)', True, self.BLACK)
        #Define rectangles for clickable areas with the correct height for circle
        option_height = 50  # Set the height for the option areas
        nought_rect = pygame.Rect(self.MARGIN, 120, self.size[0] - self.MARGIN*2, option_height)
        #Draw the text onto the screen at the specified position for circle
        self.screen.blit(text_nought, (self.MARGIN * 8, 120))
        circle_center = (self.MARGIN * 5, 120 + option_height // 5.7) # Calculate the center position for the circle
        #Draw the circle for the nought option
        pygame.draw.circle(self.screen, self.NAVY, circle_center, option_height // 6, 0)
        # Define rectangles for clickable are as with the correct height for cross
        # Draw the circle for the cross option
        text_cross = font.render('Cross (X)', True, self.BLACK)
        cross_rect = pygame.Rect(self.MARGIN, 180 + option_height, self.size[0] - self.MARGIN*2, option_height)
        self.screen.blit(text_cross, (self.MARGIN * 8, 150 ))
        circle_center = (self.MARGIN * 5, 150 + option_height // 5.7) #Calculate the center position for the circle
        pygame.draw.circle(self.screen, self.NAVY, circle_center, option_height // 6, 0)

        #THIS IS THE HUMAN VS HUMAN AND HUMAN VS COMPUTER OPTION------------------------
        #Define the x-coordinate for the start of the "Human vs" options, 
        #which will be to the right of the "Nought (O)" and "Cross (X)" options.
        second_col_x = self.MARGIN * 20 + max(text_nought.get_width(), text_cross.get_width()) + self.MARGIN

        #Render the "Human vs" options text
        text_human_human = font.render('Human vs Human', True, self.BLACK)
        text_human_computer = font.render('Human vs Computer', True, self.BLACK)

        #Calculate the y-coordinate for the "Human vs" options
        #Define rectangles for clickable areas with the correct height for "Human vs" options
        human_human_rect = pygame.Rect(second_col_x, 120, self.size[0] - second_col_x - self.MARGIN, option_height)
        human_computer_rect = pygame.Rect(second_col_x, 150, self.size[0] - second_col_x - self.MARGIN, option_height)
        # Draw the "Human vs" human text onto the screens at the specified position
        # Draw the "Human vs Human" option text and circle
        self.screen.blit(text_human_human, (second_col_x, 120))
        human_human_circle_center = (self.MARGIN * 35, 120 + option_height // 5.7)  # Centered inss the option area
        pygame.draw.circle(self.screen, self.NAVY, human_human_circle_center, option_height // 6, 0)
        # Draw the "Human vs Computer" option text and circle
        self.screen.blit(text_human_computer, (second_col_x, 150))
        human_computer_circle_center = (self.MARGIN * 35, 150 + option_height // 5.7)  # Centered in the option area
        pygame.draw.circle(self.screen, self.NAVY, human_computer_circle_center, option_height // 6, 0)
        



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
        pygame.draw.rect(self.screen, self.GREEN, button_rect)

        # Create the button label
        button_text = font.render('Start Game', True, self.BLACK, self.GREEN)

        # Get the rectangle of the button label and center it
        text_rect = button_text.get_rect()
        text_rect.center = button_rect.center

        # Blit the button label onto the screen
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
        grid_top_left_y = button_rect.bottom + self.MARGIN  # Start just below the 'Start Game' button

        #CALCULATE THE AVAILABLE SPACE
        available_width = self.size[0] - (2 * self.MARGIN)
        available_height = self.size[1] - grid_top_left_y - self.MARGIN  # Space below the 'Start Game' button
        # Calculate the size of each grid cell based on the selected board size
        GRID_SIZE = int(self.current_selection[0])  # Assuming the selection is like "3x3", "4x4", etc.
        cell_size = min((available_width // GRID_SIZE), (available_height // GRID_SIZE))

        # Calculate the total grid width and height based on cell size
        total_grid_width = cell_size * GRID_SIZE
        total_grid_height = cell_size * GRID_SIZE

        # Calculate the starting x and y positions to center the grid
        grid_start_x = (self.size[0] - total_grid_width) // 2
        grid_start_y = button_rect.bottom + (self.size[1] - button_rect.bottom - total_grid_height) // 2

        # Draw the grid
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell_rect = pygame.Rect(
                    grid_start_x + (col * cell_size),
                    grid_start_y + (row * cell_size),
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(self.screen, self.BLACK, cell_rect, 1)  # 1 for the line thickness

    
        pygame.display.update()


    def change_turn(self):

        if(self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")


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

    def is_game_over(self):

        """
        YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
        FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)
        
        YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME
        """
        #Check if the game is in a terminal state using the is_terminal method
        game_over, winner = self.game_state.is_terminal()

        #Update the winner attribute if there is one
        if game_over:
            self.winner = winner  #winner would be either 'Human', 'AI', or 'Draw'

        return game_over


    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)


    def play_ai(self):
        """
        YOUR CODE HERE TO CALL MINIMAX OR NEGAMAX DEPENDEING ON WHICH ALGORITHM SELECTED FROM THE GUI
        ONCE THE ALGORITHM RETURNS THE BEST MOVE TO BE SELECTED, YOU SHOULD DRAW THE NOUGHT (OR CIRCLE DEPENDING
        ON WHICH SYMBOL YOU SELECTED FOR THE AI PLAYER)
        
        THE RETURN VALUES FROM YOUR MINIMAX/NEGAMAX ALGORITHM SHOULD BE THE SCORE, MOVE WHERE SCORE IS AN INTEGER
        NUMBER AND MOVE IS AN X,Y LOCATION RETURNED BY THE AGENT
        """
        
        self.change_turn()
        pygame.display.update()
        terminal = self.game_state.is_terminal()
        """ USE self.game_state.get_scores(terminal) HERE TO COMPUTE AND DISPLAY THE FINAL SCORES """



    def game_reset(self):
        self.draw_game()
        """
        YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
        BOARD STATE
        """
        #Reset the board to a 2D list of zeros
        initial_board_state = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        
        #Create a new GameStatus object with the reset board
        self.game_state = GameStatus(initial_board_state)
        
        #Reset winner to None as the game is starting over
        self.winner = None
        
        #Reset scores if you're keeping track of them across games
        self.human_score = 0
        self.computer_score = 0
        
        #Redraw the game board to reflect the reset
        self.draw_game()
        pygame.display.update()

        

    def play_game(self, mode = "player_vs_ai"):
        done = False
        clock = pygame.time.Clock()
        self.draw_game()


        while not done:
            for event in pygame.event.get():  # User did something

                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    #Check if the dropdown was clicked
                    if self.dropdown_rect.collidepoint(mouse_pos):
                        self.dropdown_expanded = not self.dropdown_expanded
                        self.draw_game()
                    #Check if one of the dropdown options was clicked
                    elif self.dropdown_expanded:
                        for i, option in enumerate(self.dropdown_options):
                            option_rect = self.dropdown_rect.copy()
                            option_rect.y += (i + 1) * self.dropdown_rect.height
                            if option_rect.collidepoint(mouse_pos):
                                #Update the current selection with the clicked option
                                self.current_selection = option
                                #Collapse the dropdown as the selection has been made
                                self.dropdown_expanded = False
                                #Re-draw the game to reflect the changed selection
                                self.draw_game()
                                break


                """
                YOUR CODE HERE TO CHECK IF THE USER CLICKED ON A GRID ITEM. EXIT THE GAME IF THE USER CLICKED EXIT
                """
                
                """
                YOUR CODE HERE TO HANDLE THE SITUATION IF THE GAME IS OVER. IF THE GAME IS OVER THEN DISPLAY THE SCORE,
                THE WINNER, AND POSSIBLY WAIT FOR THE USER TO CLEAR THE BOARD AND START THE GAME AGAIN (OR CLICK EXIT)
                """
                    
                """
                YOUR CODE HERE TO NOW CHECK WHAT TO DO IF THE GAME IS NOT OVER AND THE USER SELECTED A NON EMPTY CELL
                IF CLICKED A NON EMPTY CELL, THEN GET THE X,Y POSITION, SET ITS VALUE TO 1 (SELECTED BY HUMAN PLAYER),
                DRAW CROSS (OR NOUGHT DEPENDING ON WHICH SYMBOL YOU CHOSE FOR YOURSELF FROM THE gui) AND CALL YOUR 
                PLAY_AI FUNCTION TO LET THE AGENT PLAY AGAINST YOU
                """
                
                # if event.type == pygame.MOUSEBUTTONUP:
                    # Get the position
                    
                    # Change the x/y screen coordinates to grid coordinates
                    
                    # Check if the game is human vs human or human vs AI player from the GUI. 
                    # If it is human vs human then your opponent should have the value of the selected cell set to -1
                    # Then draw the symbol for your opponent in the selected cell
                    # Within this code portion, continue checking if the game has ended by using is_terminal function
                
                    
            # Update the screen with what was drawn.
            pygame.display.update()
            clock.tick(60)

        pygame.quit()

tictactoegame = RandomBoardTicTacToe()
tictactoegame.play_game()

"""
YOUR CODE HERE TO SELECT THE OPTIONS VIA THE GUI CALLED FROM THE ABOVE LINE
AFTER THE ABOVE LINE, THE USER SHOULD SELECT THE OPTIONS AND START THE GAME. 
YOUR FUNCTION PLAY_GAME SHOULD THEN BE CALLED WITH THE RIGHT OPTIONS AS SOON
AS THE USER STARTS THE GAME
"""
