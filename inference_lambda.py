import json
import numpy as np
from datetime import datetime
import time
import cv2
import base64
import hashlib

import os
import torch
from torch import nn
from torchvision import models
from torchvision import transforms as transform_lib
import pytorch_lightning as pl
from PIL import Image as im


s3 = boto3.resource('s3')

def lambda_handler(event, context):
    ####### PUT YOUR INFORMATION HERE #######
    CAPTAIN_EMAIL = 'your_email'            #
    SALT = 'my_salt'                        #
    #########################################
    
    # Get current time
    now = int(time.time())
    
    # Generate server uuid
    server_uuid_unconverted = CAPTAIN_EMAIL + SALT
    server_uuid = generate_server_uuid(server_uuid_unconverted)
    
    # Transform base64 codes to image
    image_nparray = base64_to_image(event['image'])
    
    # Inference
    answer = predict(image_nparray)

    # Function Output = API Output
    return {  
    "esun_uuid": event['esun_uuid'],
    "server_uuid": server_uuid,
    "server_timestamp": now,
    "answer": answer
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
    """ Convert base64 to numpy.ndarray for cv2.

    @param:
        image_64_encode(str): image that encoded in base64 string format.
    @returns:
        image(numpy.ndarray): an image.
    """
    img_binary = base64.b64decode(image_64_encoded)
    image = cv2.imdecode(np.frombuffer(img_binary, np.uint8), cv2.IMREAD_COLOR)

    return image
    
def predict(image):
    """ Predict your model result.

    @param:
        image (numpy.ndarray): an image.
    @returns:
        prediction (str): a word.
    """

    ####### PUT YOUR MODEL INFERENCING CODE HERE #######
    


    ####################################################
    if _check_datatype_to_string(prediction):
        return prediction
