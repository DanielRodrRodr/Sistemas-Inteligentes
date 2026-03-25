from Deliverative.MyProblem.BCNode import BCNode
from Deliverative.MyProblem.BCProblem import BCProblem
#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node

class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.precessed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem #problema a resolver

    def GetPlan(self):
        findGoal = False
        #TODO implementar el algoritmo A*
        #cosas a tener en cuenta:
        #¿?Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        self.open.clear()
        self.precessed.clear()
        initial_node = self.problem.Initial()
        self._ConfigureNode(initial_node, None, 0)
        self.open.append(self.problem.Initial())
        path = []
        
        while len(self.open) > 0 and not findGoal:
            
            current_node = min(self.open, key=lambda n: n.G() + n.H())

            self.open.remove(current_node)
            self.precessed.add(current_node)

            if self.problem.IsASolution(current_node):
                findGoal = True
                path = self.ReconstructPath(current_node)
            else:
                successors = self.problem.GetSucessors(current_node)
                for suc in successors:
                    if suc not in self.precessed:
                        new_g = current_node.G() + 1 
                        
                        node_in_open = self.GetSucesorInOpen(suc)

                        if node_in_open is not None:
                            if new_g < node_in_open.G():
                                self._ConfigureNode(node_in_open, current_node, new_g)
                        else:
                            self._ConfigureNode(suc, current_node, new_g)
                            self.ApendInOpen(suc)
        return path[::-1]

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        #TODO Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)
        node.SetH(self.problem.Heuristic(node))


    def ApendInOpen(self, node):
        if node.g == None:
            print("ApendInOpen ", node.x, node.y)
        self.open.append(node)

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSucesorInOpen(self,sucesor):
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == sucesor:
                found = node
        return found

    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        path = []
        #TODO: devuelve el path invertido desde la meta hasta que el padre sea None.
        while goal is not None:
            path.append(goal)
            goal = goal.GetParent()

        return path



