from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

class SeekTarget(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):
        # Solo piensa, no ejecuta acciones
        return AgentConsts.NO_MOVE, False
    
    def Transit(self, perception, map):
        # Si jugador o base ya no existen -> ir a la salida
        if perception[AgentConsts.PLAYER_X] < 0 or perception[AgentConsts.COMMAND_CENTER_X] < 0:
            return "GoToExit"
    
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
        
        vision = [
            perception[AgentConsts.NEIGHBORHOOD_UP],
            perception[AgentConsts.NEIGHBORHOOD_DOWN],
            perception[AgentConsts.NEIGHBORHOOD_LEFT],
            perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        ]

        if AgentConsts.PLAYER in vision or AgentConsts.COMMAND_CENTER in vision:
            return "OrientateAndShoot"
            
        return "Move"