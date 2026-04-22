from CompetitiveStates.AgentConsts import AgentConsts
from Deliverative.GoalMonitor import GoalMonitor

class CompetitiveGoalMonitor(GoalMonitor):

    def __init__(self, problem, goals, finalGoal):
        super().__init__(problem, goals, finalGoal)

    def ForceToRecalculate(self):
        self.recalculate = True
        self.lastTime = -1

    def NeedReplaning(self, perception, map, agent):
        currentTime = perception[AgentConsts.TIME]

        if self.lastTime == -1:
            self.lastTime = currentTime
            return True

        if currentTime - self.lastTime > 3:
            self.lastTime = currentTime
            return True

        if perception[AgentConsts.PLAYER_X] != -1 and currentTime - self.lastTime > 1:
            self.lastTime = currentTime
            return True

        if perception[AgentConsts.HEALTH] <= 1:
            return True

        return False

    def SelectGoal(self, perception, map, agent):
        # Curarse solo cuando es de emergencia
        if perception[AgentConsts.HEALTH] <= 1 and perception[AgentConsts.LIFE_X] != -1:
            return self.goals[self.GOAL_LIFE]
        
        # Prioriza matar al jugador
        if perception[AgentConsts.PLAYER_X] != -1:
            return self.goals[self.GOAL_PLAYER]

        # Si no hay jugador, defender base
        if perception[AgentConsts.COMMAND_CENTER_X] >= 0:
            return self.goals[self.GOAL_COMMAND_CENTRER]

        return self.finalGoal
    
    def UpdateGoals(self, goal, goalId):
        self.goals[goalId] = goal
        
        if goalId == self.GOAL_PLAYER:
            self.ForceToRecalculate()