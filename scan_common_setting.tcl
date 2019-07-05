# keep existing design name
set_dft_insertion_configuration -preserve_design_name true

# insert lockup latch between clock domains
set_scan_configuration -add_lockup true

# insert lockup latch at the end of scan chain
set_scan_configuration -insert_terminal_lockup true

# do not do incremental compile, do not touch existing logic
set_dft_insertion_configuration -synthesis_optimization none

# disable insertion of additional logic on bidi pad
# avoiding connection to scan en
set_dft_configuration -fix_bidirectional disable
set_dft_configuration -fix_bus disable

# scan chain mix edge, not clock
set_scan_configuration -clock_mixing mix_edges

# scan chain mix power
set_scan_configuration -power_domain_mixing true -voltage_mixing true -reuse_mv_cells true

# add retiming cell to chain, start with neg edge, for edt timing
set_scan_configuration -add_test_retiming_flops begin_and_end

# allow internal clock and other pins
set_dft_drc_configuration -internal_pin enable

# allow constant cells in scan chain
set_dft_drc_rules -ignore {TEST-504 TEST-505}

# set the length of chain
#set_scan_configuration -max_length 700
