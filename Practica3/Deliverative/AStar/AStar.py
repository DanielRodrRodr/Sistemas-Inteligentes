
from Deliverative.AStar.Node import Node
from Deliverative.AStar.Problem import Problem
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
        path = []

        if self.open.count() == 0:
            return path
        
        found = self.GetSucesorInOpen(self, self.open[1])
        if found != None:
            coste = Problem.GetGCostBetween(self, self.open[0], found)
            if 0 < coste:
                Node.SetParent(found, self.open[0])
                Node.SetG(found)

        self.open.clear()
        self.precessed.clear()
        self.open.append(self.problem.Initial())

        while self.open.count() > 0 #and !meta
        #mientras no encontremos la meta y haya elementos en open....
        #TODO implementar el bucle de búsqueda del algoritmo A*
        return path[::-1]

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        #TODO Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)


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
        return path



