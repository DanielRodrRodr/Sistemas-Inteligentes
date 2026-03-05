from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

class SeekTarget(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):

        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]

        player_x = perception[AgentConsts.PLAYER_X]
        player_y = perception[AgentConsts.PLAYER_Y]

        base_x = perception[AgentConsts.COMMAND_CENTER_X]
        base_y = perception[AgentConsts.COMMAND_CENTER_Y]

        up = perception[AgentConsts.NEIGHBORHOOD_UP]
        down = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        left = perception[AgentConsts.NEIGHBORHOOD_LEFT]
        right = perception[AgentConsts.NEIGHBORHOOD_RIGHT]

        can_fire = perception[AgentConsts.CAN_FIRE]

        # Elegir objetivo
        if player_x >= 0:
            target_x = player_x
            target_y = player_y
        else:
            target_x = base_x
            target_y = base_y

        # Bajar
        if agent_y < target_y:

            if down == AgentConsts.NOTHING:
                return AgentConsts.MOVE_DOWN, False

            if down == AgentConsts.BRICK and can_fire:
                return AgentConsts.NO_MOVE, True

        # Subir
        if agent_y > target_y:

            if up == AgentConsts.NOTHING:
                return AgentConsts.MOVE_UP, False

            if up == AgentConsts.BRICK and can_fire:
                return AgentConsts.NO_MOVE, True

        # Derecha
        if agent_x < target_x:

            if right == AgentConsts.NOTHING:
                return AgentConsts.MOVE_RIGHT, False

            if right == AgentConsts.BRICK and can_fire:
                return AgentConsts.NO_MOVE, True

        # Izquierda
        if agent_x > target_x:

            if left == AgentConsts.NOTHING:
                return AgentConsts.MOVE_LEFT, False

            if left == AgentConsts.BRICK and can_fire:
                return AgentConsts.NO_MOVE, True

        # Si todo falla, moverse aleatoriamente
        moves = []

        if up == AgentConsts.NOTHING:
            moves.append(AgentConsts.MOVE_UP)

        if down == AgentConsts.NOTHING:
            moves.append(AgentConsts.MOVE_DOWN)

        if left == AgentConsts.NOTHING:
            moves.append(AgentConsts.MOVE_LEFT)

        if right == AgentConsts.NOTHING:
            moves.append(AgentConsts.MOVE_RIGHT)

        if len(moves) > 0:
            return random.choice(moves), False

        return AgentConsts.NO_MOVE, False


    def Transit(self, perception, map):

        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]

        player_x = perception[AgentConsts.PLAYER_X]
        player_y = perception[AgentConsts.PLAYER_Y]

        base_x = perception[AgentConsts.COMMAND_CENTER_X]
        base_y = perception[AgentConsts.COMMAND_CENTER_Y]

        # Atacar jugador
        if player_x >= 0 and (agent_x == player_x or agent_y == player_y):
            return "AttackPlayer"

        # Atacar base
        if agent_x == base_x or agent_y == base_y:
            return "AttackBase"

        return self.id