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
`pip install boto3 ;`
`pip3 install gitpython ;`

#### If guff with boto3, run the following:

`sudo python -m pip install --upgrade --force setuptools`

`sudo python -m pip install --upgrade --force pip`

### Add AWS Credentials
```
mkdir ~/.aws
touch ~/.aws/credentials
leafpad ~/.aws/credentials
```

Open the credentials file.  You may need to use the shitty interface, since the file descriptor doesn't default to text.  The content of the document can be found on LastPass, under S3 Key.

### Initiate the server to test

`python3 helloWorld.py`

### No need to install Serveo, since it's fucking awesome, but run the following to enable bypassing security protocols:

`ssh -o ServerAliveInterval=30 -tt -R {camera-name}:80:localhost:8080 serveo.net`

### Add the new Camera to the database, with the tunnel_url.  Make note of the ID.

### To keep your Serveo shit running all night, add the following to `/etc/ssh/ssh_config`
```
ServerAliveInterval 30
ServerAliveCountMax 3
```

### Add to crontab, so the Server and Serveo start on Boot (`crontab -e`)

That bottom part reboots the FlashCam everyday at midnight.
```
@reboot (/bin/sleep 15; /usr/bin/python /home/pi/Desktop/flash-camera-server/helloWorld.py >/home/pi/serverlog 2>&1)
@reboot (/bin/sleep 25; ssh -o ServerAliveInterval=30 -tt -R {camera-name}:80:localhost:8080 serveo.net >/home/pi/serveolog 2>&1)
0 0 * * * root reboot
```

### Set the Admin Interface to run on boot

`sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`

Add `@python3 /home/pi/Desktop/flash-camera-server/interface.py` to the file, between `@pcmanfm` and `@xscreensaver` lines.

### Add the Admin Interface shortcut to the desktop, in case the user closes it.

It should contain the following:

```
[Desktop Entry]
Name=Admin Interface
Comment=This allows the Flash Cam owner to update the software, as well as ch$
Icon=/usr/share/pixmaps/geany.xpm
Exec=python3 /home/pi/Desktop/flash-camera-server/interface.py
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

### IF you would like an hourly reset:

`sudo crontab -e -u root`

Add the following line to the bottom:

```
0 * * * * /sbin/shutdown -r >/home/pi/rebootlog 2>&1
```

This will call a reset every hour at 0 minutes.

### Update the Splash image

(still never figured out)
<!-- Change `/usr/share/plymouth/themes/pix/splash.png` to this image: https://benjs-bucket.s3-us-west-1.amazonaws.com/camera_splash.jpeg

May need to use `sudo mv`. -->

<!-- https://scribles.net/customizing-boot-up-screen-on-raspberry-pi/ -->
