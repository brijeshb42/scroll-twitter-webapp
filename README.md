# Twitter app for Test

## [Goto App](http://rocky-temple-6325.herokuapp.com/)

For usage on your local system:
* clone the repo
* rename ```twapp/app_settings.py.settings``` to ```twapp/app_settings.py```
* open ```twapp/app_settings.py```
* set TW_API to API_KEY and TW_SECRET to API_SECRET from your twwitter application
* set the value of SECRET to any value you like for session encryption
* set the value of PORT to your liking
* now got the root directory
* do ```pip install -r requirements.txt```
* from terminal, run ```python app.py```
* goto ```http://127.0.0.1:PORT```
* make sure that in your twitter application settings, the callback url is set to ```http://127.0.0.1:PORT/callback```