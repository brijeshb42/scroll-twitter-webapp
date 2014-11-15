from flask import Flask, render_template, session,\
	request, redirect, url_for
from scraper import scraper_app
import app_settings as cfg
import util
import datetime

"""
Various constants for consistency
"""
REQ_TOKEN = 'request_token'
REQ_SECRET = 'request_secret'

OAUTH_TOKEN = 'oauth_token'
OAUTH_VERIFIER = 'oauth_verifier'

ACCESS_TOKEN = 'access_token'
ACCESS_SECRET = 'access_secret'

USERNAME = 'username'

#App configuration
app = Flask(__name__, static_folder='public', template_folder='templates')
app.register_blueprint(scraper_app, url_prefix='/scrape')
app.secret_key = cfg.SECRET

# statuses1 = [];
# for i in range(30):
# 	status = {'id':i,'entities': {'urls': [{'expanded_url':'https://www.facebook.com'}]}, \
# 	'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sed sapiente quos dignissimos aliquid, pariatur fuga reiciendis? Vel accusamus, nostrum deserunt!', 'created_at': datetime.datetime.now(), 'retweet_count': 10, \
# 	'user': {'screen_name': 'user', 'profile_image_url': '/public/img.jpg'}}
# 	statuses1.append(status)

"""
To check for existing keys in current session and clear them accordingly.
If session is clear, the retrieves twitter authorization url and sets it in session.
"""
#@app.before_request
def before_req():
	if ACCESS_TOKEN in session and ACCESS_SECRET in session and USERNAME:
		return
	if OAUTH_TOKEN in session and session[OAUTH_TOKEN] is not None and \
	 OAUTH_VERIFIER in session and session[OAUTH_VERIFIER] is not None:
		return
	if 'denied' in session and session['denied'] is True:
		auth_data = util.get_auth_url()
		session['oauth_url'] = auth_data[0]
		session[REQ_TOKEN] = auth_data[1]
		session[REQ_SECRET] = auth_data[2]
	else:
		session.pop('denied',None)
	if 'oauth_url' not in session or session['oauth_url'] is '#':
		auth_data = util.get_auth_url()
		session['oauth_url'] = auth_data[0]
		session[REQ_TOKEN] = auth_data[1]
		session[REQ_SECRET] = auth_data[2]

"""
Logs out te user by clearing the session and redirects to index.
"""
@app.route('/logout')
def logout():
	session.clear();
	return redirect(url_for('index'))

"""
Index router, checks whether the user has already authorized the app or not. If not authorized,
presents the user with the link to authorize the app with twitter. If authorized, presents with
a link to see the latest link tweets.
"""
@app.route('/')
def index():
	before_req()
	message = {}
	if 'denied' in session and session['denied'] == True:
		message['type'] = 'error'
		message['message'] = 'You denied the request.'
		session.pop('denied')
	if 'oauth_url' in session:
		return render_template('index.html', title = 'Home', auth_url = session['oauth_url'] or '#',message=message)
	else:
		return render_template('index.html', title = 'Home', message=message)

"""
Callback url to handle authorization response from twitter. If user denied the authorization,
sets a denied key in session to true to show an error message to user. If user authorized 
successfully, gets the access_token and access_secret in background and sets them in session
for further usage.
"""
@app.route('/callback')
def callback():
	denied = request.args.get('denied',None)
	if denied is not None:
		session['denied'] = True
		return redirect(url_for('index'))
	else:
		session['denied'] = False

	oauth_token = request.args.get('oauth_token',None)
	oauth_verifier = request.args.get('oauth_verifier',None)

	if oauth_verifier is not None and oauth_token is not None:
		token = util.get_access_token(session.get(REQ_TOKEN), session.get(REQ_SECRET),\
			oauth_verifier)
		session.clear()
		if len(token) < 3:
			return redirect(url_for('index'))
		session[ACCESS_TOKEN] = token[0]
		session[ACCESS_SECRET] = token[1]
		session[USERNAME] = token[2]
		return redirect(url_for('index'))
	return 'error'

"""
Endpooint to retrieve tweets after successful authorization. 
"""
@app.route('/tweets')
@app.route('/tweets/')
@app.route('/tweets/<int:page>')
def get_tweets(page=1):
	if page > 50:
		return redirect(url_for('get_tweets'))
	if 'oauth_url' in session or ACCESS_TOKEN not in session:
		return redirect(url_for('index'))
	statuses = util.get_statuses(session.get(ACCESS_TOKEN), session.get(ACCESS_SECRET), page)
	#statuses = statuses1
	if type(statuses) is str:
		return render_template('tweets.html', error=statuses, title='Tweets')
	else:
		return render_template('tweets.html', statuses=statuses, title='Tweets', page_num = page)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True,port=cfg.PORT)