from tkinter import *

from wifi import Cell, Scheme

import git

window = Tk()

window.title("Wifi Networks")

window.attributes('-fullscreen', True)

buttons = []

wifi_login_fields = []

def select_wifi(wifi_name):
    destroy_all_buttons()
    global wifi_login_fields
    lbl = Label(window, text=("Connect to " + wifi_name))
    lbl.grid(column=0, row=1)
    wifi_login_fields.append(lbl)

    lbl = Label(window, text="Wifi Password: ")
    lbl.grid(column=0, row=2)
    wifi_login_fields.append(lbl)

    password = Entry(window)
    password.grid(column=1, row=2)
    wifi_login_fields.append(password)

    btn = Button(window, text="Pick another Wifi", command=refresh_wifi_buttons)
    btn.grid(column=0, row=3)
    wifi_login_fields.append(btn)

    btn = Button(window, text="Connect to Wifi", command= lambda: connect_to_wifi(wifi_name, password.get()))
    btn.grid(column=1, row=3)
    wifi_login_fields.append(btn)

def connect_to_wifi(wifi_name, wifi_password):
    print(wifi_name)
    print(wifi_password)

def destroy_all_buttons():
    global buttons
    for button in buttons:
        button.destroy()
    buttons = []

def destroy_wifi_login_fields():
    global wifi_login_fields
    for wifi_login_field in wifi_login_fields:
        wifi_login_field.destroy()
    wifi_login_fields = []

def get_wifis():
    return ['tatuin', 'stuff', 'crap', 'meh']

def refresh_wifi_buttons():
    destroy_wifi_login_fields()
    destroy_all_buttons()

    wifis = get_wifis()
    for i in range(len(wifis)):
        wifi = wifis[i]
        wifi_button = Button(window, text=wifi, command= lambda wifi=wifi: select_wifi(wifi))
        wifi_button.grid(column=0, row=(i + 4))

        buttons.append(wifi_button)
    print(buttons)

lbl = Label(window, text="Hello!  Here are the available wifi networks:")
lbl.grid(column=0, row=0)
Button(window, text="Refresh Wifis", command=refresh_wifi_buttons).grid(column=1, row=0)

refresh_wifi_buttons()

repo_update_row = len(buttons) + 4

lbl = Label(window, text="Would you like to update?  If so, click here:")
lbl.grid(column=0, row=(repo_update_row))

def update_flash_cam_repo():
	g = git.cmd.Git('/home/pi/Desktop/flash-camera-server/')
	pull_response = g.pull()
	print(pull_response)
	pull_response_label = ''
	if pull_response == "Already up-to-date.":
		pull_response_label = Label(window, text=pull_response)
	else:
		pull_response_label = Label(window, text="Updated!  You'll have the most recent version after you restart.")
	pull_response_label.grid(column=0, row=3)
update_button = Button(window, text="Update", command=update_flash_cam_repo)
update_button.grid(column=1, row=(repo_update_row))

quit_button = Button(window, text="Quit", command=window.destroy)
quit_button.grid(column=0, row=(repo_update_row + 1))

window.mainloop()
