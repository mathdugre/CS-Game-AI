from src.bot.Bot import Bot
from src.utils.Pathfinder import Pathfinder
import networkx as nx
from networkx.algorithms.shortest_paths import dijkstra_path, dijkstra_path_length
from src.symbols.ObjectSymbols import ObjectSymbols


class MyBot(Bot):

    def __init__(self):
        super().__init__()
        self.previous_health = None
        self.counter = 0
        self.my_pathfinder = MyPathfinder()
        self.run_to_base = False

    def get_name(self):
        # Find a name for your bot
        return 'Invader'

    def end_turn_routine(self, hp):
        self.previous_health = hp

    def turn(self, game_state, character_state, other_bots):
        self.counter += 1
        # Your bot logic goes here
        super().turn(game_state, character_state, other_bots)
        hp = character_state['health']
        position = character_state['location']
        base = character_state['base']

        self.my_pathfinder.set_game_state(game_state, other_bots)

        # Get back to base on time
        return_time = self.my_pathfinder.get_path_length(position, base)
        if self.counter + return_time >= 980 - return_time or self.run_to_base:
            self.run_to_base = True
            direction = self.my_pathfinder.get_next_direction(position, base)
            if position == base:
                self.run_to_base = False
                self.end_turn_routine(hp)
                return self.commands.store()
            self.end_turn_routine(hp)
            return self.commands.move(direction)

        # Heal to full when in base
        if position == base and hp != 100:
            self.run_to_base = False
            self.end_turn_routine(hp)
            return self.commands.rest()

        # Collect mineral

        # Find the position of the junk on the map
        junk_position = list()
        c = r = 0
        for row in game_state.splitlines():
            if 'J' in row:
                for column in row:
                    if 'J' == column:
                        pos = (r, c)
                        junk_position.append(pos)
                    c += 1
            r += 1
            c = 0

        nb_junk_spot = len(junk_position)

        # Mines as long as its not attacked
        if position in junk_position and self.previous_health == hp:
            self.end_turn_routine(hp)
            return self.commands.collect()

        # Select goal for mining
        goal = junk_position[0]
        for deposit in junk_position:
            if self.get_path_length(position, deposit) < self.get_path_length(position, goal):
                goal = deposit

        # Move towards goal
        direction = self.my_pathfinder.get_next_direction(self.character_state['location'], goal)
        if direction:
            self.end_turn_routine(hp)
            return self.commands.move(direction)
        else:
            self.end_turn_routine(hp)
            return self.commands.idle()


class MyPathfinder(Pathfinder):

    def __init__(self):
        super().__init__()

    def create_graph(self, game_map):
        graph = nx.Graph()
        size_x = len(game_map[0])
        size_y = len(game_map)
        for y in range(size_y):
            for x in range(size_x):
                graph.add_node((y, x))

        for y in range(size_y - 1):
            for x in range(size_x - 1):
                symbol = game_map[y][x]
                if symbol.can_pass_through() or self._is_start_or_goal((y, x)):
                    right_symbol = game_map[y][x + 1]
                    weight = 5 if right_symbol == ObjectSymbols.SPIKE else 1
                    if right_symbol.can_pass_through() or self._is_start_or_goal((y, x + 1)):
                        graph.add_edge((y, x), (y, x + 1), weight=weight)

                    bottom_symbol = game_map[y + 1][x]
                    weight = 5 if bottom_symbol == ObjectSymbols.SPIKE else 1
                    if bottom_symbol.can_pass_through() or self._is_start_or_goal((y + 1, x)):
                        graph.add_edge((y, x), (y + 1, x), weight=weight)

        return graph

    def get_next_direction(self, start, goal):
        self.start = start
        self.goal = goal
        graph = self.create_graph(self.game_map)
        path = dijkstra_path(graph, start, goal)
        direction = self.convert_node_to_direction(path)
        return direction

    def get_path_length(self, start, goal):
        self.start = start
        self.goal = goal
        graph = self.create_graph(self.game_map)
        length = dijkstra_path_length(graph, start, goal)
        return length
