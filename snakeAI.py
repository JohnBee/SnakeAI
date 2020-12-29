import argparse
from snake_engine.pygame_screen import run_display
from AI.q_learning import run_q_learn


def run(args):
    should_learn = True if args.learn is not None else False
    if not args.display:
        run_display(args.learn, args.learn)
    else:
        run_q_learn(args.learn, args.learn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Q-Learning Agent that learns to play the game Snake")
    parser.add_argument('--learn', dest="learn", type=int, help="The number of episodes (games) for the Snake to learn from (default 100000). If not specified will use prelearnt Q-table instead.", default=None)
    parser.add_argument('--no-display', dest="display", action="store_true", help="Do not use Pygame to display the final Snake gameplay.", default=False)
    args = parser.parse_args()
    run(args)