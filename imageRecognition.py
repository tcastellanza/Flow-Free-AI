# imageRecognition.py
import cv2
import numpy as np

class ImageRecognition:
    def __init__(self, image_path):
        """
        Initialize the ImageRecognition object with the image path.
        """
        self.image = cv2.imread(image_path)
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        
        # Define color ranges for different dots (HSV)
        self.color_ranges = {
            'red': [(0, 100, 100), (10, 255, 255)],   # Red color range (HSV)
            'blue': [(100, 100, 100), (130, 255, 255)], # Blue color range (HSV)
            'green': [(35, 50, 50), (75, 255, 255)],  # Green color range (HSV)
            'yellow': [(20, 100, 100), (40, 255, 255)],  # Yellow color range (HSV)
            'orange': [(10, 100, 100), (25, 255, 255)],  # Orange color range (HSV)
        }

    def detect_dots(self):
        """
        Detect dots in the image based on predefined color ranges, then scale coordinates to 5x5 grid.
        """
        detected_dots = {}

        # Loop through the colors and process each
        for color, (lower, upper) in self.color_ranges.items():
            mask = self.detect_color(self.hsv, (lower, upper))

            # Apply morphological operations to remove grid lines (only for green)
            if color == 'green':
                mask = self.remove_grid_lines(mask)

            # Detect contours in the mask (i.e., detect the dots)
            contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            dots = []
            for contour in contours:
                if cv2.contourArea(contour) > 100:  # Filter out small contours (noise)
                    x, y, w, h = cv2.boundingRect(contour)
                    center = (x + w // 2, y + h // 2)  # Find the center of the dot
                    if color == 'green':
                        if self.is_circular(contour):
                            dots.append(center)
                    else:
                        dots.append(center)

            detected_dots[color] = dots

        # Now scale the coordinates to a 5x5 grid
        grid_positions = self.scale_to_grid(detected_dots)

        # Print the grid positions
        print("Scaled Dot Positions:")
        for color, positions in grid_positions.items():
            print(f"{color}: {positions}")

        return grid_positions

    def detect_color(self, hsv, color_range):
        lower, upper = color_range
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        return mask

    def remove_grid_lines(self, mask):
        mask = cv2.erode(mask, None, iterations=2)  # Remove thin grid lines
        mask = cv2.dilate(mask, None, iterations=5)  # Expand the green areas (dots)
        return mask

    def is_circular(self, contour):
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        if perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter ** 2)
            return circularity > 0.7  # Threshold for circularity
        return False

    def scale_to_grid(self, detected_dots):
        """
        Scale the detected dot coordinates to fit within a 5x5 grid.
        """
        # Get image dimensions (height, width)
        height, width = self.image.shape[:2]
        
        # Define the 5x5 grid dimensions
        grid_size = 5
        
        scaled_positions = {}

        # Loop through each color and scale the positions
        for color, dots in detected_dots.items():
            scaled_positions[color] = []

            for dot in dots:
                # Scale the x and y coordinates to fit within the 5x5 grid
                scaled_x = int((dot[0] / width) * (grid_size - 1))
                scaled_y = int((dot[1] / height) * (grid_size - 1))
                
                scaled_positions[color].append((scaled_x, scaled_y))

        return scaled_positions
