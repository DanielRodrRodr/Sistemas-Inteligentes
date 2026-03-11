from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random


class GoToCommandCenter(State):

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
        
        target_x, target_y = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]
        
        diff_x = target_x - agent_x
        diff_y = target_y - agent_y

        if abs(diff_x) > abs(diff_y):
            dir_prim = AgentConsts.MOVE_RIGHT if diff_x > 0 else AgentConsts.MOVE_LEFT
            dir_sec = AgentConsts.MOVE_UP if diff_y > 0 else AgentConsts.MOVE_DOWN 
        else:
            dir_prim = AgentConsts.MOVE_UP if diff_y > 0 else AgentConsts.MOVE_DOWN
            dir_sec = AgentConsts.MOVE_RIGHT if diff_x > 0 else AgentConsts.MOVE_LEFT

        obstaculos_destruibles = [AgentConsts.BRICK, AgentConsts.SEMI_BREKABLE, AgentConsts.SEMI_UNBREKABLE]
        obstaculos_duros = [AgentConsts.UNBREAKABLE, AgentConsts.OTHER]

        for direccion in [dir_prim, dir_sec]:
            casilla = self.obtener_casilla(direccion, perception)
            
            if casilla in obstaculos_destruibles:
                if can_fire:
                    return direccion, True
            elif casilla not in obstaculos_duros:
                return direccion, False

        movimientos = [AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_LEFT, AgentConsts.MOVE_RIGHT]
        random.shuffle(movimientos) 
        
        for escape in movimientos:
            casilla_escape = self.obtener_casilla(escape, perception)
            
            if casilla_escape in obstaculos_destruibles:
                if can_fire:
                    return escape, True
            elif casilla_escape not in obstaculos_duros:
                return escape, False

        return AgentConsts.NO_MOVE, False
    
    def Transit(self, perception, map):
        return "SeekTarget"