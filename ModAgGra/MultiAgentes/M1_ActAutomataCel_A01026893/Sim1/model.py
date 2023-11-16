import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation 

from agent import TreeCell

class ForestFire(Model):

    def __init__(self, height=50, width=50, density=0.5):
        """
        Create a new model.
        
        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """

        # Set up model objects
        # SimultaneousActivation is a Mesa object that runs all the agents at the same time. 
        # This is necessary in this model because the next state of each cell depends on the current state of all its neighbors above -- before they've changed.
        # This activation method requires that all the agents have a step() and an advance() method. 
        # The step() method computes the next state of the agent, and the advance() method sets the state to the new computed state.
        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(height, width, torus=False)

        # A datacollector is a Mesa object for collecting data about the model.
        # We'll use it to count the number of trees in each condition each step.
        self.datacollector = DataCollector(
            {
                "Alive": lambda m: self.count_type(m, "Alive"),
                "Dead": lambda m: self.count_type(m, "Dead"),
            }
        )

        # Place a tree in each cell with Prob = density
        # coord_iter is an iterator that returns positions as well as cell contents.
        for contents, (x, y) in self.grid.coord_iter():
            # We are initializing the first agents as "Alive" set in the first row of the grid with some conditionals.
            if self.random.random() < density and y == 49:
                new_tree = TreeCell((x, y), self)
                
                new_tree.condition = "Alive"
            else:
            # We are initializing the rest of the rows as "Dead" with some conditionals
                new_tree = TreeCell((x, y), self)
                
                new_tree.condition = "Dead"

            self.grid.place_agent(new_tree, (x, y))
            self.schedule.add(new_tree)

        self.ownCount = 0 # Initializing our own counter so the simulation stops.
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        self.ownCount += 1
        print(self.ownCount)
        # Halt if the counter is 49
        if self.ownCount == 49:
           self.running = False


    # staticmethod is a Python decorator that makes a method callable without an instance.
    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count