# temp gui main window for this proj
# import gui items
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
# import common lib
import sys
import subprocess
import os

# pickle to save/load
import pickle

# for importing
import project_class

class automata_tree_item(QTreeWidgetItem):
    # tree item with pointer
    def __init__(self, tree_widget):
        super().__init__(tree_widget)
        self.pointer = None


#class MainWindow(QWidget):
class MainWindow(QMainWindow):
    # main window class
    def __init__(self, loading_projcet):
        # initial from father class
        super(MainWindow,self).__init__()
        self.project           = loading_projcet
        # initial items on this UI
        # main layout
        self.splitter_task     = None
        self.splitter_main     = None
        # task layout
        self.task_tree_box     = None
        self.task_status_box   = None
        # log layout
        self.log_box           = None
        # in task layout
        self.task_tree         = None
        self.task_status_box   = None
        self.readiness_list    = None
        self.result_check_list = None
        self.show_path         = None
        self.show_path_file    = None
        # in log layout
        self.log_shower        = None
        self.log_editer        = None
        #self.log_enter_button  = None
        self.initUI()

    def initUI(self):
        # create boxes
        self.create_task_tree_box()
        self.create_tool_bar()
        self.create_task_status_box()
        self.create_log_box()
        # main layout 
        mainLayout = QVBoxLayout()
        # create splitters
        self.splitter_task = QSplitter(Qt.Horizontal)
        self.splitter_task.addWidget(self.task_tree_box)
        #self.splitter_task.addWidget(self.file_browser_box)
        self.splitter_task.addWidget(self.task_status_box)
        self.splitter_main = QSplitter(Qt.Vertical)
        self.splitter_main.addWidget(self.splitter_task)
        self.splitter_main.addWidget(self.log_box)
        # applly to main layout
        mainLayout.addWidget(self.splitter_main)
        # add a dummy widget to load main layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(mainLayout)
        # config main UI
        self.setWindowTitle('Automata UI - %s'%self.project)
        self.resize(1200, 800)
        self.show()
        return

    def add_log_msg(self, msg = ''):
        self.log_shower.append(msg)
        return

    def create_tool_bar(self):
        # tool bar buttons
        new_action = QAction(QIcon(), 'New Version', self)
        save_action = QAction(QIcon(), 'Save status', self)
        load_action = QAction(QIcon(), 'Load status', self)
        build_action = QAction(QIcon(), 'Build tasks', self)
        build_new_action = QAction(QIcon(), 'Build single custom task', self)
        check_action = QAction(QIcon(), 'Check tasks', self)
        delete_action = QAction(QIcon(), 'Delete data', self)
        report_action = QAction(QIcon(), 'Generate report', self)
        # tool bar config
        self.project_toolbar = self.addToolBar('Project tool bar')
        self.task_toolbar = self.addToolBar('Task tool bar')
        # tool bar actions
        new_action.triggered.connect(self.add_new_version)
        save_action.triggered.connect(self.save_project)
        load_action.triggered.connect(self.load_project)
        build_action.triggered.connect(self.build_all_tasks)
        build_new_action.triggered.connect(self.build_custom_task)
        check_action.triggered.connect(self.check_selected_tree_item)
        # add to tool bar
        self.project_toolbar.addAction(new_action)
        self.project_toolbar.addAction(save_action)
        self.project_toolbar.addAction(load_action)
        self.task_toolbar.addAction(build_action)
        self.task_toolbar.addAction(build_new_action)
        self.task_toolbar.addAction(check_action)
        self.task_toolbar.addAction(delete_action)
        self.task_toolbar.addAction(report_action)
        return

    def create_task_tree_box(self):
        # create a sub layout
        sub_layout = QGridLayout()
        # initial task tree related
        self.task_tree_box = QGroupBox('Task browser')
        self.task_tree = QTreeWidget()
        self.task_tree.setColumnCount(1)
        self.task_tree.setIconSize(QSize(22, 22))
        self.task_tree.setHeaderLabels(['Block and Task'])
        # show select item to status box
        self.task_tree.itemClicked.connect(self.show_selected_tree_item)
        self.task_tree.itemDoubleClicked.connect(self.run_selected_tree_item)
        # add show path line edit
        self.show_path = QLineEdit()
        self.show_path.setReadOnly(True)
        self.show_path_file = QListWidget()
        self.show_path_file.itemDoubleClicked.connect(self.open_file)
        # update layout
        sub_layout.addWidget(self.task_tree, 0, 0, 1, 1)
        sub_layout.addWidget(self.show_path_file, 0, 1, 1, 2)
        sub_layout.addWidget(self.show_path, 1, 0, 2, 3)
        self.task_tree_box.setLayout(sub_layout)
        return

    def create_task_status_box(self):
        # create a sub layout
        sub_layout = QGridLayout()
        # initial task status related
        self.task_status_box = QGroupBox('Task status')
        self.readiness_list = QListWidget()
        self.result_check_list = QListWidget()
        # update layout
        sub_layout.addWidget(self.readiness_list, 0, 0, 3, 3)
        sub_layout.addWidget(self.result_check_list, 4, 0, 3, 3)
        self.task_status_box.setLayout(sub_layout)
        return

    def create_log_box(self):
        # create a sub layout
        sub_layout = QGridLayout()
        # initial log related
        self.log_box = QGroupBox('Log and Report')
        self.log_shower       = QTextBrowser()
        self.log_editer       = QLineEdit()
        #self.log_enter_button = QPushButton('Enter')
        #log_shower.setPlainText('log here')
        # update layout
        sub_layout.addWidget(self.log_shower, 0, 0)
        sub_layout.addWidget(self.log_editer, 5, 0)
        #sub_layout.addWidget(self.log_enter_button, 5, 22)
        self.log_box.setLayout(sub_layout)
        return

    def show_version_tree(self):
        # show tree for all version
        version_string = ''
        for version in self.project.version_dict.values():
            self.add_version_tree(version)
            version_string += version.version_name
        return 'All version loaded: %s\n'%version_string

    def add_version_tree(self, version_or_block = None, father_node = None, tree_item_string = ''):
        # display version tree
        # take version as root
        if not father_node:
        # root item have tree as father
            version_node = automata_tree_item(self.task_tree)
            version_node.setText(0, version_or_block.version_name)
            version_node.setIcon(0, QIcon('version.png'))
            father_node = version_node
            version_node.pointer = version_or_block

        # add all task
        for task_name in version_or_block.task_dict.keys():
            # edit current task
            current_node = automata_tree_item(father_node)
            current_node.setText(0, task_name)
            current_node.setIcon(0, QIcon('task.png'))
            current_node.pointer = version_or_block.task_dict[task_name]

        # add_all_sub_block
        for sub_block_name in version_or_block.sub_block_dict.keys():
            # edit current block
            current_node = automata_tree_item(father_node)
            current_node.setText(0, sub_block_name)
            current_node.setIcon(0, QIcon('block.png'))
            current_node.pointer = version_or_block.sub_block_dict[sub_block_name]
            # add sub block
            self.add_version_tree(version_or_block.sub_block_dict[sub_block_name], current_node, tree_item_string + sub_block_name)
        return

    def open_file(self, item):
        file_name = '%s/%s'%(self.show_path.displayText(), item.text())
        if not os.path.exists(file_name):
            self.add_log_msg('<font color=\"#FF9900\">' + '[Warning] File/dir not found: %s'%file_name + '</font>')
        else:
            if os.path.isdir(file_name):
                self.show_file_list_item(file_name)
            else:
                os.system('gedit %s&'%file_name)
                self.add_log_msg('<font color=\"#000000\">' + '[Info] Editing file: %s'%file_name + '</font>')
        return

    def show_file_list_item(self, path):
        ## show path and files in UI
        # show path
        self.show_path.setText(path)
        self.show_path_file.clear()
        if os.path.exists(path):
            # show file
            # clean old data on file list
            for file in ['..'] + os.listdir(path):
                new_item = QListWidgetItem(self.show_path_file)
                if os.path.isdir('%s/%s'%(path, file)):
                    new_item.setIcon(QIcon('dir.png'))
                else:
                    new_item.setIcon(QIcon('file.png'))
                new_item.setText(file)
        else:
            new_item = QListWidgetItem(self.show_path_file)
            new_item.setIcon(QIcon('failed.png'))
            new_item.setText('Path donnot exist')

    def add_new_version(self):
        version_name, ok = QInputDialog.getText(self, 'New version dialog', 'Please input the version name')
        # to check if version already exist
        if ok and not version_name in self.project.version_dict.keys():
            # to check if project config exist
            if os.path.exists('./project_conf_%s.py'%(version_name)):
                self.task_tree.clear()
                new_ver = project_class.version(version_name)
                new_ver.read_version_para(version_name)
                new_ver.initial_project_blocks()
                self.project.version_dict[version_name] = (new_ver)
                self.show_version_tree()
            else:
                # raise an error
                self.add_log_msg('<font color=\"#FF0000\">' + '[Error] Version %s not found'%version_name + '</font>')
        else:
            # version already exist
            self.add_log_msg('<font color=\"#FF0000\">' + '[Error] Version %s already exist or canceled'%version_name + '</font>')
        return

    def save_project(self):
        # save project to
        f = open('./project_data.db', 'wb')
        # save as non-text
        pickle.dump(self.project, f, 1)
        f.close()
        self.add_log_msg('<font color=\"#000000\">' + '[Info] Project data saved to ./project_data.db' + '</font>')
        return

    def load_project(self):
        if os.path.exists('./project_data.db'):
            # project data do exists, load it
            f = open('./project_data.db', 'rb')
            self.project = pickle.load(f)
            self.task_tree.clear()
            self.show_version_tree()
            f.close()
            self.add_log_msg('<font color=\"#000000\">' + '[Info] Project data loaded from ./project_data.db' + '</font>')
        else:
            # raise an error
            self.add_log_msg('<font color=\"#FF0000\">' + '[Error] Project saved data file ./project_data.db not found' + '</font>')
        return

    def build_custom_task(self):
        # check if selected in tree
        if not self.task_tree.currentItem():
            self.add_log_msg('<font color=\"#FF9900\">' + '[Warning] No item selected on task tree' + '</font>')
            return
        # check selected a task
        if not (self.task_tree.currentItem().pointer.task_name == str(self.task_tree.currentItem().pointer)):
            self.add_log_msg('<font color=\"#FF9900\">' + '[Warning] The selected item on task tree: %s is not a task'%self.task_tree.currentItem().pointer + '</font>')
            return
        else:
            task_fake_name, ok = QInputDialog.getText(self, 'New task', 'Please input a new task name with unique postfix')
            current_block = self.task_tree.currentItem().pointer.block_pointer
            current_block.read_block_para()
            current_task  = self.task_tree.currentItem().pointer
            current_block.initial_task(current_task.task_name, task_fake_name)
            self.add_log_msg('<font color=\"#000000\">' + '[Info] Building custom task env for task: %s for block: %s'%(current_task.task_name, current_block.block_name) + '</font>')
            self.task_tree.clear()
            self.show_version_tree()
        return

    def build_all_tasks(self):
        # check if selected in tree
        if not self.task_tree.currentItem():
            self.add_log_msg('<font color=\"#FF9900\">' + '[Warning] No item selected on task tree' + '</font>')
            return
        # check selected a block
        if not (self.task_tree.currentItem().pointer.block_name == str(self.task_tree.currentItem().pointer)):
            self.add_log_msg('<font color=\"#FF9900\">' + '[Warning] The selected item on task tree: %s is not a block'%self.task_tree.currentItem().pointer + '</font>')
            return
        else:
            # read block para first
            current_block = self.task_tree.currentItem().pointer
            current_block.read_block_para()
            # build all tasks
            for task_name in current_block.block_para['task_dict'].keys():
                current_block.initial_task(task_name)
                self.add_log_msg('<font color=\"#000000\">' + '[Info] Building task env for task: %s for block: %s'%(task_name, current_block.block_name) + '</font>')
            self.task_tree.clear()
            self.show_version_tree()
        return

    def check_selected_tree_item(self):
        if self.task_tree.currentItem():
            self.add_log_msg('<font color=\"#000000\">' + '[Info] Checking validness for: %s'%(self.task_tree.currentItem().pointer) + '</font>')
            self.task_tree.currentItem().pointer.check_validness()
            self.add_log_msg('<font color=\"#000000\">' + '[Info] Checking result for: %s'%(self.task_tree.currentItem().pointer) + '</font>')
            self.task_tree.currentItem().pointer.check_result()
            self.show_selected_tree_item(self.task_tree.currentItem())
        else:
            self.add_log_msg('<font color=\"#FF9900\">' + '[Warning] No item selected on task tree' + '</font>')
        return

    def run_selected_tree_item(self, item, column = 0):
        if item.pointer.task_name:
            line = 'dummyline'
            lines = ''
            f = open('%s/run_%s'%(item.pointer.path, item.pointer.task_name), 'r')
            while line:
                line = f.readline()[:-1]
                lines = lines + line + ';'
            new_process = subprocess.Popen('xterm -e "cd %s; %s"'%(item.pointer.path, lines), shell=True)
            #print('xterm -e "cd %s; %s"'%(item.pointer.path, lines))
            self.add_log_msg('<font color=\"#000000\">' + '[Info] Running task in a pop up shell: %s of block %s'%(item.pointer, item.pointer.block_name) + '</font>')
        else:
            self.add_log_msg('<font color=\"#FF9900\">' + '[Warning] Cannot run task: %s is not a task'%item.pointer + '</font>')
        return

    def show_selected_tree_item(self, item, column = 0):
        ## show path and files in UI
        # show path
        self.show_file_list_item(item.pointer.path)
        ## show selected item on status box
        # clean old showed data
        self.readiness_list.clear()
        self.result_check_list.clear()
        # show validness list
        for validness_list in item.pointer.show_validness():
            new_item = QListWidgetItem(self.readiness_list)
            new_item.setIcon(QIcon('%s.png'%validness_list[0]))
            new_item.setText(validness_list[1])
        # show result check list
        for result_check_list in item.pointer.show_result():
            new_item = QListWidgetItem(self.result_check_list)
            new_item.setIcon(QIcon('%s.png'%result_check_list[0]))
            new_item.setText(result_check_list[1])
        return
