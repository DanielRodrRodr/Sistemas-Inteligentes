from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random


class GoToExit(State):

    def __init__(self, id):
        super().__init__(id)

    def obtener_casilla(self, direccion, perception):
        if direccion == AgentConsts.MOVE_UP: return perception[AgentConsts.NEIGHBORHOOD_UP]
        if direccion == AgentConsts.MOVE_DOWN: return perception[AgentConsts.NEIGHBORHOOD_DOWN]
        if direccion == AgentConsts.MOVE_RIGHT: return perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        if direccion == AgentConsts.MOVE_LEFT: return perception[AgentConsts.NEIGHBORHOOD_LEFT]
        return AgentConsts.UNBREAKABLE 

    def Update(self, perception, map, agent):

        can_fire = perception[AgentConsts.CAN_FIRE] > 0
        agent_x, agent_y = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        
        target_x, target_y = perception[AgentConsts.EXIT_X], perception[AgentConsts.EXIT_Y]
        
        diff_x = target_x - agent_x
        diff_y = target_y - agent_y

        if abs(diff_x) > abs(diff_y):
            dir_prim = AgentConsts.MOVE_RIGHT if diff_x > 0 else AgentConsts.MOVE_LEFT
            dir_sec = AgentConsts.MOVE_UP if diff_y > 0 else AgentConsts.MOVE_DOWN 
        else:
            dir_prim = AgentConsts.MOVE_UP if diff_y > 0 else AgentConsts.MOVE_DOWN
            dir_sec = AgentConsts.MOVE_RIGHT if diff_x > 0 else AgentConsts.MOVE_LEFT

        obstaculos_destruibles = [AgentConsts.BRICK, AgentConsts.SEMI_BREKABLE]
        obstaculos_duros = [AgentConsts.UNBREAKABLE, AgentConsts.OTHER]

        casilla_prim = self.obtener_casilla(dir_prim, perception)
        casilla_sec = self.obtener_casilla(dir_sec, perception)

        if casilla_prim in obstaculos_destruibles:
            return dir_prim, (perception[AgentConsts.CAN_FIRE] > 0)
        elif casilla_prim not in obstaculos_duros:
            return dir_prim, False
        
        if casilla_sec in obstaculos_destruibles:
            return dir_sec, (perception[AgentConsts.CAN_FIRE] > 0)
        elif casilla_sec not in obstaculos_duros:
            return dir_sec, False

        movimientos = [AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_LEFT, AgentConsts.MOVE_RIGHT]
        random.shuffle(movimientos) 
        
        for escape in movimientos:
            casilla_escape = self.obtener_casilla(escape, perception)
            
            if casilla_escape in obstaculos_destruibles:
                if can_fire:
                    return AgentConsts.NO_MOVE, True
            elif casilla_escape not in obstaculos_duros:
                return escape, False

        return AgentConsts.NO_MOVE, False


    def Transit(self, perception, map):

        vision = [perception[AgentConsts.NEIGHBORHOOD_UP], perception[AgentConsts.NEIGHBORHOOD_DOWN],
                  perception[AgentConsts.NEIGHBORHOOD_LEFT], perception[AgentConsts.NEIGHBORHOOD_RIGHT]]
        danger_dist = 3
        if perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= danger_dist:
            return "DodgeBullet"
        if perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= danger_dist:
            return "DodgeBullet"
        if perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= danger_dist:
            return "DodgeBullet"
        if perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= danger_dist:
            return "DodgeBullet"
        return "GoToExit"