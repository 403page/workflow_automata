
# temp solution
'block_signal_dict'    : {
                         'arm926_tcm'       : [['CLK'], ['HRESETn']],
                         'a926ejsMMU'       : [['MMUClk'], ['MMUnReset']],
                         'a9ejsRam3r2wSDff' : [['CLK'], []],
                       },


# project scan para define
#                          | task name                | required task name list                     | result rule name list |
'task_dict'            : {
                           'pre_drc_check'            : [[],                                        []],
                           'insert_dft'               : [['pre_drc_check'],                         []],
                           'atpg_drc_check'           : [['insert_dft'],                            []],
                           'pattern_generation'       : [['atpg_drc_check'],                        []],
                           'chain_simulation'         : [['atpg_drc_check'],                        []],
                           'parallel_simulation'      : [['pattern_generation'],                    []],
                       },


# scan rule result file name define
#                                | rule name                       | file name list |
'task_result_file_dict' : {
                                 'pre_drc_check'                   : ['_pre_drc.rpt'],
                                 'insert_dft'                      : ['_scan.v', '.spf'],
                                 'atpg_drc_check'                  : ['_flatten_model.gz', '_chain.v.gz'],
                                 'pattern_generation'              : ['_parallel.v.gz'],
                                 'chain_simulation'                : ['_chain_sim.log'],
                                 'parallel_simulation'             : ['_parallel_sim.log'],
                        },

# scan rule result file name define
#                                     | rule name                       | file name list |
'task_env_file_replace_rule_dict' : {
                                      'pre_drc_check'                   : ['_run_pre_drc', '_scan_drc_check.tcl'],
                                      'insert_dft'                      : ['_run_insertion', '_insert_dft.tcl'],
                                      'atpg_drc_check'                  : ['_run_post_drc', '_atpg_drc.do', '_atpg.procedure', '_clock_def.do', '_occ_def.do'],
                                      'pattern_generation'              : ['_run_atpg', '_pattern_gen.do'],
                                      'chain_simulation'                : ['_run_chain_sim', '_chain_sim.do'],
                                      'parallel_simulation'             : ['_run_parallel_sim', '_parallel_sim.do'],
                                  },
} # project data end
