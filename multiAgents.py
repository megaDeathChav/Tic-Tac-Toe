from GameStatus_5120 import GameStatus

def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal, winner = game_state.is_terminal()
    if depth == 0 or terminal:
        newScores = game_state.get_scores()
        return newScores, None

    if maximizingPlayer:
        max_eval = float('-inf')
        best_move = None
        for move in game_state.get_moves():  
            child = game_state.get_new_state(move[0], move[1])
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
        for move in game_state.get_moves():
            child = game_state.get_new_state(move)
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
    terminal, winner = game_status.is_terminal()
    if depth == 0 or terminal:
        scores = game_status.get_scores()
        return scores * turn_multiplier, None

    max_eval = float('-inf')
    best_move = None

    for move in game_status.get_moves():
        new_game_status = game_status.get_new_state(move)
        score, _ = negamax(new_game_status, depth - 1, -turn_multiplier, -beta, -alpha)
        score = -score
    
        if score > max_eval:
            max_eval = score
            best_move = move

        alpha = max(alpha, score)
        if beta <= alpha:
            break
    return max_eval, best_move