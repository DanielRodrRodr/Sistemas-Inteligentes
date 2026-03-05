from StateMachine.State import State
from States.AgentConsts import AgentConsts


class AttackPlayer(State):

    def __init__(self, id):
        super().__init__(id)
        #self.Reset()

    def Update(self, perception, map, agent):

        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]

        player_x = perception[AgentConsts.PLAYER_X]
        player_y = perception[AgentConsts.PLAYER_Y]

        can_fire = perception[AgentConsts.CAN_FIRE]

        # Alineado vertical
        if agent_x == player_x:
            if player_y < agent_y:
                return AgentConsts.MOVE_UP, can_fire
            else:
                return AgentConsts.MOVE_DOWN, can_fire

        # Alineado horizontal
        if agent_y == player_y:
            if player_x < agent_x:
                return AgentConsts.MOVE_LEFT, can_fire
            else:
                return AgentConsts.MOVE_RIGHT, can_fire

        return AgentConsts.NO_MOVE, False


    def Transit(self, perception, map):

        player_x = perception[AgentConsts.PLAYER_X]
        player_y = perception[AgentConsts.PLAYER_Y]

        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]

        # Si jugador muerto → volver
        if player_x < 0:
            return "GoToCommandCenter"

        # Si ya no alineado → volver
        if agent_x != player_x and agent_y != player_y:
            return "GoToCommandCenter"

        return self.id