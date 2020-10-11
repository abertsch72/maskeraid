
# maskeraid

We all know how frustrating it can be to see people posting photos with their masks worn incorrectly, or walking into stores without masks on at all. It's uncomfortable and awkward to confront someone about their mask-wearing-- so why not have a program do it for you?

This project does just that, using computer vision models to identify whether people are wearing masks and setting this technology to work to improve the way people wear masks in our community. The final models are versatile, highly accurate, and culturally considerate; they correctly identify whether people are wearing masks and wearing them correctly, even on pictures of people with headscarves, hats, sunglasses, piercings, and/or facial tattoos. 

## What it does & how
We trained two Google AutoML Vision models. The first, trained on greyscale photos of people wearing masks and people without masks, identifies whether a person in an image is wearing a mask at all. The second, trained on greyscale and color photos of people wearing masks correctly and incorrectly, identifies whether a person in an image is wearing their mask correctly. Both models are deployed on a Google Cloud project and can be called to make predictions.

From this base, we built out three possible applications:
* **Mask validation for businesses:** This hardware hack asks people to stand in front of a camera briefly, then checks whether they are wearing a mask and display a message on a LCD display, either asking them to put on a mask or telling them they are okay to come in. This raspberry pi-webcam setup is lightweight and could easily be generalized to move a servo motor to unlock a door or play a warning sound, acting as a doorman for small businesses to encourage customers to wear their masks.
* **GroupMe chatbot:** This bot listens in on a GroupMe group, posting whenever someone posts a picture where they are wearing a mask incorrectly. It can be easily customized and installed in different GroupMe groups-- all it needs to run is a Google Cloud Function on a Google Cloud project (or an equivalent server or severless setup), plus access to the model to predict with. The bot comes with careful and detailed documentation for setting up forks that best suit individual groups' needs.
* **Public information campaign for Twitter:** This bot trawls Twitter, looking through popular hashtags for posts where people are wearing masks incorrectly. If it finds a photo of improper mask use, it attempts to direct message the user a short, polite message linking to [information about wearing a mask properly from the CDC](https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/how-to-wear-cloth-face-coverings.html).  If the user does not accept DMs from accounts they do not follow, it will post a reply to the post instead.

Of course, many more applications are possible with this setup-- but the weekend is only so long! maskeraid's  image cropping system and model predictions can easily be put to work for other use cases. 

## Challenges we ran into
The webcam we used for the mask validation is a much better camera than the CCTV cameras that stores commonly have-- and when we tried greyscaling the images, we found our model performance dropped significantly. We duplicated the original training data, producing both color and greyscale versions, and trained a model on both so that the model learned to tell if people were wearing masks without needing to see color in the image.
We also had to adapt the data we sent and received between many different formats as it passed between subsystems. The interactions between APIs, Python libraries, our Google Cloud project, the hardware, and locally hosted code were often complex, requiring careful testing and reformatting.

## Accomplishments that we're proud of
When we designed our training dataset, we took special care to consider people who may be adversely affected by a mask-law-enforcing model that is not trained with them in mind. Specifically, we were concerned about women who wear hijab and people of color, two groups that were severely underrepresented in the "naive" training data found in the first image search results for any query. The extra time we spent collecting a diverse dataset paid off in good performance on pictures of hijabi women, with no observable performance differences based on the ethnicity, race, or head wear of the image subject in any of our data.

## What we learned
This project was an immense crash course in Google Cloud Platform and specifically Google AutoML, which showed surprisingly good performance for training on a relatively small dataset. We gained more experience working with hardware and with social media APIs as well!

## What's next for maskeraid
Some codebase cleanup and refactoring is necessary to more cleanly expose the prediction API. As more test data comes in, the models will likely need to be refined. These applications can be improved for ease of use and efficiency, and more applications can be added to the maskeraid family.

## Full technical details- model training
The model data was collected from two sources: photos solicited from friends and photos gathered from Google and DuckDuckGo image search. The photos solicited from friends typically contained images of the same person, in roughly the same pose, with a mask worn correctly, incorrectly, and not at all. The photos from image search were chosen for diversity in subject: race, gender, age, facial expression, headscarves/hats, facial piercings, and tattoos were all factors considered in this search. 

The dataset was run through OpenCV's face detection model, which creates bounding boxes around each face detected. Bounding boxes with sufficient confidence were scaled up to include more of the ear and chin, and each modified bounded box was cropped out of the image individually. This data was manually cleaned to remove misaligned or incorrect face detection results. This resulted in approximately 140 mask-correct, 75 mask-incorrect, and 400 no-mask images. We then doubled the dataset for the mask-correct vs mask-incorrect task by saving a grey-scaled version of each image as well; this also reduced error on the blurrier, grey-scaled CCTV-style images.

The models were trained with early stopping; the training stopped when it achieved high precision and high recall with the same values for precision and recall. The confidence threshold for the binary classification is adjustable, and we did shift it slightly for the webcam photos to reflect the task: false positives for bad mask-wearing are more detrimental to a business than false negatives, as customers may become quickly frustrated.

We trained three models: first, a color-image-only model to identify whether the face in an image was wearing a mask correctly or incorrectly. This generalized well to identifying faces without any mask at all as incorrect, but performed relatively poorly on grey-scale data. We trained a model on grey-scale data to determine whether faces in images were wearing a mask or not, and this generalized well to color images. Finally, we trained a model on both grey-scale and color data to identify whether a mask in an image is being worn correctly or incorrectly. The last two of these models were the two used in production.

