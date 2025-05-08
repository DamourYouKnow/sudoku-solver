class Sudoku:
    grid: list[int | None]=[]
    candidates: list[list[int]] = []

    def __init__(
        self, 
        grid: list[int | None],
        candidates: list[list[int]] = None
    ):
        self.grid = [value for value in grid]
        
        if candidates:
             self.candidates =  [
                cell_candidates.copy() for cell_candidates in candidates
            ]
        else:
            for index in range(0, len(self.grid)):
                if self.grid[index] is None:
                    self.candidates.append(list(range(1, 10)))
                else:
                    self.candidates.append([self.grid[index]])

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

            if not current in visited:
                visited.add(current)

                if current.is_solved():
                    solutions.append(current)
                    return solutions
                else:
                    for next_option in current.expand_options():
                        stack.append(next_option)

        return solutions

    def expand_options(self) -> list['Sudoku']:
        options: list['Sudoku'] = []
        
        for x in range(0, 9):
            for y in range(0, 9):
                if self.at(x, y) is not None:
                    continue

                index = self.coordinate_to_index(x, y)        
                for candidate in self.candidates[self.coordinate_to_index(x, y)]:
                    option = Sudoku(self.grid, self.candidates)
                    option.grid[index] = candidate
                    option.candidates[index] = [candidate]
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

                    self.candidates[index] = [
                        value for value in self.candidates_at(x, y)
                    ]

                    # No valid option for cell, solution invalidated
                    if len(self.candidates[index]) == 0:
                        return None
                    # Only one possible option, place value
                    elif len(self.candidates[index]) == 1:    
                        value = self.candidates[index][0]  
                        self.grid[index] = value
                        self.candidates[index] = [value]
                        continue_reducing = True

                    # Scan rows, columns, and subgrids for candidates that 
                    # are not a candidate anywhere else
                    row_indices = self.row_indices(y)
                    column_indices = self.column_indices(x)
                    subgrid_indices = self.subgrid_indices(x, y)

                    row_indices.remove(index)
                    column_indices.remove(index)
                    subgrid_indices.remove(index)

                    row_candidates = set(merge_lists([
                        self.candidates[index] for index in row_indices
                    ]))

                    column_candidates = set(merge_lists([
                        self.candidates[index] for index in column_indices
                    ]))

                    subgrid_candidates = set(merge_lists([
                        self.candidates[index] for index in subgrid_indices
                    ]))

                    for value in range(1, 10):
                        only_candidate = (value not in row_candidates) \
                            or (value not in column_candidates) \
                            or (value not in subgrid_candidates)
                        
                        if only_candidate:
                            self.grid[index] = value
                            self.candidates[index] = [value]
                            continue_reducing = True

        return self
                    
    def is_solved(self):
        return not any(value is None for value in self.grid)

    def at(self, x: int, y: int) -> int | None:
        index = self.coordinate_to_index(x, y)
        if index < 0 or index >= len(self.grid):
            return None
        else:
            return self.grid[index]
        
    def candidates_at(self, x: int, y: int) -> list[int]:
        if self.at(x, y) is not None:
            return [self.at(x, y)]

        options = list(range(1, 10))

        # Eliminations
        invalid_options = list(
            set(self.in_row(y) + self.in_column(x) + self.in_subgrid(x, y))
        )

        for value in invalid_options:
            options.remove(value)

        return options
    
     
    def coordinate_to_index(self, x: int, y: int):
        return (y * 9) + x
    
    def index_to_coordinate(self, index: int) -> tuple[int, int]:
        return (index // 9, index % 9)
        
    def in_row(self, y: int) -> list[int]:
        return [value for value in self.row(y) if value]

    def in_column(self, x: int) -> list[int]:
        return [value for value in self.column(x) if value]

    def in_subgrid(self, x: int, y: int) -> list[int]:
        return [value for value in self.subgrid(x, y) if value]
    
    def row_indices(self, y: int) -> list[int]:
        return list(range(y * 9, (y * 9) + 9))
    
    def column_indices(self, x: int) -> list[int]:
        return list(range(x, len(self.grid), 9))
    
    def subgrid_indices(self, x: int, y: int) -> list[int]:
        start_x, start_y = 3 * (x // 3), 3 * (y // 3)
        end_x, end_y = start_x + 3, start_y + 3     
        return [
            self.coordinate_to_index(x, y) for x in range(start_x, end_x) \
                for y in range(start_y, end_y)
        ]
    
    def row(self, y: int) -> list[int]:
        return self.grid[y * 9 : (y * 9) + 9]

    def column(self, x: int) -> list[int]:
        return [self.grid[index] for index in self.column_indices(x)]

    def subgrid(self, x: int, y: int) -> list[int]:
        return [self.grid[index] for index in self.subgrid_indices(x, y)]
    
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

    with open('puzzle-hard.txt', 'r') as file:
        lines = file.readlines()
    
        for line in lines:
            for value in line:
                if value == '.':
                    grid.append(None)
                elif value.isnumeric():
                    grid.append(int(value))

    return grid



def merge_lists(lists):
    result = []
    for list in lists:
        for value in list:
            result.append(value)

    return result


if __name__ == "__main__":
    sudoku = Sudoku(read_puzzle()) 
    print(f'Puzzle input\n{str(sudoku)}') 
    solutions = sudoku.solve()

    i = 1
    for solution in solutions:
        print(f'Solution {str(i)}\n{str(solution)}')
        i += 1 
