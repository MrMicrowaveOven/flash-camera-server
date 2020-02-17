# Flash Camera Server

This is a a small server that runs on a raspberry pi.

## Installation Instructions

Plug the following into the Raspberry Pi

1. Camera
2. SD Card with N00bs on it
3. Mouse
4. Keyboard

Then put the case on, and secure the camera (duct tape).

### Connect to the internet

Top-right.  If you get it wrong the first time it's a pain in the ass.

### Set the clock on the Pi

Requires reboot.

### Enable the Camera

* Global
* Preferences
* Raspberry Pi Configuration
* Interfaces
* Camera

Requires reboot.

### Stacked terminal commands:
#### Install Git
#### Give permission for the interface to update wifi info
#### Clone the repo
#### Install boto3
#### Install gitpython

`sudo apt install git ;`
`sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf ;`
`cd ~/Desktop ;`
`git clone https://github.com/MrMicrowaveOven/flash-camera-server.git ;`
`cd flash-camera-server ;`
`pip3 install boto3 ;`
`pip3 install gitpython ;`

#### If guff with boto3, run the following:

`sudo python -m pip install --upgrade --force setuptools`

`sudo python -m pip install --upgrade --force pip`

Sometimes `pip install boto3` works as well.

You may get a 'No ordered dict' error at some point.  If so run the following:
```
pip uninstall urllib3

pip install urllib3==1.22
```

### Add AWS Credentials
```
mkdir ~/.aws
touch ~/.aws/credentials
leafpad ~/.aws/credentials
```

Fill this doc with the note on Lastpass, under S3 Key.

### Update mac_address in the database (remove the last digit that's a capital)

### Initiate the server to test

`python3 app.py`

### Add to crontab, so the app.py starts on boot (`crontab -e`)
```
@reboot (/bin/sleep 15; /usr/bin/python3.5 /home/pi/Desktop/flash-camera-server/app.py)
```

### Add relevant files to .gitignore

```
__pycache__/
*.py[cod]
```

### Set the Admin Interface to run on boot

`sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`

Add `@python3 /home/pi/Desktop/flash-camera-server/camera_interface/interface.py` to the file, between `@pcmanfm` and `@xscreensaver` lines.

### Add the Admin Interface shortcut to the desktop, in case the user closes it.

It should contain the following:

```
[Desktop Entry]
Name=Admin Interface
Comment=This allows the Flash Cam owner to update the software, as well as ch$
Icon=/usr/share/pixmaps/geany.xpm
Exec=python3 /home/pi/Desktop/flash-camera-server/camera_interface/interface.py
Type=Application
Encoding=UTF-8
Terminal=false
Categories=None;
```

Save it as `Admin Interface.desktop`

### Add WiFi credentials

Use the interface you just created.  Double-check that it worked with

`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

You should see these:

```
network={
    ssid="testing"
    psk="testingPassword"
}
```

### Update /boot/config.txt so it will work on most HDMI monitors

`sudo nano /boot/config.txt`

Add the following lines to the bottom:

```
hdmi_force_hotplug=1
hdmi_group=1
hdmi_mode=16
```

### Test!

`sudo reboot` to see if it all works!

### Update the Splash image

(still never figured out)
<!-- Change `/usr/share/plymouth/themes/pix/splash.png` to this image: https://benjs-bucket.s3-us-west-1.amazonaws.com/camera_splash.jpeg

May need to use `sudo mv`. -->

<!-- https://scribles.net/customizing-boot-up-screen-on-raspberry-pi/ -->
