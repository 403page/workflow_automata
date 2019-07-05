set search_path [ list /home/wanghua/debug_proj/common_file/lib/syn ]

set link_library [ list sc9tap_logic013_base_hvt_ff_typical_min_1p32v_0c.db \
                        sc9tap_logic013_base_lvt_ff_typical_min_1p32v_0c.db \
                        sc9tap_logic013_base_rvt_ff_typical_min_1p32v_0c.db ]

set target_library [ list sc9tap_logic013_base_hvt_ff_typical_min_1p32v_0c.db ]


_read_verilog_mark
_set_top_mark
_current_design_mark
# keep existing design name
set_dft_insertion_configuration -preserve_design_name true

set_scan_configuration -insert_terminal_lockup true
#set_dft_configuration -synthesis_optimization none

set_dft_configuration -fix_bidi disable
set_dft_configuration -fix_bus  disable

set_scan_configuration -clock_mixing mix_clocks
set_scan_configuration -power_domain_mixing true -voltage_mixing true -reuse_mv_cells true
set_scan_configuration -add_test_retiming_flops begin_and_end
set_scan_configuration -max_length 200

set_dft_drc_configuration -internal_pin enable
set_dft_drc_rules -ignore {TEST-504 TEST-505}

_scan_clk_mark
_scan_rst_mark

create_test_protocol
dft_drc > ./result/${TOP}_pre_drc.rpt
preview_dft > ./result/${TOP}_preview.rpt
