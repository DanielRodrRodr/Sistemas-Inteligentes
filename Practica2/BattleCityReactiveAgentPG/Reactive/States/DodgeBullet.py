from StateMachine.State import State
from States.AgentConsts import AgentConsts

class DodgeBullet(State):
    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):
        if perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.SHELL:
            if perception[AgentConsts.NEIGHBORHOOD_RIGHT] != AgentConsts.UNBREAKABLE: 
                return AgentConsts.MOVE_RIGHT, False
            return AgentConsts.MOVE_LEFT, False
        
        if perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.SHELL:
            if perception[AgentConsts.NEIGHBORHOOD_UP] != AgentConsts.UNBREAKABLE: 
                return AgentConsts.MOVE_UP, False
            return AgentConsts.MOVE_DOWN, False
            
        return AgentConsts.NO_MOVE, False

    def Transit(self, perception, map):
        vision = [perception[AgentConsts.NEIGHBORHOOD_UP], perception[AgentConsts.NEIGHBORHOOD_DOWN],
                  perception[AgentConsts.NEIGHBORHOOD_LEFT], perception[AgentConsts.NEIGHBORHOOD_RIGHT]]

        if AgentConsts.SHELL in vision:
            return "DodgeBullet"
        return "SeekTarget"