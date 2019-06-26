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

### Add to crontab, so the Server and Serveo start on Boot (`crontab -e`)

```
@reboot (/bin/sleep 15; /usr/bin/python /home/pi/Desktop/flash-camera-server/helloWorld.py >/home/pi/serverlog 2>&1)
@reboot (/bin/sleep 25; ssh -o TCPKeepAlive=yes ServerAliveInterval=30 -tt -R {camera-name}:80:localhost:8080 serveo.net >/home/pi/serveolog 2>&1)
```

### Test!

`sudo reboot` to see if it all works!

### Add WiFi credentials

`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

You'll see these:

```
network={
    ssid="testing"
    psk="testingPassword"
}
```

Add the necessary network credentials, so it can add itself to WiFi on boot.

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

### Update the Splash image

<!-- Change `/usr/share/plymouth/themes/pix/splash.png` to this image: https://benjs-bucket.s3-us-west-1.amazonaws.com/camera_splash.jpeg

May need to use `sudo mv`. -->

https://scribles.net/customizing-boot-up-screen-on-raspberry-pi/
