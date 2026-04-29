from StateMachine.State import State
from CompetitiveStates.AgentConsts import AgentConsts
import random

class Ambush(State):
    AMBUSH_MIN_DIST = 6
    AMBUSH_MAX_DIST = 10

    def __init__(self, id):
        super().__init__(id)
        self._ambush_target = None
        self._steps_in_ambush = 0

    def _has_line_of_sight(self, x1, y1, x2, y2, map_data):
        #Comprobar si hay línea de visión libre entre dos celdas del mapa.
        size = int(len(map_data) ** 0.5)
        blocked = {AgentConsts.UNBREAKABLE, AgentConsts.SEMI_UNBREKABLE,
                   AgentConsts.BRICK, AgentConsts.SEMI_BREKABLE}
 
        if x1 == x2:
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if 0 <= y < size and map_data[y * size + x1] in blocked:
                    return False
            return True
 
        if y1 == y2:
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if 0 <= x < size and map_data[y1 * size + x] in blocked:
                    return False
            return True
 
        return False

    def _is_walkable(self, x, y, map_data):
        size = int(len(map_data) ** 0.5)
        if x < 0 or y < 0 or x >= size or y >= size:
            return False
        val = map_data[y * size + x]
        return val not in {AgentConsts.UNBREAKABLE, AgentConsts.SEMI_UNBREKABLE, AgentConsts.BRICK, AgentConsts.SEMI_BREKABLE}

    def _find_flanking_cell(self, ax, ay, px, py, map_data):
        #Busca una celda adyacente al enemigo desde la que se tiene visión sobre él pero que no esté en línea recta directa con nuestra posición actual

        size = int(len(map_data) ** 0.5)
        candidates = []
 
        # Celdas en un radio de 2 alrededor del jugador
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                fx, fy = px + dx, py + dy
                if not self._is_walkable(fx, fy, map_data):
                    continue
                if fx == px and fy == py:
                    continue
                # Debe tener línea de visión al enemigo
                if not self._has_line_of_sight(fx, fy, px, py, map_data):
                    continue
                # Que no esté en la misma línea que nosotros
                is_flanking = not (fx == ax or fy == ay)
                dist_to_us = abs(fx - ax) + abs(fy - ay)
                candidates.append((is_flanking, -dist_to_us, fx, fy))
 
        if not candidates:
            return None
 
        # Se ordenan primero las flanqueantes y luego las más cercanas a nosotros
        candidates.sort(key=lambda c: (not c[0], c[1]), reverse=False)
        _, _, fx, fy = candidates[0]
        return fx, fy
 
    def _move_towards(self, ax, ay, tx, ty, perception):
        dx = tx - ax
        dy = ty - ay
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
 
        neighborhood = {AgentConsts.MOVE_UP: perception[AgentConsts.NEIGHBORHOOD_UP],
                        AgentConsts.MOVE_DOWN: perception[AgentConsts.NEIGHBORHOOD_DOWN],
                        AgentConsts.MOVE_RIGHT: perception[AgentConsts.NEIGHBORHOOD_RIGHT],
                        AgentConsts.MOVE_LEFT: perception[AgentConsts.NEIGHBORHOOD_LEFT],}
        
        blocked = {AgentConsts.UNBREAKABLE, AgentConsts.SEMI_UNBREKABLE, AgentConsts.BRICK, AgentConsts.SEMI_BREKABLE}
 
        for d in directions:
            if neighborhood.get(d) not in blocked:
                return d
 
        # Movimiento aleatorio de desbloqueo
        free = [d for d, v in neighborhood.items() if v not in blocked]
        return random.choice(free) if free else AgentConsts.NO_MOVE

    def Start(self, agent):
        self._ambush_target = None
        self._steps_in_ambush = 0

    def Update(self, perception, map, agent):
        ax = perception[AgentConsts.AGENT_X]
        ay = perception[AgentConsts.AGENT_Y]
        px = perception[AgentConsts.PLAYER_X]
        py = perception[AgentConsts.PLAYER_Y]
 
        self._steps_in_ambush += 1
 
        # Si se pierde de vista al jugador, moverse aleatoriamente unos pasos
        if px == -1:
            neighborhood = {AgentConsts.MOVE_UP: perception[AgentConsts.NEIGHBORHOOD_UP],
                            AgentConsts.MOVE_DOWN: perception[AgentConsts.NEIGHBORHOOD_DOWN],
                            AgentConsts.MOVE_RIGHT: perception[AgentConsts.NEIGHBORHOOD_RIGHT],
                            AgentConsts.MOVE_LEFT:  perception[AgentConsts.NEIGHBORHOOD_LEFT],}
            
            blocked = {AgentConsts.UNBREAKABLE, AgentConsts.SEMI_UNBREKABLE, AgentConsts.BRICK, AgentConsts.SEMI_BREKABLE}

            free = [d for d, v in neighborhood.items() if v not in blocked]
            return (random.choice(free) if free else AgentConsts.NO_MOVE), False
 
        # Recalcular objetivo flanqueante cada 7 pasos o si no se tiene localizado
        if self._ambush_target is None or self._steps_in_ambush % 7 == 0:
            result = self._find_flanking_cell(ax, ay, px, py, map)
            self._ambush_target = result if result else (px, py)
 
        tx, ty = self._ambush_target
 
        # Si está en la celda flanqueante, disparar
        if abs(ax - tx) <= 1 and abs(ay - ty) <= 1:
            if self._has_line_of_sight(ax, ay, px, py, map):
                move = self._move_towards(ax, ay, px, py, perception)
                return move, perception[AgentConsts.CAN_FIRE] > 0
 
        return self._move_towards(ax, ay, tx, ty, perception), False

    def Transit(self, perception, map):
        vision = [perception[AgentConsts.NEIGHBORHOOD_UP], perception[AgentConsts.NEIGHBORHOOD_DOWN],
                  perception[AgentConsts.NEIGHBORHOOD_LEFT], perception[AgentConsts.NEIGHBORHOOD_RIGHT]]
 
        if (perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.SHELL or
            perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.SHELL or
            perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.SHELL or
            perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.SHELL):
            return "DodgeBullet"
 
        if perception[AgentConsts.HEALTH] <= 1 and perception[AgentConsts.LIFE_X] != -1:
            return "Retreat"
 
        px = perception[AgentConsts.PLAYER_X]
        if px != -1:
            dist = abs(perception[AgentConsts.AGENT_X] - px) + \
                   abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y])
 
            if AgentConsts.PLAYER in vision and perception[AgentConsts.CAN_FIRE] > 0:
                return "OrientateAndShoot"
 
            if dist < Ambush.AMBUSH_MIN_DIST:
                return "ChasePlayer"
 
            if dist > Ambush.AMBUSH_MAX_DIST:
                return "ExecutePlan"
 
            return "Ambush"
 
        return "ExecutePlan"