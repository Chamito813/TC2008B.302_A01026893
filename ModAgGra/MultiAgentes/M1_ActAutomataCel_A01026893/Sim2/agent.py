from mesa import Agent

class TreeCell(Agent):
    """
        A tree cell.
        
        Attributes:
            x, y: Grid coordinates
            condition: Can be "Alive", or "Dead"
            unique_id: (x,y) tuple.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.

        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Alive"
        self._next_condition = None

    def step(self):
        """
        If the tree's Dead, change the status of it following the conditions given of its neighbors.
        """
        if self.condition == "Dead":
            neighbors = []
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if self.pos[1] == 49:
                    if neighbor.pos[1] == 0:
                        neighbors.append(neighbor)    
                else: 
                    if neighbor.pos[1] == self.pos[1] + 1:
                        neighbors.append(neighbor)

            if((neighbors[0].condition == "Dead" and neighbors[1].condition == "Dead" and neighbors[2].condition == "Alive") or 
               (neighbors[0].condition == "Dead" and neighbors[1].condition == "Alive" and neighbors[2].condition == "Alive")or
               (neighbors[0].condition == "Alive" and neighbors[1].condition == "Dead" and neighbors[2].condition == "Dead")or
               (neighbors[0].condition == "Alive" and neighbors[1].condition == "Alive" and neighbors[2].condition == "Dead")):
                self._next_condition = "Alive"
        """
        If the tree's Alive, change the status of it following the conditions given of its neighbors.
        """
        if self.condition == "Alive":
            neighbors = []
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if self.pos[1] == 49:
                    if neighbor.pos[1] == 0:
                        neighbors.append(neighbor)
                else: 
                    if neighbor.pos[1] == self.pos[1] + 1:
                        neighbors.append(neighbor)

            if((neighbors[0].condition == "Dead" and neighbors[1].condition == "Dead" and neighbors[2].condition == "Dead") or 
               (neighbors[0].condition == "Dead" and neighbors[1].condition == "Alive" and neighbors[2].condition == "Dead")or
               (neighbors[0].condition == "Alive" and neighbors[1].condition == "Dead" and neighbors[2].condition == "Alive")or
               (neighbors[0].condition == "Alive" and neighbors[1].condition == "Alive" and neighbors[2].condition == "Alive")):
                self._next_condition = "Dead"
                

    
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition