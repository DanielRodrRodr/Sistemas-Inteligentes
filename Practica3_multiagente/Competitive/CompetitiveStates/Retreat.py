from StateMachine.State import State
from CompetitiveStates.AgentConsts import AgentConsts
import random


class Retreat(State):
    def __init__(self, id):
        super().__init__(id)
        self._last_move = AgentConsts.NO_MOVE

    def _is_free(self, direction, perception):
        blocked = {AgentConsts.UNBREAKABLE, AgentConsts.SEMI_UNBREKABLE,
                   AgentConsts.BRICK, AgentConsts.SEMI_BREKABLE}
        mapping = {AgentConsts.MOVE_UP: perception[AgentConsts.NEIGHBORHOOD_UP],AgentConsts.MOVE_DOWN: perception[AgentConsts.NEIGHBORHOOD_DOWN],
                   AgentConsts.MOVE_RIGHT: perception[AgentConsts.NEIGHBORHOOD_RIGHT],AgentConsts.MOVE_LEFT: perception[AgentConsts.NEIGHBORHOOD_LEFT],}
        return mapping.get(direction, AgentConsts.UNBREAKABLE) not in blocked

    def _opposite(self, direction):
        opposites = {AgentConsts.MOVE_UP: AgentConsts.MOVE_DOWN, AgentConsts.MOVE_DOWN: AgentConsts.MOVE_UP,
                     AgentConsts.MOVE_RIGHT: AgentConsts.MOVE_LEFT, AgentConsts.MOVE_LEFT: AgentConsts.MOVE_RIGHT, }
        return opposites.get(direction, AgentConsts.NO_MOVE)

    def _flee_direction(self, ax, ay, px, py, perception):
        # Devuelve el mejor movimiento para alejarse del jugador.
        candidates = []
        moves = [AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN,
                 AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_LEFT]
        deltas = {AgentConsts.MOVE_UP: (0, -1), AgentConsts.MOVE_DOWN: (0,  1),
                  AgentConsts.MOVE_RIGHT: ( 1, 0), AgentConsts.MOVE_LEFT: (-1, 0),}

        for m in moves:
            if not self._is_free(m, perception):
                continue
            dx, dy = deltas[m]
            new_dist = abs((ax + dx) - px) + abs((ay + dy) - py)
            candidates.append((new_dist, m))

        if not candidates:
            return AgentConsts.NO_MOVE

        candidates.sort(key=lambda c: c[0], reverse=True)   # mayor distancia primero
        return candidates[0][1]

    def _move_towards_life(self, ax, ay, lx, ly, px, py, perception):
        dx = lx - ax
        dy = ly - ay
        deltas = {AgentConsts.MOVE_UP: (0, -1), AgentConsts.MOVE_DOWN: (0,  1),
                  AgentConsts.MOVE_RIGHT: ( 1, 0), AgentConsts.MOVE_LEFT: (-1, 0),}

        # Ordenar movimientos: primero los que acercan al life
        directions = []
        if abs(dx) >= abs(dy):
            if dx > 0: directions.append(AgentConsts.MOVE_RIGHT)
            elif dx < 0: directions.append(AgentConsts.MOVE_LEFT)
            if dy > 0: directions.append(AgentConsts.MOVE_DOWN)
            elif dy < 0: directions.append(AgentConsts.MOVE_UP)
        else:
            if dy > 0: directions.append(AgentConsts.MOVE_DOWN)
            elif dy < 0: directions.append(AgentConsts.MOVE_UP)
            if dx > 0: directions.append(AgentConsts.MOVE_RIGHT)
            elif dx < 0: directions.append(AgentConsts.MOVE_LEFT)

        # Añadir los restantes por si los prioritarios están bloqueados
        for m in [AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN,
                  AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_LEFT]:
            if m not in directions:
                directions.append(m)

        for d in directions:
            if not self._is_free(d, perception):
                continue
            # Si el enemigo es visible, evitar movimientos que nos acerquen a él
            if px != -1:
                ndx, ndy = deltas[d]
                new_enemy_dist = abs((ax + ndx) - px) + abs((ay + ndy) - py)
                current_enemy_dist = abs(ax - px) + abs(ay - py)
                # Si no hay alternativa, acercarnos al enemigo
                if new_enemy_dist < current_enemy_dist - 1:
                    continue
            return d

        # Último recurso: cualquier celda libre
        free = [d for d in [AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN,
                             AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_LEFT]
                if self._is_free(d, perception)]
        return random.choice(free) if free else AgentConsts.NO_MOVE

    def Start(self, agent):
        self._last_move = AgentConsts.NO_MOVE

    def Update(self, perception, map, agent):
        ax = perception[AgentConsts.AGENT_X]
        ay = perception[AgentConsts.AGENT_Y]
        px = perception[AgentConsts.PLAYER_X]
        py = perception[AgentConsts.PLAYER_Y]
        lx = perception[AgentConsts.LIFE_X]
        ly = perception[AgentConsts.LIFE_Y]

        if lx != -1 and ly != -1:
            move = self._move_towards_life(ax, ay, lx, ly, px, py, perception)
        elif px != -1:
            move = self._flee_direction(ax, ay, px, py, perception)
        else:
            free = [d for d in [AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN,
                                 AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_LEFT]
                    if self._is_free(d, perception)]
            move = random.choice(free) if free else AgentConsts.NO_MOVE

        self._last_move = move
        return move, False

    def Transit(self, perception, map):
        danger_dist = 2
        if ((perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.SHELL and
             perception[AgentConsts.NEIGHBORHOOD_DIST_UP] <= danger_dist) or
            (perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.SHELL and
             perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN] <= danger_dist) or
            (perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.SHELL and
             perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT] <= danger_dist) or
            (perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.SHELL and
             perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT] <= danger_dist)):
            return "DodgeBullet"

        if perception[AgentConsts.HEALTH] > 2:
            if perception[AgentConsts.PLAYER_X] != -1:
                return "ChasePlayer"
            return "ExecutePlan"

        if perception[AgentConsts.LIFE_X] == -1:
            return "ExecutePlan"

        return "Retreat"