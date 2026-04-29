from StateMachine.State import State
from CompetitiveStates.AgentConsts import AgentConsts

class DodgeBullet(State):
    def __init__(self, id):
        super().__init__(id)

    def es_casilla_segura(self, direccion, perception):
        obstaculos = [AgentConsts.UNBREAKABLE, AgentConsts.OTHER, 
                      AgentConsts.BRICK, AgentConsts.SEMI_BREKABLE, AgentConsts.SEMI_UNBREKABLE]
        
        if direccion == AgentConsts.MOVE_UP: casilla = perception[AgentConsts.NEIGHBORHOOD_UP]
        elif direccion == AgentConsts.MOVE_DOWN: casilla = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        elif direccion == AgentConsts.MOVE_RIGHT: casilla = perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        elif direccion == AgentConsts.MOVE_LEFT: casilla = perception[AgentConsts.NEIGHBORHOOD_LEFT]
        else: casilla = AgentConsts.UNBREAKABLE

        return casilla not in obstaculos

    def Update(self, perception, map, agent):
        danger_dist = 3
        
        up = perception[AgentConsts.NEIGHBORHOOD_UP]
        down = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        left = perception[AgentConsts.NEIGHBORHOOD_LEFT]
        right = perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        
        eje_bala = None
        if up == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= danger_dist:
            eje_bala = "VERTICAL"
        elif down == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= danger_dist:
            eje_bala = "VERTICAL"
        elif left == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= danger_dist:
            eje_bala = "HORIZONTAL"
        elif right == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= danger_dist:
            eje_bala = "HORIZONTAL"

        if eje_bala == "VERTICAL":
            if self.es_casilla_segura(AgentConsts.MOVE_RIGHT, perception):
                return AgentConsts.MOVE_RIGHT, False
            if self.es_casilla_segura(AgentConsts.MOVE_LEFT, perception):
                return AgentConsts.MOVE_LEFT, False
                
        elif eje_bala == "HORIZONTAL":
            if self.es_casilla_segura(AgentConsts.MOVE_UP, perception):
                return AgentConsts.MOVE_UP, False
            if self.es_casilla_segura(AgentConsts.MOVE_DOWN, perception):
                return AgentConsts.MOVE_DOWN, False

        return AgentConsts.NO_MOVE, False

    def Transit(self, perception, map):
        vision = [perception[AgentConsts.NEIGHBORHOOD_UP], perception[AgentConsts.NEIGHBORHOOD_DOWN],
                  perception[AgentConsts.NEIGHBORHOOD_LEFT], perception[AgentConsts.NEIGHBORHOOD_RIGHT]]
        
        danger_dist = 3
        hay_peligro = False

        if perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= danger_dist:
            hay_peligro = True
        elif perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= danger_dist:
            hay_peligro = True
        elif perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= danger_dist:
            hay_peligro = True
        elif perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= danger_dist:
            hay_peligro = True

        if hay_peligro:
            if perception[AgentConsts.CAN_FIRE] > 0:
                return "OrientateAndShoot"
            return "DodgeBullet"
        
        if perception[AgentConsts.HEALTH] <= 1 and perception[AgentConsts.LIFE_X] != -1:
            return "Retreat"
 
        px = perception[AgentConsts.PLAYER_X]
        if px != -1:
            dist = abs(perception[AgentConsts.AGENT_X] - px) + abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y])
 
            if (AgentConsts.PLAYER in vision or AgentConsts.COMMAND_CENTER in vision) and perception[AgentConsts.CAN_FIRE] > 0:
                return "OrientateAndShoot"
 
            if 6 <= dist <= 10:
                return "Ambush"
 
            return "ChasePlayer"
    
        if (AgentConsts.PLAYER in vision or AgentConsts.COMMAND_CENTER in vision) and perception[AgentConsts.CAN_FIRE] > 0: return "OrientateAndShoot"
        
        return "ExecutePlan"