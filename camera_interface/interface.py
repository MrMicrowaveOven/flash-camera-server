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
welcome_lbl = Label(window, text="Hello!  Welcome to the Administrative Control Panel.", font=(20))

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
	wifi_info_module.update_wifi_info(wifi_name_field.get(), wifi_password_field.get())
	Label(window, bg="orange", text="Wifi info added for " + wifi_name_field.get() + " added!  Restart to connect!").grid(column=0, row=4)

wifi_lbl = Label(window, text="Add Wifi Info:")

wifi_name_lbl = Label(window, text="Wifi Name")
wifi_name_field = Entry(window)

wifi_password_lbl = Label(window, text="Wifi Password")
wifi_password_field = Entry(window)

add_wifi_button = Button(window, text="Add wifi info", command=update_wifi_info)

current_wifis_lbl = Label(window, text="Current saved wifi networks:")

wifi_networks = wifi_info_module.get_wifi_list()
for i in range(len(wifi_networks)):
	y_coord = 0.25 + (0.025 * i)
	Label(window, text=wifi_networks[i]).place(relx = 0.5, rely = y_coord, anchor = CENTER)

reset_button = Button(window, text="Reset Flash-Cam", command=confirm_reset)

update_button = Button(window, text="Update Device via Network", command=update_flash_cam_repo)

camera_preview_button = Button(window, text="Preview Camera for 10 seconds", command=preview_camera)

programmer_mode_button = Button(window, text="Programmer Mode", command=window.destroy)
programmer_mode_warning_label = Label(window, text="(please don't enter Programmer Mode unless you really know what you're doing)")

welcome_lbl.place(relx = 0.5, rely = 0.2, anchor = CENTER)
current_wifis_lbl.place(relx = 0.5, rely = 0.225, anchor = CENTER)

wifi_lbl.place(relx = 0.5, rely = 0.4, anchor = CENTER)
wifi_name_lbl.place(relx = 0.5, rely = 0.425, anchor = CENTER)
wifi_name_field.place(relx = 0.5, rely = 0.45, anchor = CENTER)
wifi_password_lbl.place(relx = 0.5, rely = 0.475, anchor = CENTER)
wifi_password_field.place(relx = 0.5, rely = 0.5, anchor = CENTER)
add_wifi_button.place(relx = 0.5, rely = 0.53, anchor = CENTER)
update_button.place(relx = 0.5, rely = 0.6, anchor = CENTER)
camera_preview_button.place(relx = 0.5, rely = 0.65, anchor = CENTER)
reset_button.place(relx = 0.5, rely = 0.7, anchor = CENTER)
programmer_mode_button.place(relx = 0.5, rely = 0.75, anchor = CENTER)
programmer_mode_warning_label.place(relx = 0.5, rely = 0.775, anchor = CENTER)

window.mainloop()
