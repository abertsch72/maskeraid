import requests
import time
import tweepy

from TwitterBot.secrets import *

message = "Hi! I'm a bot working to keep people safe in the pandemic. It looks like an image you've posted shows " \
          "people who aren't wearing their masks correctly. Check out this link to learn more! " \
          "https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/how-to-wear-cloth-face-coverings.html"

# add to these to search more of Twitter! :)
tags_to_search = ["%23pictures", "hanging out", "hangout", "friends", "pals", "missed you", "sorority", "fraternity",
                  "alpha phi", "rush week", "%23college", "greek life", "%23gogreek", "weekend", "beautiful day",
                  "%23optoutside", "night out", "Friday night", "bar crawl", "pub crawl", "%23TGIF", "hosting"]

"""
# to get token if not already saved to secrets.py:
try:
    redirect_url = auth.get_authorization_url()
    print(redirect_url)

except tweepy.TweepError:
    print('Error! Failed to get request token.')

verifier = input('Verifier:')
auth.get_access_token(verifier)
print(auth.access_token)
print(auth.access_token_secret)
"""

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
i = 0
total = 0

while True:

    result = api.search(tags_to_search[i], lang="en", result_type="recent", count="50", include_entities=True)
    total += result.count
    for r in result:
        userid = r.author.id_str
        username = r.author.screen_name
        statusid = r.id
        try:
            images = r.extended_entities.get('media')
        except:
            images = r.entities.get('media', [])
        if len(images) > 0:
            userid = r.author.id_str
            username = r.author

            for image in images:
                params = {'url': image.get('media_url')}
                url = "https://us-central1-ambient-net-292105.cloudfunctions.net/face_detect"
                r = requests.post(url, json=params)
                mask_exists, mask_correct = r.text.split(",")
                if mask_exists == "[True" and mask_correct == "False]":
                    print("GOING TO SEND MESSAGE!")
                    try:
                        api.send_direct_message(userid, message)
                        print("message sent to " + userid + " about tweet " + str(statusid))
                    except tweepy.TweepError as e:
                        print(e)
                        try:
                            api.update_status(status="@" + username + " " + message, in_reply_to_status_id=statusid)
                            print("reply tweet sent to " + userid + " about tweet " + str(statusid))
                        except tweepy.TweepError as e1:
                            # already tweeted at this person!
                            print(e1)
                            print("NO message sent to " + userid + " about tweet " + str(statusid))

    print("finished tag " + tags_to_search[i])
    i = (i + 1) % len(tags_to_search)
    if(i == 0):
        time.sleep(1000)

    if total > 100000: # rate limit at least a little
        break
