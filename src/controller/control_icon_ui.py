from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSize
from controller.control_resources import GetResorcesFile


class ControlIconInUI:
    def __init__(self, controller):
        super(ControlIconInUI, self).__init__()
        self.controller = controller
        self.source_file = GetResorcesFile()

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_folder()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_source_config.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_edit_parameter_icon()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_parameter_form.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_camera_icon()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_change_camera_type.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_back()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_close_dash.setIcon(icon)

        self.set_icon_play_pause()
        self.set_icon_video_controller()

    def set_icon_play_pause(self):
        """
            Set icon for button play and pause video
        Returns:
            None
        """
        icon = QtGui.QIcon()
        if self.controller.btn_play_pause.isChecked():
            icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_pause()), QtGui.QIcon.Mode.Normal,
                           QtGui.QIcon.State.Off)
        else:
            icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_play()), QtGui.QIcon.Mode.Normal,
                           QtGui.QIcon.State.Off)
        self.controller.btn_play_pause.setIcon(icon)

    def set_icon_video_controller(self):
        """
            Set icon vidio controller
        Returns:
            None
        """
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_rewind()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_rewind.setIcon(icon)

        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_square()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_stop.setIcon(icon)

        icon.addPixmap(QtGui.QPixmap(self.source_file.get_icon_forward()), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.controller.btn_forward.setIcon(icon)
