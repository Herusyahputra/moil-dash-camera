from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSize
from controller.control_resources import GetResorcesFile


class ControlIconFeatureMode:
    def __init__(self, controller):
        super(ControlIconFeatureMode, self).__init__()
        self.controller = controller
        self.source_file = GetResorcesFile()

        if self.controller.res == "case_1":
            size_feature = QSize(40, 40)
            size_setting = QSize(30, 30)
        elif self.controller.res == "case_2":
            size_feature = QSize(60, 60)
            size_setting = QSize(50, 50)
        elif self.controller.res == "case_3":
            size_feature = QSize(80, 80)
            size_setting = QSize(60, 60)
        else:
            size_feature = QSize(35, 35)
            size_setting = QSize(30, 30)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_home()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_home.setIcon(icon)
        self.controller.btn_home.setIconSize(size_setting)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_panorama_view()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_panorama_view.setIcon(icon)
        self.controller.btn_panorama_view.setIconSize(size_feature)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_driver_view()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_driver_view.setIcon(icon)
        self.controller.btn_driver_view.setIconSize(size_feature)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_left_view()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_left_window.setIcon(icon)
        self.controller.btn_left_window.setIconSize(size_feature)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_right_view()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_right_window.setIcon(icon)
        self.controller.btn_right_window.setIconSize(size_feature)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_second_driver_view()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_second_driver_view.setIcon(icon)
        self.controller.btn_second_driver_view.setIconSize(size_feature)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_original_fisheye()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_original_view.setIcon(icon)
        self.controller.btn_original_view.setIconSize(size_feature)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_screenshot()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_screenshot_active_image.setIcon(icon)
        self.controller.btn_screenshot_active_image.setIconSize(size_feature)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_setting()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_setting.setIcon(icon)
        self.controller.btn_setting.setIconSize(size_setting)