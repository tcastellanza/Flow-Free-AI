# Python program to explain cv2.line() method 
 
# importing cv2 
import cv2 
from test import ColorGridDetector
from FlowFreePuzzleSolver import FlowFreeSolver
 
# path 
path = '/Users/tommasocastellanza/Flow Free AI/examples/IMG_5931.PNG'
 
# Reading an image in default mode
image = cv2.imread(path)

detector = ColorGridDetector(grid_size=(5, 5))
unscaledColorPositions = detector.detect_unscaled_colors(path)
scaledColourPositions = detector.detect_colors(path)
# print(unscaledColorPositions)
# print(scaledColourPositions)

solver = FlowFreeSolver(5, scaledColourPositions)

print("Solving:")
if solver.solve():
    print("✅ Solution found:")
    print(solver.grid)
    solver.print_grid()
    print(scaledColourPositions['red'])
else:
    print("❌ No solution found.")

# Window name in which image is displayed
window_name = 'Image'

def calculatesqsize():
    zeroUnscaled = unscaledColorPositions['red'][0][0]
    oneUnscaled = unscaledColorPositions['red'][1][0]
    zeroScaled = scaledColourPositions['red'][0][0]
    oneScaled = scaledColourPositions['red'][1][0]

    top = abs(zeroUnscaled - oneUnscaled)
    bottom = abs(zeroScaled - oneScaled)

    return int(top/bottom)

def finddirection(x, y, colour):
    print(x, y, colour)
    solver.grid[x][y]

    if solver.grid[x+1][y] == colour:
        return 'right'
    elif solver.grid[x][y+1] == colour:
        return 'down'
    elif solver.grid[x-1][y] == colour:
        return 'left'
    elif solver.grid[x][y-1] == colour:
        return 'up'


def draw_lines(image, unscaledColorPositions, scaledColourPositions, solver, colour):
    visited = set()
    size = calculatesqsize()
    start_point = scaledColourPositions['red'][0]
    direction = finddirection(start_point[0], start_point[1], colour)
    print(direction)

    if direction == 'right':
        end_point = unscaledColorPositions[colour][0][1] + size
    elif direction == 'down':
        end_point = (unscaledColorPositions[colour][0][1], unscaledColorPositions[colour][0][0] + size)
    elif direction == 'left':
        end_point = unscaledColorPositions[colour][0][1] - size
    elif direction == 'up':
        end_point = unscaledColorPositions[colour][0][0] - size
    
    start_coord = unscaledColorPositions['red'][0]
    print(start_coord)
    print(end_point)
    linecolor = (0, 255, 0)
    thickness = 9
    image = cv2.line(image, start_coord, end_point, linecolor, thickness)


    return image

image = draw_lines(image, unscaledColorPositions, scaledColourPositions, solver, 'red')

# Displaying the image 
cv2.imshow(window_name, image)


# Wait for a key press indefinitely or for a specific amount of time
cv2.waitKey(0)

# Close all OpenCV windows
cv2.destroyAllWindows()