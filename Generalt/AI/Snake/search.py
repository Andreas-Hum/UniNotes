import heapq
import random
import math

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Node:
    def __init__(self, state, parent, action, cost) -> None:
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def get_path(self):
        path = []
        current = self
        while current is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        return path

    def __lt__(self, other):
        return self.cost < other.cost


class Frontier:
    def __init__(self, goal) -> None:
        self.frontier = []
        self.goal = goal

    def euclidean(self, state):
        x1, y1 = state
        x2, y2 = self.goal
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def add(self, state, parent, action, cost):
        if not isinstance(state, tuple):
            raise ValueError(f"Expected state to be a tuple, got {type(state)}")
        heapq.heappush(self.frontier, Node(state, parent, action, cost))

    def pop(self):
        if len(self.frontier) == 0:
            raise Exception("Cannot pop from an empty heap")
        else:
            return heapq.heappop(self.frontier)

    def contains_state(self, state) -> bool:
        return any(node.state == state for node in self.frontier)

    def empty(self) -> bool:
        return len(self.frontier) == 0


class SnakeAI:
    def __init__(self) -> None:
        pass

    def find(self, state):
        frontier = Frontier(state["food"])

        initial_cost = self.calculate_cost(state, state["head"])
        frontier.add(state["head"], None, state["direction"], initial_cost)

        explored = set()

        while not frontier.empty():
            current_node = frontier.pop()

            if current_node.state == state["food"]:
                return current_node.get_path()[1:]

            if current_node.state not in explored:
                explored.add(current_node.state)

            actions = self.get_valid_moves(state["grid"], current_node.state)

            for cur_state, action in actions:
                if cur_state not in explored and not frontier.contains_state(cur_state):
                    cost = self.calculate_cost(state, cur_state)
                    frontier.add(cur_state, current_node, action, cost)

        # If no solution is found, switch to safe mode
        return self.safe_mode(state)

    def get_valid_moves(self, grid, position):
        valid_moves = []
        rows, cols = len(grid), len(grid[0])
        y, x = position

        # Define possible directions with their corresponding actions
        directions = [
            ((0, -1), LEFT),
            ((1, 0), DOWN),
            ((0, 1), RIGHT),
            ((-1, 0), UP),
        ]

        for (dy, dx), action in directions:
            new_y, new_x = y + dy, x + dx

            # Check if the new position is within the grid boundaries and not an obstacle
            if (
                0 <= new_y < rows
                and 0 <= new_x < cols
                and (grid[new_y][new_x] == 0 or grid[new_y][new_x] == 2)
            ):
                valid_moves.append(((new_y, new_x), action))

        return valid_moves

    def calculate_cost(self, state, position):
        return self.euclidean(position, state["food"])

    def euclidean(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def manhatten(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def safe_mode(self, state):
        possible_moves = self.get_valid_moves(state["grid"], state["head"])
        if possible_moves:
            best_move = max(
                possible_moves,
                key=lambda move: self.manhatten(move[0], state["food"]),
            )
            return [best_move[1]]
        return []
