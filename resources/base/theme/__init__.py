import os
from resource_icon import *

# print(os.path.dirname(os.path.realpath(__file__)))
os.chdir(os.path.dirname(os.path.realpath(__file__)))
with open("theme.css", "r") as file:
    Theme = file.read()
