from flask import (Flask, render_template, redirect, url_for, session, request)
import base64, os, requests, urllib
from forms import CreateGroup

app = Flask(__name__)
app.secret_key = "kjsldfbnm,nadf98u3hkjhalsdf@#"
	
APP_KEY = '2h5rdx26ysrykm9'
APP_SECRET = 'c6wbs79qp6nu628'


@app.route("/index")
@app.route("/")
def index():
	return render_template('index.html')


@app.route("/login")
def login():
	csrf_token = base64.urlsafe_b64encode(os.urandom(18))
	session['csrf_token'] = csrf_token
	return redirect('https://www.dropbox.com/1/oauth2/authorize?%s' % urllib.urlencode({
		'client_id' : APP_KEY,
		'redirect_uri' : url_for('callback', _external=True),
		'response_type' : 'code',
		'state' : csrf_token
		}))


@app.route('/callback')
def callback():
	if request.args['state'] != session.pop('csrf_token'):
		abort(403)

	data = requests.post('https://api.dropbox.com/1/oauth2/token',
		data = {
			'code' : request.args['code'],
			'grant_type' : 'authorization_code',
			'redirect_uri' : url_for('callback', _external=True)
		},	
		auth=(APP_KEY, APP_SECRET)
		).json()

	session['token'] = data['access_token']		

	return redirect(url_for('dashboard'))	


@app.route('/dashborad')
def dashboard():
	# info = requests.get('https://api.dropbox.com/1/account/info', headers={'Authorization':'Bearer %s' % session['token']}).json()
	# return 'Login as %s' % info['display_name']
	return render_template('dashboard.html')


@app.route('/create_group', methods=['GET','POST'])
def create_group():
	form = CreateGroup()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('create_group.html', form=form)
		return "group added"

	else:
		return render_template('create_group.html', form=form)

if __name__ == "__main__":
	app.run(host="127.0.0.1", port=1231, debug=True)