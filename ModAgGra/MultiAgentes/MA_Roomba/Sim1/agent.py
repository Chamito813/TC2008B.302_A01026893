from mesa import Agent


class RoombaAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0
        self.visited_positions = [(1, 1)]  
        self.battery = 100
        self.charging = False 

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 
        
        neighbors = [(p, self.model.grid.get_cell_list_contents([p])) for p in possible_steps]

        # Filtra las posiciones donde hay suciedad
        dirt_positions = [p for p, contents in neighbors if any(isinstance(agent, DirtAgent) for agent in contents)]
        
        #print(dirt_positions)
        if self.battery > 20:
            if not dirt_positions:  # Si no hay suciedad, mueve aleatoriamente pero considerando aquellas posiciones que ya han sido visitadas
                free_spaces = [p for p in possible_steps if self.model.grid.is_cell_empty(p) and p not in self.visited_positions]
                if free_spaces:
                    next_move = self.random.choice(free_spaces)
                    self.model.grid.move_agent(self, next_move)
                    self.visited_positions.append(next_move)
                    print(self.visited_positions)
                    self.steps_taken += 1
                    self.battery -= 1
                    print(self.battery)
                else:
                    free_spaces = [p for p in possible_steps if self.model.grid.is_cell_empty(p)]
                    next_move = self.random.choice(free_spaces)
                    print(next_move)
                    self.model.grid.move_agent(self, next_move)
                    print(self.visited_positions)
                    self.steps_taken += 1
                    self.battery -= 1
                    print(self.battery)
                    
            else:  # Si hay suciedad, mueve hacia la primera posición de suciedad y límpiala
                next_move = dirt_positions[0]
                self.model.grid.move_agent(self, next_move)
                self.steps_taken += 1
                self.visited_positions.append(next_move)
                print(self.visited_positions)
                dirt_agent = self.model.grid.get_cell_list_contents([next_move])[0]
                self.model.grid.remove_agent(dirt_agent)
                self.battery -= 2
                print(self.battery)

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()

class VacantCellAgent(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)

    def step(self):
        pass

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  
    

class DirtAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class ChargingStationAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass