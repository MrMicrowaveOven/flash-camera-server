from tkinter import *
import tkinter.messagebox

from wifi import Cell, Scheme

import git

import wifi_info_module

window = Tk()

window.title("Admin Control Panel")

window.attributes('-fullscreen', True)
lbl = Label(window, text="Hello!  Welcome to the Administrative Control Panel.")
lbl.grid(column=0, row=0)

lbl = Label(window, text="Add Wifi Info:")
lbl.grid(column=0, row=1)

lbl = Label(window, text="Wifi Name").grid(column=0, row=2)
ssid_entry = Entry(window)
ssid_entry.grid(column=1, row=2)

lbl = Label(window, text="Wifi Password").grid(column=0, row=3)
psk_entry = Entry(window)
psk_entry.grid(column=1, row=3)

def update_wifi_info():
	wifi_info_module.update_wifi_info(ssid_entry.get(), psk_entry.get())
	Label(window, text="Wifi info added for " + ssid_entry.get() + " added!  Restart to connect!").grid(column=0, row=4)

Button(window, text="Add wifi info", command=update_wifi_info).grid(column=2, row=3)

Label(window, text="Current saved wifi networks:").grid(column=0, row=100)

wifi_networks = wifi_info_module.get_wifi_list()
for i in range(len(wifi_networks)):
	Label(window, text=wifi_networks[i]).grid(column=0, row=(101 + i))

def remove_this_network(i):
	if tkinter.messagebox.askokcancel("Confirm Network Deletion","Would you like to remove the network " + wifi_networks[i] + " from your list of known networks?"):
		print("REMOVING " + wifi_networks[i])

def open_removal_buttons():
	for i in range(len(wifi_networks)):
		Button(window, text="X", command= lambda i=i: remove_this_network(i)).grid(column=1, row=(101 + i))

# Button(window, text="Remove a wifi network", command=open_removal_buttons).grid(column=0, row=400)

lbl = Label(window, text="Would you like to update?  If so, click here: ")
lbl.grid(column=0, row=500)

def update_flash_cam_repo():
	g = git.cmd.Git('/home/pi/Desktop/flash-camera-server/')
	pull_response = g.pull()
	print(pull_response)
	pull_response_label = ''
	if pull_response == "Already up-to-date.":
		pull_response_label = Label(window, text=pull_response)
	else:
		pull_response_label = Label(window, text="Updated!  You'll have the most recent version after you restart.")
	pull_response_label.grid(column=0, row=520)
update_button = Button(window, text="Update", command=update_flash_cam_repo)
update_button.grid(column=1, row=500)

quit_button = Button(window, text="Quit", command=window.destroy)
quit_button.grid(column=2, row=1000)

window.mainloop()
