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
    posted_stand_by_log = False
    while True:
        picture_id = False
        try:
            response = requests.get(camera_url)

            picture_id = response.json()['picture_id']
        except:
            print('get camera request failed')

        if picture_id:
            posted_stand_by_log = False
            # Take a picture
            try:
                file_name = take_picture()
            except:
                print('camera error')
            # Upload to S3
            try:
                photo_url = send_picture_to_s3(file_name)
            except:
                print('S3 send failed')
            # Delete local photo
            try:
                delete_image(file_name)
            except:
                print('Image deletion failed')

            try:
                requests.patch(mothership_url + '/pictures/' + str(picture_id), {'photo_url': photo_url})
            except:
                print('patch camera request failed')
            print('updating')
        else:
            if not posted_stand_by_log:
                print('standing by')
                posted_stand_by_log = True
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
