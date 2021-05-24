import json
import numpy as np
from datetime import datetime
import time
import cv2
import base64
import hashlib
from os import listdir
import boto3

import os
import csv
import torch
from torch import nn
from torchvision import models
from torchvision import transforms as transform_lib
import pytorch_lightning as pl
from PIL import Image as im


s3 = boto3.resource('s3')

def lambda_handler(event, context):
    ####### PUT YOUR INFORMATION HERE #######
    CAPTAIN_EMAIL = 'jason2650@gmail.com'   #
    SALT = 'my_salt'                        #
    #########################################
    
    now = int(time.time())
    
    server_uuid_unconverted = CAPTAIN_EMAIL + SALT
    server_uuid = generate_server_uuid(server_uuid_unconverted)
    
    image_nparray = base64_to_image(event['image'])
    
    # upload to s3
    if event['esun_uuid'] == 'test':
        upload_outcome = 'no upload'
    else:
        upload_outcome = image_to_s3(image_nparray)
        
    #inference
    #answer_str = inference(image_nparray)

    ############# TESTING CODES #############
    
    dirlist = listdir("/mnt/ml/model")
    
    #########################################

    return {  
    "esun_uuid": event['esun_uuid'],
    "server_uuid": server_uuid,
    "server_timestamp": now,
    "answer": "test"
    #,"test_output (upload to s3)": upload_outcome
    ,"test_output (listdir)": dirlist
    }
    
def generate_server_uuid(input_string):
    """ Create your own server_uuid.

    @param:
        input_string (str): information to be encoded as server_uuid
    @returns:
        server_uuid (str): your unique server_uuid
    """
    s = hashlib.sha256()
    data = (input_string).encode("utf-8")
    s.update(data)
    server_uuid = s.hexdigest()
    return server_uuid

def base64_to_image(image_64_encoded):
    img_binary = base64.b64decode(image_64_encoded)
    image_bgr = cv2.imdecode(np.frombuffer(img_binary, np.uint8), cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image_bgr,cv2.COLOR_BGR2RGB)

    return image_rgb
    
def image_to_s3(image_nparray):
    image = Image.fromarray(image_nparray)
    
    try:
        im.save("/mnt/ml/temp.jpg")
        
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        s3_file_path = 'API-pic-input/' + now_str + '.jpg'
        s3.meta.client.upload_file(Bucket='tbrain-2021-images', Key=s3_file_path, Filename="/mnt/ml/temp.jpg")
        upload_outcome = 'success'
    except:
        upload_outcome = 'failed'
    
    return upload_outcome
