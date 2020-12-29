from random import uniform, randint
from snake_engine.engine import Engine
import json
from pathlib import Path

q_table_path = Path("AI/q_table.json")


def argmax(in_list):
    max_val = max(in_list)
    for i in range(len(in_list)):
        if in_list[i] == max_val:
            return i


class QLearning:
    def __init__(self, engine, epochs=10000):
        self.e = engine
        self.learning_epochs = epochs
        self.qtable = {}
        self.initialise_q_table()

    def initialise_q_table(self):
        x = ["0", "1"]
        food_dir = ["0","1","2"]
        dir = ["0","1","2","3"]
        all_possible_states = [a+b+c+d+e+f for a in food_dir for b in food_dir for c in x for d in x for e in x for f in dir]
        for state in all_possible_states:
            self.qtable[state] = [0, 0, 0] # go forward, turn left, turn right

    def get_state_str(self):
        '''
        Generates a string to be used in the state action Q-table
        :return: a tuple containing the state str and a boolean stating if the game has ended or not
        '''
        # information used in a state:
        # food above or below
        # food left or right
        # danger above, left, right, or below
        head = self.e.snake.head
        food = self.e.food[0]
        direction = self.e.snake.direction
        body = self.e.snake.body

        if head[1] < food[1]:
            food_below = 1
        elif head[1] == food[1]:
            food_below = 2
        else:
            food_below = 0

        if head[0] < food[0]:
            food_right = 1
        elif head[0] == food[0]:
            food_right = 2
        else:
            food_right = 0



        # get danger ahead, left, or right
        check_spaces = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        forward = (head[0] + check_spaces[direction][0], head[1] + check_spaces[direction][1])
        left = (head[0] + check_spaces[(direction + 1) % 4][0], head[1] + check_spaces[(direction + 1) % 4][1])
        right = (head[0] + check_spaces[(direction - 1) % 4][0], head[1] + check_spaces[(direction - 1) % 4][1])

        danger_forward = 0
        danger_left = 0
        danger_right = 0

        if forward in body or forward[0] < 0 or forward[0] > 9 or forward[1] < 0 or forward[1] > 9:
            danger_forward = 1

        if left in body or left[0] < 0 or left[0] > self.e.world_width-1 or left[1] < 0 or left[1] > self.e.world_height-1:
             danger_left = 1

        if right in body or right[0] < 0 or right[0] > self.e.world_width-1 or right[1] < 0 or right[1] > self.e.world_height-1:
            danger_right = 1

        danger_str = str(danger_forward) + str(danger_left) + str(danger_right)

        return str(food_below) + str(food_right) + danger_str + str(direction),  self.e.game_end

    def q_learn_loop(self):

        discount_factor_gamma = 0.8
        learning_rate_alpha = 0.7
        greedy_policy_epsilon = 0.2
        print(f"Learning for {self.learning_epochs} epochs")

        for episode in range(self.learning_epochs):
            self.e.reset()
            state, game_over = self.get_state_str()
            while not game_over:
                if uniform(0, 1) <= greedy_policy_epsilon:
                    # explore
                    action = randint(0, 2)  # 0 go forward, 1 turn left, 2 turn right
                else:
                    # exploit
                    action = argmax(self.qtable[state])  # choose highest reward state

                reward = self.e.make_move(action)
                next_state, game_over = self.get_state_str()
                if game_over:
                    reward = -10

                old_qval = self.qtable[state][action]
                max_qreward = max(self.qtable[next_state])

                new_qval = (1-learning_rate_alpha) * old_qval + learning_rate_alpha * (reward + discount_factor_gamma * max_qreward)
                self.qtable[state][action] = new_qval
                state = next_state

            if episode % (self.learning_epochs / 10) == 0:
                print(f"{((episode*100)//self.learning_epochs)}%")

        print("Training done")

    def q_step_snake(self):
        state, game_over = self.get_state_str()
        action = argmax(self.qtable[state])
        reward = self.e.make_move(action)
        next_state, game_over = self.get_state_str()
        state = next_state
        return state, game_over

    def q_play_snake(self):
        self.e.reset()
        state, game_over = self.get_state_str()
        self.e.pretty_print_world()
        while not game_over:
            state, game_over = self.q_step_snake()
            self.e.pretty_print_world()

    def export_q_table(self):
        with open(q_table_path, 'w') as f:
            js = json.dump(self.qtable, f)
        print("exporting table")

    def load_q_table(self):
        with open(q_table_path, "r") as f:
            self.qtable = json.load(f)
        print("loading table")


def run_q_learn(episodes, learn):
    e = Engine()
    q = QLearning(e, epochs=episodes)
    if learn:
        q.q_learn_loop()
        q.export_q_table()
    else:
        q.load_q_table()