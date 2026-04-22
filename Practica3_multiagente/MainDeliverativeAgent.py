import sys
sys.path.insert(0,"./LGym")
sys.path.insert(0,"./Agent")
sys.path.insert(0,"./Deliverative")
sys.path.insert(0,"./Competitive")
from LGym.LGymClient import agentLoop
from Agent.BaseAgent import BaseAgent
from Deliverative.GoalOrientedAgent import GoalOrientedAgent
from Competitive.CompetitiveAgent import CompetitiveAgent


agent1 = GoalOrientedAgent("1","MyAgent")
agentLoop(agent1,True)
agent2 = CompetitiveAgent("1","CompetitiveAgent")
agentLoop(agent2,True)