import os
import json

from google.cloud import automl_v1

# 'content' is base-64-encoded image data.
def get_prediction(content, project_id, model_id):
    prediction_client = automl_v1.PredictionServiceClient()

    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    request = prediction_client.predict(name=name, payload=payload)
    return request  # waits till request is returned

def isMaskOnCorrect(imagePath):
    #note: make sure the service account credentials are stored here
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/secrets/credentials.json"
    project_id = "854619995345"
    model_id = "ICN5390476701450895360"

    with open(file_path, 'rb') as ff:
      content = ff.read()

    result = get_prediction(content, project_id, model_id).payload[0].display_name
    if result == "Correct":
        return True
    else:
        return False


if __name__ == '__main__':
    file_path = "testImage.jpg"
    result = isMaskOnCorrect(file_path)
    print(result)