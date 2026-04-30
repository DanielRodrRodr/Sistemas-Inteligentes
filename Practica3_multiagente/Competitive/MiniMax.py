import math
import random
from Competitive.CompetitiveStates.AgentConsts import AgentConsts


class MiniMax:

    def __init__(self, maxDepth=3):
        self.maxDepth = maxDepth

    def Decide(self, perception, map, agent):
        bestValue = -math.inf
        bestActions = []

        for action in self.GetPossibleActions():
            newState = self.Simulate(perception, map, action, True)
            value = self.MinValue(newState, map, agent, 1, -math.inf, math.inf)

            if value > bestValue:
                bestValue = value
                bestActions = [action]
            elif value == bestValue:
                bestActions.append(action)

        # Evitar empates
        return random.choice(bestActions)

    def MaxValue(self, perception, map, agent, depth, alpha, beta):
        if depth >= self.maxDepth:
            return self.Evaluate(perception, map)

        value = -math.inf

        for action in self.GetPossibleActions():
            newState = self.Simulate(perception, map, action, True)
            value = max(value, self.MinValue(newState, map, agent, depth + 1, alpha, beta))

            if value >= beta:
                return value

            alpha = max(alpha, value)

        return value

    def MinValue(self, perception, map, agent, depth, alpha, beta):
        if depth >= self.maxDepth:
            return self.Evaluate(perception, map)

        value = math.inf

        for action in self.GetPossibleActions():
            newState = self.Simulate(perception, map, action, False)
            value = min(value, self.MaxValue(newState, map, agent, depth + 1, alpha, beta))

            if value <= alpha:
                return value

            beta = min(beta, value)

        return value

    def Simulate(self, perception, map, action, isMax):
        newPerception = perception.copy()

        if isMax:
            x = newPerception[AgentConsts.AGENT_X]
            y = newPerception[AgentConsts.AGENT_Y]
        else:
            x = newPerception[AgentConsts.PLAYER_X]
            y = newPerception[AgentConsts.PLAYER_Y]

        nx, ny = x, y

        if action == 0:   # arriba
            ny += 1
        elif action == 1: # abajo
            ny -= 1
        elif action == 2: # izquierda
            nx -= 1
        elif action == 3: # derecha
            nx += 1

        if self.IsValid(nx, ny, map):
            if isMax:
                newPerception[AgentConsts.AGENT_X] = nx
                newPerception[AgentConsts.AGENT_Y] = ny
            else:
                newPerception[AgentConsts.PLAYER_X] = nx
                newPerception[AgentConsts.PLAYER_Y] = ny

        return newPerception

    def Evaluate(self, perception, map):
        playerX = perception[AgentConsts.PLAYER_X]

        # Enemigo no visible → malo (modo competitivo)
        if playerX == -1:
            return -50

        agentX = perception[AgentConsts.AGENT_X]
        agentY = perception[AgentConsts.AGENT_Y]
        playerY = perception[AgentConsts.PLAYER_Y]
        dist = abs(agentX - playerX) + abs(agentY - playerY)
        score = 0

        # Penalizar estar en la misma casilla
        if dist == 0:
            return -500

        # Distancia de 1 o 2 casillas para disparar
        if dist == 1 and self.HasLineOfSight(agentX, agentY, playerX, playerY, map):
            return 900

        # Acercarse
        score += -dist * 15

        # Línea de tiro REAL
        if self.HasLineOfSight(agentX, agentY, playerX, playerY, map):
            score += 80

        # Evitar estar alineado sin cobertura (peligro)
        if agentX == playerX or agentY == playerY:
            if not self.HasLineOfSight(agentX, agentY, playerX, playerY, map):
                score -= 10

        # Bonus por acorralar (pocos movimientos posibles del enemigo)
        enemyMoves = self.CountValidMoves(playerX, playerY, map)
        score += (4 - enemyMoves) * 10
        # Pequeña aleatoriedad
        score += random.uniform(-2, 2)
        
        return score

    def HasLineOfSight(self, x1, y1, x2, y2, map):
        # misma columna
        if x1 == x2:
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if not self.IsValid(x1, y, map):
                    return False
            return True

        # misma fila
        if y1 == y2:
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if not self.IsValid(x, y1, map):
                    return False
            return True

        return False

    def CountValidMoves(self, x, y, map):
        moves = 0
        for action in self.GetPossibleActions():
            nx, ny = x, y

            if action == 0:
                ny += 1
            elif action == 1:
                ny -= 1
            elif action == 2:
                nx -= 1
            elif action == 3:
                nx += 1

            if self.IsValid(nx, ny, map):
                moves += 1

        return moves

    def IsValid(self, x, y, map):
        size = int(len(map) ** 0.5)

        if x < 0 or y < 0 or x >= size or y >= size:
            return False

        pos = y * size + x
        value = map[pos]

        return value != AgentConsts.UNBREAKABLE and value != AgentConsts.SEMI_UNBREKABLE

    def GetPossibleActions(self):
        return [0, 1, 2, 3]