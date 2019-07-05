import os
import text_file_replacer
#import project_conf

class env_file():
    # env file
    def __init__(self, task, base_name):
        # initial env file
        self.task_pointer     = task
        self.version_pointer  = task.version_pointer
        self.origin_file_name = '%s/%s'%(self.version_pointer.version_para['base_script_path'], base_name)
        self.ori_lines        = []
        self.target_path      = '%s'%(task.path)
        self.target_file_name = '%s/%s'%(task.path, base_name)
        self.target_lines     = []
        # replace rule control
        self.replace_control  = {}
        # file handler
        self.fi               = None
        self.fo               = None

    def read_ori_file(self):
        # read ori file to ori lines
        self.fi        = open(self.origin_file_name, 'r')
        self.ori_lines = self.fi.readlines()
        self.fi.close()

    def add_replace_rule(self, mark = '', lines = []):
        # add rule
        self.replace_control[mark + '\n'] = lines

    def replace_file(self):
       # handle i/o files
       self.read_ori_file()
       self.fo = open(self.target_file_name, 'w')
       # start to check origin lines
       for current_ori_line in self.ori_lines:
           # check if mark
           if current_ori_line in self.replace_control.keys():
               # line need replace
               for line in self.replace_control[current_ori_line]:
                   self.target_lines.append(line)
           else:   
               # line need keep
               self.target_lines.append(current_ori_line)
               # return new lines
       for line in self.target_lines:
           self.fo.write(line)
       self.fo.close()

def pre_drc_check_env_builder(task):
    # func to build task env
    # for scan pre drc check
    run_file = env_file(task, 'run_pre_drc_check')
    run_file.add_replace_rule('_block_name_mark', ['dc_shell -f pre_drc_check.tcl -output_log_file ./log/run.log'])
    run_file.replace_file()

    main_script = env_file(task, 'pre_drc_check.tcl')
    main_script.add_replace_rule('_set_top_mark', ['set TOP %s\n'%task.block_name])
    main_script.add_replace_rule('_current_design_mark', ['current_design %s\n'%task.block_name])
    main_script.add_replace_rule('_read_verilog_mark', ['read_verilog %s/design_data/%s.v\n'%(task.version_pointer.version_para['common_path'], task.block_name)])
    main_script.add_replace_rule('_scan_clk_mark', ['set_dft_signal -view e -type scanclock  -port %s -timing {45 55}\n'%x_clock
                                                    for x_clock in task.block_pointer.block_para['block_scan_external_clock_signal'].keys()])
    main_script.add_replace_rule('_scan_rst_mark', ['set_dft_signal -view e -type reset -port %s -active_state 0\n'%x_reset
                                                    for x_reset in task.block_pointer.block_para['block_scan_external_reset_signal'].keys()])
    main_script.replace_file()
    return


def insert_dft_env_builder(task):
    # for insert scan
    run_file = env_file(task, 'run_insert_dft')
    run_file.add_replace_rule('_run_insert_scan', ['dc_shell -f insert_dft.tcl -output_log_file ./log/run.log'])
    run_file.replace_file()

    main_script = env_file(task, 'insert_dft.tcl')
    main_script.add_replace_rule('_set_top_mark', ['set TOP %s\n'%task.block_name])
    main_script.add_replace_rule('_current_design_mark', ['current_design %s\n'%task.block_name])
    main_script.add_replace_rule('_read_verilog_mark', ['read_verilog %s/design_data/%s.v\n'%(task.version_pointer.version_para['common_path'], task.block_name)])
    main_script.add_replace_rule('_read_ddc_mark', ['read_test_model -format ddc ../../%s/insert_dft/result/%s_scan.ddc\n'%(block, block)
                                                    for block in task.block_pointer.block_para['sub_blocks_woedt']])
    main_script.add_replace_rule('_port_creation_mark', ['create_port %s -direction %s\n'%(port, task.block_pointer.block_para['port_creation'][port])
                                                         for port in task.block_pointer.block_para['port_creation'].keys()])
    main_script.add_replace_rule('_use_ddc_mark',  ['use_test_model -true %s\n'%block
                                                    for block in task.block_pointer.block_para['sub_blocks_woedt']])
    main_script.add_replace_rule('_scan_clk_mark', ['set_dft_signal -view e -type scanclock  -port %s -timing {45 55}\n'%x_clock
                                                    for x_clock in task.block_pointer.block_para['block_scan_external_clock_signal'].keys()])
    main_script.add_replace_rule('_scan_rst_mark', ['set_dft_signal -view e -type reset -port %s -active_state 0\n'%x_reset
                                                    for x_reset in task.block_pointer.block_para['block_scan_external_reset_signal'].keys()])
    main_script.add_replace_rule('_internal_rst_mark', ['set_dft_signal -view e -type reset -hookup_pin %s -active_state 0\n'%x_reset
                                                    for x_reset in task.block_pointer.block_para['block_scan_internal_reset_signal'].keys()])
    main_script.add_replace_rule('_scan_en_mark', ['set_dft_signal -view e -type scanenable -port %s -active 1\nset_dft_signal -view spec -type scanenable -port %s -active 1\n'%(x_se, x_se)
                                                        for x_se in task.block_pointer.block_para['block_scan_scanen_signal'].keys()])
    main_script.add_replace_rule('_scan_exclude_mark', ['set exclude_list [list $exclude_list [get_cells %s]]'%(x_inst)
                                                        for x_inst in task.block_pointer.block_para['non_scan_instance']]) #.append('set_scan_configuration -exlude_elements ${exclude_list}\nset_scan_element false ${exclude}\n'))
    main_script.add_replace_rule('_disconnect_edt_mark', ['for {set i 0} {$i < %s} {incr i} {\n    disconnect_net [get_nets -of [get_pins %s/test_si[$i]] ] [get_pins -of %s/test_si[$i]]\n    disconnect_net [get_nets -of [get_pins %s/test_so[$i]] ] [get_pins -of %s/test_so[$i]]\n}\n'%(task.block_pointer.block_para['regular_scan_chain_cnt'], task.block_pointer.block_para['edt_name'][x_edt][0], task.block_pointer.block_para['edt_name'][x_edt][0], task.block_pointer.block_para['edt_name'][x_edt][0], task.block_pointer.block_para['edt_name'][x_edt][0]) for x_edt in task.block_pointer.block_para['edt_name'].keys()])
    main_script.add_replace_rule('_define_edt_connection_mark', ['for {set i 0} {$i < %s} {incr i} {\n    set_dft_signal -view spec -type scandatain -hookup_pin %s/test_si[$i]\n    set_dft_signal -view spec -type scandataout -hookup_pin %s/test_so[$i]\n}\n'%(task.block_pointer.block_para['regular_scan_chain_cnt'], task.block_pointer.block_para['edt_name'][x_edt][0], task.block_pointer.block_para['edt_name'][x_edt][0]) for x_edt in task.block_pointer.block_para['edt_name'].keys()])

    if task.block_pointer.block_para['edt_name']:
        main_script.add_replace_rule('_current_block_chain_mark', ['for {set i 0; set j 0} {$i < %s} {incr i; incr j} {\n    set_scan_path chain_$j -scan_data_in %s/test_si[$j] -scan_data_out %s/test_so[$j]\n}\n'%(task.block_pointer.block_para['regular_scan_chain_cnt'], task.block_pointer.block_para['edt_name'][x_edt][0], task.block_pointer.block_para['edt_name'][x_edt][0]) for x_edt in task.block_pointer.block_para['edt_name'].keys()])
        main_script.add_replace_rule('_sub_block_chain_mark', ['for {set i 0} {$i < %s} {incr i; incr j} {\n    set_scan_path chain_$j -scan_data_in %s/test_si[$j] -scan_data_out %s/test_so[$j] \\\n    -include %s/chain_$i -complete ture\n}\n'])
    else:
        main_script.add_replace_rule('_current_block_chain_mark', ['for {set i 0; set j 0} {$i < %s} {incr i; incr j} {\n    create_port test_si[$j] -direction in\n    create_port test_so[$j] -direction out\n    set_dft_signal -view spec -type scandatain -port test_si[$j]\n    set_dft_signal -view spec -type scandataout -port test_so[$j]\n    set_scan_path chain_$j -scan_data_in test_si[$j] -scan_data_out test_so[$j]\n}\n'%task.block_pointer.block_para['regular_scan_chain_cnt']])
        main_script.add_replace_rule('_sub_block_chain_mark', [''])

    main_script.add_replace_rule('_scan_ex_constraint_mark', ['set_dft_signal -view e -type Constant -active %s -port %s\n'%(task.block_pointer.block_para['block_scan_external_mode_signal'][x_constraint], x_constraint)
                                                        for x_constraint in task.block_pointer.block_para['block_scan_external_mode_signal'].keys()])
    main_script.add_replace_rule('_scan_in_constraint_mark', ['set_dft_signal -view e -type Constant -active %s -hookup_pin %s\n'%(task.block_pointer.block_para['block_scan_internal_mode_signal'][x_constraint], x_constraint)
                                                            for x_constraint in task.block_pointer.block_para['block_scan_internal_mode_signal'].keys()])
    main_script.add_replace_rule('_pre_signal_script_mark', ['source ../../../../common_file/common_script/%s_pre_signal_script.tcl\n\n'%task.block_pointer.block_name])


    # for occ
    internal_clk_lines = []
    for occ_name in task.block_pointer.block_para['block_scan_internal_clock_signal'].keys():
        internal_clk_lines += '\nset_dft_configuration -clock_controller enable\n'
        internal_clk_lines += '\nset_dft_signal -view e -type Oscillator -port %s\n'%task.block_pointer.block_para['block_scan_internal_clock_signal'][occ_name][0]
        internal_clk_lines += 'set_dft_signal -view e -type Oscillator -hookup_pin %s\n'%task.block_pointer.block_para['block_scan_internal_clock_signal'][occ_name][1]
        internal_clk_lines += '\nset_dft_clock_controller -cell_name %s \\\n'%occ_name
        internal_clk_lines += '    -design_name snps_clk_mux -cycles_per_clock 8 -chain_count 1 \\\n'
        internal_clk_lines += '    -pllclocks {%s} -ateclocks {%s}\n'%(task.block_pointer.block_para['block_scan_internal_clock_signal'][occ_name][1], task.block_pointer.block_para['block_scan_internal_clock_signal'][occ_name][0])
    main_script.add_replace_rule('_internal_clk_mark', internal_clk_lines)

    main_script.add_replace_rule('_scan_netlist_mark', ['write -f verilog -h -o ./result/%s_scan.v\n'%task.block_name])
    main_script.add_replace_rule('_scan_spf_mark', ['write_test_protocol -o ./result/%s.spf\n'%task.block_name])
    main_script.add_replace_rule('_scan_ddc_mark', ['write_test_model -format ddc -o ./result/%s_scan.ddc\n'%task.block_name])
    main_script.replace_file()
    return

def atpg_drc_check_env_builder(task):
    # for atpg drc
    run_file = env_file(task, 'run_atpg_drc_check')
    run_file.add_replace_rule('_stil2mgc_mark', ['cp ../insert_dft/result/%s.spf .\n'%task.block_name, 'stil2mgc %s.spf\n'%task.block_name])
    run_file.add_replace_rule('_block_name_mark', ['testkompress -dofile atpg_drc_check.do -logfile ./log/run.log -replace\n'])
    run_file.replace_file()

    main_script = env_file(task, 'atpg_drc_check.do')
    main_script.add_replace_rule('_read_verilog_mark', ['read_verilog ../insert_dft/result/%s_scan.v\n'%task.block_name])
    main_script.add_replace_rule('_block_name_mark', ['set currend_design %s\n'%task.block_name])
    main_script.add_replace_rule('_design_setup_mark', ['dofile ./%s.spf.do\n'%task.block_name])
    main_script.add_replace_rule('_save_flatten_mark', ['write_flat_model ./result/%s.flat.gz -replace\n'%task.block_name])
    main_script.add_replace_rule('_save_pattern_mark', ['write_patterns ./result/%s_chain.v.gz -verilog -chain_test -serial -replace\n'%task.block_name])
    main_script.replace_file()
    return

def pattern_generation_env_builder(task):
    # for atpg
    run_file = env_file(task, 'run_pattern_generation')
    run_file.add_replace_rule('_block_name_mark', ['testkompress -dofile pattern_generation.do -logfile ./log/run.log -replace\n'])
    run_file.replace_file()

    main_script = env_file(task, 'pattern_generation.do')
    main_script.add_replace_rule('_block_name_mark', ['set currend_design %s\n'%task.block_name])
    main_script.add_replace_rule('_read_flat_mark', ['read_flat_model ../atpg_drc_check/result/%s.flat.gz\n'%task.block_name])
    main_script.add_replace_rule('_save_pattern_mark', ['write_patterns ./result/%s_parallel.v.gz -verilog -scan -parallel -replace\n'%task.block_name])
    main_script.replace_file()
    return

def chain_simulation_env_builder(task):
    run_file = env_file(task, 'run_chain_simulation')
    run_file.add_replace_rule('_cp_mark', ['ln -sf ../atpg_drc_check/result/%s_chain.* .\n'%task.block_name])
    run_file.add_replace_rule('_run_mark', ['./run.simv +STARTPAT=0 +ENDPAT=5000 +CHAINTEST=1 +CONFIG=%s_chain.v.cfg -l ./log/run.log\n'%task.block_name])
    run_file.replace_file()

    file_list = env_file(task, 'chain_elab_file_list')
    file_list.add_replace_rule('_netlist_mark', ['../insert_dft/result/%s_scan.v\n'%task.block_name])
    file_list.add_replace_rule('_testbench_mark', ['../atpg_drc_check/result/%s_chain.v.gz\n'%task.block_name])
    file_list.replace_file()
    return

def parallel_simulation_env_builder(task):
    run_file = env_file(task, 'run_parallel_simulation')
    run_file.add_replace_rule('_cp_mark', ['ln -sf ../pattern_generation/result/%s_parallel.* .\n'%task.block_name])
    run_file.add_replace_rule('_run_mark', ['./run.simv +STARTPAT=0 +ENDPAT=5000 -parallel+no_mtvpd +CONFIG=%s_parallel.v.cfg -l ./log/run.log\n'%task.block_name])
    run_file.replace_file()

    file_list = env_file(task, 'parallel_elab_file_list')
    file_list.add_replace_rule('_netlist_mark', ['../insert_dft/result/%s_scan.v\n'%task.block_name])
    file_list.add_replace_rule('_testbench_mark', ['../pattern_generation/result/%s_parallel.v.gz\n'%task.block_name])
    file_list.replace_file()
    return

def edt_generation_env_builder(task):
    run_file = env_file(task, 'run_edt_generation')
    run_file.add_replace_rule('_block_name_mark', ['testkompress -dofile edt_gen.dofile -logfile ./log/run.log -replace\n'])
    run_file.replace_file()

    main_script = env_file(task, 'edt_gen.dofile')
    main_script.add_replace_rule('_read_verilog_mark', ['read_verilog %s/design_data/%s.v\n'%(task.version_pointer.version_para['common_path'], task.block_name)])
    main_script.add_replace_rule('_block_name_mark', ['set_current_design %s\n'%task.block_name, 'set BLOCK %s\n'%task.block_name])
    main_script.add_replace_rule('_edt_channel_mark', ['set edt -input_channels %s -output_channels %s -pipeline off -bypass on\n'%(task.block_pointer.block_para['edt_name']['main_edt'][1], task.block_pointer.block_para['edt_name']['main_edt'][1])])
    main_script.replace_file()
    return

# scan rule result file name define
#         | rule name                       | file name list |
task_env_rule_dict = {
          'edt_generation'                  : edt_generation_env_builder,        #['_run_edt_gen', '_edt_gen.dofile'],
          'insert_dft'                      : insert_dft_env_builder,            #['_run_insertion', '_insert_dft.tcl'],
          'atpg_drc_check'                  : atpg_drc_check_env_builder,        #['_run_post_drc', '_atpg_drc.do', '_atpg.procedure', '_clock_def.do', '_occ_def.do'],
          'pattern_generation'              : pattern_generation_env_builder,    #['_run_atpg', '_pattern_gen.do'],
          'chain_simulation'                : chain_simulation_env_builder,      #['_run_chain_sim', '_chain_sim.do'],
          'parallel_simulation'             : parallel_simulation_env_builder,   #['_run_parallel_sim', '_parallel_sim.do'],
          }

