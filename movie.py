import cv2
import os
import numpy as np
from moviepy.editor import ImageSequenceClip

# set the folder path
current_dir = os.getcwd()  # current folder path
config_folder = os.path.join(current_dir, 'config')
vms_folder = os.path.join(current_dir, 'vms')
temp_folder = os.path.join(current_dir, 'temp')
output_folder = os.path.join(current_dir, 'processed_images')
os.makedirs(output_folder, exist_ok=True)

rainbow_path = os.path.join(current_dir, 'R.png')  # folder path for rainbow.png

# set video resolution
video_size = (1500, 1650)
fps = 10  # frame rate
font = cv2.FONT_HERSHEY_TRIPLEX # font type
font_scale = 0.8                # font scale
font_thickness = 1              # font thickness 
font_color = (0, 0, 0)          # font color is black

# time parameter
dt = 1e-7   # timestep
t = 0       # start time

# define the title and the text
top_left_text = "Penetration of Solutionized A6 MgPlate"
top_right_text = "Sun Research Group, University of Kentucky"
bottom_right_text = "Created by Rong Jin"

# define the informaton of the impact process
impact_velocity_text = "Impact Velocity: 1.2 km/s"
plate_thickness_text = "Plate Thickness: 9.5 mm"
residual_velocity_text = "Residual Velocity: 0.79 km/s"

# get figure list
config_files = [f'config_{i:03d}.jpg' for i in range(202)]
vms_files = [f'vms_{i:03d}.jpg' for i in range(202)]
temp_files = [f'temp_{i:03d}.jpg' for i in range(202)]

config_files = [os.path.join(config_folder, img) for img in config_files if os.path.exists(os.path.join(config_folder, img))]
vms_files = [os.path.join(vms_folder, img) for img in vms_files if os.path.exists(os.path.join(vms_folder, img))]
temp_files = [os.path.join(temp_folder, img) for img in temp_files if os.path.exists(os.path.join(temp_folder, img))]

# import rainbow.png and adjust its size
rainbow_img = cv2.imread(rainbow_path)
rainbow_resized = cv2.resize(rainbow_img, (200, 30))

# process the image in sequence
for idx in range(len(config_files)):
    # create the background
    combined_image = np.ones((video_size[1], video_size[0], 3), dtype=np.uint8) * 255

    # processing part 1: config image cropped and put into 1500x850 area
    config_img = cv2.imread(config_files[idx])
    height, width, _ = config_img.shape
    crop_width = (width - 1500) // 2
    cropped_config_img = config_img[height - 850:height, crop_width:crop_width + 1500]  # the height is cut from the bottom up, and the width is cut on both sides
    combined_image[:850, :] = cropped_config_img                                        # put into the upper part

    # add the first part of the text and create a 50% transparent blurred background
    def add_text_with_background(img, text, x, y):
        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        background_width, background_height = text_w + 20, text_h + 20
        x_bg1, y_bg1 = x - 10, y - text_h - 10
        x_bg2, y_bg2 = x_bg1 + background_width, y_bg1 + background_height

        # extract the background area and blur it
        roi = img[y_bg1:y_bg2, x_bg1:x_bg2]
        blurred_roi = cv2.GaussianBlur(roi, (15, 15), 0)

        # create a 50% transparent white background
        white_background = np.ones_like(blurred_roi, dtype=np.uint8) * 255
        cv2.addWeighted(blurred_roi, 1 - 0.5, white_background, 0.5, 0, blurred_roi)

        # paste the blurred background area back into the image
        img[y_bg1:y_bg2, x_bg1:x_bg2] = blurred_roi

        # add text on blurred background
        cv2.putText(img, text, (x, y), font, font_scale, font_color, font_thickness)

    # add text to the upper left, middle left, and lower left
    add_text_with_background(combined_image, impact_velocity_text, 50, 125)
    add_text_with_background(combined_image, plate_thickness_text, 50, 425)
    add_text_with_background(combined_image, residual_velocity_text, 50, 725)

    # add timeframe to the first part
    time_text = f"t = {t:.2e} s"  # keep two decimal places
    add_text_with_background(combined_image, time_text, 1100, 725)

    # processing part 2: VMS image is cropped and placed in the lower left part of 750x800
    vms_img = cv2.imread(vms_files[idx])
    height, width, _ = vms_img.shape
    crop_width = (width - 750) // 2
    cropped_vms_img = vms_img[height - 800:height, crop_width:crop_width + 750]     # the height is cut from the bottom up, and the width is cut on both sides
    combined_image[850:1650, :750] = cropped_vms_img                                # insert into the lower left part

    # insert rainbow.png into part 2
    combined_image[1560:1590, 275:475] = rainbow_resized                            # location: lower middle
    add_text_with_background(combined_image, "Von Mises Stress (MPa)", 215, 1540)
    add_text_with_background(combined_image, "0", 225, 1580)
    add_text_with_background(combined_image, "300", 505, 1580)

    # processing part 3: crop the temp image and put it in the lower right part of 750x800
    temp_img = cv2.imread(temp_files[idx])
    height, width, _ = temp_img.shape
    crop_width = (width - 750) // 2
    cropped_temp_img = temp_img[height - 800:height, crop_width:crop_width + 750]   # the height is cut from the bottom up, and the width is cut on both sides
    combined_image[850:1650, 750:1500] = cropped_temp_img                           # insert into the lower right part

    # insert rainbow.png into part 3
    combined_image[1560:1590, 1025:1225] = rainbow_resized                          # location: lower middle
    add_text_with_background(combined_image, "Temperature (K)", 1010, 1540)
    add_text_with_background(combined_image, "298", 955, 1580)
    add_text_with_background(combined_image, "398", 1255, 1580)

    # add black dividing lines
    # first line: divides the first part from the second and third parts
    cv2.line(combined_image, (0, 850), (1500, 850), (0, 0, 0), 5)       # horizontal line

    # second line: split the second and third parts
    cv2.line(combined_image, (750, 850), (750, 1650), (0, 0, 0), 5)     # vertical line

    # add title rectangles for the text
    # upper left corner rectangle and text
    (text_w, text_h), _ = cv2.getTextSize(top_left_text, font, font_scale, font_thickness)
    cv2.rectangle(combined_image, (10, 10), (10 + text_w + 10, 10 + text_h + 20), (0, 0, 0), -1)
    cv2.putText(combined_image, top_left_text, (15, 35), font, font_scale, (255, 255, 255), font_thickness)

    # upper right corner rectangle and text
    (text_w, text_h), _ = cv2.getTextSize(top_right_text, font, font_scale, font_thickness)
    cv2.rectangle(combined_image, (video_size[0] - text_w - 20, 10), (video_size[0] - 10, 10 + text_h + 20), (0, 0, 0), -1)
    cv2.putText(combined_image, top_right_text, (video_size[0] - text_w - 15, 35), font, font_scale, (255, 255, 255), font_thickness)

    # lower right corner rectangle and text
    (text_w, text_h), _ = cv2.getTextSize(bottom_right_text, font, font_scale, font_thickness)
    cv2.rectangle(combined_image, (video_size[0] - text_w - 20, video_size[1] - text_h - 20), (video_size[0] - 10, video_size[1] - 10), (0, 0, 0), -1)
    cv2.putText(combined_image, bottom_right_text, (video_size[0] - text_w - 15, video_size[1] - 15), font, font_scale, (255, 255, 255), font_thickness)

    # save the image after process
    output_image_file = os.path.join(output_folder, f'processed_{idx:03d}.jpg')
    cv2.imwrite(output_image_file, combined_image)

    # time update
    t += dt

# generate the video
processed_images = [os.path.join(output_folder, f'processed_{i:03d}.jpg') for i in range(202)]
clip = ImageSequenceClip(processed_images, fps=fps)

# save the video file
output_video = 'output_combined_video_with_rainbow2.mp4'
clip.write_videofile(output_video, codec='libx264')
