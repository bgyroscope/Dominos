"""Module for the game state and match """
import random
from src.objects.tile import TileSet
from src.objects.typedefs import Move, Orientation
from src.logic.error import IllegalMove

TILES_IN_STARTING_HAND = 7
WIN_SCORE = 100

class Board:
    """ Board object where tiles are placed on. """

    def __init__(self):
        self.tiles = TileSet() 
        self.left = None
        self.right = None

    def is_valid(self, ind, orientation):
        """ check if the tile can be played """
        if self.left is None:
            return True
        
        tile_left, tile_right = TileSet.look_up.get(ind)
        if orientation == Orientation.LEFT:
            if tile_left == self.left or tile_right == self.left:
                return True
        if orientation == Orientation.RIGHT:
            if tile_left == self.right or tile_right == self.right:
                return True
        
        return False

    def add_tile(self,ind, orientation):
        """ add tile of ind to the board """
        if not ind:
            return 
        
        tile_left, tile_right = TileSet.look_up.get(ind)
        # no tiles in pile yet? Just place it 
        if self.left is None: 
            self.left = tile_left 
            self.right = tile_right
        
        # link the placed domino
        if orientation == Orientation.LEFT:
            if self.left == tile_left:
                self.left = tile_right
            elif self.left == tile_right:
                self.left = tile_left
            else:
                raise IllegalMove(f"The tile ({tile_left},{tile_right}) can not be added to {self.left}")

        if orientation == Orientation.RIGHT:
            if self.right == tile_left:
                self.right = tile_right
            elif self.right == tile_right:
                self.right = tile_left
            else:
                raise IllegalMove(f"The tile ({tile_left},{tile_right}) can not be added to {self.right}")

        self.tiles.add_domino(ind) 

class Game:
    """ Game object that holds the game properties. """

    def __init__(self,player_list):
        # to track whose turn it is and how many passes
        self.to_go = 0 
        self.pass_count = 0 
        # the players 
        self.players = player_list
        # pile to pick from and the play board 
        self.pile = TileSet(list(TileSet.look_up.keys())) 
        self.board = Board() 

    def get_num_players(self):
        return len(self.players)

    def set_up_hands(self): 
        """set up the hands """
        for i in range(TILES_IN_STARTING_HAND):
            for j in range(len(self.players)):
                self.to_go = j
                self.draw_tile_from_pile()

    def zeroth_move(self):
        """At the start of the game, find the first move."""
        doubles = [ TileSet.double_inds[len(TileSet.double_inds)-i-1] for i in range(len(TileSet.double_inds))] 
        while self.can_draw():
            for doub in doubles:
                for i,player in enumerate(self.players):
                    if player.hand.in_tileset(doub):
                        self.to_go = i
                        self.add_tile_to_board(doub, None)
                        return doub

            # if no doubles found, all players draw a tile
            for player in enumerate(self.players):
                self.draw_tile_from_pile()

    # playing a move 
    def can_draw(self):
        if self.pile.get_count() > 0:
            return True
        return False

    def is_legal_tile_move(self,ind, orientation):
        """Checks if the move is illegal. """
        if ind is None:
            return False
        if self.pile.in_tileset(ind):
            # TODO: raise impossible situation! 
            print("WARNING in pile")
            return False
        if self.board.tiles.in_tileset(ind):
            # TODO: raise impossible situation! 
            print("WARNING on board")
            return False
        for i,player in enumerate(self.players): 
            if i != self.to_go and player.hand.in_tileset(ind):
                # TODO: raise impossible situation! 
                print("WARNING in other player hand")
                return False
        if self.board.is_valid(ind, orientation):
            return True
        return False

    def next_turn(self,added_a_tile=False):
        self.to_go = (self.to_go + 1 ) % self.get_num_players() 
        if added_a_tile:
            self.pass_count = 0 
        else:
            self.pass_count += 1

    # the moves that can be made
    def next_move(self):
        """play the selected move on the board"""
        curr_player = self.players[self.to_go]
        move_code, ind, orientation = curr_player.select_move(self)

        if move_code == Move.PLAY_TILE:
            if not self.is_legal_tile_move(ind, orientation):
                raise IllegalMove(f"{ind} can not be played.")
            self.add_tile_to_board(ind, orientation)
        elif move_code == Move.DRAW_TILE:
            if not self.can_draw():
                raise IllegalMove(f"Can not draw from the pile.")
            self.draw_tile_from_pile()
        elif move_code == Move.PASS_MOVE:
            if curr_player.can_go(self):
                raise IllegalMove(f"Encounterd a pass with legal moves.") 
            self.pass_move()

        return move_code,ind 

    def add_tile_to_board(self,ind,orientation):
        self.board.add_tile(ind,orientation)
        self.players[self.to_go].hand.remove_domino(ind)
        self.next_turn(True)

    def draw_tile_from_pile(self):
        """
            Draw a tile from the pile. 
            If there are no tiles, return None.            
        """
        ind = random.choice(self.pile.get_list())
        print(f" --- drew tile {ind}")
        self.pile.remove_domino(ind)
        self.players[self.to_go].hand.add_domino(ind)

    def pass_move(self):
        """ pass move to next player """
        self.next_turn()

    # Play a full game
    def player_hand_count(self):
        return [player.hand.get_count() for player in self.players]

    def player_hand_scores(self):
        return [player.hand.get_score() for player in self.players]

    def game_continues(self):
        """Get the game state.""" 
        if self.pass_count >= len(self.players):
            return False 
        for count in self.player_hand_count():
            if count == 0:
                return False 

        return True

    def play_game(self):
        """ Play a full game. """
        self.set_up_hands()
        doub = self.zeroth_move()
        print(f"Found double. {doub} or {TileSet.look_up.get(doub)} was played.")

        move_count = 0 
        while self.game_continues() and move_count < 100:
            curr_player_id = self.to_go + 0 
            move_code, ind = self.next_move()
            s = f"({move_count:3d}) Player id:{curr_player_id} made move {move_code}"
            if ind:
                s += f" with ind: {ind}, i.e. ({TileSet.look_up.get(ind)})"
            s += "."
            print(s)
            self.print_current_status() 

            move_count += 1


    def print_current_status(self):
        print(f"Current Status (with player {self.to_go} to go): ")
        print(f"    Board: {self.board.tiles.get_list()}")
        print(f"    Board Tiles: {self.board.tiles.get_list_of_tiles()}")
        print(f"    Board left/right: {self.board.left},{self.board.right}")
        print(f"    Pile: {self.pile.get_list()}")
        print(f"    Pile Tiles: {self.pile.get_list_of_tiles()}")
        for i,player in enumerate(self.players):
            print(f"    P{i:d}: {player.hand.get_list()}")
            print(f"    P{i:d} Tiles: {player.hand.get_list_of_tiles()}")
            print(f"    P{i:d} Tile Count: {player.hand.get_count()}")


class Match:
    """the full match object"""

    def __init__(self, player_list):
        self.players = player_list
        self.game = Game(player_list)

    def play_match(self):
        """ play a full match to WIN_SCORE"""
        pass 