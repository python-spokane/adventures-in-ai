import logging
import sys

from .game import State
from .players import ComputerPlayer, HumanPlayer


logging.getLogger().setLevel(logging.DEBUG)


if __name__ == "__main__":
    try:
        command: str = sys.argv[1]
    except IndexError:
        command: str = ""

    if command == "train":
        p1 = ComputerPlayer("computer")
        p2 = ComputerPlayer("")
        st = State(p1, p2)
        print("training...")
        st.train(5000)
        p1.save_policy()

    elif command == "play":
        p1 = ComputerPlayer("computer", exp_rate=0)
        p1.load_policy()
        p2 = HumanPlayer("human")
        st = State(p1, p2)
        st.play()

    else:
        print("Available commands include: play, train")
