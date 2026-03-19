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
    
    def obtener_distancia(self, direccion, perception):
        if direccion == AgentConsts.MOVE_UP: return perception[AgentConsts.NEIGHBORHOOD_DIST_UP]
        if direccion == AgentConsts.MOVE_DOWN: return perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN]
        if direccion == AgentConsts.MOVE_RIGHT: return perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT]
        if direccion == AgentConsts.MOVE_LEFT: return perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT]
        return 100 

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

        obstaculos_destruibles = [AgentConsts.BRICK]
        obstaculos_duros = [AgentConsts.UNBREAKABLE]

        casilla_prim = self.obtener_casilla(dir_prim, perception)
        dist_prim = self.obtener_distancia(dir_prim, perception)

        if casilla_prim == AgentConsts.NOTHING:
            return dir_prim, False

        if dist_prim > 1:
            return dir_prim, False
        
        casilla_sec = self.obtener_casilla(dir_sec, perception)
        dist_sec = self.obtener_distancia(dir_sec, perception)

        if casilla_sec == AgentConsts.NOTHING and (diff_x > 1 and diff_y > 1):
            return dir_sec, False
        
        if dist_sec > 1 and (diff_x > 1 and diff_y > 1):
            return dir_sec, False


        for direccion in [dir_prim, dir_sec]:
            casilla = self.obtener_casilla(direccion, perception)
            dist = self.obtener_distancia(direccion, perception)
            
            if casilla == AgentConsts.EXIT:
                return direccion, False
            
            if casilla == AgentConsts.NOTHING or dist > 1 and (diff_x > 1 and diff_y > 1):
                return direccion, False
                
            if casilla in obstaculos_destruibles:
                if can_fire:
                    return direccion, True
                else:
                    return direccion, False
                    
            elif casilla not in obstaculos_duros and (diff_x > 1 and diff_y > 1):
                return direccion, False

        return AgentConsts.NO_MOVE, False


    def Transit(self, perception, map):
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