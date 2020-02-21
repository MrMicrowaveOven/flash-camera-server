from tkinter import *
import tkinter.messagebox

import git

import wifi_info_module

from picamera import PiCamera
import time

BASE_COLUMN = 0

window = Tk()

window.title("Admin Control Panel")

window.attributes('-fullscreen', True)
welcome_lbl = Label(window, text="Hello!  Welcome to the Administrative Control Panel.")

wifi_lbl = Label(window, text="Add Wifi Info:")

wifi_name_lbl = Label(window, text="Wifi Name")
wifi_name_field = Entry(window)

wifi_password_lbl = Label(window, text="Wifi Password")
wifi_password_field = Entry(window)

add_wifi_button = Button(window, text="Add wifi info", command=update_wifi_info)

current_wifis_lbl = Label(window, text="Current saved wifi networks:")

wifi_networks = wifi_info_module.get_wifi_list()
for i in range(len(wifi_networks)):
	Label(window, text=wifi_networks[i]).grid(column=BASE_COLUMN+0, row=(101 + i))

update_button = Button(window, text="Update Device", command=update_flash_cam_repo)

reset_button = Button(window, text="Reset Flash-Cam", command=confirm_reset)

camera_preview_button = Button(window, text="Preview Camera for 10 seconds", command=preview_camera)

programmer_mode_button = Button(window, text="Programmer Mode", command=window.destroy)
programmer_mode_warning_label = Label(window, text="(please don't enter Programmer Mode unless you really know what you're doing)")

welcome_lbl.grid(column=BASE_COLUMN, row=0)
wifi_lbl.grid(column=BASE_COLUMN, row=1)
wifi_name_lbl.grid(column=0, row=2)
wifi_name_field.grid(column=BASE_COLUMN+1, row=2)
wifi_password_lbl.grid(column=0, row=3)
wifi_password_field.grid(column=BASE_COLUMN+1, row=3)
add_wifi_button.grid(column=2, row=3)
current_wifis_lbl.grid(column=BASE_COLUMN+0, row=100)
update_button.grid(column=BASE_COLUMN, row=500)
reset_button.grid(column=BASE_COLUMN, row=1000)
camera_preview_button.grid(column=BASE_COLUMN, row=1500)
programmer_mode_button.grid(column=BASE_COLUMN, row=2500)
programmer_mode_warning_label.grid(column=0, row=2600)

def remove_this_network(i):
	if tkinter.messagebox.askokcancel("Confirm Network Deletion","Would you like to remove the network " + wifi_networks[i] + " from your list of known networks?"):
		print("REMOVING " + wifi_networks[i])

def open_removal_buttons():
	for i in range(len(wifi_networks)):
		Button(window, text="X", command= lambda i=i: remove_this_network(i)).grid(column=BASE_COLUMN+1, row=(101 + i))

def update_flash_cam_repo():
	g = git.cmd.Git('/home/pi/Desktop/flash-camera-server/')
	try:
		pull_response = g.pull()
	except Exception as e:
		print(e)
		pull_response_label = Label(window, bg="orange", text="There was an issue updating.  Please check your internet connection and try again.")
		pull_response_label.grid(column=BASE_COLUMN, row=520)
		return()
	print(pull_response)
	pull_response_label = ''
	if pull_response == "Already up-to-date.":
		pull_response_label = Label(window, bg="orange", text=pull_response)
	else:
		pull_response_label = Label(window, bg="orange", text="Updated!  You'll have the most recent version after you restart.")
	pull_response_label.grid(column=BASE_COLUMN, row=520)

def confirm_reset():
	if tkinter.messagebox.askokcancel("Reset Camera?","Are you sure you would like to reset your camera?"):
		reset_camera()

def reset_camera():
	command = "/usr/bin/sudo /sbin/shutdown -r now"
	import subprocess
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	print(output)

def preview_camera():
	camera = PiCamera()
	camera.start_preview()
	time.sleep(10)
	camera.close()

def update_wifi_info():
	wifi_info_module.update_wifi_info(ssid_entry.get(), psk_entry.get())
	Label(window, bg="orange", text="Wifi info added for " + ssid_entry.get() + " added!  Restart to connect!").grid(column=0, row=4)

window.mainloop()
