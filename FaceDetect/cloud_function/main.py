"""
Author: Joseph Acevedo
This accepts an http request with json of the format {'url':'some-url-to-an-image'} and downloads
the image, then detects all the faces in it, and runs both vision models on all faces to return
two booleans, the first on whether anyone in the picture is wearing masks, and the second for 
whether everyone is wearing their mask correctly. If the first boolean is False (no one is wearing
a mask) then the second will be garbage data and should be ignored
"""
from flask import escape
import json
import cv2
import requests
import urllib.request
import numpy as np
from google.cloud import storage, automl_v1
from PIL import Image
import io
import base64

X_BOUNDING_BOX_INCREASE = 0.1
Y_BOUNDING_BOX_INCREASE = 0.2

def hello_http(request):
    mask_on = False
    mask_correct = True
    faces = []
    request_data = request.get_data()
    json_dict = json.loads(request_data)
    image_url = json_dict['url']
    resp = urllib.request.urlopen(image_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    client = storage.Client(project="ambient-net-292105")

    bucket = client.bucket("opencv_dnn_model")
    proto = bucket.blob('deploy.prototxt.txt').download_as_string()
    model = bucket.blob('res10_300x300_ssd_iter_140000.caffemodel').download_as_string()

    net = cv2.dnn.readNetFromCaffe(proto, model)
    # load the input image and construct an input blob for the image
    # by resizing to a fixed 300x300 pixels and then normalizing it
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > 0.25:
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            dx = (int) ((endX - startX) * (X_BOUNDING_BOX_INCREASE / 2))
            dy = (int) ((endY - startY) * (Y_BOUNDING_BOX_INCREASE / 2))

            startX = max(startX - dx, 0)
            startY = max(startY - dy, 0)
            endX = min(endX + dx, image.shape[1] - 1)
            endY = min(endY + dy, image.shape[0] - 1)

            if startX >= endX or startY >= endY:
                continue

            cropped_img = image[startY:endY, startX:endX]

            is_success, imbuffer = cv2.imencode(".jpg", cropped_img)
            if isMaskOn(imbuffer.tobytes()):
                mask_on = True
                if not isMaskOnCorrect(imbuffer.tobytes()):
                    mask_correct = False

    return '[{},{}]'.format(mask_on, mask_correct)

# 'content' is base-64-encoded image data.
def get_prediction(content, project_id, model_id):
    prediction_client = automl_v1.PredictionServiceClient()

    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    request = prediction_client.predict(name=name, payload=payload)
    return request  # waits till request is returned

def isMaskOnCorrect(imageBytes):
    #note: make sure the service account credentials are stored here
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/secrets/credentials.json"
    project_id = "854619995345"
    model_id = "ICN2477492167472316416"

    result = get_prediction(imageBytes, project_id, model_id).payload[0].display_name
    if result == 'Correct':
        return True
    else:
        return False

def isMaskOn(imageBytes):
    #note: make sure the service account credentials are stored here
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/secrets/credentials.json"
    project_id = "854619995345"
    model_id = "ICN3259992602727940096"

    result = get_prediction(imageBytes, project_id, model_id).payload[0].display_name
    if result == "Mask_on":
        return True
    else:
        return False