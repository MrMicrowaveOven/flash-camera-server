# Used for name generation
import time

# Used for requests
import requests

# name.py
import name

camera_name = name.camera_name

name_suffix = int(time.time())

camera_url_name = camera_name + str(name_suffix)
camera_full_url = camera_url_name + '.serveo.net'

camera_id = name.camera_id

server_url = 'https://flash-sms-server.herokuapp.com/cameras/' + str(camera_id)

params = { 
	'id': camera_id,
	'url': camera_full_url
}


def call_serveo(camera_url):
        print('serveo will be called soon')
        print(camera_url_name)


response = requests.patch(url = server_url, params = params)

if response:
	call_serveo(camera_url_name)
else:
	raise Exception('Call to Camera Update server failed')