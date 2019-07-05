block_para = { # block level para start
# project scan para define
#                          | task name                | required task name list                     | result rule name list |
'task_dict'              : {
                           'insert_dft'               : [[],                                        []],
                           'atpg_drc_check'           : [['insert_dft'],                            []],
                           'pattern_generation'       : [['atpg_drc_check'],                        []],
                           'chain_simulation'         : [['atpg_drc_check'],                        []],
                           'parallel_simulation'      : [['pattern_generation'],                    []],
                           },


# scan rule result file name define
#                          | rule name                       | file name list |
'task_result_file_dict'  : {
                           'insert_dft'                      : ['./result/BLOCK_NAME_scan.v', './result/BLOCK_NAME_scan.ddc', './result/BLOCK_NAME.spf'],
                           'atpg_drc_check'                  : ['./result/BLOCK_NAME.flat.gz', './result/BLOCK_NAME_chain.v.gz'],
                           'pattern_generation'              : ['./result/BLOCK_NAME_parallel.v.gz'],
                           'chain_simulation'                : ['./log/elab.log', './log/run.log'],
                           'parallel_simulation'             : ['./log/elab.log', './log/run.log'],
                           },

# scan rule result file name define
#                                     | rule name                       | file name list |
'task_env_file_replace_rule_dict'   : {
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
'port_creation' : {},
'regular_scan_chain_cnt' : '8',
'edt_name' : {},
'block_scan_external_clock_signal' : {'phy_top_u/xiaoxue_cha_u/cha_clk_path/i6/clk_ca_t_o': '', 'phy_top_u/xiaoxue_cha_u/cha_clk_path/i6/clk_dp_1g_o': ''},
'block_scan_external_reset_signal' : {'dfi_phy_reset_n_b': '', 'dfi_phy_reset_n_a': ''},
'block_scan_external_mode_signal'  : {'dfi_calvl_en_b': '1', 'dfi_calvl_en_a': '1'},
'block_scan_internal_clock_signal' : {},
'block_scan_internal_reset_signal' : {},
'block_scan_internal_mode_signal'  : {'phy_top_u/on_pwr': '1', 'phy_top_u/on_pwr phy_top_u/xiaoxue_cha_u/on_pwr': '1', 'phy_top_u/xiaoxue_common/on_pwr': '1', 'phy_top_u/xiaoxue_chb_u/on_pwr': '1', 'phy_top_u/xiaoxue_cha_u/i20/on_pwr': '1', 'phy_top_u/xiaoxue_cha_u/i20/lp/on_pwr': '1', 'phy_top_u/xiaoxue_common/init/on_pwr': '1', 'phy_top_u/xiaoxue_chb_u/ca_slice_b/on_pwr': '1', 'phy_top_u/xiaoxue_chb_u/ca_slice_b/lp/on_pwr': '1'},
'block_scan_scanen_signal'         : {'scan_en': '1'},
} # block para data end
