from random import randint

class Engine:
    def __init__(self, world_width = 10, world_height = 10):
        '''
        Initialise the snake engine where all game operations will take place.

        :param world_width: Width of the game world the snake should roam
        :param world_height: Height of the game world the snake should roam
        '''

        self.world_width = world_width
        self.world_height = world_height
        self.food = []

        ## Initialise the snake
        self.snake = Snake(world_width//2, world_height//2, 4)
        self.add_food()

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
            self.food.append(possible_locations[randint(0, len(possible_locations)-1)])
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
                    if(x, y) == self.snake.body[-1]:
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
        self.head = [(pos_x, pos_y)]
        self.direction = 0 # 0 = right, 1 = up, 2 = left, 3 = down
        self.body = self.gen_tail(pos_x, pos_y, length) + self.head

    @staticmethod
    def gen_tail(head_x, head_y, length=3):
        return [(x, head_y) for x in range(head_x, head_x-length, -1)]


if __name__ == "__main__":
    e = Engine()
    e.pretty_print_world()