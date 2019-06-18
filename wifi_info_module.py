def get_wifi_list():
    file = open('wpa_supplicant.conf', 'r')
    file_list = file.read().splitlines()

    ssid_names = []
    for i in range(len(file_list)):
        line = file_list[i]
        if is_ssid_line(line):
            ssid_names.append(get_ssid_name(line))
    return ssid_names

def update_wifi_info(ssid, psk):
    file = open('wpa_supplicant.conf', 'r')
    file_list = file.read().splitlines()
    ssid_exists = False

    for i in range(len(file_list)):
        line = file_list[i]
        if is_ssid_line(line):
            ssid_name = get_ssid_name(line)
            if ssid_name == ssid:
                file_list[i + 1] = get_updated_psk_line(file_list[i + 1], psk)
                ssid_exists = True
    if not ssid_exists:
        wifi_info_block = make_wifi_info_block(ssid, psk)
        bottom_of_file = len(file_list) + 2

        for i in range(6):
            file_list.append(wifi_info_block[i])
    open('wpa_supplicant.conf', 'w').write('\n'.join(file_list))

def get_ssid_name(ssid_line):
    return ssid_line[9:].replace('"', '')

def is_ssid_line(line):
    return "ssid" in line and line.index("ssid") == 4

def is_psk_line(line):
    return "psk" in line and line.index("psk") == 4

def make_wifi_info_block(ssid, psk):
    wifi_info_arr = ['']
    wifi_info_arr.append('network={')
    wifi_info_arr.append('    ssid="' + ssid + '"')
    wifi_info_arr.append('    psk="' + psk + '"')
    wifi_info_arr.append('    key_mgmt=WPA-PSK')
    wifi_info_arr.append('}')
    return wifi_info_arr

def get_updated_psk_line(psk_line, new_psk):
    PSK_LINE_START = '    psk="'
    PSK_LINE_END = '"'
    if is_psk_line(psk_line):
        return PSK_LINE_START + new_psk + PSK_LINE_END
    else:
        raise TypeError('get_updated_psk_line was called without a valid psk_line')
