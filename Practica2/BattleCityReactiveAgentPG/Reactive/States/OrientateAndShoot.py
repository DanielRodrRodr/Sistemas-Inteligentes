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

        can_fire = perception[AgentConsts.CAN_FIRE] > 0

        # alineado verticalmente
        if abs(agent_x - target_x) < 1.0:

            if target_y > agent_y:
                action = AgentConsts.MOVE_DOWN
            else:
                action = AgentConsts.MOVE_UP

            return action, can_fire

        # alineado horizontalmente
        if abs(agent_y - target_y) < 1.0:

            if target_x > agent_x:
                action = AgentConsts.MOVE_RIGHT
            else:
                action = AgentConsts.MOVE_LEFT

            return action, can_fire

        # no alineado → acercarse
        if abs(target_x - agent_x) > abs(target_y - agent_y):
            action = AgentConsts.MOVE_RIGHT if target_x > agent_x else AgentConsts.MOVE_LEFT
        else:
            action = AgentConsts.MOVE_DOWN if target_y > agent_y else AgentConsts.MOVE_UP

        return action, False
        #if abs(agent_x - target_x) < 1.0: 
         #   action = AgentConsts.MOVE_DOWN if target_y > agent_y else AgentConsts.MOVE_UP
        #else: 
         #   action = AgentConsts.MOVE_RIGHT if target_x > agent_x else AgentConsts.MOVE_LEFT
            
        #shot = perception[AgentConsts.CAN_FIRE] > 0
        #return action, shot

    def Transit(self, perception, map):
        vision = [perception[AgentConsts.NEIGHBORHOOD_UP], perception[AgentConsts.NEIGHBORHOOD_DOWN],
                  perception[AgentConsts.NEIGHBORHOOD_LEFT], perception[AgentConsts.NEIGHBORHOOD_RIGHT]]
        
        # Detectar la bala antes de que llegue al agente
        danger_dist = 3
        if perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= danger_dist:
            return "DodgeBullet"
        if perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= danger_dist:
            return "DodgeBullet"
        if perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= danger_dist:
            return "DodgeBullet"
        if perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.SHELL and perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= danger_dist:
            return "DodgeBullet"
        
        
        player_x, player_y = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        base_x, base_y = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]
        agent_x, agent_y = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]

        if player_x < 0 and base_x < 0:
            return "GoToExit"

        if AgentConsts.PLAYER in vision or AgentConsts.COMMAND_CENTER in vision:
            return "OrientateAndShoot"

        return "SeekTarget"
        #player_x, player_y = perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y]
        #base_x, base_y = perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y]
        #agent_x, agent_y = perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y]
        
        #target_x = player_x if player_x >= 0 else base_x
        #target_y = player_y if player_x >= 0 else base_y
        
        #if abs(agent_x - target_x) < 1.0 or abs(agent_y - target_y) < 1.0:
         #   return "OrientateAndShoot"
            
        #return "SeekTarget"