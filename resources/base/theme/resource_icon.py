import os
from PyQt5.QtCore import QDir

"""
This used to manipulate path names, access information regarding paths and files, 
and manipulate the underlying file system
"""
CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
QDir.addSearchPath("icons", CURRENT_DIRECTORY + "../images")
