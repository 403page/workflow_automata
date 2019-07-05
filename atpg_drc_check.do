//set_context dft -no_rtl
//set_context pattern -scan
set_edt_options off

//read_cell_library
read_cell_library /home/gd6b/fe/wanghua/view1/scan/common_file/lib/mgc/libcomp.atpglib
//read_verilog
_read_verilog_mark

_block_name_mark

//dofile design_setup.do
_design_setup_mark

add black box -auto

//dofile internal_clock_define.do

set system mode atpg
//save flatten model ./result/
_save_flatten_mark
_save_pattern_mark
