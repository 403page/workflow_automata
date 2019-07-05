block_para = { # block level para start
# project scan para define
#                          | task name                | required task name list                     | result rule name list |
'task_dict'              : {
                           'edt_generation'           : [[],                                        []],
                           'insert_dft'               : [[],                                        []],
                           'atpg_drc_check'           : [['insert_dft'],                            []],
                           'pattern_generation'       : [['atpg_drc_check'],                        []],
                           'chain_simulation'         : [['atpg_drc_check'],                        []],
                           'parallel_simulation'      : [['pattern_generation'],                    []],
                           },


# scan rule result file name define
#                          | rule name                       | file name list |
'task_result_file_dict'  : {
                           'edt_generation'                  : ['./result/edt.v', './log/run.log'],
                           'insert_dft'                      : ['./result/BLOCK_NAME_scan.v', './result/BLOCK_NAME_scan.ddc', './result/BLOCK_NAME.spf'],
                           'atpg_drc_check'                  : ['./result/BLOCK_NAME.flat.gz', './result/BLOCK_NAME_chain.v.gz'],
                           'pattern_generation'              : ['./result/BLOCK_NAME_parallel.v.gz'],
                           'chain_simulation'                : ['./log/elab.log', './log/run.log'],
                           'parallel_simulation'             : ['./log/elab.log', './log/run.log'],
                           },

# scan rule result file name define
#                                     | rule name                       | file name list |
'task_env_file_replace_rule_dict'   : {
                                      'edt_generation'                  : ['_run_edt_gen', '_edt_gen.dofile'],
                                      'insert_dft'                      : ['_run_insertion', '_insert_dft.tcl'],
                                      'atpg_drc_check'                  : ['_run_post_drc', '_atpg_drc.do', '_atpg.procedure', '_clock_def.do', '_occ_def.do'],
                                      'pattern_generation'              : ['_run_atpg', '_pattern_gen.do'],
                                      'chain_simulation'                : ['_run_chain_sim', '_chain_sim.do'],
                                      'parallel_simulation'             : ['_run_parallel_sim', '_parallel_sim.do'],
                                      },

'sub_blocks_woedt' : {},
'sub_blocks_withedt' : [],
'sub_blocks' : [],
'non_scan_instance' : [],
'regular_scan_chain_cnt' : '20',
'edt_name' : {'main_edt': ['main_edt_top', '1', '20']},
'block_scan_external_clock_signal' : {'clk': ''},
'block_scan_external_reset_signal' : {'rstn': ''},
'block_scan_external_mode_signal'  : {},
'block_scan_internal_clock_signal' : {},
'block_scan_internal_reset_signal' : {},
'block_scan_internal_mode_signal'  : {},
'block_scan_scanen_signal'         : {},
} # block para data end
