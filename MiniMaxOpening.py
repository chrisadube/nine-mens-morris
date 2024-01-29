'''
GROUP MEMBERS:
Christopher Dube
Jake Furtaw

COSC 461
Fall 2023
Project 2

Part 1: MINIMAX
Step 1: MiniMaxOpening
'''

import sys
import NineMensMorrisVariantD as Game

global depth
global evaluations

def isWhitesTurn(d): return d%2 == 0

def NextMove(board, d=0):
    global evaluations
    evaluations += 1
    
    # Base Case 1 (max depth reached)
    if d == depth:
        return board.StaticEstimation_Opening()
    
    move_est = []
    if isWhitesTurn(d): # White's turn
        moves = board.GenerateMovesOpening()
        
        # Base Case 2 (no moves remaining)
        if len(moves) == 0:
            return board.StaticEstimation_Opening()
        
        curmax = float('-inf')
        for s in moves:
            se = NextMove(s, d+1)
            curmax = max(curmax, se)
            if d == 0:
                move_est.append( (s, se) ) # Add to list of moves/se for this turn (useful for randomly selecting one)
        
        if d==0:
            minimax = max(move_est, key=lambda item: item[1])
            return minimax[0], minimax[1]
        
        return curmax
    
    else: # Black's turn
        # Swap colors
        tempb = board.createCopy()
        tempb.swap_colors()
        moves = tempb.GenerateMovesOpening()
        
        # Base Case 2 (no moves remaining)
        if len(moves) == 0:
            return board.StaticEstimation_Opening()
        
        for i in range(0,len(moves)):
            moves[i].swap_colors()
        
        curmin = float('+inf')
        for s in moves:
            se = NextMove(s, d+1)
            curmin = min(curmin, se)
        
        return curmin


if __name__ == '__main__':
    filename_board_in = sys.argv[1]
    filename_board_out = sys.argv[2]
    depth = int(sys.argv[3])
    
    evaluations = -1
    
    input_state = Game.BoardStateFromFile(filename_board_in)
    
    output_state, estimation = NextMove(input_state)
    
    print('Input position: ', Game.GetBoardOutput(input_state))
    print('Output position:', Game.GetBoardOutput(output_state))
    print('Positions evaluated by static estimation:', evaluations)
    print('MINIMAX estimate:', estimation)
    
    # Put output position into output file
    out_file = open(filename_board_out, 'w')
    out_file.write(Game.GetBoardOutput(output_state))
    out_file.close()
