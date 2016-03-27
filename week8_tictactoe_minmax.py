"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
import random

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(120)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def minmax(board, player):  
    """
    Mini max function 
    """
    if board.check_win()==2:
        return SCORES[provided.PLAYERX]
    elif board.check_win()==3:
        return SCORES[provided.PLAYERO]
    elif board.check_win()==4:
        return SCORES[provided.DRAW]
 
    all_move =[]
    for each in board.get_empty_squares():
        temp = board.clone()
        temp.move(each[0], each[1], player)
        
        all_move.append(minmax(temp, provided.switch_player(player))) 
        
    if player == provided.PLAYERX:
        all_move.sort(reverse=True)
    else:
        all_move.sort()
    
    return all_move[0]
    
def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if len(board.get_empty_squares())==0:
        return 0, (-1,-1)
    
    all_move =[]
    for each in board.get_empty_squares():
        temp = board.clone()
        temp.move(each[0], each[1], player)
      
        all_move.append([minmax(temp, provided.switch_player(player)), each]) 
        
    if player == provided.PLAYERX:
        all_move.sort(key = lambda x: x[0], reverse=True)
    else:
        all_move.sort(key = lambda x: x[0])
    
    return all_move[0][0], all_move[0][1]

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
