from unittest import TestCase
from SnakeAi.snake_engine.engine import Engine, Snake


class TestSnake(TestCase):
    def test_gen_tail(self):
        t_tail = Snake.gen_tail(0, 0, length=10)
        print(t_tail)
        self.assertEqual(len(t_tail), 10, "snake tail correct length")

    def test_turn_left(self):
        s = Snake()
        self.assertEqual(s.direction, 0)
        s.turn_left()
        self.assertEqual(s.direction, 1)
        s.turn_left()
        self.assertEqual(s.direction, 2)
        s.turn_left()
        self.assertEqual(s.direction, 3)
        s.turn_left()
        self.assertEqual(s.direction, 0)

    def test_turn_right(self):
        s = Snake()
        self.assertEqual(s.direction, 0)
        s.turn_right()
        self.assertEqual(s.direction, 3)
        s.turn_right()
        self.assertEqual(s.direction, 2)
        s.turn_right()
        self.assertEqual(s.direction, 1)
        s.turn_right()
        self.assertEqual(s.direction, 0)


class TestEngine(TestCase):
    def test_add_food(self):
        e = Engine()
        # fill up game with food until false
        while e.add_food():
            pass
        self.assertEqual(96, len(e.food))  # exactly 96 food for all space, 100 spaces - 4 for snake = 96

