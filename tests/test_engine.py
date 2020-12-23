from unittest import TestCase
from snake_engine.engine import Engine, Snake


class TestEngine(TestCase):
    def test_gen_world(self):
        t_world = Engine.gen_world(10, 10)
        self.assertEqual(len(t_world), 10, "Array wrong height")
        self.assertEqual(len(t_world[0]), 10, "Array wrong width")


class TestSnake(TestCase):
    def test_gen_tail(self):
        t_tail = Snake.gen_tail(0,0,length=10)
        self.assertEqual(len(t_tail), 10, "snake tail correct length")
