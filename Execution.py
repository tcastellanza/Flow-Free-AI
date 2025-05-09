import cv2
from FlowFreePuzzleSolver import FlowFreeSolver
from test import ColorGridDetector


def main():
    detector = ColorGridDetector(grid_size=(5, 5))
    image_path = "examples/IMG_5927.PNG"

    color_positions = detector.detect_colors(image_path)

    print("Detected Color Positions:")
    print(color_positions)

    solver = FlowFreeSolver(5, color_positions)

    if solver.solve():
        print("✅ Solution found:")
        solver.print_grid()
    else:
        print("❌ No solution found.")

if __name__ == "__main__":
    main()