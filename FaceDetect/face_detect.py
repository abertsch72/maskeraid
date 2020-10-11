"""
Author: Joseph Acevedo, Amanda Bertsch

A script for normalizing images of people's faces that are both wearing masks and not wearing them. The default location of the input images
is specified by IMAGE_DIR. The script will go through every image in the directory and detect faces (using the script from 
https://github.com/sr6033/face-detection-with-OpenCV-and-DNN/blob/master/detect_faces.py ) then expand the bounding box by
10% horizonally and 20% vertically (this can be modified by changing X/Y_BOUNDING_BOX_INCREASE) and crops the image then saves a colored and grayscale version of
the cropped image to their respective output folders (ORIG_DIR and BW_DIR respectively) 
"""
import os
import cv2
import numpy as np
from datetime import datetime
import urllib.request
import matplotlib.pyplot as plt
from MaskClassifierClient.MaskClassifierClient import isMaskOn, isMaskOnCorrect

PROTOTXT = "deploy.prototxt.txt"
MODEL = "res10_300x300_ssd_iter_140000.caffemodel"
MIN_CONF = 0.25
X_BOUNDING_BOX_INCREASE = 0.1
Y_BOUNDING_BOX_INCREASE = 0.2


def process_folder():
    IMAGE_DIR = "images/"
    OUTPUT_DIR = "norm_images/"
    ORIG_DIR = f"{OUTPUT_DIR}original/"
    BW_DIR = f"{OUTPUT_DIR}blackwhite/"

    # Verify output folder structure exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        os.makedirs(ORIG_DIR)
        os.makedirs(BW_DIR)
    else:
        if not os.path.exists(ORIG_DIR):
            os.makedirs(ORIG_DIR)
        if not os.path.exists(BW_DIR):
            os.makedirs(BW_DIR)

    for img_path in os.listdir(IMAGE_DIR):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Processing file: {IMAGE_DIR}{img_path}")
        # load our serialized model from disk
        net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)

        # load the input image and construct an input blob for the image
        # by resizing to a fixed 300x300 pixels and then normalizing it
        image = cv2.imread(f"{IMAGE_DIR}{img_path}")
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))

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
            if confidence > MIN_CONF:
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


                file_prefix = img_path.split('.')[0]
                try:
                    cropped_img = image[startY:endY, startX:endX]
                    gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(f"{ORIG_DIR}{file_prefix}_i{i}_o.jpeg", cropped_img)
                    cv2.imwrite(f"{BW_DIR}{file_prefix}_i{i}_bw.jpeg", gray_img)
                except Exception:
                    print(f"Failed to save modified images... continuing")

                # draw the bounding box of the face along with the associated
                # probability
                """
                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(image, (startX, startY), (endX, endY),
                    (0, 0, 255), 2)
                cv2.putText(image, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                """

def process_image(image_url):
    # load our serialized model from disk
    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)

    # load the input image and construct an input blob for the image
    # by resizing to a fixed 300x300 pixels and then normalizing it
    resp = urllib.request.urlopen(image_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))

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
        if confidence > MIN_CONF:
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            dx = (int)((endX - startX) * (X_BOUNDING_BOX_INCREASE / 2))
            dy = (int)((endY - startY) * (Y_BOUNDING_BOX_INCREASE / 2))

            startX = max(startX - dx, 0)
            startY = max(startY - dy, 0)
            endX = min(endX + dx, image.shape[1] - 1)
            endY = min(endY + dy, image.shape[0] - 1)

            if startX >= endX or startY >= endY:
                continue

            cropped_img = image[startY:endY, startX:endX]
            issuccess, imbuffer = cv2.imencode(".jpg", cropped_img)
            if(isMaskOn(imbuffer.tobytes())):
                print("got here!")
                if(not isMaskOnCorrect(imbuffer.tobytes())):
                    return True

    return False


print(process_image("https://cdn.cms.prod.nypr.digital/images/Screen_Shot_2020-06-13_at_2.19.11_.2e16d0ba.fill-661x496.png"))