from StateMachine.State import State
from States.AgentConsts import AgentConsts

class OrientateAndShoot(State):
    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):
        can_fire = perception[AgentConsts.CAN_FIRE] > 0

        up = perception[AgentConsts.NEIGHBORHOOD_UP]
        down = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        left = perception[AgentConsts.NEIGHBORHOOD_LEFT]
        right = perception[AgentConsts.NEIGHBORHOOD_RIGHT]

        if can_fire:
            if up == AgentConsts.SHELL:
                return AgentConsts.MOVE_UP, True
            if down == AgentConsts.SHELL:
                return AgentConsts.MOVE_DOWN, True
            if left == AgentConsts.SHELL:
                return AgentConsts.MOVE_LEFT, True
            if right == AgentConsts.SHELL:
                return AgentConsts.MOVE_RIGHT, True
            if up == AgentConsts.PLAYER:
                return AgentConsts.MOVE_UP, True
            if down == AgentConsts.PLAYER:
                return AgentConsts.MOVE_DOWN, True
            if left == AgentConsts.PLAYER:
                return AgentConsts.MOVE_LEFT, True
            if right == AgentConsts.PLAYER:
                return AgentConsts.MOVE_RIGHT, True
            if up == AgentConsts.COMMAND_CENTER:
                return AgentConsts.MOVE_UP, True
            if down == AgentConsts.COMMAND_CENTER:
                return AgentConsts.MOVE_DOWN, True
            if left == AgentConsts.COMMAND_CENTER:
                return AgentConsts.MOVE_LEFT, True
            if right == AgentConsts.COMMAND_CENTER:
                return AgentConsts.MOVE_RIGHT, True

        return AgentConsts.NO_MOVE, 0

    def Transit(self, perception, map):
        vision = [perception[AgentConsts.NEIGHBORHOOD_UP], perception[AgentConsts.NEIGHBORHOOD_DOWN],
                  perception[AgentConsts.NEIGHBORHOOD_LEFT], perception[AgentConsts.NEIGHBORHOOD_RIGHT]]
        
        if (AgentConsts.PLAYER in vision or AgentConsts.COMMAND_CENTER in vision) and perception[AgentConsts.CAN_FIRE] > 0:
            return "OrientateAndShoot"

        return "ExecutePlan"