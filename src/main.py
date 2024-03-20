
import numpy as np
import cv2
from ctypes import *
import yaml
import os
import datetime
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from controller.control_main import Controller


def main():
    """
    This is the main code for running the application

    This modification by example.


    Returns:
        Showing user interface
    """
    app = QApplication(sys.argv)
    main = QtWidgets.QMainWindow()
    ui = Controller(main)
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
