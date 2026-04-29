import sys
import threading

sys.path.insert(0, "./LGym")
sys.path.insert(0, "./Agent")
sys.path.insert(0, "./Deliverative")
sys.path.insert(0, "./Competitive")
sys.path.insert(0, "./")

from LGym.LGymClient import agentLoop
from Deliverative.GoalOrientedAgent import GoalOrientedAgent
from Competitive.CompetitiveAgent import CompetitiveAgent


agent1 = GoalOrientedAgent("1", "Deliverative")
agent2 = CompetitiveAgent("2", "CompetitiveAgent")
agentLoop(agent2, True)
