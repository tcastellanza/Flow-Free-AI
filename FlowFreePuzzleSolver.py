from copy import deepcopy

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class FlowFreeSolver:
    def __init__(self, size, color_positions):
        self.size = size
        # Filter out colors with no detected positions
        self.color_positions = {
            color: positions for color, positions in color_positions.items() if positions
        }
        # Create empty grid
        self.grid = [[None for _ in range(size)] for _ in range(size)]

        # Mark start and end points and add to grid
        self.endpoints = set()
        for color, (start, end) in self.color_positions.items():
            self.grid[start[0]][start[1]] = color
            self.grid[end[0]][end[1]] = color
            self.endpoints.add(start)

    def is_valid(self, x, y, target):
        # Valid if within bounds, empty or it's the target
        return (0 <= x < self.size and 0 <= y < self.size and
                (self.grid[x][y] is None or (x, y) == target))

    def solve(self):
        colors = list(self.color_positions.keys())
        return self.backtrack(colors, 0)

    def backtrack(self, colors, index):
        if index == len(colors):
            return self.is_complete()

        color = colors[index]
        start, end = self.color_positions[color]
        return self.dfs(start[0], start[1], end, color, set(), colors, index)

    def dfs(self, x, y, end, color, visited, colors, index):
        if (x, y) == end:
            return self.backtrack(colors, index + 1)

        visited.add((x, y))
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny, end) and (nx, ny) not in visited:
                # Save previous value to backtrack
                prev = self.grid[nx][ny]
                if (nx, ny) != end:
                    self.grid[nx][ny] = color

                if self.dfs(nx, ny, end, color, visited, colors, index):
                    return True

                if (nx, ny) != end:
                    self.grid[nx][ny] = prev

        visited.remove((x, y))
        return False

    def is_complete(self):
        # All cells must be filled
        return all(all(cell is not None for cell in row) for row in self.grid)

    def print_grid(self):
        for row in self.grid:
            print(" ".join(cell[0].upper() if cell else '.' for cell in row))
        print()

if __name__ == "__main__":
    # Example usage with potential missing color (orange)
    detected_positions_example = {
    'red': [(4, 0), (3, 2)],
    'green': [(3, 1), (2, 2)],
    'blue': [(4, 4), (3, 0)],
    'yellow': [(3, 4), (0, 0)],
    'orange': [],
}

    solver = FlowFreeSolver(5, detected_positions_example)

    print("Solving:")
    if solver.solve():
        print("✅ Solution found:")
        solver.print_grid()
    else:
        print("❌ No solution found.")

""" # ------------------------------
# Test with your exact grid input
# ------------------------------
color_positions = {
    'red':    [(0, 0), (4, 1)],
    'green':  [(0, 2), (3, 1)],
    'blue':   [(1, 2), (4, 2)],
    'yellow': [(0, 4), (3, 3)],
    'orange': [(4, 3), (1, 4)],
}

solver = FlowFreeSolver(5, color_positions)

if solver.solve():
    print("✅ Solution found:")
    solver.print_grid()
else:
    print("❌ No solution found.")

 """