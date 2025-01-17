"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def minimizing_opponent_moves(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    #my_moves = len(game.get_legal_moves(player))
    #opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    #return float(my_moves - 5 * opponent_moves)

    # get current move count
    move_count = game.move_count

    # count number of moves available
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # calculate weight
    w = 10 / (move_count + 1)

    # return weighted delta of available moves
    return float(own_moves - (w * opp_moves))

def maximizing_player_moves(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(5 * my_moves - opponent_moves)

def maximizing_ratio_of_player_to_opponent_move(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    #my_moves = len(game.get_legal_moves(player))
    #opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    #if(my_moves == 0):
    #    return float("-inf")

    #if(opponent_moves == 0):
    #    return float("inf")

    #return float(my_moves / opponent_moves)

    score = .0
    total_spaces = game.width * game.height
    remaining_spaces = len(game.get_blank_spaces())
    coefficient = float(total_spaces - remaining_spaces) / float(total_spaces)

    my_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    for move in my_moves:
        isNearWall = 1 if (move[0] == 0 or move[0] == game.width - 1 or move[1] == 0 or move[1] == game.height - 1) else 0
        score += 1 - coefficient * isNearWall

    for move in opponent_moves:
        isNearWall = 1 if (move[0] == 0 or move[0] == game.width - 1 or move[1] == 0 or move[1] == game.height - 1) else 0
        score -= 1 - coefficient * isNearWall

    return score

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return minimizing_opponent_moves(game,player)
    
def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return maximizing_player_moves(game,player)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return maximizing_ratio_of_player_to_opponent_move(game,player)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        
        moves = game.get_legal_moves(self)
        bestmove = (-1, -1)

        xlist = []
        for move in moves:
            xgame = game.forecast_move(move)
            tmpvalue = self.Min_Value(xgame, depth - 1)
            
            xlist.append((tmpvalue,xgame.is_winner(self),move))

            if(xgame.is_winner(self)):
                bestmove = xgame.get_player_location(self)

        xxlist = sorted(xlist, key=lambda tup: tup[0],reverse=True)
        if(bestmove == (-1,-1) and len(xxlist) != 0): _,_,bestmove = xxlist[:1][0]

        return bestmove

    def Max_Value(self, game, depth):
        """Max Value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        alpha = float("-inf")
        moves = game.get_legal_moves(self)
        if(depth == 0 or len(moves) == 0):
           return self.score(game,self)

        for move in moves:
            alpha = max(alpha, self.Min_Value(game.forecast_move(move), depth - 1))
            
        return alpha

    def Min_Value(self, game, depth):
        """Min Value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        alpha = float("inf")
        moves = game.get_legal_moves(game.get_opponent(self)) 
        if(depth == 0 or len(moves) == 0):
           return self.score(game,self)

        for move in moves:
            alpha = min(alpha, self.Max_Value(game.forecast_move(move), depth - 1))

        return alpha

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        # TODO: finish this function!
        
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)


        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            
            for depth in range(1, game.width * game.height):
                moves = game.get_legal_moves(self)
                if not moves:
                    return best_move

                best_move = self.alphabeta(game, depth)


        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        #self.TIMER_THRESHOLD = float("-inf")
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        moves = game.get_legal_moves(self)
        bestmove = (-1, -1)
        bestscore = float("-inf")

        for move in moves:
            xgame = game.forecast_move(move)
            tmpvalue = self.Min_Value(xgame, depth - 1, bestscore, beta)
            if(tmpvalue > bestscore):
                bestscore = tmpvalue
                bestmove = move

        return bestmove

    def Max_Value(self, game, depth, alpha, beta):
        """Max Value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = game.get_legal_moves(self)

        if(depth == 0 or not moves):
            xscore = self.score(game,self)
            return xscore

        val = float("-inf")

        for move in moves:
            xgame = game.forecast_move(move)
            val = max(val, self.Min_Value(xgame, depth - 1, alpha, beta))
            if(val >= beta):
                return val
            alpha = max(alpha,val)
            
        return val

    def Min_Value(self, game, depth, alpha, beta):
        """Min Value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        moves = game.get_legal_moves(game.get_opponent(self))

        if(depth == 0 or not moves):
            xscore = self.score(game,self)
            return xscore

        val = float("inf")

        for move in moves:
            xgame = game.forecast_move(move)
            val = min(val, self.Max_Value(xgame, depth - 1, alpha, beta))
            if(val <= alpha):
                return val
            beta = min(beta,val)

        return val
