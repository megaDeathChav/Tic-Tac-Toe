from GameStatus_5120 import GameStatus

def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
	terminal = game_state.is_terminal()
	if (depth==0) or (terminal):
		newScores = game_state.get_scores(terminal)
		return newScores, None

	"""
    YOUR CODE HERE TO FIRST CHECK WHICH PLAYER HAS CALLED THIS FUNCTION (MAXIMIZING OR MINIMIZING PLAYER)
    YOU SHOULD THEN IMPLEMENT MINIMAX WITH ALPHA-BETA PRUNING AND RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE
    
    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    """

	# return value, best_move

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
	terminal = game_status.is_terminal()
	if depth == 0 or terminal:
        scores = game_status.get_negamax_scores(terminal)
        return scores * turn_multiplier, None

    max_eval = float('-inf')  # Initialize maximum evaluation to negative infinity
    best_move = None  # Initialize best move to None

    # Iterate through all possible moves
    for move in game_status.get_possible_moves():
        new_game_status = game_status.make_move(move)  # Make move
        # Recursively evaluate new game state using Negamax algorithm
        score, _ = negamax(new_game_status, depth - 1, -turn_multiplier, -beta, -alpha)
        score = -score  # Invert score due to alternating player perspectives
    
        # Update maximum evaluation and best move if a higher score is found
        if score > max_eval:
            max_eval = score
            best_move = move

        alpha = max(alpha, max_eval)  # Update alpha
        if beta <= alpha:
            break  # Prune search tree if a better option exists elsewhere

    return max_eval, best_move