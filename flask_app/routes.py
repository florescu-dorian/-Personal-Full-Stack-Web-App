# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for
from flask import jsonify, copy_current_request_context
#from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from .utils.blockchain.blockchain import Block, Blockchain
from pprint import pprint
import json
import random
import functools
import os
from werkzeug.utils import secure_filename
#from . import socketio
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function


def getUser():
	return db.reversibleEncrypt('decrypt', session['email']) if 'email' in session else 'Unknown'

@app.route('/login')
def login():
    if "email" in session:
        return redirect('/home')
    else:
	    return render_template('login.html', user=getUser())


@app.route('/logout')
def logout():
    session.pop('email', default=None)
    session.pop('nft', default=None)
    return redirect('/')


@app.route('/processlogin', methods = ["POST", "GET"])
def processlogin():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    exists = db.authenticate(form_fields['email'], form_fields['password'])
    if (exists['success'] == 1):
        session['email'] = db.reversibleEncrypt('encrypt', form_fields['email']) 
        session['nft'] = False
        return json.dumps({'success':1})
    else:
        return json.dumps({'success':0})
    


@app.route('/processSignup', methods = ["POST","GET"])
def processSignup():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    created = db.createUser(form_fields['email'], form_fields['password'], 'user')
    if (created['success'] == 1):
        session['email'] = db.reversibleEncrypt('encrypt', form_fields['email'])
        session['nft'] = False
        return json.dumps({'success':1})
    else:
        return json.dumps({'success':0})


#######################################################################################
# MARKETPLACE RELATED
#######################################################################################
@app.route('/sellers', methods=["POST"])
@login_required
def sellers():
    user_id = db.getUserIdfromEmail(getUser())
    if request.method == 'POST':
        if request.form['purpose'] == 'file':
            desc = request.form['desc']
            token = request.form['token']
            file = request.files['file']
            filename = secure_filename(file.filename)
            path = os.path.join("./flask_app/static/main/images", filename)
            file.save(path)
            db.insertRows('nft', columns=['user_id', 'description', 'token', 'file_data'], parameters=[[user_id, desc, token, filename]])
        elif request.form['purpose'] == 'edit':
            desc = request.form['desc']
            token = request.form['token']
            nft_id = request.form['nft_id']
            query = "UPDATE nft SET description = %s, token = %s WHERE nft_id = %s;"
            db.query(query, parameters= [desc, token, nft_id])
    userNFTs = db.getUserNFTs(user_id)
    return render_template('sellers.html', user=getUser(), NFTs=userNFTs)


@app.route('/buyers', methods=["POST"])
@login_required
def buyers():
    user_id = db.getUserIdfromEmail(getUser())
    NFTs = db.getAllNFTs() 
    if request.method == 'POST':
        if request.form['purpose'] == 'buy':
            nft_id = request.form['nft_id']
            print('NFT ID', nft_id)
            left = db.userMAFAMATICS(user_id, nft_id)
            print('LEFT OVER', left)
            if left and left >= 0:
                query = "UPDATE users SET tokens = %s WHERE user_id = %s;"
                db.query(query, parameters= [left, user_id])
                query = "DELETE FROM nft WHERE nft_id = %s;"
                db.query(query, parameters= [nft_id])
                NFTs = db.getAllNFTs() 
    return render_template("buyers.html", user=getUser(), userBalance=db.getUserTokens(user_id), NFTs = NFTs)


"""
@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')

"""
#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	print(db.query('SELECT * FROM users'))
	x = random.choice(['Going through "The Capstone Experience."','Favorite sport is soccer.','I speak two languages.'])
	return render_template('home.html', user=getUser(), fun_fact = x)

@app.route('/<page>')
def route(page):
	return render_template(page, user = getUser())

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	return render_template('resume.html', user=getUser(), resume_data = resume_data)

@app.route('/signup')
def signup():
	return render_template('signup.html')


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

