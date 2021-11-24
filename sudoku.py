from __future__ import annotations
from typing import Iterable, ValuesView


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: list[list[int]] = []
        self._grid_column: list[list[int]] = []
        self._grid_block: list[list[int]] = []
        self._zeroes: list[list[int]] = []
        self._count: int = 0

        # Save sudoku row wise
        for puzzle_row in puzzle:
            row = []
            for element in puzzle_row:
                row.append(int(element))
            self._grid.append(row)
        
        # Save sudoku column wise
        for i in range(9):
            column = []
            for row in self._grid:
                column.append(row[i])   
            self._grid_column.append(column)

        # Save sudoku block wise
        for i in range(9):
            x_start = (i % 3) * 3
            y_start = (i // 3) * 3
            block = []
            for x in range(x_start, x_start + 3):
                for y in range(y_start, y_start + 3):
                    block.append(self._grid[y][x])
            self._grid_block.append(block)
        
        # Save location of 0 values
        for x in range(9):
            for y in range(9):
                if self._grid[y][x] == 0:
                    self._zeroes.append([y, x])

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y][x] = value
        self._grid_column[x][y] = value

        block_value = x // 3 + y // 3 * 3
        block_index = x % 3 * 3 + y % 3
        self._grid_block[block_value][block_index] = value

        self._count += 1

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[y][x] = 0
        self._grid_column[x][y] = 0

        block_value = x // 3 + y // 3 * 3
        block_index = x % 3 * 3 + y % 3
        self._grid_block[block_value][block_index] = 0

        self._count -= 1

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""

        return self._grid[y][x]

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the row, column and block
        remaining = list(options - set(self.row_values(y)) - set(self.column_values(x)) - set(self.block_values(block_index)))

        return remaining

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """        
        while self._count < len(self._zeroes):
            next = self._zeroes[self._count]
            return next[1], next[0]

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""

        return self._grid[i]

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""

        return self._grid_column[i]

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """

        return self._grid_block[i]

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