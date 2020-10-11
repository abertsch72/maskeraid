GROUPME_API = "https://api.groupme.com/v3/bots/post?"
BOT_ID = "8eaaaef61bd2dce30f1af87d0d"
BOT_NAME = "maskeraid"

MASK_CLASSIFIER_API = "https://us-central1-ambient-net-292105.cloudfunctions.net/face_detect"

import requests

mask_on_message = "Hi! I'm a bot working to keep people safe in the pandemic. It looks to me like you're wearing your mask correctly, keep up the good work!"

mask_off_message = "Hi! I'm a bot working to keep people safe in the pandemic. It looks like an image you've posted shows people who aren't wearing their masks correctly. Check out this link to learn more! https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/how-to-wear-cloth-face-coverings.html"

def process(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request_json["name"] != BOT_NAME:
        for attachment in request_json["attachments"]:
            if attachment["type"] == "image":
                #send image to classifier
                params = {'url': attachment["url"]}
                r = requests.post(MASK_CLASSIFIER_API, json=params)
                mask_exists, mask_correct = r.text.split(",")
                
                if mask_exists == "[True":
                    #send_message("mask on")
                    if mask_correct == "True]":
                        send_message(mask_on_message)
                        #send_message("correctly")
                    else:
                        send_message(mask_off_message)
			#send_message("incorrectly")
                else:
                    pass
                    #send_message("mask off")

                #send_message(attachment["url"])
        #requests.post("https://api.groupme.com/v3/bots/post?bot_id=" + BOT_ID + "&text='" + str(request_json) + "'")
        
    #    send_message("testing")
        
    return f'Recieved'

def send_message(msg):
    requests.post(GROUPME_API + "bot_id=" + BOT_ID + "&text=" + str(msg))
