""" Module to store the tile set object """
from src.logic.error import InvalidDomino, UnexpectedDomino

# Parameters of the tiles
N = 6 # maximum number on one side of a domino
NUM_DOMINOS = int((N+1)*(N+2)/2)

class TileSet:
    """ A set of domino tiles. 
        
        Class attributes includes 
            look_up -- dictionary from ind to left,right of tile
            double_inds -- tuple of the inds that are doubles
                (0,0), (1,1), ...
    """
    look_up = {}
    double_inds = []
    count = 0 
    for i in range(N+1):
        for j in range(0,i+1):
            look_up[count] = (i,j) 
            if i == j:
                double_inds += [count]
            count += 1 
    double_inds = tuple(double_inds)

    def get_domino(i):
        return TileSet.look_up.get(i,None)

    #Individual tile set functions 
    def __init__(self, inds=None):
        """ Initiate an instance of a tile set. 
            Args: 
                inds(None|list) - list of inds to include 
        """
        if not inds:
            inds = set()
        for ind in inds:
            if not ind in TileSet.look_up:
                raise TypeError(f"{ind} is not valid for dominos of max number {N}")
        self.inds = set(inds)

    def clear_tileset(self):
        self.inds = set() 

    def __str__(self):
        return "inds with inds: " + str(self.inds)

    # Add / Remove dominos from the set 

    def is_domino(self, i):
        """Test if domino of ind, i, is in the tile set."""
        if i in TileSet.look_up.keys():
            return True
        return False

    def in_tileset(self,i):
        if i in self.inds:
            return True
        return False

    def add_domino(self,i):
        if not self.is_domino(i):
            raise InvalidDomino(f"{i} is not in the tile set.")
        if self.in_tileset(i):
            raise UnexpectedDomino(f"{i} is already in set. Can not add.") 
        self.inds.add(i)

    def remove_domino(self,i):
        if not self.is_domino(i):
            raise InvalidDomino(f"{i} is not in the tile set.")
        if not self.in_tileset(i):
            raise UnexpectedDomino(f"{i} is not in set. Can not remove.") 

        self.inds.remove(i)

    # Get properties of the tile set 
    def get_list(self):
        return list(self.inds)

    def get_list_of_tiles(self):
        return [TileSet.look_up.get(i) for i in self.get_list()]

    def get_count(self):
        return len(self.inds)
    
    def get_score(self):
        return sum([sum(TileSet.look_up.get(i)) for i in self.inds])