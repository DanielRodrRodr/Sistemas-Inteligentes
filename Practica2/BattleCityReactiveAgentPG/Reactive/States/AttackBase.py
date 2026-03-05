from StateMachine.State import State
from States.AgentConsts import AgentConsts


class AttackBase(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):

        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]

        base_x = perception[AgentConsts.COMMAND_CENTER_X]
        base_y = perception[AgentConsts.COMMAND_CENTER_Y]

        can_fire = perception[AgentConsts.CAN_FIRE]

        # Alineado vertical
        if agent_x == base_x:
            if base_y < agent_y:
                return AgentConsts.MOVE_UP, can_fire
            else:
                return AgentConsts.MOVE_DOWN, can_fire

        # Alineado horizontal
        if agent_y == base_y:
            if base_x < agent_x:
                return AgentConsts.MOVE_LEFT, can_fire
            else:
                return AgentConsts.MOVE_RIGHT, can_fire

        return AgentConsts.NO_MOVE, False


    def Transit(self, perception, map):

        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]

        base_x = perception[AgentConsts.COMMAND_CENTER_X]
        base_y = perception[AgentConsts.COMMAND_CENTER_Y]

        # Si ya no alineado → volver
        if agent_x != base_x and agent_y != base_y:
            return "GoToCommandCenter"

        return self.id