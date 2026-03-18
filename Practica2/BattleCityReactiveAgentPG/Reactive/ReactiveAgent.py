from Agent.BaseAgent import BaseAgent
from StateMachine.StateMachine import StateMachine
from States.DodgeBullet import DodgeBullet
from States.GoToCommandCenter import GoToCommandCenter
from States.OrientateAndShoot import OrientateAndShoot
from States.GoToExit import GoToExit
from States.AgentConsts import AgentConsts
import random


class ReactiveAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
        dictionary = {
            "GoToCommandCenter": GoToCommandCenter("GoToCommandCenter"),
            "OrientateAndShoot": OrientateAndShoot("OrientateAndShoot"),
            "DodgeBullet": DodgeBullet("DodgeBullet"),
            "GoToExit": GoToExit("GoToExit")
        }
        self.stateMachine = StateMachine("ReactiveBehavior",dictionary,"GoToCommandCenter")

        self.last_x = None
        self.last_y = None
        self.ciclos_atascado = 0
        self.last_action = None

    #Metodo que se llama al iniciar el agente. No devuelve nada y sirve para contruir el agente
    def Start(self):
        print("Inicio del agente ")
        self.stateMachine.Start(self)

    #Metodo que se llama en cada actualización del agente, y se proporciona le vector de percepciones
    #Devuelve la acción u el disparo si o no
    def Update(self, perception, map):
        action, shot = self.stateMachine.Update(perception, map, self)
        if action == AgentConsts.NO_MOVE:
            if self.last_action is not None:
                action = self.last_action
        else:
            self.last_action = action
        #action, shot = self.stateMachine.Update(perception, map, self)

        x = perception[AgentConsts.AGENT_X]
        y = perception[AgentConsts.AGENT_Y]

        #Comprobar si se queda atascado el agente
        if self.last_x is not None and self.last_y is not None:
            if abs(x - self.last_x) < 0.05 and abs(y - self.last_y) < 0.05:
                self.ciclos_atascado += 1
            else:
                self.ciclos_atascado = 0

        self.last_x = x
        self.last_y = y

        # Si se queda atascado varios ciclos se mueve
        if self.ciclos_atascado >= 2:
            action = random.choice([
                AgentConsts.MOVE_LEFT,
                AgentConsts.MOVE_RIGHT,
                AgentConsts.MOVE_UP,
                AgentConsts.MOVE_DOWN
            ])
            self.ciclos_atascado = 0

        return action, shot
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        super().End(win)
        self.stateMachine.End()