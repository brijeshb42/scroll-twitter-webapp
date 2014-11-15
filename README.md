# Twitter app for Test

## [Goto App](http://rocky-temple-6325.herokuapp.com/)

Initially, the web app presents the user with a link to authorize the app via twitter.

If the user denies authorization, an error message is shown and the authorization url is again shown.

If the authorization is granted, a link to fetch the latest tweets with links is presented to the user.

When the user goes to the link, all the latest tweets of the user's followers are shown sorted by the number of retweets on that particular page.

A ```Next``` link is also presented to fetch the next set of tweets.

Every tweet has a link beside its content in the form of ```[#]```.

On clicking this ```[#]```, the title and description of the link in the tweet is fetched from the server via an ajax call and shown below that particular tweet.

For usage on your local system:
* clone the repo
* rename ```twapp/app_settings.py.settings``` to ```twapp/app_settings.py```
* open ```twapp/app_settings.py```
* set TW_API to API_KEY and TW_SECRET to API_SECRET from your twitter application
* set the value of SECRET to any value you like for session encryption
* set the value of PORT to your liking
* now got the root directory
* do ```pip install -r requirements.txt```
* from terminal, run ```python app.py```
* goto ```http://127.0.0.1:PORT```
* make sure that in your twitter application settings, the callback url is set to ```http://127.0.0.1:PORT/callback```