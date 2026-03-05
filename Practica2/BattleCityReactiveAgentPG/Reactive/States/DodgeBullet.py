from StateMachine.State import State
from States.AgentConsts import AgentConsts


class DodgeBullet(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):

        can_fire = perception[AgentConsts.CAN_FIRE]

        # Disparar si puede
        if can_fire:
            return AgentConsts.NO_MOVE, True

        # Esquivar lateralmente
        return AgentConsts.MOVE_LEFT, False


    def Transit(self, perception, map):

        # Si ya no hay bala cerca
        if perception[AgentConsts.NEIGHBORHOOD_UP] != AgentConsts.SHELL and \
           perception[AgentConsts.NEIGHBORHOOD_DOWN] != AgentConsts.SHELL and \
           perception[AgentConsts.NEIGHBORHOOD_LEFT] != AgentConsts.SHELL and \
           perception[AgentConsts.NEIGHBORHOOD_RIGHT] != AgentConsts.SHELL:
            return "SeekTarget"

        return self.id