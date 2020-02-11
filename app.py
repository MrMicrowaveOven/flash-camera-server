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

while True:
    response = requests.get(camera_url)

    picture_id = response.json()['picture_id']
    if picture_id:
        # Take a picture
        file_name = take_picture()
        # Upload to S3
        photo_url = send_picture_to_s3(file_name)
        # Delete local photo
        delete_image(file_name)

        requests.patch(mothership_url + '/pictures/' + str(picture_id), {'photo_url': photo_url})
        print('updating')
    else:
        print('standing by')
        sleep(1)

def send_picture_to_s3(file_name):
    s3_client = boto3.client('s3')
    bucket_name = 'flash-images-store'

    s3_client.upload_file(file_name, bucket_name, file_name, ExtraArgs={'ContentType': 'image/jpeg'})

    return 'https://s3-us-west-1.amazonaws.com/%s/%s' % (bucket_name, file_name)

def take_picture():
    file_name = camera_name_str + str(int(time.time()))
    camera = PiCamera()
    sleep(2)
    camera.capture(file_name)
    camera.close()
    return file_name

def delete_image(file_name):
    os.remove(file_name)
    print("File removed!")
    print(file_name)
