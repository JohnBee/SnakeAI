class Engine:
    def __init__(self, world_width = 10, world_height = 10):
        ## Generate empty world
        self.world = self.gen_world(world_width, world_height)
        ## Initialise the snake
        self.snake = Snake(int(world_width)/2, int(world_height)/2, 3)

    @staticmethod
    def gen_world(width, height):
        world_out = ["."*width]*height
        return world_out


class Snake:
    def __init__(self, pos_x=0, pos_y=0, length=3):
        self.head_x = pos_x
        self.head_y = pos_y

        # init tail of given length
        self.tail = self.gen_tail(self.head_x, self.head_y, length)

    @staticmethod
    def gen_tail(head_x, head_y, length=3):
        return [(x, head_y) for x in range(head_x, head_x-length, -1)]
