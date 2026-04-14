from States.AgentConsts import AgentConsts

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    GOAL_EXIT = 3
    def __init__(self, problem, goals, finalGoal):
        self.goals = goals
        self.finalGoal = finalGoal
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False

    def ForceToRecalculate(self):
        self.recalculate = True

    def NeedReplaning(self, perception, map, agent):
        if self.recalculate:
            self.recalculate = False
            self.lastTime = perception[AgentConsts.TIME]
            return True
        #TODO definir la estrategia de cuando queremos recalcular
        #puede ser , por ejemplo cada cierto tiempo o cuando tenemos poca vida.
        #return False
        currentTime = perception[AgentConsts.TIME]
        if self.lastTime == -1: #La primera vez
            self.lastTime = currentTime

        if currentTime - self.lastTime > 5:
            self.lastTime = currentTime
            return True
        if perception[AgentConsts.HEALTH] <= 1:
            return True

        return False

    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        #TODO definir la estrategia del cambio de meta
        #print("TODO aqui faltan cosas :)")
        #return self.goals[random.randint(0,len(self.goals))]
        # Si tiene poca vida, ir a vida. También se comprueba que haya vida
        if perception[AgentConsts.HEALTH] <= 1 and perception[AgentConsts.LIFE_X] != -1: 
            return self.goals[self.GOAL_LIFE]
        # Si no hay base, salir
        if perception[AgentConsts.COMMAND_CENTER_X] < 0 or perception[AgentConsts.PLAYER_X] < 0 :
            return self.finalGoal
        # Ir a la base
        return self.goals[self.GOAL_COMMAND_CENTRER]
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
