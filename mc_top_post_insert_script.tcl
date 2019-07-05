set pll_bypass_net [get_net -of pll_bypass]
set pll_reset_net [get_net -of pll_reset]
set test_mode_net [get_net -of test_mode]

disconnect_net $pll_bypass_net pll_bypass
disconnect_net $pll_reset_net pll_reset
disconnect_net $test_mode_net test_mode

connect_net $pll_bypass_net scan_in_ch4
connect_net $pll_reset_net scan_mode_inv/Y

disconnect_net test_mode occ_dfi_clk/test_mode
disconnect_net test_mode occ_tck/test_mode
connect_pin -from scan_mode -to  occ_dfi_clk/test_mode -port for_occ_test_mode
connect_pin -from scan_mode -to  occ_tck/test_mode   -port for_occ_test_mode

disconnect_net [get_nets -of main_edt_top/edt_low_power_shift_en] main_edt_top/edt_low_power_shift_en
connect_pin -from scan_mode -to main_edt_top/edt_low_power_shift_en -port for_edt_low_pwr

remove_port pll_bypass
remove_port pll_reset
remove_port test_mode

for {set i 0} {$i < 8} {incr i} {
    create_cell scan_dummy$i sc10p5mcpp84_14lppxl_base_rvt_c14_ssa_sigcmax_max_0p72v_125c/DFFQ_X1N_A10P5PP84TR_C14
    connect_pin -from main_edt_top/edt_scan_in[$i] -to scan_dummy$i/D -port for_dummy_D_$i
    disconnect_net [get_net -of main_edt_top/edt_scan_out[$i]] main_edt_top/edt_scan_out[$i]
    connect_pin -from scan_dummy$i/Q -to main_edt_top/edt_scan_out[$i] -port for_dummy_Q_$i
    connect_pin -from occ_tck/U2/U2/Y -to scan_dummy$i/CK -port for_dummy_CK_$i
}
