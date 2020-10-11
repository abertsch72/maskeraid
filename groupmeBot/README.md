# groupme bot readme

## Overview
The GroupMe bot lives in a GroupMe group chat and posts after people post pictures. It can be configured to post after any picture of someone with a mask on, whether that's correctly or incorrectly, or to only post when someone posts a picture with a mask worn incorrectly.

## To set up the bot in a new group
Go to the [GroupMe developer website's pages on bots](https://dev.groupme.com/bots) and click "Create Bot." Select the group chat you want it to listen in to and give the bot a name. You can give any photo's url as the avatar image; the one used in the demos is https://i.groupme.com/400x400.jpeg.209a16c4fada4b269c9bbbe471ca252d. 

Now, set up the server-side code. In Google Functions, this is as simple as creating a Python function that allows unauthenticated requests and pasting the code in. Make sure to change the bot name to the name of your bot, and the bot id # to your bot's ID, which you should have on the Developer page. Finally, on the Developer page, edit the bot and paste the function's HTTP request URL in the "Callback URL" field.

You can modify the message text for masks on correctly or masks on incorrectly; you can also disable sending messages for masks on correctly entirely by removing that send_message call.  Have fun and experiment!

