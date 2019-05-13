from flask import Flask

import boto3
import time

app = Flask(__name__)
@app.route('/')
def index():
    s3_client = boto3.client('s3')
    bucket_name = 'flash-images-store'
    time_num = str(int(time.time()))
    bucket_file_name = 'marilyn' + time_num + '.jpg'
    s3_client.upload_file('marilyn.jpg', bucket_name, bucket_file_name, ExtraArgs={'ContentType': 'image/jpeg'})
    return 'https://s3-us-west-1.amazonaws.com/flash-images-store/' + bucket_file_name
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
