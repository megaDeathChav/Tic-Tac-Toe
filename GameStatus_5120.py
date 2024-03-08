# -*- coding: utf-8 -*-


class GameStatus:


	def __init__(self, board_state=None, turn_O=True):

		self.board_state = board_state
		if board_state == None:
			board_state = [[0,0,0], [0,0,0], [0,0,0]]
		self.board_state = board_state
		self.turn_O = turn_O
		self.oldScores = 0

		self.winner = ""


	def is_terminal(self):
		"""
        YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
        THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
        """

		if len(self.board_state) == 3:
			scores = self.get_scores()
			if scores > 0:
				return True, 'Human'
			elif scores < 0:
				return True, 'AI'

		# Check if there are any empty cells left
		if 0 not in [item for sublist in self.board_state for item in sublist]:
			# If there are no empty cells, the game is over
			# Calculate scores for each player
			scores = self.get_scores(True)
			# Determine the winner based on the scores
			if scores > 0:
				return True, 'Human'
			elif scores < 0:
				return True, 'AI'
			else:
				return True, 'Draw'
		else:
			# If there are still empty cells, the game is not over
			return False, None

	def get_scores(self, terminal=False):
		"""
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        """        
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point_player = 3
		check_point_AI = -3


	    # Check rows
		for row in self.board_state:
			for i in range(len(row) - 2):
				total = sum(row[i:i+3])
				if total == check_point_player:
					scores += 1
				elif total == check_point_AI:
					scores -= 1

		# Check columns
		for col in range(cols):
			for i in range(rows - 2):
				total = sum(self.board_state[j][col] for j in range(i, i+3))
				if total == check_point_player:
					scores += 1
				elif total == check_point_AI:
					scores -= 1
					
		# Check main diagonals
		for i in range(rows - 2):
			for j in range(cols - 2):
				total = sum(self.board_state[i + k][j + k] for k in range(3))
				if total == check_point_player:
					scores += 1
				elif total == check_point_AI:
					scores -= 1

		# Check anti-diagonals
		for i in range(rows - 2):
			for j in range(2, cols):
				total = sum(self.board_state[i + k][j - k] for k in range(3))
				if total == check_point_player:
					scores += 1
				elif total == check_point_AI:
					scores -= 1

		return scores	


	def get_negamax_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point = 3 if terminal else 2
	    
	    # Check rows
		for row in self.board_state:
			if sum(row) == check_point:
				scores += 100 if terminal else 1

		# Check columns
		for col in range(cols):
			if sum(self.board_state[row][col] for row in range(rows)) == check_point:
				scores += 100 if terminal else 1

		# Check diagonals
		if sum(self.board_state[i][i] for i in range(rows)) == check_point:
			scores += 100 if terminal else 1
		if sum(self.board_state[i][rows - i - 1] for i in range(rows)) == check_point:
			scores += 100 if terminal else 1

		return scores

	def get_moves(self):
		moves = []
		"""
        YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
        MINIMAX OR NEGAMAX FUNCTIONS
        """
		for i in range(len(self.board_state)):
			for j in range(len(self.board_state[i])):
				# If the cell is empty (has the value 0), add it to the list of possible moves
				if self.board_state[i][j] == 0:
					moves.append((i, j))
		return moves

	def get_new_state(self, move):
		new_board_state = self.board_state.copy()
		x, y = move[0], move[1]
		new_board_state[x][y] = 1 if self.turn_O else -1
		self.turn_O = not self.turn_O
		return GameStatus(new_board_state, self.turn_O)
