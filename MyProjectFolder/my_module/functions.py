import random
from time import sleep
from IPython.display import clear_output

# from A4
def add_lists (list1, list2):
    """ Adds together 2 lists of ints.
    
    Parameters
    ----------
    list1 : list of int
        The first list, to be added.
    list2 : list of int
        The second list, to be added.
    
    Returns
    -------
    output : list
        The result of the addition of lists.
    """
    
    output = []
    for item1, item2 in zip(list1, list2):
        output.append(item1 + item2)
    return output

# from A4
def check_bounds (position, size):
    """ Checks whether the position is inside the grid.
    
    Parameters
    ----------
    position : list of int
        The position that is being checked.
    size : int
        The size of the square grid.
    
    Returns
    -------
    boolean
        Whether the position is within the restraints of the grid.
    """
    
    for item in position:
        # checks whether item is out of bounds
        if item < 0 or item >= size:
            return False
    return True

def eat(bots, food_list):
    """ Bots eat food if on same spot.
    
    Parameters
    ----------
    bots : list of list of int
        A list of the bot positions.
    food_list : list of list of int
        List of the food positions.
    """
    
    # iterates through bot positions
    for bot in bots:
        # iterates through food positions
        for food_loc in food_list:
            # compare bot and food positions
            first_pos = bot.position[0] == food_loc[0]
            second_pos = bot.position[1] == food_loc[1]
        
            # if food and bot in same spot, food is removed
            if first_pos and second_pos:
                food_list.remove(food_loc)
                
# This function runs your bots on a grid world
# from A4 although modified to incorporate food
def play_board(bots, n_iter=25, grid_size=5, sleep_time=0.3):
    """Run a bot across a board.
    
    Parameters
    ----------
    bots : Bot() type or list of Bot() type
        One or more bots to be be played on the board
    n_iter : int, optional
        Number of turns to play on the board. default = 25
    grid_size : int, optional
        Board size. default = 5
    sleep_time : float, optional
        Amount of time to pause between turns. default = 0.3.
    """
    
    food_icon = chr(1160)
    counter = grid_size * 4
    food_list = []
    # finds positions for food                                                 
    while counter is not 0:
        food_list.append([random.randrange(grid_size),
                          random.randrange(grid_size)])
        counter -= 1
    
    # If input is a single bot, put it in a list so that procedures work
    if not isinstance(bots, list):
        bots = [bots]
    
    # Update each bot to know about the grid_size they are on
    for bot in bots:
        bot.grid_size = grid_size

    for it in range(n_iter):

        # Create the grid
        grid_list = [['.'] * grid_size for ncols in range(grid_size)]
        
        # bots will eat food if in same location
        eat(bots, food_list)
        
        # Add bot(s) to the grid
        for bot in bots:
            grid_list[bot.position[0]][bot.position[1]] = bot.character    
                         
        # Add food to the grid
        for food_loc in food_list:
            grid_list[food_loc[0]][food_loc[1]] = food_icon

        
        # Clear the previous iteration, print the new grid, and wait
        clear_output(True)
        print('\n'.join([' '.join(lst) for lst in grid_list]))
        sleep(sleep_time)

        # Update bot position(s) for next turn
        for bot in bots:
            bot.move()   

# from A4            
class Bot():
    """ Base class for the all of the bots.
    
    Attributes
    ----------
    character : int
        The Unicode for what the bot will look like.
    position : list of int
        The position of the bot in the grid.
    moves : list of list of int
        The possible moves for the bot.
    grid_size : int
        The size of the grid that the bot is in.
    """
    
    def __init__(self, character = 8982):
        self.character = chr(character)
        self.position = [0,0]
        self.moves = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        self.grid_size = None

# from A4        
class WanderBot(Bot):
    """ Bot that travels in a random pattern.
    
    Attributes
    ----------
    character : int
        The Unicode for what the bot will look like.
    position : list of int
        The position of the bot in the grid.
    moves : list of list of int
        The possible moves for the bot.
    grid_size : int
        The size of the grid that the bot is in.
    """    
    
    def __init__(self, character = 8982):
        super().__init__(character)
        
    def wander(self):
        """ Randomly chooses the next valid move.

        Returns
        -------
        new_pos : list of int
            The new position of the bot.
        """
    
        has_new_pos = False
        while not has_new_pos:
            move = random.choice(self.moves)
            new_pos = add_lists(move, self.position)
            has_new_pos = check_bounds(new_pos, self.grid_size)
        return new_pos
    
    def move(self):
        """ Randomly chooses the next valid move.
        """
    
        self.position = self.wander()

# from A4        
class ExploreBot(Bot):
    """ Bot that biased to travel in a single direction rather than randomly.
    
    Attributes
    ----------
    character : int
        The Unicode for what the bot will look like.
    position : list of int
        The position of the bot in the grid.
    moves : list of list of int
        The possible moves for the bot.
    grid_size : int
        The size of the grid that the bot is in.
    move_prob : float
        The probability that the bot will continue in the same direction.
    last_move : list of int
        The previous move of the bot.
    """     
    
    def __init__ (self, character = 8982, move_prob = 0.75):
        
        super().__init__(character)
        
        self.move_prob = move_prob
        self.last_move = None
        
    def biased_choice(self):
        """ Randomly chooses the next valid move.

        Returns
        -------
        move : list of int
            The next move of the bot.
        """
        
        move = None
        # checks if this is the first move
        if self.last_move is not None:
            # checks whether to keep moving in the same direction
            if random.random() < self.move_prob:
                move = self.last_move
        # chooses a random move
        if move is None:
            move = random.choice(self.moves)
        return move
    
    def explore(self):
        """ Adds move, chosen from biased_choice, to current position
            to get new position.
    
        Returns
        -------
        new_pos : list of int
            The new position of the bot.
        """
        
        has_new_pos = False
        while not has_new_pos:
            move = self.biased_choice()
            new_pos = add_lists(move, self.position)
            has_new_pos = check_bounds(new_pos, self.grid_size)
        return new_pos
    
    def move(self):
        """ Calls explore to chooses the next valid move.
        """
        
        self.position = self.explore()

        
class FollowBot(WanderBot):
    """ Bot that follows other bots.
    
    Attributes
    ----------
    character : int
        The Unicode for what the bot will look like.
    position : list of int
        The position of the bot in the grid.
    moves : list of list of int
        The possible moves for the bot.
    grid_size : int
        The size of the grid that the bot is in.
    """     
    
    def __init__(self, character = 8982):
        super().__init__(character)
        
    def follow(self):
        """ If there's a bot nearby, it will follow it.
    
        Returns
        -------
        item/self.position : list of int
            If a bot is found, will move towards it.
            Otherwise returns current position.
        """
        
        # create list to add with moves
        pos_list = [self.position, self.position, self.position, self.position]
        # list of surrounding indices
        moveset = add_lists(self.moves, pos_list)
        
        # checks if there is bot nearby
        for item in moveset:
            if type(item) is Bot:
                return item
            
        # if no bot found, returns original position
        return self.position
    
    def move(self):
        """ If a bot is found, moves towards it.
            Otherwise moves randomly.
        """
        
        # checks for bots nearby
        next_move = self.follow()
        
        # finds a random move if no bot
        if next_move is self.position:
            self.position = self.wander()
        else:
            self.position = next_move