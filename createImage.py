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
    
    # Find valid start with swapped coordinates
    start_grid_pos = get_valid_start(solver.grid, scaledColourPositions, colour)
    if not start_grid_pos:
        print(f"No valid direction found for {colour}")
        return image
    
    start_unscaled_pos = unscaledColorPositions[colour][0]  # pixel coordinates (x, y)

    x_grid, y_grid = start_grid_pos


    direction = find_direction(solver.grid, x_grid, y_grid, colour)
    if not direction:
        print(f"No valid direction found for {colour}")
        return image

    # calculate end point based on direction
    x, y = start_unscaled_pos
    if direction == 'up':
        end_point = (x, y - size)
    elif direction == 'down':
        end_point = (x, y + size)
    elif direction == 'left':
        end_point = (x - size, y)
    elif direction == 'right':
        end_point = (x + size, y)

    # draw the line
    line_color = colorPicker(colour)
    thickness = 40
    image = cv2.line(image, start_unscaled_pos, end_point, line_color, thickness)

    print(f"Checking {colour} at grid position {start_grid_pos}")
    print(f"Value in solver.grid at that position: {solver.grid[y_grid][x_grid]}")

    print(f"Checking directions for {colour} at {start_grid_pos}")
    for dy, dx, dir in [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]:
        ny, nx = y_grid + dy, x_grid + dx
        if 0 <= ny < len(solver.grid) and 0 <= nx < len(solver.grid[0]):
            print(f"Checking {dir} → ({nx}, {ny}): {solver.grid[ny][nx]}")    

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