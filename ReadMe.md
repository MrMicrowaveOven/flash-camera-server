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
* Interfaces
* Camera

Requires reboot.

### Install Git

`sudo apt install git`

### Clone the repo

`git clone https://github.com/MrMicrowaveOven/flash-camera-server.git`

### Add AWS Credentials
```
mkdir ~/.aws
touch ~/.aws/credentials
leafpad ~/.aws/credentials
```

Open the credentials file.  You may need to use the shitty interface, since the file descriptor doesn't default to text.  The content of the document can be found on LastPass, under S3 Key.

### Install boto3

`pip install boto3`

### Initiate the server

`python helloWorld.py`

### Add the new Camera to the database, with the tunnel_url.

### Add to crontab, so the Server and Serveo start on Boot

```
@reboot (/bin/sleep 15; /usr/bin/python /home/pi/Desktop/flash-camera-server/helloWorld.py >/home/pi/serverlog 2>&1)
@reboot (/bin/sleep 25; ssh -o ServerAliveInterval=30 -tt -R flash-chateau:80:localhost:8080 serveo.net >/home/pi/serveolog 2>&1)
```
