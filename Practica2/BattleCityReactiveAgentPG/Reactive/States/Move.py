from StateMachine.State import State
from States.AgentConsts import AgentConsts

class Move(State):
    def __init__(self, id):
        super().__init__(id)

    def esta_bloqueado(self, direccion, perception):
        obstaculos = [AgentConsts.UNBREAKABLE, AgentConsts.BRICK, AgentConsts.SEMI_UNBREKABLE, AgentConsts.SEMI_BREKABLE]
        if direccion == AgentConsts.MOVE_UP: return perception[AgentConsts.NEIGHBORHOOD_UP] in obstaculos
        if direccion == AgentConsts.MOVE_DOWN: return perception[AgentConsts.NEIGHBORHOOD_DOWN] in obstaculos
        if direccion == AgentConsts.MOVE_RIGHT: return perception[AgentConsts.NEIGHBORHOOD_RIGHT] in obstaculos
        if direccion == AgentConsts.MOVE_LEFT: return perception[AgentConsts.NEIGHBORHOOD_LEFT] in obstaculos
        return False

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

        if not self.esta_bloqueado(dir_prim, perception): return dir_prim, False
        if not self.esta_bloqueado(dir_sec, perception): return dir_sec, False
        
        for escape in [AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_LEFT, AgentConsts.MOVE_RIGHT]:
            if not self.esta_bloqueado(escape, perception): return escape, False
            
        return AgentConsts.NO_MOVE, False

    def Transit(self, perception, map):
        # Mismas interrupciones que SeekTarget para no tener que salir de este estado si no es necesario
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