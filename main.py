import itertools

class Sudoku:
    grid: list[int | None]=[]

    def __init__(self, grid):
        self.grid = grid

    def solve(self):
        while not self.is_solved():
            for x in range(0, 9):
                for y in range(0, 9):
                    print(f"({x}, {y})")

                    if self.at(x, y) is not None:
                        continue

                    options = set(range(1, 10))

                    invalid_options = self.in_row(y)
                    invalid_options.update(self.in_column(x))
                    invalid_options.update(self.in_subgrid(x, y))
                    print(f"Invalid {invalid_options}")

                    for value in invalid_options:
                        options.remove(value)

                    print(f"Valid {options}")
                    if len(options) == 0:
                        print("Invalid puzzle")
                        return
                    elif len(options) == 1:
                        index = self.coordinate_to_index(x, y)
                        self.grid[index] = list(options)[0]
                        print(self)
                    
    def is_solved(self):
        return not any(value is None for value in self.grid)

    def at(self, x, y) -> int | None:
        index = self.coordinate_to_index(x, y)
        if index < 0 or index >= len(self.grid):
            return None
        else:
            return self.grid[index]
        
    def coordinate_to_index(self, x, y):
        return (y * 9) + x
        
    def in_row(self, y) -> set[int]:
        return set(value for value in self.row(y) if value)

    def in_column(self, x) -> set[int]:
        return set(value for value in self.column(x) if value)

    def in_subgrid(self, x, y) -> set[int]:
        return set(value for value in self.subgrid(x, y) if value)

    def row(self, y) -> list[int]:
        return self.grid[y * 9 : (y * 9) + 9]

    def column(self, x) -> list[int]:
        return [self.grid[i] for i in range(x, len(self.grid), 9)]

    def subgrid(self, x, y) -> list[int]:
        start_x, start_y = 3 * (x // 3), 3 * (y // 3)
        end_x, end_y = start_x + 3, start_y + 3     
        return [
            self.at(x, y) for x in range(start_x, end_x) \
                for y in range(start_y, end_y)
        ]
    
    def matrix(self) -> list[list[int | None]]:
        return [
            self.grid[row_start : row_start + 9] \
                for row_start in range(0, len(self.grid), 9)
        ]
        
    def __repr__(self) -> str:
        return '\n'.join(
            ' '.join('.' if value is None else str(value) for value in row) \
                for row in self.matrix()
        )


    def __str__(self) -> str:
        return self.__repr__()


def read_puzzle() -> Sudoku:
    grid = []

    with open('puzzle.txt', 'r') as file:
        lines = file.readlines()
    
        for line in lines:
            for value in line:
                if value == '.':
                    grid.append(None)
                elif value.isnumeric():
                    grid.append(int(value))

    return grid


if __name__ == "__main__":
    sudoku = Sudoku(read_puzzle())
    print(sudoku)
    sudoku.solve()
    print(sudoku)
