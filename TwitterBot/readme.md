# twitter bot readme

## Overview
The Twitter bot messages people who post pictures that show someone wearing their mask incorrectly. If the bot finds such a post, it will first attempt to DM that person, then attempt to reply to the tweet if that fails. If both methods fail, it moves on. 

## To modify
You can change the hashtags the bot looks through by modifying the _tags_to_search_ array, and change the message from the default by editing the _message_ string. For security reasons, you will have to set up your own developer account with your own bot and request auth tokens using the commented-out code; see the [Twitter developer site](https://developer.twitter.com/en/docs) for details.


