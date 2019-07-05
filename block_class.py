# block class define
# import task class
from task_class import *
# load pickle for save/load
import pickle
import importlib

# block class define
class block:
    def __init__(self, name = ''):
        # block basic para
        self.block_name           = name
        # father&child in block structure
        self.sub_block_dict       = {}
        self.father_block_pointer = None
        self.version_pointer      = None
        # loaded from block_conf of this block
        self.block_para           = None
        # show status
        self.validness_list       = [['task_arrow', 'Please check validness for this block']]
        self.result_list          = [['task_arrow', 'Please check result for this block']]
        self.path                 = ''
        self.task_name            = ''
        self.task_dict            = {}

    def add_sub_block(self, sub_block_name, sub_block):
        # add a sub block to this block
        self.sub_block_dict[sub_block_name] = sub_block

    def read_block_para(self):
        # load block para from block conf py file
        self.block_para = importlib.import_module('block_conf_%s'%self.block_name).block_para
        return

    def initial_task(self, task_name, task_fake_name = ''):
        # build one single task
        current_task = task(task_name)
        current_task.block_name      = self.block_name
        current_task.task_fake_name  = task_fake_name
        current_task.block_pointer   = self
        current_task.version_pointer = self.version_pointer
        # path of fake task name
        if task_fake_name:
            current_task.path        = self.path + '/%s'%task_fake_name
        else:
            current_task.path        = self.path + '/%s'%task_name
        # build task env
        current_task.build_env()
        # add task file to current block
        if task_fake_name:
            self.task_dict[task_fake_name] = current_task
        else:
            self.task_dict[task_name] = current_task
        return current_task

    def check_validness(self):
        # all checks in sub tasks
        result_list = []
        for task in self.task_dict.values():
            # a task headline of this block
            result_list.append(['task_arrow', 'Task %s validness'%task.task_name])
            for result in task.check_validness():
                # a result list
                if result:
                    # add to result list if not empty
                    result_list.append(result)
        self.validness_list = result_list
        return self.validness_list

    def check_result(self):
        # all checks in sub tasks
        result_list = []
        for task in self.task_dict.values():
            # a task headline of this block
            result_list.append(['task_arrow', 'Task %s result'%task.task_name])
            for result in task.check_result():
                # a result list
                if result:
                    # add to result list if not empty
                    result_list.append(result)
        self.result_list = result_list
        return self.result_list

    def show_validness(self):
        if not self.validness_list:
            self.check_validness()
        return self.validness_list

    def show_result(self):
        if not self.result_list:
            self.check_result
        return self.result_list

    def __repr__(self):
        # print block name when used as para
        return self.block_name
