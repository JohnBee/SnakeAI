import pygame
from SnakeAi.snake_engine.engine import Engine
from SnakeAi.AI.q_learning import QLearning
import sys


class snake_screen_controller:
    def __init__(self, screen, learn=True, learn_epochs=100000):
        self.e = Engine()
        self.q = QLearning(self.e, learn_epochs)
        if learn:
            self.do_qlearning()
            self.q.export_q_table()
        else:
            self.q.load_q_table()
        self.screen = screen

    def do_qlearning(self):
        self.q.q_learn_loop()

    def draw_scene(self):
        env = self.e.output_world()
        self.screen.fill((0, 0, 0))  # fill screen black
        for y in range(len(env)):
            for x in range(len(env[y])):
                if (x, y) in self.e.snake.body:
                    i = self.e.snake.body.index((x,y))
                    # 100 -> 255
                    scale = 155/len(self.e.snake.body)
                    col = i*scale
                    pygame.draw.rect(screen, (0, 255-col, 0),(x*50, y*50, 50, 50))
                if (x, y) in self.e.food:
                    pygame.draw.rect(screen, (255, 0, 0), (x * 50, y * 50, 50, 50))
                if (x,y) == self.e.snake.head:
                    pygame.draw.rect(screen, (00, 255, 00), (x * 50, y * 50, 50, 50))

        pygame.display.flip()

    def main_event_loop(self):
        self.e.reset()
        game_over = False
        clock = pygame.time.Clock()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.event.pump()
            self.draw_scene()
            state, game_over = self.q.q_step_snake()

            clock.tick(10)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    scc = snake_screen_controller(screen, False, 100000)
    scc.main_event_loop()
    #pygame.quit()
