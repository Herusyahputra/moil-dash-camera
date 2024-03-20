# import necessary library you used here
import os
from pwd import getpwuid
from os import stat
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QKeySequence, QImage, QPixmap
from PyQt5.QtWidgets import QPushButton, QShortcut

from view.ui_main import Ui_MainWindow
from controller.control_setting_config import DashSettingConfig
from controller.control_select_media import SelectMedia
# from controller.control_camera_type import select_camera_type
# from controller.control_camera_parameter import CameraParametersForm
from controller.control_select_conditional import SelectCondition
from controller.control_icon_feature_mode import ControlIconFeatureMode
from controller.control_icon_ui import ControlIconInUI
from controller.control_resources import GetResorcesFile

from model.model_main import Model
import model.moilutils.moilutils as mutils
from model.moilutils.camera_parameter import CameraParametersForm
from model.moilutils.camera_type import camera_type


class Controller(Ui_MainWindow):
    """
    The controllers class is The brains of the application that controls how data is displayed.
    The controller's responsibility is to pull, modify, and provide data to the user.
    Essentially, the controllers is the link between the view and model.
    """

    def __init__(self, parent):
        super().__init__()
        self.setupUi(parent)
        parent.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.model = Model()
        self.parent = parent
        self.source_file = GetResorcesFile()
        self.model.set_source_file(self.source_file)
        self.setting_config = DashSettingConfig(self)
        self.additional = SelectCondition(self)

        self.auto_set_resolution_screen()
        self.label_text_dash_2.hide()
        self.parent.resizeEvent = self.resize_event

        self.stackedWidget_setting.setCurrentIndex(self.comboBox_setting_select_main_view.currentIndex())

        # option feature mode
        # 0 = setting mode, 1 = home, 2 = panorama, 3 = left_window
        # 4 = right_window, 5 = driver_view, 6 = second_driver_view, 7 = original_view
        self.feature_mode_option = ["setting", "home", "panorama_view", "left_window", "right_window",
                                    "driver_view", "second_driver_view", "original_view", ]

        self.stackedWidget.setCurrentIndex(3)

        # set ui to center
        self.move_ui_to_center()

        self.res = "case_1"

        # set theme
        self.set_theme_ui()

        # control timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(round(1000 / 24))
        self.timer.timeout.connect(self.update_to_user_interface)

        # set icon to ui
        self.set_icon = ControlIconInUI(self)

        # init zoom view
        self.zoom_anypoint_2 = self.parent.width() - 20
        self.zoom_x_panorama = self.parent.width() - 20

        # brigness
        self.val_brightness = self.spinBox_brighness.value()
        self.val_contrast = self.spinBox_contrast.value()

        self.parent.closeEvent = self.closeEvent

        self.resize_result_image()

        # connect button to the function
        self.connect_button()

    def connect_button(self):
        """
        This function is for connect the button user interface to the function.

        Returns:
            None
        """
        # shortcut = QShortcut(QKeySequence("Ctrl+R"), self.parent)
        # shortcut.activated.connect(self.onclick_select_media)

        self.btn_source_config.clicked.connect(self.onclick_select_media)
        self.btn_change_camera_type.clicked.connect(self.onclick_change_camera_type)
        self.btn_parameter_form.clicked.connect(self.onclick_modify_camera_parameter)

        self.btn_home.clicked.connect(self.onclick_home_button)

        self.btn_panorama_view.clicked.connect(self.onclick_panorama_view)
        self.btn_left_window.clicked.connect(self.onclick_left_window_view)
        self.btn_driver_view.clicked.connect(self.onclick_driver_view)
        self.btn_second_driver_view.clicked.connect(self.onclick_second_driver_view)
        self.btn_right_window.clicked.connect(self.onclick_right_window_view)
        self.btn_original_view.clicked.connect(self.onclick_original_view)

        self.btn_setting.clicked.connect(self.onclick_button_settings)

        # control video
        self.btn_play_pause.clicked.connect(self.onclick_play_pause_video)
        self.btn_stop.clicked.connect(self.onclick_stop_video)
        self.btn_rewind.clicked.connect(self.onclick_rewind_video)
        self.btn_forward.clicked.connect(self.onclick_forward_video)
        self.slider_video.valueChanged.connect(self.onclick_slider_video)

        # change front view
        self.comboBox_setting_select_main_view.currentIndexChanged.connect(self.change_front_view)

        # label event
        self.lbl_panorama_image.mousePressEvent = self.onclick_lbl_panorama_image
        self.label_left_window.mousePressEvent = self.onclick_lbl_left_dash
        self.label_right_window.mousePressEvent = self.onclick_lbl_right_dash
        self.label_driver_view.mousePressEvent = self.onclick_lbl_steering_dash
        self.label_second_driver_view.mousePressEvent = self.onclick_lbl_original_dash
        self.lbl_image_single_view.mousePressEvent = self.onclick_lbl_image_single_view

        # control zoom view
        self.btn_zoom_in.clicked.connect(self.zoom_in_view)
        self.btn_zoom_out.clicked.connect(self.zoom_out_view)

        # control brightness
        self.spinBox_brighness.valueChanged.connect(self.showing_image_to_ui)
        self.spinBox_contrast.valueChanged.connect(self.showing_image_to_ui)

        self.btn_record.clicked.connect(self.record_video)
        self.btn_screenshot_active_image.clicked.connect(self.save_image)

    def zoom_in_view(self):
        if self.comboBox_setting_select_main_view.currentIndex() == 0:
            if self.size == self.parent.width() - 20:
                pass
            else:
                self.size += 100

        elif self.comboBox_setting_select_main_view.currentIndex() == 1:
            if self.zoom_anypoint_2 == self.parent.width() - 20:
                pass
            else:
                self.zoom_anypoint_2 += 100
        else:
            if self.zoom_x_panorama == self.parent.width() - 20:
                pass
            else:
                self.zoom_x_panorama += 100

        self.showing_image_to_ui()

    def zoom_out_view(self):
        if self.comboBox_setting_select_main_view.currentIndex() == 0:
            if self.size == 400:
                pass
            else:
                self.size -= 100

        elif self.comboBox_setting_select_main_view.currentIndex() == 1:
            if self.zoom_anypoint_2 < 400:
                pass
            else:
                self.zoom_anypoint_2 -= 100

        else:
            if self.zoom_x_panorama < 400:
                pass
            else:
                self.zoom_x_panorama -= 100

        self.showing_image_to_ui()

    def auto_set_resolution_screen(self):
        w, h = self.model.get_monitor_resolution()
        self.parent.resize(w, h)
        self.parent.setMaximumSize(QtCore.QSize(w, h))

    def resize_event(self, event):
        if self.stackedWidget.currentIndex() == 3:
            image = cv2.imread(self.source_file.get_welcome_logo_file())
            w = self.parent.width()
            h = self.parent.height()
            if w % 4 == 0:
                image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)
            image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_RGB888).rgbSwapped()
            self.label_7.setPixmap(QPixmap.fromImage(image))

        self.resize_result_image()
        self.config_ui_scaled_by_screen_ratio()
        # self.showing_image_to_ui()

    def resize_result_image(self):
        if self.parent.width() % 4 == 0:
            self.size = round(self.parent.width() - 20)
            self.zoom_anypoint_2 = self.parent.width() - 20
            self.zoom_x_panorama = self.parent.width() - 20
        else:
            self.size = self.size
            self.zoom_anypoint_2 = self.zoom_anypoint_2
            self.zoom_x_panorama = self.zoom_x_panorama
        self.showing_image_to_ui()

    def config_ui_scaled_by_screen_ratio(self):
        """
        Changing the user interface based on the screen resolution.

        Returns:

        """
        # resolution screen is 1024 x 576 (16:9)
        if self.parent.height() in range(550, 700):
            self.res = "case_1"
            self.label_text_dash_2.hide()
            self.set_icon_feature = ControlIconFeatureMode(self)

            # config showing image
            self.width_ori_and_any_setting = 220
            self.width_any_in_home = 240

            self.frame_button.setMaximumHeight(45)
            self.frame_button.setMinimumHeight(45)

            self.frame_feature_mode.setMinimumWidth(340)
            self.frame_feature_mode.setMaximumWidth(340)

            self.frame_26.setMinimumHeight(24)
            self.frame_26.setMaximumHeight(24)

            self.frame_4.setMinimumWidth(110)
            self.frame_4.setMaximumWidth(110)

            self.frame_config_btn.setMinimumWidth(96)
            self.frame_config_btn.setMaximumWidth(96)

            self.frame_configuration_view.setMinimumHeight(155)
            self.frame_configuration_view.setMaximumHeight(155)
            self.frame_config_setting_panorama_view.setMinimumHeight(25)

            self.frame_config_button_group.setMinimumWidth(60)
            self.frame_config_button_group.setMaximumWidth(60)

        # resolution screen is 1600 x 900 (16:9)
        elif self.parent.height() in range(700, 950):
            self.res = "case_2"
            self.label_text_dash_2.show()
            self.set_icon_feature = ControlIconFeatureMode(self)

            self.width_ori_and_any_setting = 280
            self.width_any_in_home = 300

            self.frame_button.setMaximumHeight(60)
            self.frame_button.setMinimumHeight(60)

            self.frame_feature_mode.setMinimumWidth(450)
            self.frame_feature_mode.setMaximumWidth(450)

            self.frame_26.setMinimumHeight(30)
            self.frame_26.setMaximumHeight(30)

            self.frame_4.setMinimumWidth(150)
            self.frame_4.setMaximumWidth(150)

            self.frame_config_btn.setMinimumWidth(115)
            self.frame_config_btn.setMaximumWidth(115)

            self.frame_configuration_view.setMinimumHeight(220)
            self.frame_configuration_view.setMaximumHeight(220)
            self.frame_config_setting_panorama_view.setMinimumHeight(30)

            self.frame_config_button_group.setMinimumWidth(80)
            self.frame_config_button_group.setMaximumWidth(80)

        # resolution screen is 1920 x 1080 (16:9)
        elif self.parent.height() in range(950, 1150):
            self.res = "case_3"
            self.label_text_dash_2.show()
            self.set_icon_feature = ControlIconFeatureMode(self)

            self.width_ori_and_any_setting = 360
            self.width_any_in_home = 420

            self.frame_button.setMaximumHeight(80)
            self.frame_button.setMinimumHeight(80)

            self.frame_feature_mode.setMinimumWidth(600)
            self.frame_feature_mode.setMaximumWidth(600)

            self.frame_26.setMinimumHeight(40)
            self.frame_26.setMaximumHeight(40)

            self.frame_4.setMinimumWidth(200)
            self.frame_4.setMaximumWidth(200)

            self.frame_config_btn.setMinimumWidth(160)
            self.frame_config_btn.setMaximumWidth(160)

            self.frame_configuration_view.setMinimumHeight(280)
            self.frame_configuration_view.setMaximumHeight(280)
            self.frame_config_setting_panorama_view.setMinimumHeight(35)

            self.frame_config_button_group.setMinimumWidth(100)
            self.frame_config_button_group.setMaximumWidth(100)

    def set_theme_ui(self):
        """
        Set theme to user interface

        Returns:
            None
        """
        with open(self.source_file.get_theme_file(), "r") as file:
            Theme = file.read()
        self.centralwidget.setStyleSheet(Theme)

    def move_ui_to_center(self):
        """
        Move the user interface to the center of monitor when the first run the application.

        Returns:
            None
        """
        qr = self.parent.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.parent.move(qr.topLeft())

    def change_permission_root_file(self):
        """
        Get
        Returns:

        """
        target = "/opt/MoilDashCamera/maps/"
        user = getpwuid(stat(target).st_uid).pw_name
        if user == "root":
            passwd = self.get_password()
            if passwd is None:
                QtWidgets.QMessageBox.information(None,
                                                  "Warning!!", "you not write the password!!")
                return False
            else:
                os.system("echo " + passwd + "| sudo -S chown $USER /opt/MoilDashCamera/maps/")
                user = getpwuid(stat(target).st_uid).pw_name
                if user == "root":
                    QtWidgets.QMessageBox.information(None,
                                                      "Warning!!", "Your Password Is Wrong!!")
                    return False

                else:
                    for filename in os.listdir(target):
                        os.system("echo " + passwd + "| sudo -S chown $USER /opt/MoilDashCamera/maps/" + filename)
                    os.system("echo " + passwd + "| sudo -S chown $USER "
                                                 "/opt/MoilDashCamera/data_config/configuration_view.yaml")
                    return True

        else:
            return True

    @classmethod
    def get_password(cls):
        passwd, ok = QtWidgets.QInputDialog.getText(None, "First Authentication", "Write your Password?",
                                                    QtWidgets.QLineEdit.Password)
        if ok and passwd != '':
            return passwd

        else:
            return None

    def onclick_lbl_image_single_view(self, event):
        self.set_unchecked_btn()
        self.feature_mode = self.feature_mode_option[1]
        self.btn_home.setChecked(True)
        self.stackedWidget.setCurrentIndex(0)
        self.showing_image_to_ui()

    def onclick_lbl_panorama_image(self, event):
        self.onclick_panorama_view()

    def onclick_lbl_left_dash(self, event):
        self.onclick_left_window_view()

    def onclick_lbl_right_dash(self, event):
        self.onclick_right_window_view()

    def onclick_lbl_steering_dash(self, event):
        self.onclick_driver_view()

    def onclick_lbl_original_dash(self, event):
        self.onclick_second_driver_view()

    def onclick_select_media(self):
        """
        Select source media, It will pop up the window and give you choice to select the media source
        such as USB camera, Streaming camera, Load Video or Load Image

        Returns:
            None
        """
        # if self.change_permission_root_file():
        source_cam = SelectMedia(self)
        source_cam.exec()

        print(self.model.media_source)
        # else:
        #     QtWidgets.QMessageBox.information(None, "Warning!!", "Permission denied!!")

    # def onclick_change_camera_type(self):
    #     cam_type = camera_type(self.source_file.get_parameter_file())
    #     self.model.set_camera_type(cam_type)
    #     if self.model.camera_type is not None:
    #         self.model.create_object_moildev()
    #         self.show_properties_camera()
    #
    #         self.model.create_maps_panorama_dash()
    #         self.showing_image_to_ui()

    def onclick_change_camera_type(self):
        cam_type = camera_type(self.source_file.get_parameter_file())
        self.model.set_camera_type(cam_type)
        if self.model.camera_type is not None:
            self.model.create_object_moildev()
            self.show_properties_camera()
            self.model.create_maps_anypoint_view(self.setting_config.list_selection_view[0])
            self.model.create_maps_anypoint_view(self.setting_config.list_selection_view[1])
            self.model.create_maps_anypoint_view(self.setting_config.list_selection_view[2])
            self.model.create_maps_anypoint_view(self.setting_config.list_selection_view[3])
            self.model.create_maps_panorama_dash()
            self.showing_image_to_ui()

    def set_condition_car(self, condition):
        self.condition_car = condition
        if self.condition_car == "Car Parking":
            self.label_left_window.show()
            self.label_right_window.show()
            self.label_driver_view.show()
            self.label_second_driver_view.show()
        elif self.condition_car == "Car Stop":
            self.label_left_window.show()
            self.label_right_window.show()
            self.label_driver_view.setText("Moil Dash \n Camera")
            self.label_second_driver_view.setText("Moil Dash \n Camera")
        elif self.condition_car == "Car Moving":
            self.label_left_window.setText("Moil Dash \n Camera")
            self.label_right_window.setText("Moil Dash \n Camera")
            self.label_driver_view.show()
            self.label_second_driver_view.show()
        if self.model.image is not None:
            self.showing_image_to_ui()

    def onclick_modify_camera_parameter(self):
        ui_params = QtWidgets.QDialog()
        ui = CameraParametersForm(ui_params, self.source_file.get_parameter_file())
        ui_params.exec()
        # here reload the process using the new parameter modification

    def show_properties_camera(self):
        self.lbl_info_camera_type.setText(self.model.camera_type)
        self.lbl_info_source.setText(self.model.media_source_type)
        self.lbl_info_width_image.setText(str(self.model.moildev.image_width))
        self.lbl_info_height_image.setText(str(self.model.moildev.image_height))
        self.lbl_info_icx.setText(str(self.model.moildev.icx))
        self.lbl_info_icy.setText(str(self.model.moildev.icy))

    def update_to_user_interface(self):
        if self.model.image is None:
            print("No source media")
            self.timer.stop()
            self.feature_mode = self.feature_mode_option[0]
            self.onclick_select_media()
            self.btn_play_pause.setChecked(False)

        else:
            self.model.next_frame_process()
            self.showing_image_to_ui()

    def change_front_view(self):
        self.stackedWidget_setting.setCurrentIndex(self.comboBox_setting_select_main_view.currentIndex())
        self.showing_image_to_ui()

    @staticmethod
    def boundary_fov(image: np.ndarray, moildev, fov: int = 90,
                     color: tuple = (255, 255, 0)) -> np.ndarray:

        icx = moildev.icx
        icy = moildev.icy
        center = (icx, icy)

        boundary_radius = int(moildev.get_rho_from_alpha(fov))
        thickness = int(5)

        cv2.circle(image, center, radius=boundary_radius, color=color, thickness=thickness)

        return image

    def showing_image_to_ui(self):
        if self.model.image is not None:
            # setting mode
            image = mutils.rotate_image(self.model.image, self.model.rotation_angle_ori)
            image = self.model.control_contrast(image, self.spinBox_brighness.value(), self.spinBox_contrast.value())
            if self.feature_mode == self.feature_mode_option[0]:
                if self.comboBox_setting_select_main_view.currentIndex() == 0:
                    res_image = self.model.create_panorama_image(image.copy())
                    mutils.show_image_to_label(self.lbl_image_dash_main, res_image, self.size)
                elif self.comboBox_setting_select_main_view.currentIndex() == 1:
                    res_image = self.model.create_anypoint_mode_2(image.copy())
                    mutils.show_image_to_label(self.lbl_image_dash_main, res_image, self.zoom_anypoint_2)
                elif self.comboBox_setting_select_main_view.currentIndex() == 2:
                    image = self.boundary_fov(image, self.model.moildev, 70, (255, 0, 0))
                    image = self.boundary_fov(image, self.model.moildev, 90, (0, 0, 255))
                    image = self.boundary_fov(image, self.model.moildev, 110, (0, 255, 0))
                    res_image = self.model.create_panorama_x(image.copy())
                    mutils.show_image_to_label(self.lbl_image_dash_main, res_image, self.zoom_x_panorama)

                # cv2.imwrite("output_panorama.jpg", pano_image)
                if self.comboBox_select_view.currentIndex() == 0:
                    __image = self.model.create_anypoint_left_window(image.copy())
                    # cv2.imwrite("output_anypoint_left.jpg", image)
                elif self.comboBox_select_view.currentIndex() == 1:
                    __image = self.model.create_anypoint_right_window(image.copy())
                    # cv2.imwrite("output_anypoint_right.jpg", image)
                elif self.comboBox_select_view.currentIndex() == 2:
                    __image = self.model.create_anypoint_driver_view(image.copy())
                    # cv2.imwrite("output_driver_view.jpg", image)
                elif self.comboBox_select_view.currentIndex() == 3:
                    __image = self.model.create_anypoint_second_driver_view(image.copy())
                    # cv2.imwrite("output_second_driver_view.jpg", image)
                else:
                    __image = self.model.image.copy()

                mutils.show_image_to_label(self.lbl_image_anypoint_view, __image, self.width_ori_and_any_setting)
                mutils.show_image_to_label(self.lbl_image_original_dash, image, self.width_ori_and_any_setting)

            # home mode
            elif self.feature_mode == self.feature_mode_option[1]:
                if self.condition_car == "Car Parking":
                    if self.comboBox_setting_select_main_view.currentIndex() == 0:
                        res_image = self.model.create_panorama_image(image.copy())
                    elif self.comboBox_setting_select_main_view.currentIndex() == 1:
                        res_image = self.model.create_anypoint_mode_2(image.copy())
                    elif self.comboBox_setting_select_main_view.currentIndex() == 2:
                        res_image = self.model.create_panorama_x(image.copy())
                    else:
                        res_image = self.model.image
                    mutils.show_image_to_label(self.lbl_panorama_image, res_image, self.size)
                    image_left_window = self.model.create_anypoint_left_window(image.copy())
                    mutils.show_image_to_label(self.label_left_window, image_left_window, self.width_any_in_home)
                    image_right_window = self.model.create_anypoint_right_window(image.copy())
                    mutils.show_image_to_label(self.label_right_window, image_right_window, self.width_any_in_home)
                    image_driver_view = self.model.create_anypoint_driver_view(image.copy())
                    mutils.show_image_to_label(self.label_driver_view, image_driver_view, self.width_any_in_home)
                    image_second_driver = self.model.create_anypoint_second_driver_view(image.copy())
                    mutils.show_image_to_label(self.label_second_driver_view, image_second_driver,
                                               self.width_any_in_home)

                elif self.condition_car == "Car Stop":
                    if self.comboBox_setting_select_main_view.currentIndex() == 0:
                        res_image = self.model.create_panorama_image(image.copy())
                    elif self.comboBox_setting_select_main_view.currentIndex() == 1:
                        res_image = self.model.create_anypoint_mode_2(image.copy())
                    elif self.comboBox_setting_select_main_view.currentIndex() == 2:
                        res_image = self.model.create_panorama_x(image.copy())
                    else:
                        res_image = self.model.image
                    mutils.show_image_to_label(self.lbl_panorama_image, res_image, self.size)
                    image_left_window = self.model.create_anypoint_left_window(image.copy())
                    mutils.show_image_to_label(self.label_left_window, image_left_window, self.width_any_in_home)
                    image_right_window = self.model.create_anypoint_right_window(image.copy())
                    mutils.show_image_to_label(self.label_right_window, image_right_window, self.width_any_in_home)

                elif self.condition_car == "Car Moving":
                    if self.comboBox_setting_select_main_view.currentIndex() == 0:
                        res_image = self.model.create_panorama_image(image.copy())
                    elif self.comboBox_setting_select_main_view.currentIndex() == 1:
                        res_image = self.model.create_anypoint_mode_2(image.copy())
                    elif self.comboBox_setting_select_main_view.currentIndex() == 2:
                        res_image = self.model.create_panorama_x(image.copy())
                    else:
                        res_image = image
                    mutils.show_image_to_label(self.lbl_panorama_image, res_image, self.size)
                    image_driver_view = self.model.create_anypoint_driver_view(image.copy())
                    mutils.show_image_to_label(self.label_driver_view, image_driver_view, self.width_any_in_home)
                    image_second_driver = self.model.create_anypoint_second_driver_view(image.copy())
                    mutils.show_image_to_label(self.label_second_driver_view, image_second_driver,
                                               self.width_any_in_home)

            # panorama mode
            elif self.feature_mode == self.feature_mode_option[2]:
                if self.comboBox_setting_select_main_view.currentIndex() == 0:
                    res_image = self.model.create_panorama_image(image.copy())
                elif self.comboBox_setting_select_main_view.currentIndex() == 1:
                    res_image = self.model.create_anypoint_mode_2(image.copy())
                elif self.comboBox_setting_select_main_view.currentIndex() == 2:
                    res_image = self.model.create_panorama_x(image.copy())
                else:
                    res_image = image
                mutils.show_image_to_label(self.lbl_image_single_view, res_image, self.size)

            # left window view
            elif self.feature_mode == self.feature_mode_option[3]:
                image_left_window = self.model.create_anypoint_left_window(image.copy())
                mutils.show_image_to_label(self.lbl_image_single_view, image_left_window, self.size)

            # right window view
            elif self.feature_mode == self.feature_mode_option[4]:
                image_right_window = self.model.create_anypoint_right_window(image.copy())
                mutils.show_image_to_label(self.lbl_image_single_view, image_right_window, self.size)

            # driver view
            elif self.feature_mode == self.feature_mode_option[5]:
                image_driver_view = self.model.create_anypoint_driver_view(image.copy())
                mutils.show_image_to_label(self.lbl_image_single_view, image_driver_view, self.size)

            # second driver view
            elif self.feature_mode == self.feature_mode_option[6]:
                image_second_driver = self.model.create_anypoint_second_driver_view(image.copy())
                mutils.show_image_to_label(self.lbl_image_single_view, image_second_driver, self.size)

            # original view
            elif self.feature_mode == self.feature_mode_option[7]:
                mutils.show_image_to_label(self.lbl_image_single_view, image.copy(), self.size)

        else:
            self.timer.stop()

        self.set_value_slider_video()
        self.set_time_video()

    # video controller
    def onclick_play_pause_video(self):
        """
            This function is for control timer running video

        Returns:
            None
        """
        if self.btn_play_pause.isChecked():
            self.timer.start()

        else:
            self.timer.stop()

        if self.model.image is not None:
            self.set_icon.set_icon_play_pause()

    def onclick_stop_video(self):
        """
            This function is for get action stop video
        Returns:
            None
        """
        self.btn_play_pause.setChecked(False)
        self.model.stop_video()
        self.set_value_slider_video()
        self.timer.stop()
        self.update_to_user_interface()
        self.set_icon.set_icon_play_pause()

    def onclick_rewind_video(self):
        """
            This function is for get action rewind video
        Returns:

        """
        self.model.rewind_video()
        self.set_value_slider_video()
        self.update_to_user_interface()

    def onclick_forward_video(self):
        """
            This function is get action for forward video
        Returns:

        """
        self.model.forward_video()
        self.set_value_slider_video()
        self.update_to_user_interface()

    def onclick_slider_video(self, value):
        """
            This function is to get value input from slider user interface
        Args:
            value: position of slider

        Returns:
            None
        """
        value_max = self.slider_video.maximum()
        self.model.slider_controller(value, value_max)
        self.update_to_user_interface()

    def set_value_slider_video(self):
        """
            set slider position base on length video
        Returns:
            None
        """
        value = self.slider_video.maximum()
        if not self.model.frame_count <= 0:
            current_position = self.model.get_value_slider_video(value)
            self.slider_video.blockSignals(True)
            # self.slider_video.setValue(current_position)
            self.slider_video.blockSignals(False)

    def set_time_video(self):
        """
            set time of video in label
        Returns:
            None
        """
        total_minute = self.model.total_minute
        total_second = self.model.total_second
        current_minute = self.model.current_minute
        current_second = self.model.current_second
        self.lbl_current_time.setText("%02d:%02d" % (current_minute, current_second))
        if total_minute < 0:
            self.lbl_total_time.setText("--:--")
        else:
            self.lbl_total_time.setText("%02d:%02d" % (total_minute, total_second))

    def onclick_home_button(self):
        if self.model.image is None:
            self.stackedWidget.setCurrentIndex(3)
            self.btn_home.setChecked(False)
            self.parent.setWindowTitle("Moil Dash Camera")
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.set_unchecked_btn()
            self.feature_mode = self.feature_mode_option[1]
            self.btn_setting.setChecked(False)
            self.btn_home.setChecked(True)
            self.showing_image_to_ui()
            self.parent.setWindowTitle("Home - Moil Dash Camera")

    # btn_panorama_view
    def onclick_panorama_view(self):
        if self.model.image is None:
            self.stackedWidget.setCurrentIndex(3)
            self.btn_home.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.btn_panorama_view.setChecked(True)
            self.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[2]
            self.showing_image_to_ui()
            self.parent.setWindowTitle("Panorama View - Moil Dash Camera")

    def onclick_left_window_view(self):
        if self.model.image is None:
            self.stackedWidget.setCurrentIndex(3)
            self.btn_home.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.btn_left_window.setChecked(True)
            self.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[3]
            self.showing_image_to_ui()
            self.parent.setWindowTitle("Left Window View - Moil Dash Camera")

    def onclick_right_window_view(self):
        if self.model.image is None:
            self.stackedWidget.setCurrentIndex(3)
            self.btn_home.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.btn_right_window.setChecked(True)
            self.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[4]
            self.showing_image_to_ui()
            self.parent.setWindowTitle("Right Window View - Moil Dash Camera")

    def onclick_driver_view(self):
        if self.model.image is None:
            self.stackedWidget.setCurrentIndex(3)
            self.btn_home.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.btn_driver_view.setChecked(True)
            self.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[5]
            self.showing_image_to_ui()
            self.parent.setWindowTitle("Driver View - Moil Dash Camera")

    def onclick_second_driver_view(self):
        if self.model.image is None:
            self.stackedWidget.setCurrentIndex(3)
            self.btn_home.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.btn_second_driver_view.setChecked(True)
            self.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[6]
            self.showing_image_to_ui()
            self.parent.setWindowTitle("Second Driver View - Moil Dash Camera")

    def onclick_original_view(self):
        if self.model.image is None:
            self.stackedWidget.setCurrentIndex(3)
            self.btn_home.setChecked(False)
        else:
            self.set_unchecked_btn()
            self.btn_original_view.setChecked(True)
            self.stackedWidget.setCurrentIndex(1)
            self.feature_mode = self.feature_mode_option[7]
            self.showing_image_to_ui()
            self.parent.setWindowTitle("Original View - Moil Dash Camera")

    def onclick_button_settings(self):
        if self.btn_setting.isChecked():
            self.set_unchecked_btn()
            self.btn_setting.setChecked(True)
            self.stackedWidget.setCurrentIndex(2)
            self.feature_mode = self.feature_mode_option[0]
            self.parent.setWindowTitle("Setting - Moil Dash Camera")

        else:
            self.onclick_close_setting_mode()
        self.showing_image_to_ui()

    def onclick_close_setting_mode(self):
        if self.model.image is None:
            self.stackedWidget.setCurrentIndex(3)
            self.btn_setting.setChecked(False)
            self.parent.setWindowTitle("Moil Dash Camera")
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.feature_mode = self.feature_mode_option[1]
            self.btn_setting.setChecked(False)
            self.btn_home.setChecked(True)
            self.parent.setWindowTitle("Home - Moil Dash Camera")
            self.showing_image_to_ui()

    def set_unchecked_btn(self):
        self.btn_home.setChecked(False)
        self.btn_panorama_view.setChecked(False)
        self.btn_second_driver_view.setChecked(False)
        self.btn_driver_view.setChecked(False)
        self.btn_left_window.setChecked(False)
        self.btn_right_window.setChecked(False)
        self.btn_original_view.setChecked(False)
        self.btn_setting.setChecked(False)

    def record_video(self):
        self.timer.stop()
        self.btn_play_pause.setChecked(False)
        self.set_icon.set_icon_play_pause()
        if self.btn_record.isChecked():
            if self.model.image is not None and self.model.media_source_type != "Image":
                directory = mutils.select_directory(title="Select saved directory !!")
                if directory:
                    self.model.record_video(True, directory)
                    self.status_recording.setText("Now Recording !!")
                    self.btn_record.setText("Stop")
                else:
                    self.btn_record.setChecked(False)
                    QtWidgets.QMessageBox.warning(None, "Warning!!",
                                                  "You not select the directory!")
                    self.status_recording.setText("")
                    self.btn_record.setText("Rec")
            else:
                self.btn_record.setChecked(False)
                self.status_recording.setText("")
                self.btn_record.setText("Rec")

        else:
            self.status_recording.setText("")
            self.btn_record.setText("Rec")
            self.model.record_video(False)
            QtWidgets.QMessageBox.information(None, "Information!!", "Record Finish!")

    def save_image(self):
        active_main_view = self.comboBox_setting_select_main_view.currentIndex()
        if self.model.image is not None:
            if self.btn_play_pause.isChecked():
                self.timer.stop()
                self.btn_play_pause.setChecked(False)
                self.set_icon.set_icon_play_pause()
            directory = mutils.select_directory(title="Select directory!")
            if directory:
                self.model.save_image(directory, self.feature_mode, active_main_view)
                QtWidgets.QMessageBox.information(None, "Information!!", "Image saved!")
            else:
                QtWidgets.QMessageBox.warning(None, "Warning!!", "Please select a directory to save image!")
            if self.btn_play_pause.isChecked():
                self.timer.start()

    def closeEvent(self, event):
        self.timer.stop()
        self.btn_play_pause.setChecked(False)
        self.set_icon.set_icon_play_pause()
        reply = QtWidgets.QMessageBox.question(self.parent, "Message?", "Are you sure want to quit ?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.timer.stop()
            event.accept()
        else:
            event.ignore()

    # # SELECT
    # @classmethod
    # def selected_button(cls):
    #     MENU_SELECTED_STYLESHEET_DARK_MODE = """
    #         background-color: rgb(19, 102, 161);
    #         """
    #     select = MENU_SELECTED_STYLESHEET_DARK_MODE
    #     return select
    #
    # # RESET SELECTION
    # def unselected_button(self):
    #     MENU_SELECTED_STYLESHEET_DARK_MODE = """
    #
    #         background-color: rgb(25, 70, 102);
    #         """
    #     for w in self.frame_button.findChildren(QPushButton):
    #         if w.isChecked() is False:
    #             w.setStyleSheet(MENU_SELECTED_STYLESHEET_DARK_MODE)
    #
    #     for w in self.frame_button.findChildren(QPushButton):
    #         if w.isChecked() is False:
    #             w.setStyleSheet(MENU_SELECTED_STYLESHEET_DARK_MODE)
    #
    # def set_button_style(self):
    #     self.unselected_button()
    #     for w in self.frame_button.findChildren(QPushButton):
    #         if w.isChecked():
    #             w.setStyleSheet(self.selected_button())
