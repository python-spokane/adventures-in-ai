from typing import Optional

from .board import Board
from .players import Player

BOARD_ROWS = 3
BOARD_COLS = 3


class State:
    def __init__(self,
        p1: Player,
        p2: Player,
        board: Optional[Board] = None,
    ):
        self.board = board or Board()
        self.p1 = p1
        self.p2 = p2
        self.is_end = False
        self.board_hash: Optional[str] = None
        # init p1 plays first
        self.player_symbol: int = 1

    def update(self, position: tuple[int, int]):
        self.board.set(position, self.player_symbol)
        # switch to another player
        self.player_symbol = -1 if self.player_symbol == 1 else 1

    # only when game ends
    def give_reward(self):
        result = self.board.calculate_winner()
        # backpropagate reward
        if result == 1:
            self.p1.feed_reward(1)
            self.p2.feed_reward(0)
        elif result == -1:
            self.p1.feed_reward(0)
            self.p2.feed_reward(1)
        else:
            self.p1.feed_reward(0.1)
            self.p2.feed_reward(0.5)

    # board reset
    def reset(self):
        self.board = self.board.reset()
        self.board_hash = None
        self.is_end = False
        self.player_symbol = 1

    def train(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            while not self.is_end:
                # Player 1
                positions = self.board.list_available_positions()
                p1_action = self.p1.choose_action(positions, self.board, self.player_symbol)
                # take action and upate board state
                self.update(p1_action)
                board_hash = hash(self.board)
                self.p1.add_state(board_hash)
                # check board status if it is end

                win = self.board.calculate_winner()
                if win is not None:
                    # self.show_board()
                    # ended with p1 either win or draw
                    self.give_reward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.board.list_available_positions()
                    p2_action = self.p2.choose_action(positions, self.board, self.player_symbol)
                    self.update(p2_action)
                    board_hash = hash(self.board)
                    self.p2.add_state(board_hash)

                    win = self.board.calculate_winner()
                    if win is not None:
                        # self.show_board()
                        # ended with p2 either win or draw
                        self.give_reward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    # play with human
    def play(self):
        while not self.is_end:
            # Player 1
            positions = self.board.list_available_positions()
            p1_action = self.p1.choose_action(positions, self.board, self.player_symbol)
            # take action and upate board state
            self.update(p1_action)
            self.show_board()
            # check board status if it is end
            win = self.board.calculate_winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.board.list_available_positions()
                p2_action = self.p2.choose_action(positions, self.board, self.player_symbol)

                self.update(p2_action)
                self.show_board()
                win = self.board.calculate_winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def show_board(self):
        print(self.board)
