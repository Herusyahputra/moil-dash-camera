import json
import cv2
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtWidgets
from view.ui_select_media import Ui_Dialog
from model.moilutils.moilutils import select_file
from model.moilutils.camera_parameter import CameraParametersForm


class SelectMedia(QDialog):
    """
    This class has function to select the media want to use in application.
    The media support for this application is USB camera, 
    Streaming camera/Ip camera ideo and Image.
    """
    def __init__(self, control_main):
        super(SelectMedia, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.resize(550, 280)

        self.control_main = control_main

        self.ui.central_widget.setStyleSheet(style_appearance)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.camera_path = None
        self.select_media_source_type()

        self.refresh_camera_parameter_list()

        self.connect_button()

    def connect_button(self):
        """
        Connect button to function for make an event in user interface
        
        Returns:
            None
        """
        self.ui.comboBox_camera_sources.currentIndexChanged.connect(self.select_media_source_type)
        self.ui.btn_detect_port_Camera.clicked.connect(self.check_port_usb_camera)
        self.ui.btn_load_media.clicked.connect(self.onclick_load_media)
        self.ui.btn_add_camera_params.clicked.connect(self.onclick_camera_parameter_form)
        self.ui.btn_cancel.clicked.connect(self.close)
        self.ui.btn_ok.clicked.connect(self.onclick_ok)

    def refresh_camera_parameter_list(self):
        """
        When editing the camera parameter, this will show the list of the camera parameter in uptodate

        Returns:
            None
        """
        new_list = []
        with open(self.control_main.source_file.get_parameter_file()) as f:
            data_parameter = json.load(f)
        for key in data_parameter.keys():
            new_list.append(key)
        self.ui.comboBox_cam_type.addItems(new_list)

    def onclick_camera_parameter_form(self):
        """
        Showing camera parameter form that can edit, delete, add new parameter on databases.

        Returns:
            None
        """
        ui_params = QtWidgets.QDialog()
        ui = CameraParametersForm(ui_params, self.control_main.source_file.get_parameter_file())
        ui_params.exec()
        self.refresh_camera_parameter_list()

    def onclick_ok(self):
        """
        When you press button "ok" in load media windows, if media is not None then will begin the process

        Returns:
            None
        """
        self.camera_source_used()
        if self.state is True:
            self.control_main.update_to_user_interface()
            self.control_main.show_properties_camera()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(None, "Warning !!", "You not select the file path !!")

    def onclick_load_media(self):
        """
        Load media function to select the media path in your local directory,
        the media can be images or videos

        Returns:
            None
        """
        file_path = select_file(None, "Select Media !!", "",
                                "Files format (*.jpeg *.jpg *.png *.gif *.bmg *.avi *.mp4)")
        if file_path:
            self.ui.media_path.setText(file_path)

    def camera_source_used(self):
        """
        This function will set the source of camera used in model class depend on what the media used.

        Returns:
            set media source
        """
        if self.ui.comboBox_camera_sources.currentText() == "USB Camera":
            self.control_main.model.set_camera_type(self.ui.comboBox_cam_type.currentText())
            self.control_main.model.set_media_source_used(int(self.ui.portCamera.currentText()))
            self.state = True

        elif self.ui.comboBox_camera_sources.currentText() == "Load Media":
            if self.ui.media_path.text() == "":
                self.state = False

            else:
                self.control_main.model.set_camera_type(self.ui.comboBox_cam_type.currentText())
                self.control_main.model.set_media_source_used(self.ui.media_path.text())
                print(self.ui.media_path.text())
                self.state = True
        else:
            self.control_main.model.set_camera_type(self.ui.comboBox_cam_type.currentText())
            self.control_main.model.set_media_source_used(self.ui.camera_stream_link.text())
            self.state = True

    def select_media_source_type(self):
        """
        Select the media source type from the comboBox event.

        Returns:
            None
        """
        if self.ui.comboBox_camera_sources.currentText() == "USB Camera":
            self.ui.label_3.setText("Select Port :")
            self.ui.portCamera.show()
            self.ui.btn_detect_port_Camera.show()
            self.ui.camera_stream_link.hide()
            self.ui.btn_load_media.hide()
            self.ui.media_path.hide()

        elif self.ui.comboBox_camera_sources.currentText() == "WEB Camera":
            self.ui.label_3.setText("Camera Link :")
            self.ui.camera_stream_link.show()
            self.ui.portCamera.hide()
            self.ui.btn_load_media.hide()
            self.ui.media_path.hide()
            self.ui.btn_detect_port_Camera.hide()

        elif self.ui.comboBox_camera_sources.currentText() == "Load Media":
            self.ui.label_3.setText("Media Path :")
            self.ui.camera_stream_link.hide()
            self.ui.portCamera.hide()
            self.ui.btn_load_media.show()
            self.ui.media_path.show()
            self.ui.btn_detect_port_Camera.hide()

        else:
            pass

    @classmethod
    def check_port_usb_camera(cls):
        """
        Check the port of USB camera available in your device

        Returns:
            None
        """
        list_port_available = []
        for camera_idx in range(5):
            cap = cv2.VideoCapture(camera_idx)
            if cap.isOpened():
                list_port_available.append(camera_idx)
                cap.release()
        msgbox = QtWidgets.QMessageBox()
        msgbox.setStyleSheet("color:white;background-color: rgb(37, 41, 48)")
        msgbox.setWindowTitle("Camera Port Available")
        # self.ui.central_widget.setStyleSheet(style_appearance)
        # msgbox.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        # msgbox.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        msgbox.setText(
            "Select the port camera from the number in list !! \n"
            "Available Port = " + str(list_port_available))
        msgbox.exec()


style_appearance = """
    QWidget {
        color: rgb(221, 221, 221);
        font: 10pt "Segoe UI";
        border: none;
    }

    #frame{
        background-color: rgb(37, 41, 48);
        border: 1px solid rgb(44, 49, 58);
        border-radius: 10px;
    }

    #label_title{
        color: rgb(238,238,238);
        font: 14pt "Segoe UI";
    }

    QLineEdit {
        font: 9pt "Segoe UI";
        background-color: rgb(33, 37, 43);
        border-radius: 5px;
        border: 2px solid rgb(33, 37, 43);
        padding-left: 10px;
        selection-color: rgb(255, 255, 255);
        selection-background-color: rgb(255, 121, 198);
    }

QLineEdit:hover {
    border: 2px solid rgb(64, 71, 88);
}

QLineEdit:focus {
    border: 2px solid rgb(91, 101, 124);
}

QComboBox{
    background-color: rgb(27, 29, 35);
    border-radius: 5px;
    border: 2px solid rgb(33, 37, 43);
    padding: 1px;
    padding-left: 15px;
}
#portCamera::drop-down{
    border:0Px;
}

QComboBox:hover{
    border: 2px solid rgb(64, 71, 88);
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px; 
    border-left-width: 3px;
    border-left-color: rgba(39, 44, 54, 150);
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;	
    background-position: center;
    background-repeat: no-reperat;
 }
QComboBox QAbstractItemView {
    color: rgb(255, 121, 198);	
    background-color: rgb(33, 37, 43);
    padding: 10px;
    selection-background-color: rgb(39, 44, 54);
}

QPushButton {
    border: 2px solid rgb(52, 59, 72);
    border-radius: 5px;	
    background-color: rgb(52, 59, 72);
}

QPushButton:hover {
    background-color: rgb(57, 65, 80);
    border: 2px solid rgb(61, 70, 86);
}

QPushButton:pressed {	
    background-color: rgb(35, 40, 49);
    border: 2px solid rgb(43, 50, 61);
}"""
