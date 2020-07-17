from flask import Flask,render_template,redirect,url_for,request,flash
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from flask_login import UserMixin,LoginManager,login_user,logout_user,current_user,login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask,render_template
import json
import urllib.request 
app=Flask(__name__)
app.secret_key="1234"

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

@login_manager.user_loader
def load_user(user_id):
	return session.query(Products).get(int(user_id))

@app.route("/home")
def homePage():
	return render_template("home.html")

@app.route("/", methods = ['GET', 'POST'])
def getCity():
	if request.method == 'POST':
		city = request.form['cityName']

		api = "place_your_api_key_here"
		urll = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api
		try:
			source = urllib.request.urlopen(urll).read()
			list_of_data = json.loads(source)
			data = {
				"city": city,
		        "country_code": str(list_of_data['sys']['country']), 
		        "coordinate": str(list_of_data['coord']['lon']) + ' ' 
		                    + str(list_of_data['coord']['lat']), 
		        "temp": str(list_of_data['main']['temp']) + 'k', 
		        "pressure": str(list_of_data['main']['pressure']), 
		        "humidity": str(list_of_data['main']['humidity'])
		    }
		except Exception as e:
			data = "invalid"
		print(data)
		return render_template("index.html", data = data)
	else:
		return render_template("index.html", data = '')

app.run(debug=True)
