#set SE_pins [get_attri [get_pins -h */SE] full_name -filter "full_name ~= *clk_gate*"]
set cg_cells [get_attri [get_cells -h * -filter "ref_name =~ *ICG*"] full_name]

foreach cg_cell $cg_cells {
    disconnect_net [get_net -of $cg_cell/SE] $cg_cell/SE
    connect_pin -from scan_en -to $cg_cell/SE -port scan_clock_path
}



create_cell main_edt_top edt_main_edt
#create_port edt_clock -direction in
connect_pin -from scan_edt_clk -to main_edt_top/edt_clock -port for_edt_clk
connect_pin -from scan_update -to main_edt_top/edt_update -port for_edt_update
connect_pin -from scan_bypass -to main_edt_top/edt_bypass -port for_edt_bypass
#connect_pin -from scan_mode 
disconnect_net [get_net -of scan_out_ch1] scan_out_ch1
disconnect_net [get_net -of scan_out_ch2] scan_out_ch2
disconnect_net [get_net -of scan_out_ch3] scan_out_ch3
connect_pin -from scan_in_ch1 -to main_edt_top/edt_channels_in[0] -port for_edt_channel_in_0
connect_pin -from main_edt_top/edt_channels_out[0] -to scan_out_ch1 -port for_edt_channel_out_0
connect_pin -from scan_in_ch2 -to main_edt_top/edt_channels_in[1] -port for_edt_channel_in_1
connect_pin -from main_edt_top/edt_channels_out[1] -to scan_out_ch2 -port for_edt_channel_out_1
connect_pin -from scan_in_ch3 -to main_edt_top/edt_channels_in[2] -port for_edt_channel_in_2
connect_pin -from main_edt_top/edt_channels_out[2] -to scan_out_ch3 -port for_edt_channel_out_2


create_cell scan_mode_inv sc10p5mcpp84_14lppxl_base_rvt_c14_ssa_sigcmax_max_0p72v_125c/INVP_X0P4N_A10P5PP84TR_C14
connect_pin -from scan_mode -to scan_mode_inv/A -port for_scan_mode_inv
#connect_pin -from scan_mode_inv/Y -to main_edt_top/edt_low_power_shift_en -port for_edt_low_pwr
#connect_pin -from scan_out_ch4
