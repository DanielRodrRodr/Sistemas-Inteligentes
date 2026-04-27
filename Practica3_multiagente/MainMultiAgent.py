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


def run_agent(agent, debug):
    print(f"[{agent.Name()}] Iniciando...")
    agentLoop(agent, debug)
    print(f"[{agent.Name()}] Finalizado")


agent1 = GoalOrientedAgent("1", "Deliverative")
agent2 = CompetitiveAgent("2", "CompetitiveAgent")

t1 = threading.Thread(target=run_agent, args=(agent1, True), daemon=True)
t2 = threading.Thread(target=run_agent, args=(agent2, True), daemon=True)

t1.start()
t2.start()

t1.join()
t2.join()
