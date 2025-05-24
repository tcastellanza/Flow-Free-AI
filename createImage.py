import cv2
from test import ColorGridDetector
from FlowFreePuzzleSolver import FlowFreeSolver

path = '/Users/tommasocastellanza/Flow Free AI/examples/IMG_5931.PNG'

# Reading the image
image = cv2.imread(path)

detector = ColorGridDetector(grid_size=(5, 5))
unscaledColorPositions = detector.detect_unscaled_colors(path)
scaledColourPositions = detector.detect_colors(path)

def colorPicker(colour):
    # colours in BGR
    if colour == 'red':
        return (0, 0, 255)
    elif colour == 'blue':
        return (255, 40, 9)
    elif colour == 'green':
        return (0, 140, 0)
    elif colour == 'yellow':
        return (0, 222, 236)
    elif colour == 'orange':
        return (0, 137, 248)
    else:
        return (0, 0, 0)

solver = FlowFreeSolver(5, scaledColourPositions)

print("Solving:")
if solver.solve():
    print("✅ Solution found:")
    print(solver.grid)
    solver.print_grid()
else:
    print("❌ No solution found.")

def find_direction(grid, x, y, colour):
    # Check all directions with boundary checks
    if y > 0 and grid[y-1][x] == colour:
        return 'up'
    if y < len(grid) - 1 and grid[y+1][x] == colour:
        return 'down'
    if x > 0 and grid[y][x-1] == colour:
        return 'left'
    if x < len(grid[0]) - 1 and grid[y][x+1] == colour:
        return 'right'
    return None

def calculate_square_size():
    # Calculate pixel size of one grid square (unscaled/scaled ratio)
    zeroUnscaled = unscaledColorPositions['red'][0][0]
    oneUnscaled = unscaledColorPositions['red'][1][0]
    zeroScaled = scaledColourPositions['red'][0][0]
    oneScaled = scaledColourPositions['red'][1][0]

    top = abs(zeroUnscaled - oneUnscaled)
    bottom = abs(zeroScaled - oneScaled)

    return int(top / bottom)

def get_valid_start(grid, scaled_positions, colour):
    if colour not in scaled_positions:
        print(f"No scaled positions found for {colour}")
        return None
    for pos in scaled_positions[colour]:
        # Swap coordinates here: scaled positions are (row, col) but grid is grid[y][x]
        x, y = pos[1], pos[0]
        if grid[y][x] == colour:
            print(f"Valid start found for {colour} at ({x},{y})")
            return (x, y)
    print(f"No valid starting cell found for {colour}")
    return None

def draw_lines(image, unscaledColorPositions, scaledColourPositions, solver, colour):
    size = calculate_square_size()
    grid = solver.grid
    visited = set()

    start_grid_pos = get_valid_start(grid, scaledColourPositions, colour)
    if not start_grid_pos:
        print(f"No valid direction found for {colour}")
        return image

    x_grid, y_grid = start_grid_pos
    x_unscaled, y_unscaled = unscaledColorPositions[colour][0]
    current_pixel = (x_unscaled, y_unscaled)

    # Move through the path step by step
    stack = [(x_grid, y_grid, current_pixel)]

    while stack:
        x, y, pixel_pos = stack.pop()
        visited.add((x, y))
        
        #Checks all 4 directions: up, down, left, right.        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if (nx, ny) not in visited and grid[ny][nx] == colour:
                    # Calculate the next pixel position
                    next_pixel = (pixel_pos[0] + dx * size, pixel_pos[1] + dy * size)

                    # Draw the line segment
                    image = cv2.line(image, pixel_pos, next_pixel, colorPicker(colour), thickness=40)

                    # Add next step to stack
                    stack.append((nx, ny, next_pixel))
                    break  # move one step at a time like DFS

    return image

# Choose which color to draw for testing
image = draw_lines(image, unscaledColorPositions, scaledColourPositions, solver, 'blue')
image = draw_lines(image, unscaledColorPositions, scaledColourPositions, solver, 'red')
image = draw_lines(image, unscaledColorPositions, scaledColourPositions, solver, 'green')
image = draw_lines(image, unscaledColorPositions, scaledColourPositions, solver, 'yellow')
image = draw_lines(image, unscaledColorPositions, scaledColourPositions, solver, 'orange')

# Display the image
window_name = 'Image'
cv2.imshow(window_name, image)

cv2.waitKey(0)
cv2.destroyAllWindows()