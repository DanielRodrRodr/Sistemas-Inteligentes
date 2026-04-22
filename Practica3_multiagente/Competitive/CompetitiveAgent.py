from Agent.BaseAgent import BaseAgent
from StateMachine.StateMachine import StateMachine
from CompetitiveStates.ExecutePlan import ExecutePlan
from CompetitiveStates.OrientateAndShoot import OrientateAndShoot
from CompetitiveStates.DodgeBullet import DodgeBullet
from CompetitiveStates.ChasePlayer import ChasePlayer
from AStar.AStar import AStar
from MyProblem.BCNode import BCNode
from MyProblem.BCProblem import BCProblem
from CompetitiveStates.AgentConsts import AgentConsts
from CompetitiveGoalMonitor import CompetitiveGoalMonitor
from MiniMax import MiniMax

class CompetitiveAgent(BaseAgent):

    def __init__(self, id, name):
        super().__init__(id, name)
        dictionary = {
            "ExecutePlan": ExecutePlan("ExecutePlan"),
            "OrientateAndShoot": OrientateAndShoot("OrientateAndShoot"),
            "DodgeBullet": DodgeBullet("DodgeBullet"),
            "ChasePlayer": ChasePlayer("ChasePlayer")
        }

        self.stateMachine = StateMachine("CompetitiveBehavior", dictionary, "ExecutePlan")
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False
        self.minimax = MiniMax(3)

    def Start(self):
        print("Inicio del agente COMPETITIVO")
        self.stateMachine.Start(self)
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False

    def Update(self, perception, map):

        if perception == True or perception == False:
            return 0, True

        if not self.agentInit:
            self.InitAgent(perception, map)
            self.agentInit = True

        # Usar minimax si el enemigo está cerca
        if perception[AgentConsts.PLAYER_X] != -1:

            dist = abs(perception[AgentConsts.AGENT_X] - perception[AgentConsts.PLAYER_X]) + abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y])

            if dist <= 4:
                action = self.minimax.Decide(perception, map, self)
                return action, True
    
        action, shot = self.stateMachine.Update(perception, map, self)

        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor.UpdateGoals(goal3Player, 2)

        if self.goalMonitor.NeedReplaning(perception, map, self):
            self.problem.InitMap(map)
            self.plan = self._CreatePlan(perception, map)

        if perception[AgentConsts.PLAYER_X] != -1:
            if self.minimax.HasLineOfSight(perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y],
                                           perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y], map):
                shot = True

        return action, shot

    def _CreatePlan(self, perception, map):

        if self.goalMonitor is not None:
            goal = self.goalMonitor.SelectGoal(perception, map, self)
            initial = self._CreateInitialNode(perception)

            self.problem.SetInitial(initial)
            self.problem.SetGoal(goal)

            self.plan = self.aStar.GetPlan()

        return self.plan

    @staticmethod
    def CreateNodeByPerception(perception, value, perceptionID_X, perceptionID_Y, ySize):
        xMap, yMap = BCProblem.WorldToMapCoord(perception[perceptionID_X],perception[perceptionID_Y],ySize)
        newNode = BCNode(None,BCProblem.GetCost(value),value,xMap,yMap)
        return newNode

    def _CreatePlayerGoal(self, perception):
        return CompetitiveAgent.CreateNodeByPerception(perception,AgentConsts.PLAYER,AgentConsts.PLAYER_X,AgentConsts.PLAYER_Y,15)

    def _CreateExitGoal(self, perception):
        return CompetitiveAgent.CreateNodeByPerception(perception,AgentConsts.EXIT,AgentConsts.EXIT_X,AgentConsts.EXIT_Y,15)

    def _CreateLifeGoal(self, perception):
        return CompetitiveAgent.CreateNodeByPerception(perception,AgentConsts.LIFE,AgentConsts.LIFE_X,AgentConsts.LIFE_Y,15)

    def _CreateInitialNode(self, perception):
        node = CompetitiveAgent.CreateNodeByPerception(perception,AgentConsts.NOTHING,AgentConsts.AGENT_X,AgentConsts.AGENT_Y,15)
        node.SetG(0)
        return node

    def _CreateDefaultGoal(self, perception):
        return CompetitiveAgent.CreateNodeByPerception(perception,AgentConsts.COMMAND_CENTER,AgentConsts.COMMAND_CENTER_X,AgentConsts.COMMAND_CENTER_Y,15)

    def InitAgent(self, perception, map):
        initialNode = self._CreateInitialNode(perception)
        goalNode = self._CreateDefaultGoal(perception)
        self.problem = BCProblem(initialNode, goalNode, 15, 15)
        self.problem.InitMap(map)

        self.aStar = AStar(self.problem)

        goal1 = self._CreateDefaultGoal(perception)
        goal2 = self._CreateLifeGoal(perception)
        goal3 = self._CreatePlayerGoal(perception)
        exitGoal = self._CreateExitGoal(perception)

        # 🔥 Usamos el monitor competitivo
        self.goalMonitor = CompetitiveGoalMonitor(self.problem, [goal1, goal2, goal3], exitGoal)

        self.plan = self._CreatePlan(perception, map)

    @staticmethod
    def ShowPlan(plan):
        for n in plan:
            print("X: ",n.x,"Y:",n.y,"[",n.value,"]{",n.G(),"} => ")

    def GetPlan(self):
        return self.plan

    def End(self, win):
        super().End(win)
        self.stateMachine.End()