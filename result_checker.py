import os
import re

def file_check(task):
    # check result file existance
    file_name_list = []
    pass_flag = 'ok'
    for result_file_name in task.block_pointer.block_para['task_result_file_dict'][task.task_name]:
        # get full name
        file_full_name = '%s/%s'%(task.path, result_file_name)
        file_full_name = file_full_name.replace('BLOCK_NAME', task.block_name)
        file_name_list.append(file_full_name)
        # check existance
        if not os.path.exists(file_full_name):
            #print(file_full_name)
            pass_flag = 'failed'
    # file list as detailed data
    return [pass_flag, 'Task %s result file existance check'%task.task_name, 'text_list', file_name_list]

def fatal_pre_drc_free_check(task):
    # fatal DRC like D1 D2 D3
    detail_list = []
    drc_report_file = '%s/result/%s_pre_drc.rpt'%(task.path, task.block_name)
    # check if DRC report exist
    if not os.path.exists(drc_report_file):
        return ['failed', 'Fatal pre-scan DRC check', 'text', 'DRC report file not found: %s'%drc_report_file]
    else:
        # file exist
        fi = open(drc_report_file, 'r')
        lines = fi.readlines()
        pass_flag = 'ok'
        for line in lines:
            if 'Uncontrollable clock input of flip-flop violations (D1)' in line:
                pass_flag = 'failed'
                continue
            elif 'DFF set/reset line not controlled violations (D2)' in line:
                pass_flag = 'failed'
                continue
            elif 'DFF set/reset line not controlled violations (D3)' in line:
                pass_flag = 'failed'
                continue
        fi.close()
        return [pass_flag, 'Fatal pre-scan DRC check', 'text_list', detail_list]

# scan rule result file name define
#         | task name                       | rule name list |
task_result_check_dict = {
          'edt_generation'                  : [file_check],
          'insert_dft'                      : [file_check],
          'atpg_drc_check'                  : [file_check],
          'pattern_generation'              : [file_check],
          'chain_simulation'                : [file_check],
          'parallel_simulation'             : [file_check],
          }

