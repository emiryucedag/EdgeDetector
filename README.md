# EdgeDetection - Outline Extraction from PNG Files

This project is a Python-based image processing tool that detects and extracts the outermost contour (outline) of a given PNG image using OpenCV. 
It is designed for vector-style technical drawings such as ship deck plans, character vectors or architectural elements. You can check the examples of some png images and their processed states.

## 🔍 Features

- Supports PNG images with or without alpha channels.
- Automatically detects the outermost contour.
- Allows customization of the contour line thickness via a simple user interface (UI).
- Outputs a transparent image with only the detected outline drawn.
- Handles noise and small artifacts using morphological filtering.
- Simple and focused — designed for consistent technical output.

## 🛠 Technologies Used

- Python 3.13
- OpenCV (cv2)
- NumPy
- Tkinter (for the UI)

## 🧪 How It Works

1. Loads the image and detects alpha or brightness-based edges.
2. Applies a binary threshold to isolate the shape.
3. Uses `cv2.findContours` to detect all external contours.
4. Filters out small areas to avoid noise.
5. Draws the largest contour onto a blank transparent canvas.
6. Exports the result with your desired thickness.

## 🖱 How to Use

1. Run the `EdgeDetection.py` file.
2. Select a PNG file via the file picker.
3. Choose a thickness between 1 and 20.
4. Press the **Detect Edge** button.
5. Your output will be saved in the same directory as `*_R.png`.

## 📎 Notes

- Currently only supports PNG files.
- Designed for images with clear outlines (e.g., blueprints, technical figures).
- Make sure the input images have sufficient contrast or transparency.


Feel free to contribute or raise issues!
