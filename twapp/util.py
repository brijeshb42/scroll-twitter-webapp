"""
A utility module to simplify tweepy usage from within the flask app
"""
import tweepy
from tweepy import Cursor
import app_settings as cfg

def sort_statuses(statuses):
	length = len(statuses)
	for cnt1 in range(length):
		for cnt2 in range(length-1):
			if statuses[cnt2].retweet_count < statuses[cnt2+1].retweet_count:
				tmp = statuses[cnt2]
				statuses[cnt2] = statuses[cnt2+1]
				statuses[cnt2+1] = tmp
	return statuses

def get_twitter_auth():
	auth = tweepy.OAuthHandler(cfg.TW_API, cfg.TW_SECRET)
	return auth

def get_auth_url():
	auth = get_twitter_auth()
	auth_url = auth.get_authorization_url()
	return [auth_url, auth.request_token.key, auth.request_token.secret]

def get_access_token(token, secret, vfr):
	auth = get_twitter_auth()
	auth.set_request_token(token, secret)
	try:
		auth.get_access_token(vfr)
		auth.get_username()
		return [auth.access_token.key, auth.access_token.secret, auth.username]
	except tweepy.TweepError:
		return []
		raise e

def get_access_auth(key, secret):
	auth = get_twitter_auth()
	auth.set_access_token(key, secret)
	return auth

def get_api(key, secret):
	auth = get_access_auth(key, secret)
	return tweepy.API(auth)

def get_statuses(key, secret, page=1):
	api = get_api(key, secret)
	try:
		statuses = api.home_timeline(page=page, count=100)
		return sort_statuses(statuses)
	except tweepy.TweepError as e:
		return e.message
	# try:
	# 	statuses = []
	# 	for status in Cursor(api.home_timeline).items(200):
	# 		statuses.append(status)
	# 	return sort_statuses(statuses)
	# except tweepy.TweepError as e:
	# 	return e.message

def get_me(key, secret):
	api = get_api(key, secret)
	try:
		user = api.me()
		print(user)
		return user
	except tweepy.TweepError as e:
		return e.message