set SE_pins [get_attri [get_pins -h */SE] full_name]

foreach se $SE_pins {
    disconnect_net [get_net -of $se] $se
    connect_pin -from scan_en -to $se -port scan_clock_path
}
