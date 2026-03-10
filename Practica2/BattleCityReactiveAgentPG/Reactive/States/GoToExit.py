from StateMachine.State import State
from States.AgentConsts import AgentConsts


class GoToExit(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):

        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]

        exit_x = perception[AgentConsts.EXIT_X]
        exit_y = perception[AgentConsts.EXIT_Y]

        if agent_x < exit_x:
            return AgentConsts.MOVE_RIGHT, False
        elif agent_x > exit_x:
            return AgentConsts.MOVE_LEFT, False
        elif agent_y < exit_y:
            return AgentConsts.MOVE_DOWN, False
        elif agent_y > exit_y:
            return AgentConsts.MOVE_UP, False

        return AgentConsts.NO_MOVE, False


    def Transit(self, perception, map):
        return self.id