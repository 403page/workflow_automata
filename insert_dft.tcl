# read synopsys design lib
source /home/gd6b/fe/wanghua/view1/scan/common_file/ref_script_file/read_lib.tcl

# read design netlist
_read_verilog_mark

# read sub block test model, with scan chain, without edt
_read_ddc_mark
_use_ddc_mark

# set current design
_set_top_mark
_current_design_mark


# set scan common setting
source /home/gd6b/fe/wanghua/view1/scan/common_file/ref_script_file/scan_common_setting.tcl

# scan exclude list
set exclude_list []
_scan_exclude_mark

if ${exclude_list} {
    set_scan_configuration -exlude_elements ${exclude_list}
    set_scan_element false ${exclude_list}
}
# set dft signals
_port_creation_mark
_pre_signal_script_mark
_scan_clk_mark
_scan_rst_mark
_scan_en_mark
_scan_ex_constraint_mark
_scan_in_constraint_mark
_internal_rst_mark

# occ on internal clocks
_internal_clk_mark

# scan chain connection
_disconnect_edt_mark
_define_edt_connection_mark
_current_block_chain_mark
_sub_block_chain_mark

# begin drc check
create_test_protocol
dft_drc > ./result/${TOP}_pre_drc.rpt
preview_dft > ./result/${TOP}_preview.rpt
insert_dft

# write result data
_scan_netlist_mark
_scan_spf_mark
_scan_ddc_mark
