from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

class SeekTarget(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):
        return AgentConsts.NO_MOVE, False
    
    def Transit(self, perception, map):
        
    
        vision = [perception[AgentConsts.NEIGHBORHOOD_UP], perception[AgentConsts.NEIGHBORHOOD_DOWN],
                  perception[AgentConsts.NEIGHBORHOOD_LEFT], perception[AgentConsts.NEIGHBORHOOD_RIGHT]]
        
        if AgentConsts.SHELL in vision:
            return "DodgeBullet"
        
        if perception[AgentConsts.PLAYER_X] < 0 or perception[AgentConsts.COMMAND_CENTER_X] < 0:
            return "GoToExit"

        if AgentConsts.PLAYER in vision or AgentConsts.COMMAND_CENTER in vision:
            return "OrientateAndShoot"
            
        return "GoToCommandCenter"