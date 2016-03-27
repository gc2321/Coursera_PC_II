"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7

class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)

        if obstacle_list != None:
            self._obstacle_list = list(obstacle_list)
            for cell in self._obstacle_list:
                self.set_full(cell[0], cell[1])
        else:
            self._obstacle_list = []
        
        #print poc_grid.Grid.__str__(self)
        
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list=[]       
        self._zombie_list=[]
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
        
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)   
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for num in self._zombie_list:
                yield num

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for num in self._human_list:
                yield num
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        self._visited = self._cells
        self._distance_field = [[(self._grid_width*self._grid_height)for _ in range(self._grid_width)] 
                       for __ in range(self._grid_height)]
        
        self._boundary = poc_queue.Queue()
        
        type_dic={HUMAN: self.humans(), ZOMBIE: self.zombies()}
        
        for item in type_dic[entity_type]:
                self._boundary.enqueue(item)
                self._visited[item[0]][item[1]]= FULL
                self._distance_field[item[0]][item[1]]=0
                
        _score = 0
        
        while len(self._boundary)!=0:
            
            number_in_boundary = len(self._boundary)
            neighbor_set = set()
            
            for _ in range(number_in_boundary):
                cell = self._boundary.dequeue() 
                neighbors = self.four_neighbors(cell[0], cell[1])
                for each in neighbors:
                        neighbor_set.add(each)
                    
            for neighbor in neighbor_set:
                if self._visited[neighbor[0]][neighbor[1]]!= FULL:
                    self._visited[neighbor[0]][neighbor[1]]= FULL
                    self._distance_field[neighbor[0]][neighbor[1]]=_score+1
                    self._boundary.enqueue(neighbor)
            
            _score += 1
                                
        return self._distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """

        update_list = []
        for item in self._human_list:
            possible_move = self.eight_neighbors(item[0], item[1])
            possible_move.append((item[0], item[1]))
            
            possible_move2=[] 
            for each in possible_move:
                if self.is_empty(each[0], each[1]):
                    possible_move2.append(each)

            move ={}
            for each in possible_move2:
                move[each]= zombie_distance_field[each[0]][each[1]]
            
            _max = max(move.values())
            max_key=[]
            for key, value in move.items():
                if value==_max:
                    max_key.append(key)
            
            update_list.append(random.choice(max_key))
        
        self._human_list = update_list
                                 
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """

        update_list = []
        for item in self._zombie_list:
            possible_move = self.four_neighbors(item[0], item[1])
            possible_move.append((item[0], item[1]))
            
            possible_move2=[] 
            for each in possible_move:
                if self.is_empty(each[0], each[1]):
                    possible_move2.append(each)
                                              
            move ={}
            for each in possible_move2:
                move[each]= human_distance_field[each[0]][each[1]]
            
            _min = min(move.values())
            min_key=[]
            for key, value in move.items():
                if value==_min:
                    min_key.append(key)
            
            update_list.append(random.choice(min_key))

        self._zombie_list =  update_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
