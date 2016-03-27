"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]
    
    def get_row_col(self, number):
        """
        Return row, col for a given number
        """
        for row in range(self._height):
            for col in range(self._width):
                if self.get_number(row, col)== number:
                    return (row, col)
                        
    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction + str(self.get_row_col(0))
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction + str(self.get_row_col(0))
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction + str(self.get_row_col(0))
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction + str(self.get_row_col(0))
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction + str(self.get_row_col(0))

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        okay = 3
        if self.get_number(target_row, target_col)!=0:
            okay -=1
                
        if target_row < self._height:
            for row in range(target_row+1, self._height):                         
                for col in range(self._width):            
                    if self.current_position(row, col)!=(row, col):
                        okay -=1
        
        if target_col < self._width:
            for col in range(target_col+1, self._width):
                if self.current_position(target_row, col)!=(target_row, col):
                    okay -=1
                        
        return okay == 3
       
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        if self.lower_row_invariant(target_row, target_col) and target_row>1 and target_col>0:
            
            # move[0]= history of move, move[1]=True/False - solved
            move=["", False]
        
            while move[1]==False:

                if self.current_position(target_row, target_col)==(target_row, target_col-1):
                    move[0] +="l"
                    self.update_puzzle("l")
                    move[1]=True
                    break
                elif self.current_position(target_row, target_col)==(target_row-1, target_col-1):
                    move[0] +="lurdl"
                    self.update_puzzle("lurdl")
                    move[1]=True
                    break
                elif self.current_position(target_row, target_col)==(target_row-1, target_col):
                    move[0] +="lurdlurdl"
                    self.update_puzzle("lurdlurdl")
                    move[1]=True
                    break
                else:
                    move_temp = ""
                    move_temp +="l"*target_col
                    move_temp +="u"*target_row 
                    move_temp +="r"*(self._width-1) 
                    move_temp +="d" 
                    move_temp +="l"*(self._width-2)
                    
                    row_left = target_row - 2
                    
                    while row_left > 0:                        
                        if row_left==1:
                            move_temp +="d"
                            move_temp += "r"*(self._width-2)                       
                            move_temp += "u"
                            move_temp +="l"*(self._width-2)
                            move_temp +="d"
                            row_left -=1
                        else:
                            move_temp +="d"
                            move_temp += "r"*(self._width-2)                       
                            move_temp += "d"
                            move_temp +="l"*(self._width-2)
                            row_left -=2
           
                    # return to initial position
                    move_temp +="l"
                    move_temp +="d"
                    move_temp +="r"*target_col
                    
                    self.update_puzzle(move_temp)
                    move[0] += move_temp
                                        
        return move[0]
            
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        if self.lower_row_invariant(target_row, 0) and target_row > 1:
            
            # move[0]= history of move, move[1]=True/False - solved
            move=["", False]
        
            while move[1]==False:
                if self.current_position(target_row, 0)==(target_row-1, 0):
                    move[0] +="u"+"r"*(self._width-1) 
                    self.update_puzzle("u"+"r"*(self._width-1))
                    move[1]=True
                    break
                elif self.current_position(target_row, 0)==(target_row-1, 1):
                    move[0] +="ruldruldrdlurdluruldrdlu"+"r"*(self._width-1) 
                    self.update_puzzle("ruldruldrdlurdluruldrdlu"+"r"*(self._width-1))
                    move[1]=True
                    break
                elif self.current_position(target_row, 0)==(target_row-2, 0):
                    move[0] += "rulurddlu"+"r"*(self._width-1) 
                    self.update_puzzle("rulurddlu"+"r"*(self._width-1))
                    move[1]=True
                    break
                elif self.current_position(target_row, 0)==(target_row-2, 1):
                    move[0] +="urdlurdluruldrdlu"+"r"*(self._width-1)
                    self.update_puzzle("urdlurdluruldrdlu"+"r"*(self._width-1))
                    move[1]=True
                    break
                else:
                    move_temp = ""               
                    move_temp +="u"*target_row 
                    move_temp +="r"*(self._width-1) 
                    move_temp +="d" 
                    move_temp +="l"*(self._width-2)
                    
                    row_left = target_row - 2
                    
                    while row_left > 0:                        
                        if row_left==1:
                            move_temp +="d"
                            move_temp += "r"*(self._width-2)                       
                            move_temp += "u"
                            move_temp +="l"*(self._width-2)
                            move_temp +="d"
                            row_left -=1
                        else:
                            move_temp +="d"
                            move_temp += "r"*(self._width-2)                       
                            move_temp += "d"
                            move_temp +="l"*(self._width-2)
                            row_left -=2
           
                    # return to initial position
                    move_temp +="dlur"
                    move_temp +="dlurdl"
                    
                    self.update_puzzle(move_temp)
                    move[0] += move_temp
                                               
        return move[0]

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        okay = 3
        
        if self.get_number(0, target_col)!=0:
            okay -=1
                
        if self._height > 1:
            for row in range(1, self._height):                         
                for col in range(self._width):            
                    if self.current_position(row, col)!=(row, col):
                        if row==1 and col < target_col:
                            pass
                        else:
                            okay -=1
        
        if target_col < self._width-1:
            for col in range(target_col+1, self._width):
                if self.current_position(1, col)!=(1, col):
                    okay -=1
                        
        return okay == 3

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        okay = 4
        
        if self.get_number(1, target_col)!=0:
            okay -=1
                
        if self._height > 2:
            for row in range(2, self._height):                         
                for col in range(self._width):            
                    if self.current_position(row, col)!=(row, col):
                        okay -=1
        
        if target_col < self._width-1:
            for col in range(target_col+1, self._width):
                if self.current_position(1, col)!=(1, col):
                    okay -=1
        
        for col in range (target_col+1, self._width):
            if self.current_position(0, col)!=(0, col):
                    okay -=1
        
        return okay == 4
        
    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        if self.row0_invariant(target_col):
            
            # move[0]= history of move, move[1]=True/False - solved
            move=["", False]
        
            while move[1]==False:
                if self.current_position(0, target_col)==(0, target_col-1):                    
                    move[0] +="ld"
                    self.update_puzzle("ld")
                    move[1]=True
                    break
                elif self.current_position(0, target_col)==(1, target_col-1):                    
                    move[0] +="lldruldrurdluldrruld"
                    self.update_puzzle("lldruldrurdluldrruld")
                    move[1]=True
                    break                                
                elif self.current_position(0, target_col)==(1, target_col-2):                     
                    move[0] += "ldruldruldlurrdlurdl" 
                    self.update_puzzle("ldruldruldlurrdlurdl")
                    move[1]=True
                    break               
                elif self.current_position(0, target_col)==(0, target_col-2):                   
                    move[0] += "lldruldrruldruldlurdruld" 
                    self.update_puzzle("lldruldrruldruldlurdruld")
                    move[1]=True
                    break
         
                else:
                    move_temp = ""               
                    move_temp +="l"*target_col 
                    move_temp +="d"
                    move_temp +="r"*(target_col-1)
                    move_temp +="u" 
                    move_temp +="r"
                    
                    self.update_puzzle(move_temp)
                    
                    move[0] += move_temp
                                       
        return move[0]

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        if self.row1_invariant(target_col):
            
            move=["", False]
        
            while move[1]==False:

                if self.current_position(1, target_col)==(0, target_col):
                    move[0] +="u"
                    self.update_puzzle("u")
                    move[1]=True
                    break
                elif self.current_position(1, target_col)==(1, target_col-1):
                    move[0] +="uldruldru"
                    self.update_puzzle("uldruldru")
                    move[1]=True
                    break
                elif self.current_position(1, target_col)==(0, target_col-1):
                    move[0] +="lurdlur"
                    self.update_puzzle("lurdlur")
                    move[1]=True
                    break
                else:
                    move_temp = ""
                    move_temp +="u"
                    move_temp +="l"*target_col
                    move_temp +="d"
                    move_temp +="r"*target_col
                   
                    self.update_puzzle(move_temp)
                    move[0] += move_temp
                                        
        return move[0]
        
    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move=""
        if self.row1_invariant(1):
            if self.get_row_col(1)==(0, 0):
                move +="ul"               
            elif self.get_row_col(1)==(1, 0):
                move +="uldrul"              
            elif self.get_row_col(1)==(0, 1):
                move +="uldruldrul"
                           
        self.update_puzzle(move)                                
        return move
    
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move=""
        
        # check if 0-tile is in the last place, if not put it there        
        if self.get_row_col(0)!=(self._width-1, self._height-1):
            move_temp =""
            move_temp +="d"*(self._height-self.get_row_col(0)[0]-1)
            move_temp +="r"*(self._width-self.get_row_col(0)[1]-1)
            self.update_puzzle(move_temp)
            move += move_temp

        # solve_interior_tile and solve_col0_tile for row >=2
        for row in range(self._height-1, 1, -1):
            for col in range(self._width-1, -1, -1):
                if col!=0:
                    assert self.lower_row_invariant(row, col), "error at ("+str(row)+","+str(col)+")"
                    move += self.solve_interior_tile(row, col)
                else:
                    move += self.solve_col0_tile(row)
                
        # solve_row1_tile and solve_row0_tile for row <2, and col<=1   
        for col in range(self._width-1, 1, -1):
            assert self.row1_invariant(col), "error at (1,"+str(col)+")"
            move += self.solve_row1_tile(col)
            assert self.row0_invariant(col), "error at (0,"+str(col)+")"
            move += self.solve_row0_tile(col)
            
        # solve_2x2
        move += self.solve_2x2()
        
        return move

# Start interactive simulation

#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
