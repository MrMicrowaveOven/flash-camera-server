from tkinter import *
def launch_interface():
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

	wifi_networks = wifi_info_module.get_wifi_list()

	def remove_this_network(network_name):
		if tkinter.messagebox.askokcancel("Confirm Network Deletion","Would you like to remove the network `" + network_name + "` from your list of known networks?"):
			print("REMOVING " + network_name)
			wifi_info_module.remove_network(network_name)
			refresh_interface()

	def show_network_list():
		wifi_networks = wifi_info_module.get_wifi_list()

		for i in range(len(wifi_networks)):
			y_coord = 0.25 + (0.025 * i)
			wifi_label = Label(window, text=wifi_networks[i])
			wifi_label.place(relx = 0.5, rely = y_coord, anchor = CENTER)

	def show_removal_buttons():
		for i in range(len(wifi_networks)):
			y_coord = 0.25 + (0.025 * i)
			removal_button = Button(window, text="X", command= lambda i=i: remove_this_network(wifi_networks[i]))
			removal_button.place(relx = 0.4, rely = y_coord, anchor = CENTER)

	def update_flash_cam_repo():
		g = git.cmd.Git('/home/pi/Desktop/flash-camera-server/')
		try:
			pull_response = g.pull()
		except Exception as e:
			print(e)
			pull_response_label = Label(window, bg="orange", text="There was an issue updating.  Please check your internet connection and try again.")
			pull_response_label.place(relx = 0.5, rely = 0.625, anchor = CENTER)
			return()
		print(pull_response)
		pull_response_label = ''
		if pull_response == "Already up-to-date.":
			pull_response_label = Label(window, bg="orange", text=pull_response)
		else:
			pull_response_label = Label(window, bg="orange", text="Updated!  You'll have the most recent version after you Refresh Interface.")
		pull_response_label.place(relx = 0.5, rely = 0.625, anchor = CENTER)

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
		wifi_confirmation_lbl = Label(window, bg="orange", text="Wifi info for `" + wifi_name_field.get() + "` added!  You'll see it when you Refresh Interface.  I also suggest you Reset Flash-Cam before testing.")
		wifi_confirmation_lbl.place(relx = 0.5, rely = 0.56, anchor = CENTER)

	def refresh_interface():
		window.destroy()
		launch_interface()

	add_wifi_button = Button(window, text="Add Network to the list", state=DISABLED, command=update_wifi_info)

	wifi_lbl = Label(window, text="Add Wifi Info:")

	def wifi_name_callback(wifi_name):
		field_entry = wifi_name.get()
		if field_entry == '':
			add_wifi_button['state'] = 'disabled'
		else:
			add_wifi_button['state'] = 'normal'

	wifi_name_lbl = Label(window, text="Wifi Name")
	wifi_name = StringVar()
	wifi_name.trace("w", lambda name, index, mode, wifi_name=wifi_name: wifi_name_callback(wifi_name))
	wifi_name_field = Entry(window, textvariable=wifi_name)

	wifi_password_lbl = Label(window, text="Wifi Password")
	wifi_password_field = Entry(window)

	show_wifi_remove_buttons_button = Button(window, text="Remove a Network from the list", command=show_removal_buttons)

	current_wifis_lbl = Label(window, text="Current saved wifi networks:")

	show_network_list()

	reset_button = Button(window, text="Reset Flash-Cam", command=confirm_reset)

	update_button = Button(window, text="Update Device via Network", command=update_flash_cam_repo)

	camera_preview_button = Button(window, text="Preview Camera for 10 seconds", command=preview_camera)

	programmer_mode_button = Button(window, text="Programmer Mode", command=window.destroy)
	programmer_mode_warning_label = Label(window, text="(please don't enter Programmer Mode unless you really know what you're doing)")

	refresh_button = Button(window, text="Refresh Interface", command=refresh_interface)

	welcome_lbl.place(relx = 0.5, rely = 0.2, anchor = CENTER)
	current_wifis_lbl.place(relx = 0.5, rely = 0.225, anchor = CENTER)

	wifi_lbl.place(relx = 0.5, rely = 0.4, anchor = CENTER)
	wifi_name_lbl.place(relx = 0.5, rely = 0.425, anchor = CENTER)
	wifi_name_field.place(relx = 0.5, rely = 0.45, anchor = CENTER)
	wifi_password_lbl.place(relx = 0.5, rely = 0.475, anchor = CENTER)
	wifi_password_field.place(relx = 0.5, rely = 0.5, anchor = CENTER)
	add_wifi_button.place(relx = 0.4, rely = 0.53, anchor = CENTER)
	show_wifi_remove_buttons_button.place(relx = 0.6, rely = 0.53, anchor = CENTER)
	update_button.place(relx = 0.5, rely = 0.6, anchor = CENTER)
	camera_preview_button.place(relx = 0.5, rely = 0.65, anchor = CENTER)
	reset_button.place(relx = 0.5, rely = 0.7, anchor = CENTER)
	programmer_mode_button.place(relx = 0.5, rely = 0.75, anchor = CENTER)
	programmer_mode_warning_label.place(relx = 0.5, rely = 0.775, anchor = CENTER)
	refresh_button.place(relx = 0.7, rely = 0.4, anchor = CENTER)

	window.mainloop()

launch_interface()
