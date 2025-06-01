# Dominos

Play and train an engine to play Dominos. This is the classic game where players in a term try to empty their hands matching the dots on the tiles with the play board. 

When designing the engine, keep in mind that the explosion game state is an issue here, for example, Q-learning on the full gamestate would be computationally difficult to implement. Instead, one can consider using only certain features. 

Options include:
* abuse of scikit-learning by using supervised learning weighted by data where engine does well 
    * Generate many game episodes 
    * save (state_features, action_taken, outcome probability / return) as tuple
    * treat like supervised classifcation problem 
* PyTorch unsupervised learning 



# Data structure
Objects include: 
* TileSet - used for sets of tile like player hands. Tiles are referenced by index. 
    * s 
s


