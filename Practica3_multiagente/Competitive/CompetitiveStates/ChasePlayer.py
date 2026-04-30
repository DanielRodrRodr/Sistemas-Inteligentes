from StateMachine.State import State
from CompetitiveStates.AgentConsts import AgentConsts

class ChasePlayer(State):
    def __init__(self, id):
        super().__init__(id)

    def is_free(self, direction, perception):
        if direction == AgentConsts.MOVE_UP:
            return perception[AgentConsts.NEIGHBORHOOD_UP] not in [AgentConsts.UNBREAKABLE, AgentConsts.BRICK]
        if direction == AgentConsts.MOVE_DOWN:
            return perception[AgentConsts.NEIGHBORHOOD_DOWN] not in [AgentConsts.UNBREAKABLE, AgentConsts.BRICK]
        if direction == AgentConsts.MOVE_LEFT:
            return perception[AgentConsts.NEIGHBORHOOD_LEFT] not in [AgentConsts.UNBREAKABLE, AgentConsts.BRICK]
        if direction == AgentConsts.MOVE_RIGHT:
            return perception[AgentConsts.NEIGHBORHOOD_RIGHT] not in [AgentConsts.UNBREAKABLE, AgentConsts.BRICK]
        return False

    def Update(self, perception, map, agent):
        ax = perception[AgentConsts.AGENT_X]
        ay = perception[AgentConsts.AGENT_Y]
        px = perception[AgentConsts.PLAYER_X]
        py = perception[AgentConsts.PLAYER_Y]

        # Si no se ve el jugador, no hacer nada
        if px == -1:
            return AgentConsts.NO_MOVE, False

        # Mover hacia el jugador
        dx = px - ax
        dy = py - ay
        dist = abs(dx) + abs(dy)

        # Si ya son adyacentes, orientarse y disparar sin avanzar encima
        if dist <= 1:
            if abs(dx) >= abs(dy):
                face = AgentConsts.MOVE_RIGHT if dx > 0 else AgentConsts.MOVE_LEFT
            else:
                face = AgentConsts.MOVE_DOWN if dy > 0 else AgentConsts.MOVE_UP
            return face, perception[AgentConsts.CAN_FIRE] > 0
        
        if abs(dx) >= abs(dy):
            if dx > 0 and self.is_free(AgentConsts.MOVE_RIGHT, perception):
                return AgentConsts.MOVE_RIGHT, False
            if dx < 0 and self.is_free(AgentConsts.MOVE_LEFT, perception):
                return AgentConsts.MOVE_LEFT, False
            # Si el eje X está bloqueado, intentar eje Y
            if dy > 0 and self.is_free(AgentConsts.MOVE_DOWN, perception):
                return AgentConsts.MOVE_DOWN, False
            if dy < 0 and self.is_free(AgentConsts.MOVE_UP, perception):
                return AgentConsts.MOVE_UP, False
        else:
            if dy > 0 and self.is_free(AgentConsts.MOVE_DOWN, perception):
                return AgentConsts.MOVE_DOWN, False
            if dy < 0 and self.is_free(AgentConsts.MOVE_UP, perception):
                return AgentConsts.MOVE_UP, False
            # Si el eje Y está bloqueado, intentar eje X
            if dx > 0 and self.is_free(AgentConsts.MOVE_RIGHT, perception):
                return AgentConsts.MOVE_RIGHT, False
            if dx < 0 and self.is_free(AgentConsts.MOVE_LEFT, perception):
                return AgentConsts.MOVE_LEFT, False
 
        return AgentConsts.NO_MOVE, False

    def Transit(self, perception, map):

        vision = [perception[AgentConsts.NEIGHBORHOOD_UP], perception[AgentConsts.NEIGHBORHOOD_DOWN],
                  perception[AgentConsts.NEIGHBORHOOD_LEFT], perception[AgentConsts.NEIGHBORHOOD_RIGHT]]

        if (perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.SHELL or
            perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.SHELL or
            perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.SHELL or
            perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.SHELL):
            return "DodgeBullet"

        if perception[AgentConsts.HEALTH] <= 1 and perception[AgentConsts.LIFE_X] != -1:
            return "Retreat"
 
        px = perception[AgentConsts.PLAYER_X]
        if px != -1:
            dist = abs(perception[AgentConsts.AGENT_X] - px) + abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y])
            
        if (AgentConsts.PLAYER in vision) and perception[AgentConsts.CAN_FIRE] > 0:
            return "OrientateAndShoot"

        if 6 <= dist <= 10:
                return "Ambush"
 
        if px != -1:
            return "ChasePlayer"

        return "ExecutePlan"