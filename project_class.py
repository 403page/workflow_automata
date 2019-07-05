# project&version class define
# import std libs
#import os
#import re
#import collections

# load task class
from task_class import *
# load block class
from block_class import *

# only version initial function can import project_conf
import importlib

# load pickle for save/load
import pickle

class project:
    def __init__(self, name = ''):
        # common project
        self.project_name     = name
        self.version_dict     = {}

    def __repr__(self):
        return self.project_name

class version:
    def __init__(self, name = ''):
        # common version para
        self.version_name         = name
        # fake block name same as version name
        self.block_name           = ''
        # fake task name same as version name
        self.task_name            = ''
        # fake version pointer
        self.version_pointer      = self

        # version para to load project_conf
        self.version_para         = None
        #self.block_para_dict      = {}

        # use this list to update task
        self.all_block_dict       = {}

        # fake task dict pretend to be a block
        self.sub_block_dict       = {}
        self.task_dict            = {}

        # status list
        self.validness_list       = [['task_arrow', 'Please check validness for this version']]
        self.result_list          = [['task_arrow', 'Please check result for this version']]
        self.path                 = ''

    def read_version_para(self, version_name):
        current_version = importlib.import_module('project_conf_%s'%version_name)
        # get para from project_conf
        self.version_para         = current_version.version_data
        self.path                 = self.version_para['version_path']
        #for block_name in self.version_para['block_structure_dict'].keys():
        #    self.block_para_dict[block_name] = importlib.import_module('block_conf_%s'%block_name).block_para
        #return

    def initial_project_blocks(self):
        # main func to add data to version
        # initial all top blocks
        for current_top_name in self.version_para['top_block_name_list']:
            self.sub_block_dict[current_top_name] = self.initial_block(current_top_name, None)
        return

    def initial_block(self, block_name, father_block):
        # initial a single block and sub blocks
        current_block = block(block_name)
        current_block.father_block_pointer = father_block
        current_block.version_pointer      = self.version_pointer
        current_block.path                 = self.path + '/work/%s'%block_name
        os.system('mkdir -p %s'%current_block.path)

        for sub_block_name in self.version_para['block_structure_dict'][block_name]:
            # search for sub_blocks
            current_block.add_sub_block(sub_block_name, self.initial_block(sub_block_name, current_block))

        # add task list to this block
        #current_block.initial_task_list(list(self.version_para['task_dict'].keys()))
        self.all_block_dict[block_name] = current_block

        # return to father block
        return current_block

    def __repr__(self):
        # print project version name when used as para
        return self.version_name

    def show_validness(self):
        return self.validness_list

    def show_result(self):
        return self.result_list

    def check_validness(self):
        # show all block status
        result_list = []
        for block in self.all_block_dict.values():
            # a single block
            result_list.append(['task_arrow', 'Block %s validness'%block.block_name])
            for result in block.check_validness():
                # a result list
                if result:
                    # add to result list if not empty
                    result_list.append(result)
        self.validness_list = result_list
        return self.validness_list

    def check_result(self):
        # show all block status
        result_list = []
        for block in self.all_block_dict.values():
            # a single block
            result_list.append(['task_arrow', 'Block %s result'%block.block_name])
            for result in block.check_result():
                # a result list
                if result:
                    # add to result list if not empty
                    result_list.append(result)
        self.result_list = result_list
        return self.result_list

