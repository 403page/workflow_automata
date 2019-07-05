import os
import glob

def dc_lib_check(task):
    # dc lib check for dc, pt and fm
    lib_list = []
    dc_lib_path = '%s/lib/syn'%(task.version_pointer.version_para['common_path'])
    if not os.path.exists(dc_lib_path):
        return ['disable', 'Syn lib check for DC, PT and FM', 'text', 'Lib folder not found']
    else:
        lib_list = glob.glob('%s/*.db'%dc_lib_path)
        if not lib_list:
            return ['disable', 'Syn lib check for DC, PT and FM', 'text', 'No db lib found in path: %s'%dc_lib_path]
        else:
            return ['ok', 'Syn lib check for DC, PT and FM', 'text_list', lib_list]

def tk_lib_check(task):
    # tk lib check for testkompress and lv
    lib_list = []
    tk_lib_path = '%s/lib/mgc'%(task.version_pointer.version_para['common_path'])
    if not os.path.exists(tk_lib_path):
        return ['disable', 'Mentor lib check for Testkompress and LogicVision', 'text', 'Lib folder not found']
    else:
        lib_list = glob.glob('%s/*.atpglib'%tk_lib_path)
        if not lib_list:
            return ['disable', 'Mentor lib check for Testkompress and LogicVision', 'text', 'No Mentor lib found in path: %s'%tk_lib_path]
        else:
            return ['ok', 'Mentor lib check for Testkompress and LogicVision', 'text_list', lib_list]

def vcs_lib_check(task):
    # tk lib check for testkompress and lv
    lib_list = []
    vcs_lib_path = '%s/lib/vlog'%(task.version_pointer.version_para['common_path'])
    if not os.path.exists(vcs_lib_path):
        return ['disable', 'Verilog lib check for VCS and Tetramax', 'text', 'Lib folder not found']
    else:
        lib_list = glob.glob('%s/*.v'%vcs_lib_path)
        if not lib_list:
            return ['disable', 'Verilog lib check for VCS and Tetramax', 'text', 'No verilog lib found in path: %s'%vcs_lib_path]
        else:
            return ['ok', 'Verilog lib check for VCS and Tetramax', 'text_list', lib_list]


def pre_scan_netlist_check(task):
    # tk lib check for testkompress and lv
    netlist_list = []
    pre_scan_netlist_path = '%s/netlist'%(task.version_pointer.version_para['common_path'])
    if not os.path.exists(pre_scan_netlist_path):
        return ['disable', 'Pre scan verilog netlist check', 'text', 'Netlist folder not found']
    else:
        netlist_list = glob.glob('%s/%s.v'%(pre_scan_netlist_path, task.block_name))
        if not netlist_list:
            return ['disable', 'Pre scan verilog netlist check', 'text', 'Verilog netlist not found in path: %s/%s.v'%(pre_scan_netlist_path, task.block_name)]
        else:
            return ['ok', 'Pre scan verilog netlist check', 'text', '%s/%s.v'%(pre_scan_netlist_path, task.block_name)]

def sub_block_result_check(task):
    # if no sub block
    if not task.block_pointer.block_para['sub_blocks']:
        return ['ok', 'No sub_blocks need scan']
    # check sub block scan result
    fail_blocks = ''
    fail_flag   = 0
    for block in task.block_pointer.block_para['sub_blocks']:
        # if not build
        if not task.block_pointer.sub_block_dict[block].task_dict:
            return ['disable', 'Sub_blocks need initial']
        # if built
        task.block_pointer.sub_block_dict[block].task_dict['insert_dft'].check_result()
        if not task.block_pointer.sub_block_dict[block].task_dict['insert_dft'].show_result()[0][0] == 'ok':
            fail_flag = 1
            fail_blocks += '%s '%block
    if not fail_flag:
        return ['ok', 'All sub_blocks scan inserting done']
    else:
        return ['disable', '%sblocks scan not done'%fail_blocks]

def pre_drc_check_result_check(task):
    task.block_pointer.task_dict['pre_drc_check'].check_result()
    return task.block_pointer.task_dict['pre_drc_check'].show_result()[0]

def insert_dft_result_check(task):
    task.block_pointer.task_dict['insert_dft'].check_result()
    return task.block_pointer.task_dict['insert_dft'].show_result()[0]

def atpg_drc_result_check(task):
    task.block_pointer.task_dict['atpg_drc_check'].check_result()
    return task.block_pointer.task_dict['atpg_drc_check'].show_result()[0]

def atpg_result_check(task):
    task.block_pointer.task_dict['pattern_generation'].check_result()
    return task.block_pointer.task_dict['pattern_generation'].show_result()[0]

# scan rule result file name define
#         | rule name                       | file name list |
task_validness_check_dict = {
          'edt_generation'                  : [],
          'insert_dft'                      : [dc_lib_check, pre_scan_netlist_check, sub_block_result_check],
          'atpg_drc_check'                  : [tk_lib_check, insert_dft_result_check],
          'pattern_generation'              : [tk_lib_check, atpg_drc_result_check],
          'chain_simulation'                : [vcs_lib_check, atpg_drc_result_check],
          'parallel_simulation'             : [vcs_lib_check, atpg_result_check],
          }

