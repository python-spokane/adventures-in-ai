import logging
import pickle
from typing import Optional, Protocol

import numpy as np

from .board import Board


class Player(Protocol):
    name: str

    def choose_action(self,
        positions: list[tuple[int, int]],
        current_board: "Board",
        symbol: int,
    ) -> tuple[int, int]:
        ...

    def add_state(self, state):
        ...

    def feed_reward(self, reward):
        ...

    def reset(self):
        ...


class ComputerPlayer(Player):
    def __init__(self,
        name: str,
        exp_rate: float = 0.3
    ):
        self.name: str = name
        self.states: list = []  # record all positions taken
        self.lr: float = 0.2
        self.exp_rate: float = exp_rate
        self.decay_gamma: float = 0.9
        self.states_value: dict[int, float] = {}  # state -> value

    def choose_action(self,
        positions: list[tuple[int, int]],
        current_board: Board,
        symbol: int
    ):
        """Choose the next move to make."""
        action = None
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board.set(p, symbol)
                next_boardHash = hash(current_board)
                value = self.states_value.get(next_boardHash, 0)
                # print("value", value)
                if value >= value_max:
                    value_max = value
                    action = p
        if action is None:
            raise ValueError("action is None")
        logging.debug("{} takes action {}".format(self.name, action))
        return action

    def add_state(self, state):
        """Append a hash state."""
        self.states.append(state)

    def feed_reward(self, reward):
        """At the end of game, backpropagate and update states value."""
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def save_policy(self, policy_name: Optional[str] = None) -> None:
        """Save computer"""
        policy_name = self._generate_policy_name()
        with open(policy_name, 'wb') as fw:
            pickle.dump(self.states_value, fw)

    def load_policy(self, policy_name: Optional[str] = None) -> None:
        policy_name = self._generate_policy_name()
        with open(policy_name, 'rb') as fr:
            self.states_value = pickle.load(fr)

    def _generate_policy_name(self) -> str:
        return f"policy_{self.name}"


class HumanPlayer(Player):

    def __init__(self, name):
        self.name = name

    def choose_action(self,
        positions: list[tuple[int, int]],
        current_board: "Board",
        symbol: int,
    ) -> tuple[int, int]:
        while True:
            row = int(input("Input your action row:"))
            col = int(input("Input your action col:"))
            action = (row, col)
            if action in positions:
                return action

    # append a hash state
    def add_state(self, state):
        pass

    # at the end of game, backpropagate and update states value
    def feed_reward(self, reward):
        pass

    def reset(self):
        pass
