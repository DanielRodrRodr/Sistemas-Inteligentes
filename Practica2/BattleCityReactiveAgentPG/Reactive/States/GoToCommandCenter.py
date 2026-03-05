from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random


class GoToCommandCenter(State):

    def __init__(self, id):
        super().__init__(id)
        #self.Reset()

    def Update(self, perception, map, agent):
        #self.updateTime += perception[AgentConsts.TIME]
        #if self.updateTime > 1.0:
            #self.Reset()
        #return self.action,True
        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]

        base_x = perception[AgentConsts.COMMAND_CENTER_X]
        base_y = perception[AgentConsts.COMMAND_CENTER_Y]

        # Moverse hacia la base
        if agent_x < base_x:
            return AgentConsts.MOVE_RIGHT, False
        elif agent_x > base_x:
            return AgentConsts.MOVE_LEFT, False
        elif agent_y < base_y:
            return AgentConsts.MOVE_DOWN, False
        elif agent_y > base_y:
            return AgentConsts.MOVE_UP, False

        return AgentConsts.NO_MOVE, False
    
    def Transit(self,perception, map):
        #return self.id
        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]

        player_x = perception[AgentConsts.PLAYER_X]
        player_y = perception[AgentConsts.PLAYER_Y]

        base_x = perception[AgentConsts.COMMAND_CENTER_X]
        base_y = perception[AgentConsts.COMMAND_CENTER_Y]

        # Si jugador existe y está alineado → atacar jugador
        if player_x >= 0:
            if agent_x == player_x or agent_y == player_y:
                return "AttackPlayer"

        # Si base está alineada → atacar base
        if agent_x == base_x or agent_y == base_y:
            return "AttackBase"

        return self.id
    
    #def Reset(self):
        #self.action = random.randint(1,4)
        #self.updateTime = 0