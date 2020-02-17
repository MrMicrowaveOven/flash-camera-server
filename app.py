import time
from time import sleep

import requests
import boto3

from picamera import PiCamera

import os

import uuid

mothership_url = 'https://flash-sms-server.herokuapp.com'

camera_url = mothership_url + '/cameras'
mac_address = hex(uuid.getnode())
camera_url_with_params = camera_url + '?mac_address=' + mac_address


def start_heartbeat():
    last_posted_message = []
    while True:
        current_message_log = []
        picture_id = False
        try:
            response = requests.get(camera_url_with_params)
            picture_id = response.json()['picture_id']
        except:
            current_message_log.append('get camera request failed')

        if picture_id:
            # Take a picture
            try:
                file_name = take_picture()
            except:
                current_message_log.append('camera error')
            # Upload to S3
            try:
                photo_url = send_picture_to_s3(file_name)
            except:
                current_message_log.append('S3 send failed')
            # Delete local photo
            try:
                delete_image(file_name)
            except:
                current_message_log.append('Image deletion failed')

            try:
                requests.patch(mothership_url + '/pictures/' + str(picture_id), {'photo_url': photo_url})
            except:
                current_message_log.append('patch camera request failed')


            if len(current_message_log) == 0:
                log('sending picture ' + str(picture_id))
        elif len(current_message_log) == 0:
            current_message_log.append('standing by')

        if current_message_log != last_posted_message:
            for message in current_message_log:
                log(message)
        last_posted_message = current_message_log
        sleep(1)

def log(message):
    current_time = time.ctime()
    print(current_time + ' -- ' + message)

def send_picture_to_s3(file_name):
    s3_client = boto3.client('s3')
    bucket_name = 'flash-images-store'

    s3_client.upload_file(file_name, bucket_name, file_name, ExtraArgs={'ContentType': 'image/jpeg'})

    return 'https://s3-us-west-1.amazonaws.com/' + bucket_name + '/' + file_name

def take_picture():
    file_name = mac_address + '-' + str(int(time.time())) + '.jpg'
    camera = PiCamera()
    sleep(2)
    camera.capture(file_name)
    camera.close()
    return file_name

def delete_image(file_name):
    os.remove(file_name)

start_heartbeat()
