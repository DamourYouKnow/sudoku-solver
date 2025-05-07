class Sudoku:
    grid: list[int | None]=[]
    options: list[set[int]] = []

    def __init__(self, grid):
        self.grid = [value for value in grid]
        self.options = [set(range(1, 10)) for _ in grid]

    # https://en.wikipedia.org/wiki/Depth-first_search
    def solve(self) -> 'Sudoku':
        solutions: list['Sudoku'] = []

        stack = [Sudoku(self.grid)]
        visited: set['Sudoku'] = set()
        while stack:
            current = stack.pop()
            current = current.reduce()

            if not current:
                continue

            print(f'Current\n{str(current)}')

            if current.is_solved():
                solutions.append(current)

            if not current in visited:
                visited.add(current)
                for next_option in current.expand_options():
                    stack.append(next_option)

        return solutions

    def expand_options(self) -> list['Sudoku']:
        options: list['Sudoku'] = []
        
        for x in range(0, 9):
            for y in range(0, 9):
                index = self.coordinate_to_index(x, y)        
                for cell_option in self.options_at(x, y):
                    option = Sudoku(self.grid)
                    option.grid[index] = cell_option
                    options.append(option)

        return options

    def reduce(self) -> 'Sudoku | None':
        continue_reducing = True

        while continue_reducing:
            continue_reducing = False

            for x in range(0, 9):
                for y in range(0, 9):
                    index = self.coordinate_to_index(x, y)

                    if self.at(x, y) is not None:
                        continue

                    to_remove = [
                        value for value in self.options[index] \
                            if value not in self.options_at(x, y) 
                    ]

                    for value in to_remove:
                        self.options[index].remove(value)

                    # No valid option for cell, solution invalidated
                    if len(self.options[index]) == 0:
                        return None
                    # Only one possible option, place value
                    elif len(self.options[index]) == 1:          
                        self.grid[index] = list(self.options[index])[0]
                        self.options[index] = set()
                        continue_reducing = True

                    # Scan rows, columns, and subgrids for options that
                    # only appear once

        return self
                    
    def is_solved(self):
        return not any(value is None for value in self.grid)

    def at(self, x: int, y: int) -> int | None:
        index = self.coordinate_to_index(x, y)
        if index < 0 or index >= len(self.grid):
            return None
        else:
            return self.grid[index]
        
    def options_at(self, x: int, y: int) -> list[int]:
        options = set(range(1, 10))

        # Eliminations
        invalid_options = self.in_row(y)
        invalid_options.update(self.in_column(x))
        invalid_options.update(self.in_subgrid(x, y))

        for value in invalid_options:
            options.remove(value)

        # Only options
        for values in range(1, 10):
            pass

        return options
     
    def coordinate_to_index(self, x: int, y: int):
        return (y * 9) + x
        
    def in_row(self, y: int) -> set[int]:
        return set(value for value in self.row(y) if value)

    def in_column(self, x: int) -> set[int]:
        return set(value for value in self.column(x) if value)

    def in_subgrid(self, x: int, y: int) -> set[int]:
        return set(value for value in self.subgrid(x, y) if value)

    def row(self, y: int) -> list[int]:
        return self.grid[y * 9 : (y * 9) + 9]

    def column(self, x: int) -> list[int]:
        return [self.grid[i] for i in range(x, len(self.grid), 9)]

    def subgrid(self, x: int, y: int) -> list[int]:
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
    print(f'Puzzle input\n{str(sudoku)}') 
    solutions = sudoku.solve()

    i = 1
    for solution in solutions:
        print(f'Solution {str(i)}\n{str(solution)}')
        i += 1 
