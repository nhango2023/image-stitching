from . import utils
import os
import cv2
import time
import timeit
from tkinter import Label

def stitch_images(self, list_path_image, stitch_direction):
    pivot_img = cv2.imread(list_path_image[0])
    num_images = len(list_path_image)
    for i in range(1, num_images, 1):
        join_img = cv2.imread(list_path_image[i])
        pivot_img = utils.stitch_image_pair(self, pivot_img, join_img, stitch_direc=stitch_direction)
    
    return pivot_img

def stitch_images_and_save(self, list_path_image, stitch_direction=1, output_folder=None):
    Label(self.stitching_log_top_frame, text="Start stitching images..",  font=("Arial", 25))
    start = timeit.default_timer()
    timestr = time.strftime("%Y%m%d_%H%M%S")
    filename = "stitched_image_" + timestr + ".jpg"
    stitched_img = stitch_images(self, list_path_image, stitch_direction)
    full_save_path = os.path.join(output_folder, filename)
    cv2.imwrite(full_save_path, stitched_img)
    stop = timeit.default_timer()
    self.stitching_step = "finish"
    self.calculate_time=str(stop-start)
    self.view_image.bind("<Button-1>", lambda event: self.displayImage(stitched_img))
    self.view_image.place(relx=0.1, rely=0.5, anchor='c')

 