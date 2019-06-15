from tkinter import *

from wifi import Cell, Scheme

import git

window = Tk()

window.title("Wifi Networks")

window.attributes('-fullscreen', True)
# lbl = Label(window, text="Hello!  Here are the available wifi networks:")

# lbl.grid(column=0, row=0)

lbl = Label(window, text="Would you like to update?  If so, click here: ")
lbl.grid(column=0, row=1)

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
update_button.grid(column=2, row=1)

quit_button = Button(window, text="Quit", command=window.destroy)
quit_button.grid(column=5, row=10)

window.mainloop()
