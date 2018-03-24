from src.bot.Bot import Bot
from src.utils.Pathfinder import Pathfinder


class Bot2(Bot):

    def __init__(self):
        super().__init__()
        self.counter = 0

    def get_name(self):
        # Find a name for your bot
        return 'Invader2'

    def turn(self, game_state, character_state, other_bots):
        # Your bot logic goes here
        super().turn(game_state, character_state, other_bots)

        # # Find the position of the junk on the map
        # junk_position = list()
        # c = r = 0
        # for row in game_state.splitlines():
        #     if 'J' in row:
        #         for column in row:
        #             if 'J' == column:
        #                 pos = (r, c)
        #                 junk_position.append(pos)
        #             c += 1
        #     r += 1
        #     c = 0
        #
        # # print(game_state)
        #
        # # print(other_bots)
        # goal = junk_position[2]
        #
        # direction = self.pathfinder.get_next_direction(self.character_state['location'], goal)
        # if direction:
        #     return self.commands.move(direction)
        # else:
        #     return self.commands.idle()
        if self.counter < 2:
            return self.commands.move('N')
        return self.commands.attack('W')



class MyPathfinder(Pathfinder):
    pass
