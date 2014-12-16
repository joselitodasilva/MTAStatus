from app import app
from urllib.request import urlopen
from xml.etree.ElementTree import parse
from flask import render_template,redirect,request,url_for
from datetime import datetime,timedelta
import html

#global variables
times = list()
times.append({'feedstamp':None, 'lastfetch':datetime.now()})
doc = None 

#function to fetch the feed and create the document object after iterating the xml
def fetch_iterate(service):
	global doc,times
	#if multiple requests occur within the same given seconds interval
	#they'll get the information from the same feed fetched
	#to improve speed and avoid flooding concurrents downloads of the feed
	if datetime.now() > times[0]['lastfetch'] + timedelta(seconds=5): 
		u = urlopen('http://web.mta.info/status/serviceStatus.txt')
		doc = parse(u)
		times[0]['lastfetch'] = datetime.now()
		times[0]['feedstamp'] = doc.find('timestamp').text 
	lines = []
	for line in doc.iterfind(service + '/line'):
		name = line.findtext('name')
		status = line.findtext('status')
		time = line.findtext('Time')
		text = line.findtext('text')
		lines.append({'name':name,'status':status,'time':time,'text':text})
	return(lines)	

#the main form
@app.route('/')
def index():
	return render_template("layout.html")

#if the form is submited, this function will redirect accordingly 
@app.route('/redirect',methods=['POST','GET'])
def redir():
	if request.form['service_chosen'] == "none": 
		return render_template("layout.html")
	return redirect(url_for(request.form['service_chosen']))
	
#routes to the transport services statuses available  
@app.route('/subway')
def subway():
	lines = fetch_iterate('subway')
	return render_template("status.html",title='Subway',lines=lines,timestamp=times[0]['feedstamp'])

@app.route('/bus')
def bus():
	lines = fetch_iterate('bus')
	return render_template("status.html",title='Buses',lines=lines,timestamp=times[0]['feedstamp'])

@app.route('/bt')
def bt():
	lines = fetch_iterate('BT')
	return render_template("status.html",title='BT',lines=lines,timestamp=times[0]['feedstamp'])

@app.route('/lirr')
def lirr():
	lines = fetch_iterate('LIRR')
	return render_template("status.html",title="LIRR",lines=lines,timestamp=times[0]['feedstamp'])

@app.route('/metronorth')
def metronorth():
	lines = fetch_iterate('MetroNorth')
	return render_template("status.html",title="MetroNorth",lines=lines,timestamp=times[0]['feedstamp']) 
