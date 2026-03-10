from StateMachine.State import State
from States.AgentConsts import AgentConsts

class DodgeBullet(State):
    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):

        can_fire = perception[AgentConsts.CAN_FIRE] > 0

        up = perception[AgentConsts.NEIGHBORHOOD_UP]
        down = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        left = perception[AgentConsts.NEIGHBORHOOD_LEFT]
        right = perception[AgentConsts.NEIGHBORHOOD_RIGHT]

        dist_up = perception[AgentConsts.NEIGHBORHOOD_DIST_UP]
        dist_down = perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN]
        dist_left = perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT]
        dist_right = perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT]

        # Detectar la bala antes de que llegue al agente y disparar
        danger_dist = 3
        if up == AgentConsts.SHELL and dist_up <= danger_dist:
            if can_fire:
                return AgentConsts.MOVE_UP, True
            return AgentConsts.MOVE_RIGHT, False

        if down == AgentConsts.SHELL and dist_down <= danger_dist:
            if can_fire:
                return AgentConsts.MOVE_DOWN, True
            return AgentConsts.MOVE_RIGHT, False

        if left == AgentConsts.SHELL and dist_left <= danger_dist:
            if can_fire:
                return AgentConsts.MOVE_LEFT, True
            return AgentConsts.MOVE_UP, False

        if right == AgentConsts.SHELL and dist_right <= danger_dist:
            if can_fire:
                return AgentConsts.MOVE_RIGHT, True
            return AgentConsts.MOVE_UP, False


        # Bala vertical -> esquivar lateralmente
        if up == AgentConsts.SHELL or down == AgentConsts.SHELL:
            if right != AgentConsts.UNBREAKABLE:
                return AgentConsts.MOVE_RIGHT, False
            if left != AgentConsts.UNBREAKABLE:
                return AgentConsts.MOVE_LEFT, False

        # Bala horizontal -> esquivar verticalmente
        if right == AgentConsts.SHELL or left == AgentConsts.SHELL:
            if up != AgentConsts.UNBREAKABLE:
                return AgentConsts.MOVE_UP, False
            if down != AgentConsts.UNBREAKABLE:
                return AgentConsts.MOVE_DOWN, False

        return AgentConsts.NO_MOVE, False

    def Transit(self, perception, map):
        vision = [perception[AgentConsts.NEIGHBORHOOD_UP], perception[AgentConsts.NEIGHBORHOOD_DOWN],
                  perception[AgentConsts.NEIGHBORHOOD_LEFT], perception[AgentConsts.NEIGHBORHOOD_RIGHT]]

        if AgentConsts.SHELL in vision:
            return "DodgeBullet"
        
        return "SeekTarget"