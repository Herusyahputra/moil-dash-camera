from PyQt5 import QtWidgets, QtCore


class SelectCondition:
    def __init__(self, main_control):
        self.main_control = main_control
        self.comboBox_select_condition_car = QtWidgets.QComboBox(self.main_control.lbl_panorama_image)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_select_condition_car.sizePolicy().hasHeightForWidth())
        self.comboBox_select_condition_car.setSizePolicy(sizePolicy)
        self.comboBox_select_condition_car.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_select_condition_car.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBox_select_condition_car.setObjectName("comboBox_select_condition_car")
        self.comboBox_select_condition_car.addItem("Car Parking")
        self.comboBox_select_condition_car.addItem("Car Stop")
        self.comboBox_select_condition_car.addItem("Car Moving")
        self.main_control.set_condition_car(self.comboBox_select_condition_car.currentText())
        self.comboBox_select_condition_car.currentIndexChanged.connect(self.selection_changed)

    def selection_changed(self):
        self.main_control.set_condition_car(self.comboBox_select_condition_car.currentText())
