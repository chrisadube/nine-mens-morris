'''
GROUP MEMBERS:
Christopher Dube
Jake Furtaw

COSC 461
Fall 2023
Project 2

This file contains the functionality to play
the Nine Men's Morris, Variant-D game, and
some utility functions.

Note: This program was designed around object
      oriented programming rather than
      functional programming.

KEY METHODS REQUIRED FOR PROJECT IN THIS FILE:
    StaticEstimation_Opening_Improved()
    StaticEstimation_MidgameEndgame_Improved()

    *Inside the improved static estimation
    functions are explanations to why
    particular strategies were chosen.
'''

import copy

def neighbors(j):
    '''
        *** DOES NOT BELONG TO INSTANCE OF CLASS ***
    
    Parameter j (int): index of board position
    Return: L (list)
    '''
    if   j==0:  return [1,3,8] # a0
    elif j==1:  return [0,2,4] # d0
    elif j==2:  return [1,5,13] # g0
    elif j==3:  return [0,4,6,9] # b1
    elif j==4:  return [1,3,5] # d1
    elif j==5:  return [2,4,7,12] # f1
    elif j==6:  return [3,7,10] # c2
    elif j==7:  return [5,6,11] # e2
    elif j==8:  return [0,9,20] # a3
    elif j==9:  return [3,8,10,17] # b3
    elif j==10: return [6,9,14] # c3
    elif j==11: return [7,12,16] # e3
    elif j==12: return [5,11,13,19] # f3
    elif j==13: return [2,12,22] # g3
    elif j==14: return [10,15,17] # c4
    elif j==15: return [14,16,18] # d4
    elif j==16: return [11,15,19] # e4
    elif j==17: return [9,14,18,20] # b5
    elif j==18: return [15,17,19,21] # d5
    elif j==19: return [12,16,18,22] # f5
    elif j==20: return [8,17,21] # a6
    elif j==21: return [18,20,22] # d6
    elif j==22: return [13,19,21] # g6

def location_weight(j):
    '''
    Used for improved static estimation.
    Returns the utility value of a specified location.
    The value is comprised of:
        Number of neighbors +
        Number of mills connected
    
    Parameter j (int): index of board position
    Return (int): utility value of position on board
    '''
    if   j==0:  return 6 # a0
    elif j==1:  return 4 # d0
    elif j==2:  return 6 # g0
    elif j==3:  return 7 # b1
    elif j==4:  return 4 # d1
    elif j==5:  return 7 # f1
    elif j==6:  return 5 # c2
    elif j==7:  return 5 # e2
    elif j==8:  return 5 # a3
    elif j==9:  return 6 # b3
    elif j==10: return 5 # c3
    elif j==11: return 5 # e3
    elif j==12: return 6 # f3
    elif j==13: return 5 # g3
    elif j==14: return 6 # c4
    elif j==15: return 5 # d4
    elif j==16: return 6 # e4
    elif j==17: return 7 # b5
    elif j==18: return 6 # d5
    elif j==19: return 7 # f5
    elif j==20: return 6 # a6
    elif j==21: return 5 # d6
    elif j==22: return 6 # g6

def BoardStateFromFile(filename):
    '''
    Reads the board state from the specified file
    and returns a BoardState object.
    '''
    return BoardState(open(filename, 'r').readline().strip())

def GetBoardOutput(board):
    '''
    Returns the string representation of the
    specified board state.
    '''
    return ''.join(board.getBoardState())


class BoardState():
    '''
    Object representing a state of the board.
    '''
    BOARD_SIZE = 23 # 7 or 23
    LOCATIONS = range(0, BOARD_SIZE)
    MAX_STATIC_ESTIMATION_VALUE = 10000
    MULT_STATIC_ESTIMATION_VALUE = 1000
    WHITE = 'W'
    BLACK = 'B'
    EMPTY = 'x'
    
    def __init__(self, state=None):
        if not state:
            self.board = ['x']*BoardState.BOARD_SIZE
        elif type(state) == list:
            self.board = state
        elif type(state) == str:
            self.board = list(state)
    
    # Utility functions
    def getBoardOutput(self):
        return ''.join(self.getBoardState())
    
    def getBoardState(self):
        return self.board
    
    def isEmpty(self, index):
        return self.board[index] == BoardState.EMPTY
    
    def setEmpty(self, index):
        self.board[index] = BoardState.EMPTY
        
    def isWhite(self, index):
        return self.board[index] == BoardState.WHITE
    
    def setWhite(self, index):
        self.board[index] = BoardState.WHITE
        
    def isBlack(self, index):
        return self.board[index] == BoardState.BLACK
    
    def setBlack(self, index):
        self.board[index] = BoardState.BLACK
        
    def whiteCount(self):
        count = 0
        for location in self.board:
            if location == BoardState.WHITE:
                count += 1
        return count
    
    def blackCount(self):
        count = 0
        for location in self.board:
            if location == BoardState.BLACK:
                count += 1
        return count
    
    def createCopy(self):
        return BoardState(copy.deepcopy(self.board))
    
    def whiteMoves(self):
        '''
        Returns the number of moves that White
        has on the current board state.
        '''
        return len(self.GenerateMovesMidgameEndgame())
    
    def blackMoves(self):
        '''
        Returns the number of moves that Black
        has on the current board state.
        '''
        tempb = self.createCopy()
        tempb.swap_colors()
        return len(tempb.GenerateMovesMidgameEndgame())
    
    # Core functions
    def GenerateAdd(self):
        '''
        Parameter b (BoardState)
        Opening Phase
        '''
        L = []
        for index in BoardState.LOCATIONS:
            if self.isEmpty(index):
                b = self.createCopy()
                b.setWhite(index)
                if b.closeMill(index):
                    b.GenerateRemove(L)
                else:
                    L.append(b)
        return L

    def GenerateMove(self):
        '''
        Returns a list of board states where
        the player (currently white) can
        move to.
        '''
        L = []
        for index in BoardState.LOCATIONS:
            if self.isWhite(index):
                n = neighbors(index)
                
                for j in range(0, len(n)):
                    if self.isEmpty(n[j]):
                        b = self.createCopy()
                        b.setEmpty(index)
                        b.setWhite(n[j])
                        if b.closeMill(n[j]):
                            b.GenerateRemove(L)
                        else:
                            L.append(b)
        return L

    def GenerateMovesOpening(self):
        '''
        Returns a list of board states where
        the player can spawn an opening piece.
        '''
        return self.GenerateAdd()

    def GenerateMovesMidgameEndgame(self):
        '''
        Returns a list of board states where
        the player can move a piece to.
        '''
        if self.whiteCount() == 3:
            return self.GenerateHopping()
        else:
            return self.GenerateMove()

    def GenerateHopping(self):
        '''
        Returns a list of board states where
        the player can hop a piece to.
        '''
        L = []
        for index in BoardState.LOCATIONS:
            if self.isWhite(index):
                for j in BoardState.LOCATIONS:
                    if self.isEmpty(j):
                        b = self.createCopy()
                        b.setEmpty(index)
                        b.setWhite(j)
                        if b.closeMill(j):
                            b.GenerateRemove(L)
                        else:
                            L.append(b)
        return L

    def GenerateRemove(self, L):
        '''
        Returns a list of board states, that
        after a close-mill is formed, the
        player can remove an opponent's piece.
        '''
        positionAddedToList = False
        for index in BoardState.LOCATIONS:
            if self.isBlack(index):
                if not self.closeMill(index):
                    b = self.createCopy()
                    b.setEmpty(index)
                    L.append(b)
                    positionAddedToList = True
        
        if not positionAddedToList:
            for index in BoardState.LOCATIONS:
                if self.isBlack(index):
                    b = self.createCopy()
                    b.setEmpty(index)
                    L.append(b)
        
        # return void (None), L is updated in outer frame.
    
    def swap_colors(self):
        '''
        Swaps while pieces for blacks, and
        black piece for white.
        '''
        for index in BoardState.LOCATIONS:
            if   self.isBlack(index): self.setWhite(index)
            elif self.isWhite(index): self.setBlack(index)

    def StaticEstimation_Opening(self):
        '''
        Basic static estimation for opening phase.
        '''
        return self.whiteCount() - self.blackCount()

    def StaticEstimation_MidgameEndgame(self):
        '''
        Basic static estimation for midgame and
        endgame phases.
        '''
        numBlackMoves = self.blackMoves()
        
        if self.blackCount() <= 2: return BoardState.MAX_STATIC_ESTIMATION_VALUE
        elif self.whiteCount() <= 2: return -BoardState.MAX_STATIC_ESTIMATION_VALUE
        elif numBlackMoves == 0: return BoardState.MAX_STATIC_ESTIMATION_VALUE
        else: return BoardState.MULT_STATIC_ESTIMATION_VALUE * \
            (self.whiteCount() - self.blackCount()) - numBlackMoves
        
    def StaticEstimation_Opening_Improved(self):
        '''
        Required for Part 4, Step 1
        '''
        location_value_white = 0
        for i in BoardState.LOCATIONS:
            if self.isWhite(i):
                location_value_white += location_weight(i)
        location_value_black = 0
        for i in BoardState.LOCATIONS:
            if self.isBlack(i):
                location_value_black += location_weight(i)
        if location_value_black != 0:
            location_value = int(location_value_white/location_value_black)
        else:
            location_value = location_value_white
        
        return self.whiteCount() - self.blackCount() + location_value

    def StaticEstimation_MidgameEndgame_Improved(self):
        '''
        Required for Part 4, Step 2
        '''
        numBlackMoves = self.blackMoves()
        # IDEAS
        # Check for double mill
        # Distance between chips (sum of distances)
        # Weight for each board location occupied
        # Number of neighbors (+ for W, - for B)
        # Number of possible mills connected
        # Sum of mobility level +[0,4] for each W, -[0,4] for each B (like number of moves)
        # Use multiple of these, but apply a weight for each?
        
        if self.blackCount() <= 2: return BoardState.MAX_STATIC_ESTIMATION_VALUE
        elif self.whiteCount() <= 2: return -BoardState.MAX_STATIC_ESTIMATION_VALUE
        elif numBlackMoves == 0: return BoardState.MAX_STATIC_ESTIMATION_VALUE
        else: 
            # Value regarding number of neighbors.
            # The more chips adjacent to other chips,
            # the higher the value. Applies to White
            # and Black. Points rewarded depends on
            # the ratio between White and Black.
            neighbor_value_white = 0
            for i in BoardState.LOCATIONS: # should be range(22), minor inefficiency
                if self.isWhite(i):
                    curneighbors = neighbors(i)
                    for n in curneighbors:
                        if i < n and self.isWhite(n):
                            neighbor_value_white += 1
            neighbor_value_black = 0
            for i in BoardState.LOCATIONS: # should be range(22), minor inefficiency
                if self.isBlack(i):
                    curneighbors = neighbors(i)
                    for n in curneighbors:
                        if i < n and self.isBlack(n):
                            neighbor_value_black += 1
            if neighbor_value_black != 0:
                neighbor_value = int(neighbor_value_white/neighbor_value_black)
            else:
                neighbor_value = neighbor_value_white
            # Value regarding locations occupied and 
            # their utility. Takes the sum of values
            # occupied by White and Black, and calculates
            # the ratio of them for a final value.
            location_value_white = 0
            for i in BoardState.LOCATIONS:
                if self.isWhite(i):
                    location_value_white += location_weight(i)
            location_value_black = 0
            for i in BoardState.LOCATIONS:
                if self.isBlack(i):
                    location_value_black += location_weight(i)
            if location_value_black != 0:
                location_value = int(location_value_white/location_value_black)
            else:
                location_value = location_value_white
            # Double mills
            # Iterates through the board
            # and checks for double mills,
            # granting one point per
            # double mill.
            double_mills = 0
            for i in BoardState.LOCATIONS:
                if self.isWhite(i) and self.closeMill(i):
                    n = neighbors(i)
                    for j in n:
                        if self.isEmpty(j) and self.closeMill(j):
                            double_mills += 1
            
            return  BoardState.MULT_STATIC_ESTIMATION_VALUE * \
                    (self.whiteCount() - self.blackCount()) \
                    - numBlackMoves \
                    + neighbor_value \
                    + location_value \
                    + double_mills
    
    def closeMill(self, j):
        '''
        Parameter j (int): index of board position
        Parameter b (list): 
        '''
        c = self.board[j]
        if   j==0:
            return ((self.board[1] == c and self.board[2] == c) or
                    (self.board[3] == c and self.board[6] == c) or
                    (self.board[8] == c and self.board[20] == c))
        elif j==1:
            return ((self.board[0] == c and self.board[2] == c))
        elif j==2:
            return ((self.board[0] == c and self.board[1] == c) or
                    (self.board[5] == c and self.board[7] == c) or
                    (self.board[13] == c and self.board[22] == c))
        elif j==3:
            return ((self.board[0] == c and self.board[6] == c) or
                    (self.board[4] == c and self.board[5] == c) or
                    (self.board[9] == c and self.board[17] == c))
        elif j==4:
            return ((self.board[3] == c and self.board[5] == c))
        elif j==5:
            return ((self.board[2] == c and self.board[7] == c) or
                    (self.board[3] == c and self.board[4] == c) or
                    (self.board[12] == c and self.board[19] == c))
        elif j==6:
            return ((self.board[0] == c and self.board[3] == c) or
                    (self.board[10] == c and self.board[14] == c))
        elif j==7:
            return ((self.board[2] == c and self.board[5] == c) or
                    (self.board[11] == c and self.board[16] == c))
        elif j==8:
            return ((self.board[0] == c and self.board[20] == c) or
                    (self.board[9] == c and self.board[10] == c))
        elif j==9:
            return ((self.board[3] == c and self.board[17] == c) or
                    (self.board[8] == c and self.board[10] == c))
        elif j==10:
            return ((self.board[6] == c and self.board[14] == c) or
                    (self.board[8] == c and self.board[9] == c))
        elif j==11:
            return ((self.board[7] == c and self.board[16] == c) or
                    (self.board[12] == c and self.board[13] == c))
        elif j==12:
            return ((self.board[5] == c and self.board[19] == c) or
                    (self.board[11] == c and self.board[13] == c))
        elif j==13:
            return ((self.board[2] == c and self.board[22] == c) or
                    (self.board[11] == c and self.board[12] == c))
        elif j==14:
            return ((self.board[6] == c and self.board[10] == c) or
                    (self.board[15] == c and self.board[16] == c) or
                    (self.board[17] == c and self.board[20] == c))
        elif j==15:
            return ((self.board[14] == c and self.board[16] == c) or
                    (self.board[18] == c and self.board[21] == c))
        elif j==16:
            return ((self.board[7] == c and self.board[11] == c) or
                    (self.board[14] == c and self.board[15] == c) or
                    (self.board[19] == c and self.board[22] == c))
        elif j==17:
            return ((self.board[3] == c and self.board[9] == c) or
                    (self.board[14] == c and self.board[20] == c) or
                    (self.board[18] == c and self.board[19] == c))
        elif j==18:
            return ((self.board[15] == c and self.board[21] == c) or
                    (self.board[17] == c and self.board[19] == c))
        elif j==19:
            return ((self.board[5] == c and self.board[12] == c) or
                    (self.board[16] == c and self.board[22] == c) or
                    (self.board[17] == c and self.board[18] == c))
        elif j==20:
            return ((self.board[0] == c and self.board[8] == c) or
                    (self.board[14] == c and self.board[17] == c) or
                    (self.board[21] == c and self.board[22] == c))
        elif j==21:
            return ((self.board[15] == c and self.board[18] == c) or
                    (self.board[20] == c and self.board[22] == c))
        elif j==22:
            return ((self.board[2] == c and self.board[13] == c) or
                    (self.board[16] == c and self.board[19] == c) or
                    (self.board[20] == c and self.board[21] == c))
    