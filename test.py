import cv2
import numpy as np
import matplotlib.colors as mc

class ColorGridDetector:
    def __init__(self, grid_size=(5, 5), color_ranges=None, min_blob_area=50, aspect_ratio_threshold=0.8):
        """
        Initializes the ColorGridDetector.

        Args:
            grid_size (tuple): (rows, cols) of the grid. Defaults to (5, 5).
            color_ranges (dict): {'color': [(lower_hsv, upper_hsv), ...]}. Defaults to None.
            min_blob_area (int): Minimum area (in pixels) for a detected color blob. Defaults to 50.
            aspect_ratio_threshold (float): Minimum aspect ratio to consider a blob circle-like. Defaults to 0.8.
        """
        self.grid_size = grid_size
        self.color_ranges = color_ranges if color_ranges else self._default_color_ranges()
        self.min_blob_area = min_blob_area
        self.aspect_ratio_threshold = aspect_ratio_threshold

    def _default_color_ranges(self):
        """Returns default HSV color ranges."""
        blue_hex = "#1028ff"
        green_hex = "#008d00"

        blue_hsv = self._hex_to_hsv(blue_hex)
        green_hsv = self._hex_to_hsv(green_hex)

        tolerance_h = 5
        tolerance_sv = 30

        return {
            'red':   [((0, 100, 100), (10, 255, 255)), ((170, 100, 100), (180, 255, 255))],
            'green': [((max(0, green_hsv[0] - tolerance_h), max(0, green_hsv[1] - tolerance_sv), max(0, green_hsv[2] - tolerance_sv)),
                       (min(179, green_hsv[0] + tolerance_h), min(255, green_hsv[1] + tolerance_sv), min(255, green_hsv[2] + tolerance_sv)))],
            'blue':  [((max(0, blue_hsv[0] - tolerance_h), max(0, blue_hsv[1] - tolerance_sv), max(0, blue_hsv[2] - tolerance_sv)),
                       (min(179, blue_hsv[0] + tolerance_h), min(255, blue_hsv[1] + tolerance_sv), min(255, blue_hsv[2] + tolerance_sv)))],
            'yellow': [((20, 100, 100), (40, 255, 255))],
            'orange': [((10, 100, 100), (25, 255, 255))]
        }

    def _hex_to_hsv(self, hex_color):
        """Converts a hex color code to HSV (OpenCV scale: H 0-179, S 0-255, V 0-255)."""
        rgb = mc.to_rgb(hex_color)
        hsv_float = mc.rgb_to_hsv(rgb)
        return (int(hsv_float[0] * 179), int(hsv_float[1] * 255), int(hsv_float[2] * 255))

    def detect_colors(self, image_path):
        """
        Detects colored circles in a grid image.

        Args:
            image_path (str): Path to the image.

        Returns:
            dict: {'color': [(row, col), ...]}
        """
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not open or find the image at {image_path}")
            return {}

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        color_positions = {color: [] for color in self.color_ranges}
        height, width, _ = img.shape
        rows, cols = self.grid_size
        cell_height = height // rows
        cell_width = width // cols

        for color, ranges in self.color_ranges.items():
            for lower_hsv, upper_hsv in ranges:
                lower_bound = np.array(lower_hsv, dtype=np.uint8)
                upper_bound = np.array(upper_hsv, dtype=np.uint8)
                mask = cv2.inRange(hsv, lower_bound, upper_bound)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > self.min_blob_area:
                        x, y, w, h = cv2.boundingRect(contour)
                        aspect_ratio = float(w) / h if h > 0 else 0
                        if aspect_ratio > self.aspect_ratio_threshold and aspect_ratio < (1 / self.aspect_ratio_threshold):
                            # It's somewhat circle-like, calculate centroid
                            M = cv2.moments(contour)
                            if M["m00"] != 0:
                                cX = int(M["m10"] / M["m00"])
                                cY = int(M["m01"] / M["m00"])
                                row = cY // cell_height
                                col = cX // cell_width
                                if 0 <= row < rows and 0 <= col < cols:
                                    color_positions[color].append((row, col))

        return color_positions

    def detect_unscaled_colors(self, image_path):
        """
        Detects colored circles in an image and returns their unscaled pixel coordinates.

        Args:
            image_path (str): Path to the image.

        Returns:
            dict: {'color': [(x, y), ...]} — pixel coordinates of each detected colored blob.
        """
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not open or find the image at {image_path}")
            return {}

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        color_coords = {color: [] for color in self.color_ranges}

        for color, ranges in self.color_ranges.items():
            for lower_hsv, upper_hsv in ranges:
                lower_bound = np.array(lower_hsv, dtype=np.uint8)
                upper_bound = np.array(upper_hsv, dtype=np.uint8)
                mask = cv2.inRange(hsv, lower_bound, upper_bound)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > self.min_blob_area:
                        x, y, w, h = cv2.boundingRect(contour)
                        aspect_ratio = float(w) / h if h > 0 else 0
                        if aspect_ratio > self.aspect_ratio_threshold and aspect_ratio < (1 / self.aspect_ratio_threshold):
                            # Compute centroid (unscaled)
                            M = cv2.moments(contour)
                            if M["m00"] != 0:
                                cX = int(M["m10"] / M["m00"])
                                cY = int(M["m01"] / M["m00"])
                                color_coords[color].append((cX, cY))

        return color_coords
    


if __name__ == "__main__":
    detector = ColorGridDetector(grid_size=(5, 5))
    image_file = "/Users/tommasocastellanza/Downloads/IMG_5929.PNG"
    detected_positions = detector.detect_colors(image_file)
    print("color_positions = {")
    for color, positions in detected_positions.items():
        print(f"    '{color}': {positions},")
    print("}")