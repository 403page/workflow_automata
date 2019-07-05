import sys
import pickle

sys.path.append('/home/gd6b/fe/wanghua/view1/scan')
sys.path.append('/home/gd6b/fe/wanghua/view1/scan/rules')

from project_class import *
from main_window_gui import *

front_app = QApplication(sys.argv)

current_proj = project('Bridge')

UI = MainWindow(current_proj)
sys.exit(front_app.exec_())
