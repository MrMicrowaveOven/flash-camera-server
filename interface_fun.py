from tkinter import *

from wifi import Cell, Scheme

import git

window = Tk()

window.title("Wifi Networks")

window.attributes('-fullscreen', True)

def select_wifi(wifi_id):
    print(wifi_id)

buttons = []

def refresh_wifi_buttons():
    global buttons
    for button in buttons:
        button.destroy()
    buttons = []
    wifis = ['tatuin', 'stuff', 'crap', 'meh']
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
