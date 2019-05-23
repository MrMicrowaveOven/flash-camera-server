import time
from time import sleep

import boto3

from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    try:
        file_name = take_picture()
        return send_picture_to_s3(file_name)
    except Exception:
        print Exception
        return "CAMERA ERROR"
def take_picture():
    from picamera import PiCamera

    time_num = int(time.time())
    file_name = 'chateau%s.jpg' % time_num

    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(2)
    camera.capture(file_name)
    camera.close()

    print file_name
    return file_name
def send_picture_to_s3(file_name):
    s3_client = boto3.client('s3')
    bucket_name = 'flash-images-store'

    s3_client.upload_file(file_name, bucket_name, file_name, ExtraArgs={'ContentType': 'image/jpeg'})

    return 'https://s3-us-west-1.amazonaws.com/%s/%s' % (bucket_name, file_name)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
