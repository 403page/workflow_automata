# task class define
# load std libs
import os
# load pickle for save/load
import pickle
# load rules
import env_builder
import validness_checker
import result_checker

# task class define
class task:
    def __init__(self, name = ''):
        # task initial basic paras
        self.task_name               = name
        self.task_fake_name          = ''
        self.block_name              = ''
        self.block_pointer           = None
        self.version_pointer         = None

        # required task list
        #self.required_task_name_list = []
        # result rule list
        #self.result_rule_list        = []
        # task env to I/O
        #self.task_env_file_list      = None
        # task status
        self.validness_list          = []
        self.result_list             = []
        self.path                    = ''

    def show_validness(self):
        if not self.validness_list:
            self.check_validness()
        return self.validness_list

    def show_result(self):
        if not self.result_list:
            self.check_result()
        return self.result_list

    def check_validness(self):
        # check rules
        result_list = []
        # check all rules
        for rule in validness_checker.task_validness_check_dict[self.task_name]:
            result_list.append(rule(self))
        # save result
        self.validness_list = result_list
        return result_list

    def check_result(self):
        result_list = []
        # all rules
        for rule in result_checker.task_result_check_dict[self.task_name]:
            result_list.append(rule(self))
        # save result
        self.result_list = result_list
        return result_list

    def build_env(self):
        # build path dir
        if not os.path.exists('%s'%self.path):
            os.system('mkdir -p %s'%self.path)
            os.system('mkdir -p %s/log'%self.path)
            os.system('mkdir -p %s/result'%self.path)
            os.system('mkdir -p %s/report'%self.path)
        # find build env func from dict
        env_builder.task_env_rule_dict[self.task_name](self)
        return

    def __repr__(self):
        # print task status when used as para
        return self.task_name
