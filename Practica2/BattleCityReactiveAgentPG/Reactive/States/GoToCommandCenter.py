from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random


class GoToCommandCenter(State):

    def __init__(self, id):
        super().__init__(id)

    def esta_bloqueado(self, direccion, perception):
        obstaculos = [AgentConsts.UNBREAKABLE, AgentConsts.BRICK, AgentConsts.SEMI_UNBREKABLE, AgentConsts.SEMI_BREKABLE]
        
        if direccion == AgentConsts.MOVE_UP:
            return perception[AgentConsts.NEIGHBORHOOD_UP] in obstaculos
        elif direccion == AgentConsts.MOVE_DOWN:
            return perception[AgentConsts.NEIGHBORHOOD_DOWN] in obstaculos
        elif direccion == AgentConsts.MOVE_RIGHT:
            return perception[AgentConsts.NEIGHBORHOOD_RIGHT] in obstaculos
        elif direccion == AgentConsts.MOVE_LEFT:
            return perception[AgentConsts.NEIGHBORHOOD_LEFT] in obstaculos
        return False

    def Update(self, perception, map, agent):
        agent_x, agent_y = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        
        # Determinar objetivo
        if perception[AgentConsts.PLAYER_X] >= 0:
            target_x, target_y = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        else:
            target_x, target_y = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]

        diff_x = target_x - agent_x
        diff_y = target_y - agent_y

        if abs(diff_x) > abs(diff_y):
            dir_primaria = AgentConsts.MOVE_RIGHT if diff_x > 0 else AgentConsts.MOVE_LEFT
            dir_secundaria = AgentConsts.MOVE_UP if diff_y > 0 else AgentConsts.MOVE_DOWN 
        else:
            dir_primaria = AgentConsts.MOVE_UP if diff_y > 0 else AgentConsts.MOVE_DOWN
            dir_secundaria = AgentConsts.MOVE_RIGHT if diff_x > 0 else AgentConsts.MOVE_LEFT

        if not self.esta_bloqueado(dir_primaria, perception):
            return dir_primaria, False
        elif not self.esta_bloqueado(dir_secundaria, perception):
            return dir_secundaria, False
        else:
            for direccion_escape in [AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_LEFT, AgentConsts.MOVE_RIGHT]:
                if not self.esta_bloqueado(direccion_escape, perception):
                    return direccion_escape, False
            
        return AgentConsts.NO_MOVE, False
    def Transit(self, perception, map):
        return "SeekTarget"