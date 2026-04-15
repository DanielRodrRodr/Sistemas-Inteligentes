import sys
sys.path.insert(0,"./LGym")
sys.path.insert(0,"./Agent")
sys.path.insert(0,"./Deliverative")
from LGym.LGymClient import agentLoop
from Agent.BaseAgent import BaseAgent
from Deliverative.CompetitiveAgent import CompetitiveAgent


agent = CompetitiveAgent("1","CompetitiveAgent")
agentLoop(agent,True)

