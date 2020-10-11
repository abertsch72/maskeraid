import requests
import time
import tweepy
import os
#from MaskClassifierClient import isMaskOn, isMaskOnCorrect

message = "Hi! I'm a bot working to keep people safe in the pandemic. It looks like an image you've posted shows " \
          "people who aren't wearing their masks correctly. Check out this link to learn more! " \
          "https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/how-to-wear-cloth-face-coverings.html"

tags_to_search = ["%23pictures", "hanging out", "hangout", "friends", "pals", "missed you", "sorority", "fraternity",
                  "alpha phi", "rush week", "%23college", "greek life", "%23gogreek", "weekend", "beautiful day",
                  "%23optoutside", "night out", "Friday night", "bar crawl", "pub crawl", "%23TGIF", "hosting"]

from TwitterBot.secrets import *

"""
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
"""
while i <= 0:

    result = api.search(tags_to_search[i], lang="en", result_type="recent", count="1", include_entities=True)

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
            print(username)
            print(r._json)

            for image in images:
                print(image.get('media_url'))
                if False:
                    try:
                        pass
                        #api.send_direct_message(userid, message)
                    except tweepy.TweepError:
                        pass
                        #api.update_status("@" + username + " " + message)



    i = (i + 1) % len(tags_to_search)
"""

username = "abertsch72"
statusid = "1079468144710672384"

api.update_status(status="@" + username + " " + message, in_reply_to_status_id=statusid)

#api.send_direct_message("2780950260", message)
