from tkinter import Label
import timeit
class InsufficientImagesError(Exception):
    """Exception class that can be called when there is insufficient number of images.
    
    Args:
        num_images (int): number of images (this is just used to display in the message)
    """
    def __init__(self, num_images):
        msg = "Expected 2 or more images but got only " +  str(num_images)
        super(InsufficientImagesError, self).__init__(msg)


class InvalidImageFilesError(Exception):
    """Exception class that can be called when files ar invalid image files or they do not exist.
    
    Args:
        msg (str): Error description
    """
    def __init__(self, msg):
        super(InvalidImageFilesError, self).__init__(msg)


class NotEnoughMatchPointsError(Exception):
    """Exception class that can be called when there are not enough matches points between images
        as defined by the mimimum
    
    Args:
        num_match_points (int): number of matches found
        min_match_points_req (int): minimum number of match points between images required 
    """
    def __init__(self, num_match_points, min_match_points_req, ui):
        msg = "There are not enough match points between images in the input images. \nRequired atleast " + \
               str(min_match_points_req) + " matches \nbut could find only " + str(num_match_points) + " matches!"
        Label(ui.stitching_log_top_frame, text=msg, font=("Arial", 25), fg='red').pack(fill="x")
        ui.stop_calculate_time = timeit.default_timer()
        ui.calculate_time=str(ui.stop_calculate_time-ui.start_calculate_time)
        ui.stitching_step = "finish"
        super(NotEnoughMatchPointsError, self).__init__(msg)


class MatchesNotConfident(Exception):
    """Exception class that can be called when the outliers matches count to all matches count ratio is
        above a minimum threshold to calculate the homography matrix confidently.
    
    Args:
        confidence (int): percentage indicating the confidence of match points 
    """
    def __init__(self, confidence, ui):
        msg = "The confidence in the matches is less than the defined threshold \nand hence the stitching operation cannot be performed. \nPerhaps the input images have very less overlapping content to detect good match points!\nConfidence: " +str(confidence)
        Label(ui.stitching_log_top_frame, text=msg, font=("Arial", 25), fg='red').pack(fill="x")
        ui.stop_calculate_time = timeit.default_timer()
        ui.calculate_time=str(ui.stop_calculate_time-ui.start_calculate_time)
        ui.stitching_step = "finish"
        super(MatchesNotConfident, self).__init__(msg)