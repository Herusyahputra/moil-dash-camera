"""
This is introduction praragrafh from model class.

"""

import datetime
import os
import yaml
import cv2
import numpy as np
from screeninfo import get_monitors

from .moilutils.moildev import Moildev
from .model_multitrading import Multithreading


class Model(object):
    def __init__(self):
        """
        The backend that contains all the data logic.
        The model's job is to simply manage the data.
        Whether the data is from a database, API,
        or a JSON object, the model is responsible for managing it.

        """
        super(Model, self).__init__()

        # Start variables
        self.media_source = None
        self.record = None
        self.rec_status = False
        self.current_setting_view = 0
        self.moildev = None
        self.cap = None
        self.image = None
        self.media_source_type = None
        self.camera_type = None
        self.panorama_view = None
        self.rotation_angle_ori = 0

        # video properties
        self.pos_frame = 0
        self.frame_count = 0
        self.total_minute = 0
        self.total_second = 0
        self.current_minute = 0
        self.current_second = 0
        # End variables

    @classmethod
    def control_contrast(cls, img, brightness=255, contrast=127):
        brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
        contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
        if brightness != 0:

            if brightness > 0:
                shadow = brightness
                max = 255

            else:
                shadow = 0
                max = 255 + brightness

            al_pha = (max - shadow) / 255
            ga_mma = shadow

            # The function addWeighted calculates
            # the weighted sum of two arrays
            cal = cv2.addWeighted(img, al_pha, img, 0, ga_mma)

        else:
            cal = img

        if contrast != 0:
            Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
            Gamma = 127 * (1 - Alpha)

            # The function addWeighted calculates
            # the weighted sum of two arrays
            cal = cv2.addWeighted(cal, Alpha, cal, 0, Gamma)

        return cal

    def set_source_file(self, source_file):
        self.source_file = source_file

    def set_rotation_angle_ori(self):
        with open(self.source_file.get_configuration_view_file(), "r") as file:
            configuration_view = yaml.safe_load(file)
        self.rotation_angle_ori = configuration_view["original"]["rotate"]

    def set_camera_type(self, camera_type):
        self.camera_type = camera_type

    @classmethod
    def get_monitor_resolution(cls):
        width = str(get_monitors()).split(",")[2].split("=")[1]
        height = str(get_monitors()).split(",")[3].split("=")[1]
        print(width, height)
        return int(width), int(height)

    def set_media_source_used(self, media):
        self.media_source = media
        if isinstance(self.media_source, int):
            self.media_source_type = "usb_cam"
            self.running_media_source(self.media_source)

        else:
            if self.media_source.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmg")):
                self.media_source_type = "Image"
                self.running_media_source(self.media_source)

            elif self.media_source.endswith((".avi", ".mp4")):
                self.media_source_type = "Video"
                self.running_media_source(self.media_source)

            elif self.media_source.endswith(".mjpg"):
                self.media_source_type = "Streaming"
                self.running_media_source(self.media_source)

    def create_object_moildev(self):
        """
        Test


        Returns:

        """
        self.moildev = Moildev(self.source_file.get_parameter_file(), self.camera_type)

    def running_media_source(self, media_source):
        """

        Args:
            media_source ():

        Returns:

        """
        if self.media_source_type == "Image":
            self.cap = None
            self.image = cv2.imread(media_source)
        elif self.media_source_type == "Video" or self.media_source_type == "usb_cam":
            self.cap = cv2.VideoCapture(media_source)
        elif self.media_source_type == "Streaming":
            self.cap = Multithreading(media_source)

        self.create_object_moildev()
        self.create_initial_maps()
        self.next_frame_process()

    def create_initial_maps(self):
        for view in ["panorama", "left_window", "right_window", "driver", "second_driver"]:
            if view == "panorama":
                if str(np.load(self.source_file.get_maps_x_panorama_dash(), allow_pickle=True)) == "None":
                    self.create_maps_panorama_dash()

                else:
                    self.map_x_panorama = np.load(self.source_file.get_maps_x_panorama_dash())
                    self.map_y_panorama = np.load(self.source_file.get_maps_y_panorama_dash())

            else:
                if str(np.load(self.source_file.get_maps_x_anypoint_left(), allow_pickle=True)) == "None" or \
                        str(np.load(self.source_file.get_maps_x_anypoint_right(), allow_pickle=True)) == "None" or \
                        str(np.load(self.source_file.get_maps_x_anypoint_driver(), allow_pickle=True)) == "None" or \
                        str(np.load(self.source_file.get_maps_x_anypoint_second_driver(),
                                    allow_pickle=True)) == "None" or \
                        str(np.load(self.source_file.get_maps_x_anypoint_mode_2(), allow_pickle=True)) == "None" or \
                        str(np.load(self.source_file.get_maps_x_panorama_x(), allow_pickle=True)) == "None":
                    self.create_maps_anypoint_view(view)
                    self.create_maps_panorama_x()
                    self.create_maps_anypoint_mode_2()

                else:
                    self.map_x_left_window = np.load(self.source_file.get_maps_x_anypoint_left())
                    self.map_y_left_window = np.load(self.source_file.get_maps_y_anypoint_left())

                    self.map_x_right_window = np.load(self.source_file.get_maps_x_anypoint_right())
                    self.map_y_right_window = np.load(self.source_file.get_maps_y_anypoint_right())

                    self.map_x_driver_view = np.load(self.source_file.get_maps_x_anypoint_driver())
                    self.map_y_driver_view = np.load(self.source_file.get_maps_y_anypoint_driver())

                    self.map_x_second_driver_view = np.load(self.source_file.get_maps_x_anypoint_second_driver())
                    self.map_y_second_driver_view = np.load(self.source_file.get_maps_y_anypoint_second_driver())

                    self.map_x_anypoint_mode_2 = np.load(self.source_file.get_maps_x_anypoint_mode_2())
                    self.map_y_anypoint_mode_2 = np.load(self.source_file.get_maps_y_anypoint_mode_2())

                    self.map_x_panorama_x = np.load(self.source_file.get_maps_x_panorama_x())
                    self.map_y_panorama_x = np.load(self.source_file.get_maps_y_panorama_x())

    def next_frame_process(self):
        if self.cap is not None:
            if self.media_source_type == "Video" or self.media_source_type == "usb_cam":
                _, self.image = self.cap.read()

            else:
                self.image = self.cap.get_frame()

            if self.media_source_type == "Video":
                self.video_duration()
            if self.rec_status:
                self.record.write(self.image)

        else:
            "This condition is when the media type source is image"
            pass

    def video_duration(self):
        """
            This function is for get time of video
        Returns:
            None
        """
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.pos_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_sec = int(self.frame_count / fps)

        self.total_minute = int(duration_sec // 60)
        duration_sec %= 60
        self.total_second = duration_sec
        sec_pos = int(self.pos_frame / fps)
        self.current_minute = int(sec_pos // 60)
        sec_pos %= 60
        self.current_second = sec_pos

    def reset_total_video_time(self):
        """
            This function is for set properties video total length is 0
        Returns:
            None
        """
        self.total_minute = 0
        self.total_second = 0

    def stop_video(self):
        """
            This function is set video in to frame 0
        Returns:
            None
        """
        if self.image is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.next_frame_process()

    def forward_video(self):
        """
            This function is for forward video frame for 5 seconds
        Returns:
            None
        """
        if self.image is not None:
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            position = self.pos_frame + 5 * fps
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
            self.next_frame_process()

    def rewind_video(self):
        """
            This function is for rewind video frame for 5 seconds
        Returns:
            None
        """
        if self.image is not None:
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            position = self.pos_frame - 5 * fps
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
            self.next_frame_process()

    def slider_controller(self, value, slider_maximum):
        """
            This function is for change video position base on input slider
        Args:
            value: current slider position
            slider_maximum: value maximum slider video
        Returns:
            None
        """
        if self.image is not None:
            dst = self.frame_count * value / slider_maximum
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, dst)
            self.next_frame_process()

    def get_value_slider_video(self, value):
        """
            This function is for get current position slider time base on position slider maximum
        Args:
            value: value slider maximum
        Returns:
            None
        """
        return self.pos_frame * (value + 1) / self.frame_count

    def create_maps_panorama_dash(self):
        moildev = Moildev(self.source_file.get_parameter_file(), self.camera_type)
        with open(self.source_file.get_configuration_view_file(), "r") as file:
            configuration_view = yaml.safe_load(file)
        alpha_max = configuration_view["panorama"]["alpha_max"]
        alpha = configuration_view["panorama"]["alpha"]
        beta = configuration_view["panorama"]["beta"]
        alpha_from = configuration_view["panorama"]["alpha_from"]
        alpha_end = 1

        self.map_x_panorama, self.map_y_panorama = moildev.maps_panorama_car(alpha_max, alpha, beta,
                                                                             alpha_from, alpha_end)
        # saving the Maps to the system
        np.save(self.source_file.get_maps_x_panorama_dash(), self.map_x_panorama)
        np.save(self.source_file.get_maps_y_panorama_dash(), self.map_y_panorama)

    def create_maps_anypoint_mode_2(self):
        with open(self.source_file.get_configuration_view_file(), "r") as file:
            configuration_view = yaml.safe_load(file)
        alpha = configuration_view["anypoint_mode_2"]["alpha"]
        beta = configuration_view["anypoint_mode_2"]["beta"]
        zoom = configuration_view["anypoint_mode_2"]["zoom"]

        moildev = Moildev(self.source_file.get_parameter_file(), self.camera_type)
        self.map_x_anypoint_mode_2, self.map_y_anypoint_mode_2 = moildev.maps_anypoint_mode2(alpha, beta, 0, zoom)

        np.save(self.source_file.get_maps_x_anypoint_mode_2(), self.map_x_anypoint_mode_2)
        np.save(self.source_file.get_maps_y_anypoint_mode_2(), self.map_y_anypoint_mode_2)

    def create_maps_panorama_x(self):
        with open(self.source_file.get_configuration_view_file(), "r") as file:
            configuration_view = yaml.safe_load(file)
        alpha_max = configuration_view["x_panorama"]["alpha_max"]
        alpha_min = configuration_view["x_panorama"]["alpha_min"]

        moildev = Moildev(self.source_file.get_parameter_file(), self.camera_type)
        self.map_x_panorama_x, self.map_y_panorama_x = moildev.maps_panorama_tube(alpha_min, alpha_max)

        np.save(self.source_file.get_maps_x_panorama_x(), self.map_x_panorama_x)
        np.save(self.source_file.get_maps_y_panorama_x(), self.map_y_panorama_x)

    def create_maps_anypoint_view(self, view):
        with open(self.source_file.get_configuration_view_file(), "r") as file:
            configuration_view = yaml.safe_load(file)
        alpha = configuration_view[view]["alpha"]
        beta = configuration_view[view]["beta"]
        roll = configuration_view[view]["roll"]
        zoom = configuration_view[view]["zoom"]

        if view == "left_window":
            moildev = Moildev(self.source_file.get_parameter_file(), self.camera_type)
            self.map_x_left_window, self.map_y_left_window = moildev.maps_anypoint_mode2(alpha, beta, roll, zoom)

            # saving the Maps to the system
            np.save(self.source_file.get_maps_x_anypoint_left(), self.map_x_left_window)
            np.save(self.source_file.get_maps_y_anypoint_left(), self.map_y_left_window)

        elif view == "right_window":
            moildev = Moildev(self.source_file.get_parameter_file(), self.camera_type)
            self.map_x_right_window, self.map_y_right_window = moildev.maps_anypoint_mode2(alpha, beta, roll, zoom)

            # saving the Maps to the system
            np.save(self.source_file.get_maps_x_anypoint_right(), self.map_x_right_window)
            np.save(self.source_file.get_maps_y_anypoint_right(), self.map_y_right_window)

        elif view == "driver":
            moildev = Moildev(self.source_file.get_parameter_file(), self.camera_type)
            self.map_x_driver_view, self.map_y_driver_view = moildev.maps_anypoint_mode2(alpha, beta, roll, zoom)

            # saving the Maps to the system
            np.save(self.source_file.get_maps_x_anypoint_driver(), self.map_x_driver_view)
            np.save(self.source_file.get_maps_y_anypoint_driver(), self.map_y_driver_view)

        elif view == "second_driver":
            moildev = Moildev(self.source_file.get_parameter_file(), self.camera_type)
            self.map_x_second_driver_view, self.map_y_second_driver_view = moildev.maps_anypoint_mode2(alpha, beta,
                                                                                                       roll,
                                                                                                       zoom)
            # saving the Maps to the system
            np.save(self.source_file.get_maps_x_anypoint_second_driver(), self.map_x_second_driver_view)
            np.save(self.source_file.get_maps_y_anypoint_second_driver(), self.map_y_second_driver_view)

    def create_panorama_image(self, image):
        with open(self.source_file.get_configuration_view_file(), "r") as file:
            configuration_view = yaml.safe_load(file)
        left = configuration_view["panorama"]["crop_left"]
        right = configuration_view["panorama"]["crop_right"]
        top = configuration_view["panorama"]["crop_top"]
        bottom = configuration_view["panorama"]["crop_bottom"]
        image = cv2.resize(cv2.remap(image, self.map_x_panorama, self.map_y_panorama, cv2.INTER_CUBIC),
                           (image.shape[1] * 2, image.shape[0]))
        return image[round(image.shape[0] * (top + 0.3)):round(image.shape[0] * (top + 0.3)) +
                                                         round(image.shape[0] * (bottom - 0.3)),
               round(image.shape[1] * left):
               round(image.shape[1] * left) + round(image.shape[1] * (right - left))]

    def create_anypoint_mode_2(self, image):
        with open(self.source_file.get_configuration_view_file(), "r") as file:
            configuration_view = yaml.safe_load(file)
        crop_top = configuration_view["anypoint_mode_2"]["crop_top"]
        crop_bottom = configuration_view["anypoint_mode_2"]["crop_bottom"]
        image = cv2.remap(image, self.map_x_anypoint_mode_2, self.map_y_anypoint_mode_2, cv2.INTER_CUBIC)
        return image[round(image.shape[0] * crop_top):round(image.shape[0] * crop_top) +
                                                      round(image.shape[0] * crop_bottom), round(image.shape[1] * 0):
                                                                                           round(image.shape[
                                                                                                     1] * 0) + round(
                                                                                               image.shape[1] * 1 - 0)]

    def create_panorama_x(self, image):
        # return cv2.remap(image, self.map_x_panorama_x, self.map_y_panorama_x, cv2.INTER_CUBIC)
        with open(self.source_file.get_configuration_view_file(), "r") as file:
            configuration_view = yaml.safe_load(file)
        crop_top = configuration_view["x_panorama"]["crop_top"]
        crop_bottom = configuration_view["x_panorama"]["crop_bottom"]
        image = cv2.remap(image, self.map_x_panorama_x, self.map_y_panorama_x, cv2.INTER_CUBIC)
        return image[round(image.shape[0] * crop_top):round(image.shape[0] * crop_top) +
                                                      round(image.shape[0] * crop_bottom), round(image.shape[1] * 0):
                                                                                           round(image.shape[
                                                                                                     1] * 0) + round(
                                                                                               image.shape[1] * 1 - 0)]

    def create_anypoint_left_window(self, image):
        return cv2.remap(image, self.map_x_left_window, self.map_y_left_window, cv2.INTER_CUBIC)

    def create_anypoint_right_window(self, image):
        return cv2.remap(image, self.map_x_right_window, self.map_y_right_window, cv2.INTER_CUBIC)

    def create_anypoint_driver_view(self, image):
        return cv2.remap(image, self.map_x_driver_view, self.map_y_driver_view, cv2.INTER_CUBIC)

    def create_anypoint_second_driver_view(self, image):
        return cv2.remap(image, self.map_x_second_driver_view, self.map_y_second_driver_view, cv2.INTER_CUBIC)

    # @classmethod
    # def clahe_equalization(cls, image):
    #     clahe_model = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    #     color_image_b = clahe_model.apply(image[:, :, 0])
    #     color_image_g = clahe_model.apply(image[:, :, 1])
    #     color_image_r = clahe_model.apply(image[:, :, 2])
    #     color_image_clahe = np.stack((color_image_b, color_image_g, color_image_r), axis=2)
    #     return color_image_clahe

    def record_video(self, record, directory=None):
        ss = datetime.datetime.now().strftime("%m_%d_%H_%M_%S")
        self.rec_status = record
        if self.image is not None and self.rec_status:
            H, W, _ = self.image.shape
            self.record = cv2.VideoWriter(directory + '/' + ss + '_output.avi',
                                          cv2.VideoWriter_fourcc(*'MJPG'), 14, (W, H))  # MJPG, XVID

    def save_image(self, dst_directory, feature_mode=None, active_main_view=None):
        image = None
        ss = datetime.datetime.now().strftime("%m_%d_%H_%M_%S")
        if self.image is not None:
            cv2.imwrite(dst_directory + "/" + str(ss) + "_ori.png", self.image)
            if feature_mode == "panorama_view":
                if active_main_view == 0:
                    image = self.create_panorama_image(self.image.copy())
                elif active_main_view == 1:
                    image = self.create_anypoint_mode_2(self.image.copy())
                elif active_main_view == 2:
                    image = self.create_panorama_x(self.image.copy())
            elif feature_mode == "left_window":
                image = self.create_anypoint_left_window(self.image.copy())
            elif feature_mode == "right_window":
                image = self.create_anypoint_right_window(self.image.copy())
            elif feature_mode == "second_driver_view":
                image = self.create_anypoint_second_driver_view(self.image.copy())
            elif feature_mode == "driver_view":
                image = self.create_anypoint_driver_view(self.image.copy())

            if image is not None:
                cv2.imwrite(dst_directory + "/" + str(ss) + "_" + feature_mode + "_.png", image)
