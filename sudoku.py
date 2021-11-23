from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: list[int] = []

        for puzzle_row in puzzle:
            row = []
            for element in puzzle_row:
                row.append(int(element))

            self._grid.append(row)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y][x] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[y][x] = 0

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        return self._grid[y][x]

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the row, column and block
        options = list(options - set(self.row_values(y)) - set(self.column_values(x)) - set(self.block_values(block_index)))

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        for y in range(9):
            for x in range(9):
                if self._grid[y][x] == 0 and next_x == -1 and next_y == -1:
                    next_x, next_y = x, y
                    return next_x, next_y

        return next_x, next_y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        return self._grid[i]

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        values = []

        for row in self._grid:
            values.append(row[i])

        return values

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.append(self._grid[y][x])
        
        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        for i in range(9):
            if values != set(self.column_values(i)):
                return False

            if values != set(self.row_values(i)):
                return False

            if values != set(self.block_values(i)):
                return False

        return True

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            for elem in row:
                representation += str(elem)
            representation += "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")
            puzzle.append(line)

    return Sudoku(puzzle)
