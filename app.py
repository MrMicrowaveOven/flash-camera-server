import time
from time import sleep

import requests
import boto3

import camera_name

from picamera import PiCamera

import os

mothership_url = 'https://flash-sms-server.herokuapp.com'
# camera_name_str = camera_name.camera_name

camera_url = mothership_url + '/cameras/' +  str(camera_name.camera_id)
camera_name_str = camera_name.camera_name

def start_heartbeat():
    last_posted_message = False
    current_message_log = []
    while True:
        picture_id = False
        try:
            response = requests.get(camera_url)
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
                print('sending picture' + file_name)
        elif len(current_message_log) == 0:
            current_message_log.append('standing by')

        if current_message_log != last_posted_message:
            for message in current_message_log:
                print(message)
        last_posted_message = current_message_log
        sleep(1)

def send_picture_to_s3(file_name):
    s3_client = boto3.client('s3')
    bucket_name = 'flash-images-store'

    s3_client.upload_file(file_name, bucket_name, file_name, ExtraArgs={'ContentType': 'image/jpeg'})

    return 'https://s3-us-west-1.amazonaws.com/' + bucket_name + '/' + file_name

def take_picture():
    file_name = camera_name_str + str(int(time.time())) + '.jpg'
    camera = PiCamera()
    sleep(2)
    camera.capture(file_name)
    camera.close()
    return file_name

def delete_image(file_name):
    os.remove(file_name)

start_heartbeat()
