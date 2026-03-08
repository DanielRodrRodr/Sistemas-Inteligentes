from StateMachine.State import State
from States.AgentConsts import AgentConsts

class ShootingEvaluation(State):
    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):
        if perception[AgentConsts.CAN_FIRE] == 1:
            return AgentConsts.NO_MOVE, True
        return AgentConsts.NO_MOVE, False

    def Transit(self, perception, map):
        if perception[AgentConsts.CAN_FIRE] == 1:
            return "OrientateForShooting"
        return "SeekTarget"