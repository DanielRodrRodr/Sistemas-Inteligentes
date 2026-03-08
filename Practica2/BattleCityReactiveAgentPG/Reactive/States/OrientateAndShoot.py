from StateMachine.State import State
from States.AgentConsts import AgentConsts

class OrientateAndShoot(State):
    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):
        agent_x, agent_y = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        player_x, player_y = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        base_x, base_y = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]
        
        target_x = player_x if player_x >= 0 else base_x
        target_y = player_y if player_x >= 0 else base_y

        if abs(agent_x - target_x) < 1.0: 
            action = AgentConsts.MOVE_UP if target_y > agent_y else AgentConsts.MOVE_DOWN
        else: 
            action = AgentConsts.MOVE_RIGHT if target_x > agent_x else AgentConsts.MOVE_LEFT
            
        shot = perception[AgentConsts.CAN_FIRE] > 0
        return action, shot

    def Transit(self, perception, map):
        vision = [perception[AgentConsts.NEIGHBORHOOD_UP], perception[AgentConsts.NEIGHBORHOOD_DOWN],
                  perception[AgentConsts.NEIGHBORHOOD_LEFT], perception[AgentConsts.NEIGHBORHOOD_RIGHT]]
        
        if AgentConsts.SHELL in vision: return "DodgeBullet"
        
        player_x, player_y = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        base_x, base_y = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]
        agent_x, agent_y = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        
        target_x = player_x if player_x >= 0 else base_x
        target_y = player_y if player_x >= 0 else base_y
        
        if abs(agent_x - target_x) < 1.0 or abs(agent_y - target_y) < 1.0:
            return "OrientateAndShoot"
            
        return "SeekTarget"