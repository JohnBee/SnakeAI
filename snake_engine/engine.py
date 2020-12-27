from random import randint


class Engine:
    def __init__(self, world_width=10, world_height=10):
        '''
        Initialise the snake engine where all game operations will take place.

        :param world_width: Width of the game world the snake should roam
        :param world_height: Height of the game world the snake should roam
        '''

        self.world_width = world_width
        self.world_height = world_height
        self.food = []

        ## Initialise the snake
        self.snake = Snake(world_width // 2, world_height // 2, 4)
        self.score = 0
        self.game_end = False

        # place the first piece of food
        self.add_food()

    def reset(self):
        self.food = []

        ## Initialise the snake
        self.snake = Snake(self.world_width // 2, self.world_height // 2, 4)
        self.score = 0
        self.game_end = False

        # place the first piece of food
        self.add_food()

    def make_move(self, input_move):
        old_head = (self.snake.head[0], self.snake.head[1])

        if input_move == 0:
            self.snake.move_forward(self)
        elif input_move == 1:
            self.snake.turn_left(self)
        elif input_move == 2:
            self.snake.turn_right(self)

        # add food if it's been eaten
        reward = 0
        if not self.food:
            self.score += 1
            reward += 10
            if not self.add_food():
                self.game_end

        # return reward for making this move
        # if closer to food, increase reward, else decrease
        new_head = (self.snake.head[0], self.snake.head[1])
        food = (self.food[0][0], self.food[0][1])
        # taxicab geometry
        old_dist = abs(food[0] - old_head[0]) + abs(food[1] - old_head[1])
        new_dist = abs(food[0] - new_head[0]) + abs(food[1] - new_head[1])

        if new_dist < old_dist:
            reward += 1
        else:
            reward -= 1

        return reward

    def export_game_state(self):
        '''
        Exports the game state
        :return: a dictionary with set values representing the game state
        '''
        return {"score": self.score,
                "world_width": self.world_width,
                "world_height": self.world_height,
                "food": self.food,
                "snake_direction": self.snake.direction,
                "snake_body": self.snake.body,
                "snake_head": self.snake.head,
                "snake_size": self.snake.length,
                "game_end": self.game_end}

    def import_game_state(self, game_state):
        '''
        Import a game state to load
        :param game_state: a dictionary with the defined
        :return: True or false depending on if it was successful in loading the game state
        '''
        try:
            self.score = game_state["score"]
            self.world_width = game_state["world_width"]
            self.world_height = game_state["world_height"]
            self.food = game_state["food"]
            self.snake.body = game_state["snake_body"]
            self.snake.head = game_state["snake_head"]
            self.snake.direction = game_state["snake_direction"]
            self.snake.length = game_state["snake_length"]
            self.game_end = game_state["game_end"]

        except KeyError as error:
            print("Missing game state argument!")
            print(error)
            return False
        return True

    def add_food(self):
        '''
        Add food to the game world, possible locations are only where the snake isn't
        :return: True or False depending if food was able to be added, if it false then the game must be complete.
        '''
        possible_locations = [(x, y) for x in range(self.world_width) for y in range(self.world_height)]
        for s_not_possible in self.snake.body + self.food:
            if s_not_possible in possible_locations:
                possible_locations.remove(s_not_possible)

        if not possible_locations:
            return False
        else:
            # select a possible location
            self.food.append(possible_locations[randint(0, len(possible_locations) - 1)])
            return True

    def output_world(self):
        '''
        Output the game world as a list of list of characters to the parsed by AI or printed
        :return:
        '''
        out = []
        for y in range(self.world_height):
            out.append([])
            for x in range(self.world_width):
                if (x, y) not in self.food and (x, y) not in self.snake.body:
                    out[-1].append(".")
                elif (x, y) in self.food:
                    out[-1].append("o")
                elif (x, y) in self.snake.body:
                    if (x, y) == self.snake.body[0]:
                        if self.snake.direction == 0:
                            out[-1].append(">")
                        if self.snake.direction == 1:
                            out[-1].append("^")
                        if self.snake.direction == 2:
                            out[-1].append("<")
                        if self.snake.direction == 3:
                            out[-1].append("v")
                    else:
                        out[-1].append("#")
        return out

    def pretty_print_world(self):
        for y in self.output_world():
            print(" ".join(y))


class Snake:
    def __init__(self, pos_x=0, pos_y=0, length=3):
        # init tail of given length
        self.head = (pos_x, pos_y)
        self.direction = 0  # 0 = right, 1 = up, 2 = left, 3 = down
        self.length = length
        self.body = self.gen_tail(pos_x, pos_y, self.length)

    def turn_left(self, engine):
        self.direction = (self.direction + 1) % 4
        self.move_forward(engine)

    def turn_right(self, engine):
        self.direction = (self.direction - 1) % 4
        self.move_forward(engine)

    def move_forward(self, engine):
        if self.direction == 0:
            self.body = [(self.head[0] + 1, self.head[1])] + self.body
        elif self.direction == 1:
            self.body = [(self.head[0], self.head[1] - 1)] + self.body
        elif self.direction == 2:
            self.body = [(self.head[0] - 1, self.head[1])] + self.body
        elif self.direction == 3:
            self.body = [(self.head[0], self.head[1] + 1)] + self.body

        # check if head not on food then don't increase snake length
        if self.body[0] not in engine.food:
            self.body.pop()
        else:
            # eat the food
            engine.food.remove(self.body[0])
            engine.score += 1
        self.head = self.body[0]

        # check if dead
        if len([a for a in self.body if a == self.head]) > 1:
            engine.game_end = True
        if self.head[1] < 0 or self.head[0] < 0 or self.head[0] >= engine.world_width or self.head[1] >= engine.world_height:
            engine.game_end = True

    @staticmethod
    def gen_tail(head_x, head_y, length=3):
        return [(x, head_y) for x in range(head_x, head_x - length, -1)]


def play_game():
    e = Engine()
    # draw game state
    while not e.game_end:
        e.pretty_print_world()
        move = None
        while move is None:
            move = int(input("Enter 0 or 1 or 2 for no change, turn left or turn right: "))
            if move in [0,1,2]:
                e.make_move(move)
            else:
                print(f"Invalid move: {move}")
                move = None

if __name__ == "__main__":
    play_game()
