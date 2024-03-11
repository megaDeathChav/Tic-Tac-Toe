from GameStatus_5120 import GameStatus
from copy import deepcopy

def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    game_copy = GameStatus(deepcopy(game_state.board_state), deepcopy(game_state.turn_O))
    terminal, winner = game_state.is_terminal()
    if depth == 0 or terminal:
        # get_scores returns a tuple of the scores for each player: (player, AI) where AI score is negative
        newScores = game_copy.get_scores()
        # return the sum of scores for both players, returns negative if AI wins, positive if player wins
        return newScores[0] + newScores[1], None 
        # if not maximizingPlayer:
        #     if newScores[0] > -1*newScores[1]:
        #         return newScores[0], None
        #     elif newScores[0] < -1*newScores[1]:
        #         return newScores[1], None
        #     else:
        #         return 0, None
        # else:
        #     if newScores[0] > -1*newScores[1]:
        #         return newScores[1], None
        #     elif newScores[0] < -1*newScores[1]:
        #         return newScores[0], None
        #     else:
        #         return 0, None
            
    if maximizingPlayer:
        max_eval = float('-inf')
        best_move = None
        for move in game_copy.get_moves():  
            child = game_copy.get_new_state(move)
            eval, _ = minimax(child, depth - 1, False, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in game_copy.get_moves():
            child = game_copy.get_new_state(move)
            eval, _ = minimax(child, depth - 1, True, alpha, beta)
            print("eval", eval, "min_eval", min_eval, "best_move", best_move, "move", move, "_", _)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    game_copy = GameStatus(deepcopy(game_status.board_state), deepcopy(game_status.turn_O))
    terminal, winner = game_status.is_terminal()

    if depth == 0 or terminal:
        scores = game_copy.get_scores()
        return turn_multiplier * (scores[0] + scores[1]), None

    max_eval = float('-inf')
    best_move = None
    for move in game_copy.get_moves():
        child = game_copy.get_new_state(move)
        eval, _ = negamax(child, depth - 1, -turn_multiplier, -beta, -alpha)
        eval = -eval

        if eval > max_eval:
            max_eval = eval
            best_move = move
        alpha = max(alpha, eval)
        if alpha >= beta:
            break
    return max_eval, best_move