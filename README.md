# Image and Video Processing Project

This project uses Python to process images and generate a video from the resulting image sequence. The code leverages OpenCV for image manipulation, MoviePy for video generation, and NumPy for array operations.

## Project Overview

The project performs the following tasks:
- **Image Reading:** Loads three sets of images from specified folders: `config`, `vms`, and `temp`.
- **Image Processing:**  
  - Crops and composes images into a single composite image with a defined layout.
  - Overlays text with a semi-transparent blurred background for clarity.
  - Inserts decorative elements such as a rainbow image and dividing lines.
- **Video Generation:** Saves each processed image to a folder and compiles them into an MP4 video.

## Directory Structure

The project directory should be organized as follows:
```
├── config/                # Contains config images (e.g., config_000.jpg to config_201.jpg)
├── vms/                   # Contains vms images (e.g., vms_000.jpg to vms_201.jpg)
├── temp/                  # Contains temp images (e.g., temp_000.jpg to temp_201.jpg)
├── processed_images/      # Folder where processed images are saved (created automatically)
├── R.png                  # Rainbow image used for decoration
├── output_combined_video_with_rainbow2.mp4  # Generated video file
└── main.py                # Main script that performs image processing and video generation
```

## Dependencies

Make sure to install the following Python libraries:
- [OpenCV](https://opencv.org/) (`cv2`)
- [NumPy](https://numpy.org/)
- [MoviePy](https://zulko.github.io/moviepy/)

Install the dependencies using:
```bash
pip install opencv-python numpy moviepy
```

## Usage Instructions

1. **Prepare the Image Resources:**  
   Place your images in the corresponding folders:
   - `config/` for config images (named `config_000.jpg` to `config_201.jpg`)
   - `vms/` for vms images (named `vms_000.jpg` to `vms_201.jpg`)
   - `temp/` for temp images (named `temp_000.jpg` to `temp_201.jpg`)

2. **Prepare the Rainbow Image:**  
   Add the decorative rainbow image (`R.png`) to the project’s root directory.

3. **Run the Script:**  
   Execute the main script:
   ```bash
   python main.py
   ```
   The script will process the images and save each frame in the `processed_images` folder, then compile them into a video named `output_combined_video_with_rainbow2.mp4`.

## Code Explanation

- **Parameter Settings:**
  - **Video Settings:** The video resolution is set to `1500x1650` with a frame rate of `10 fps`.
  - **Text Settings:** The code defines the font type, scale, thickness, and color for overlay texts.
  - **Time Parameter:** A small time step `dt` is used to update the timestamp displayed on each frame.

- **Image Processing Workflow:**
  1. **Reading and Cropping:**  
     Images from `config`, `vms`, and `temp` directories are read in sequence and cropped to fit designated areas within the composite image.
  2. **Overlaying Text:**  
     A custom function, `add_text_with_background`, is used to add text with a semi-transparent, blurred background to enhance readability.
  3. **Adding Decorative Elements:**  
     The rainbow image is inserted, and black lines are drawn to separate different parts of the composite image.
  4. **Saving and Video Generation:**  
     Processed images are saved in the `processed_images` folder. The `ImageSequenceClip` function from MoviePy is then used to compile these images into a video.

## Notes

- Ensure all dependencies are installed and the required folders and image files exist.
- Adjust parameters like frame rate, resolution, or text content in the code as needed.
- Processing may take some time depending on the number and size of images.
