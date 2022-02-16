import os

import numpy as np


class Board:

    def __init__(self,
        rows: int = 3,
        cols: int = 3,
    ) -> None:
        self.rows = rows
        self.cols = cols
        self._board = np.zeros((self.rows, self.cols), dtype=np.intc)

    def __hash__(self) -> int:
        res = self._board.reshape(self.rows * self.cols)
        res_sum = int(sum(res))
        return res_sum

    def __str__(self) -> str:
        # p1: x  p2: o
        res: str = ""
        for i in range(0, self.rows):
            res += '-------------' + os.linesep
            out = '| '
            for j in range(0, self.cols):
                if self._board[i, j] == 1:
                    token = 'x'
                elif self._board[i, j] == -1:
                    token = 'o'
                elif self._board[i, j] == 0:
                    token = ' '
                else:
                    raise ValueError(self._board, i, j)
                out += token + ' | '
            res += out + os.linesep
        res += '-------------' + os.linesep
        return res

    def reset(self) -> "Board":
        board = Board(self.rows, self.cols)
        return board

    def copy(self) -> "Board":
        _board = self._board.copy()
        board = Board(self.rows, self.cols)
        board._board = _board
        return board

    def get(self, position: tuple[int, int]) -> int:
        """Get the value of the board position"""
        return self._board[position]

    def set(self, position: tuple[int, int], value: int) -> None:
        """Update the position on the board with a player's value."""
        self._board[position] = value

    def calculate_winner(self):
        """Calculate who the winner of the board is."""
        # row
        for i in range(self.rows):
            if sum(self._board[i, :]) == 3:
                self.is_end = True
                return 1
            if sum(self._board[i, :]) == -3:
                self.is_end = True
                return -1
        # col
        for i in range(self.cols):
            if sum(self._board[:, i]) == 3:
                self.is_end = True
                return 1
            if sum(self._board[:, i]) == -3:
                self.is_end = True
                return -1
        # diagonal
        diag_sum1 = sum([self._board[i, i] for i in range(self.cols)])
        diag_sum2 = sum([self._board[i, self.cols - i - 1] for i in range(self.cols)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.is_end = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        # tie
        # no available positions
        if len(self.list_available_positions()) == 0:
            self.is_end = True
            return 0
        # not end
        self.is_end = False
        return None
    
    def list_available_positions(self) -> list[tuple[int, int]]:
        """List all available positions on the board."""
        positions: list[tuple[int, int]] = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self._board[i, j] == 0:
                    positions.append((i, j))  # need to be tuple
        return positions
