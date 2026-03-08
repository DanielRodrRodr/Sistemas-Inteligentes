from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

class Move(State):
    def __init__(self, id):
        super().__init__(id)

    # Ahora comprobamos qué hay exactamente en esa casilla
    def obtener_casilla(self, direccion, perception):
        if direccion == AgentConsts.MOVE_UP: return perception[AgentConsts.NEIGHBORHOOD_UP]
        if direccion == AgentConsts.MOVE_DOWN: return perception[AgentConsts.NEIGHBORHOOD_DOWN]
        if direccion == AgentConsts.MOVE_RIGHT: return perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        if direccion == AgentConsts.MOVE_LEFT: return perception[AgentConsts.NEIGHBORHOOD_LEFT]
        return AgentConsts.UNBREAKABLE # Por si acaso devuelve muro duro

    def Update(self, perception, map, agent):
        agent_x, agent_y = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        player_x, player_y = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        base_x, base_y = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]
        
        target_x = player_x if player_x >= 0 else base_x
        target_y = player_y if player_x >= 0 else base_y

        diff_x = target_x - agent_x
        diff_y = target_y - agent_y

        if abs(diff_x) > abs(diff_y):
            dir_prim = AgentConsts.MOVE_RIGHT if diff_x > 0 else AgentConsts.MOVE_LEFT
            dir_sec = AgentConsts.MOVE_UP if diff_y > 0 else AgentConsts.MOVE_DOWN 
        else:
            dir_prim = AgentConsts.MOVE_UP if diff_y > 0 else AgentConsts.MOVE_DOWN
            dir_sec = AgentConsts.MOVE_RIGHT if diff_x > 0 else AgentConsts.MOVE_LEFT

        obstaculos_destruibles = [AgentConsts.BRICK, AgentConsts.SEMI_BREKABLE, AgentConsts.SEMI_UNBREKABLE]
        obstaculos_duros = [AgentConsts.UNBREAKABLE, AgentConsts.OTHER] # Muros de acero o agua

        casilla_prim = self.obtener_casilla(dir_prim, perception)
        
        if casilla_prim in obstaculos_destruibles:
            return dir_prim, (perception[AgentConsts.CAN_FIRE] > 0)
        elif casilla_prim not in obstaculos_duros:
            return dir_prim, False

        casilla_sec = self.obtener_casilla(dir_sec, perception)
        
        if casilla_sec in obstaculos_destruibles:
            return dir_sec, (perception[AgentConsts.CAN_FIRE] > 0)
        elif casilla_sec not in obstaculos_duros:
            return dir_sec, False
        
        movimientos = [AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_LEFT, AgentConsts.MOVE_RIGHT]
        random.shuffle(movimientos) # Un poco de azar para que no se quede rebotando siempre igual
        
        for escape in movimientos:
            casilla_escape = self.obtener_casilla(escape, perception)
            if casilla_escape not in obstaculos_duros:
                disparar = casilla_escape in obstaculos_destruibles and (perception[AgentConsts.CAN_FIRE] > 0)
                return escape, disparar

        return AgentConsts.NO_MOVE, False

    def Transit(self, perception, map):
        vision = [perception[AgentConsts.NEIGHBORHOOD_UP], perception[AgentConsts.NEIGHBORHOOD_DOWN],
                  perception[AgentConsts.NEIGHBORHOOD_LEFT], perception[AgentConsts.NEIGHBORHOOD_RIGHT]]
        
        if AgentConsts.SHELL in vision: return "DodgeBullet"
        if AgentConsts.PLAYER in vision or AgentConsts.COMMAND_CENTER in vision: return "OrientateAndShoot"
        
        player_x, player_y = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        base_x, base_y = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]
        agent_x, agent_y = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        
        target_x = player_x if player_x >= 0 else base_x
        target_y = player_y if player_x >= 0 else base_y
        
        if abs(agent_x - target_x) < 1.0 or abs(agent_y - target_y) < 1.0:
            return "OrientateAndShoot"
            
        return "Move"