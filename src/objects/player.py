""" Module for the player object."""
from src.objects.tile import TileSet
from src.logic.error import IllegalMove
from src.objects.typedefs import Move, Orientation
import random

class Player:
    """ Player object that preserves for a whole match. """ 

    def __init__(self, player_ind, hand=None):
        """
            player_ind (int) - player 0, 1, ... 
            hand (None|list) - list of inds of tiles to start with 
        """
        self.points = 0 
        self.player_ind = player_ind
        self.hand = TileSet(hand)

    def __str__(self):
        return f"Player of ind {self.player_ind}. With hand {self.hand}"

    # preliminary to check options 
    def legal_moves(self, game_state):
        legal_tile_moves = []
        for ind in self.hand.get_list():
            for orien in [Orientation.LEFT, Orientation.RIGHT]:
                # print(f"Check ind:{ind} and orien:{orien}. Status: {game_state.is_legal_tile_move(ind, orien)}")
                # print(f"    Manual check: {TileSet.look_up.get(ind)} vs ({game_state.board.left},{game_state.board.right})")
                if game_state.is_legal_tile_move(ind, orien):
                    legal_tile_moves += [(ind,orien)]

        can_draw = False
        if game_state.can_draw():
            can_draw = True

        return can_draw, legal_tile_moves

    def can_go(self, game_state):
        can_draw, legal_tile_moves = self.legal_moves(game_state)
        if can_draw or len(legal_tile_moves) > 0:
            return True
        return False

    def select_move(self,game_state):
        " Basic select move if can, draw, or pass in that order."
        can_draw, legal_tile_moves = self.legal_moves(game_state)

        # print("Player checking legal moves...")
        # print(can_draw, legal_tile_moves)

        if len(legal_tile_moves) > 0:
            ind, orientation = legal_tile_moves[0]
            return Move.PLAY_TILE,ind, orientation 
        if can_draw:
            return Move.DRAW_TILE, None, None
        return Move.PASS_MOVE, None, None


    # # modify the game state
    # def play_tile(self,game_state,ind):
    #     """
    #         play a tile to the board 

    #         Args:
    #             game_state (Game) - game object of the current game
    #             ind (None|int) - ind of the tile that is played. 
    #                             None means draw a tile.
    #     """
    #     if not game_state.is_legal_tile_move(ind):
    #         raise IllegalMove(f"{ind} can not be played.")

    #     game_state.add_tile_to_board(ind)
    #     self.hand.remove_domino(ind)

    # def draw_tile(self, game_state):
    #     """
    #         player draws a tile 

    #         Args:
    #             game_state (Game) - game object of the current game
    #     """
    #     if not game_state.can_draw():
    #         raise IllegalMove(f"Can not draw from the pile.")
    #     ind = game_state.draw_tile_from_pile()
    #     self.hand.add_domino(ind)

    # def pass_move(self, game_state):
    #     """
    #         Do not make a move. Only valid if there are no available moves.
    #     """
    #     if self.can_go(game_state):
    #         raise IllegalMove(f"Encounterd a pass with legal moves.") 
    #     game_state.pass_move()

    # # def play_move(self,game_state,move_code, ind=None):
    #     if move_code == Move.PLAY_TILE:
    #         self.play_tile(game_state, ind)  
    #     elif move_code == Move.DRAW_TILE:
    #         self.draw_tile(game_state)
    #     elif move_code == Move.PASS_MOVE:
    #         self.pass_move(game_state)

    #     return move_code, ind


class RandPlayer(Player):
    """Random Player. """

    def __str__(self):
        return "RANDOM" + super().__str__()

    def select_move(self, game_state):
        if not self.can_go(game_state):
            return Move.PASS_MOVE, None, None 
        # make a random selection 
        placeholder = -1 
        can_draw, legal_tile_moves = self.legal_moves(game_state)
        if can_draw:
            legal_tile_moves += [(placeholder,None)]

        ind, orientation = random.choice(legal_tile_moves)
        if ind == placeholder:
            return Move.DRAW_TILE, None, None
        else:
            return Move.PLAY_TILE, ind, orientation

