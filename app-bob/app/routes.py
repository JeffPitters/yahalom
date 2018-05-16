#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
from app import app, diffie
import requests
import json
from datetime import datetime
key = None
ident = None
Rb = None
seanse = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global key
    global Rb
    global ident
    global seanse
    if key == None:
        return render_template('index.html')
    elif seanse == None:
        flash('Key Bob and Trent')
        flash(key)
        flash('Waiting')
        return render_template('index.html')
    else:
        flash('Identificator')
        flash(ident)
        flash('Rb')
        flash(Rb)
        flash('seanse key')
        flash(seanse)
        return render_template('index.html')

@app.route('/dh', methods=['POST'])
def dh():
    global key
    p = int(request.json['p'])
    g = int(request.json['g'])
    T = int(request.json['T'])
    b, B = diffie.start(p, g)
    k = diffie.create_key(T, b, p)
    key = k[0:16].encode('utf-8')
    return jsonify({"B": str(B)})

@app.route('/yahalom', methods=['POST'])
def yahalom():
    global Rb
    global ident
    global key
    #ident = diffie.gen()
    #Rb = diffie.gen()
    ident = 'bbbbbbbbbbbbbbbb'
    Rb = 'BBBBBBBBBBBBBBBB'
    alice_ident = request.json['id']
    Ra = request.json['Ra']
    msg = alice_ident+Ra+Rb
    enc = diffie.encrypt(key, msg).decode('utf-8')
    requests.post('http://server-trent/yahalom',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({"id": ident, "enc": enc}))
    return 0

@app.route('/end', methods=['POST'])
def end():
    global seanse
    global key
    global Rb
    msg = request.json['one']
    buf = diffie.decrypt(key, msg.encode('utf-8'))
    seanse = buf[0:16]
    text = diffie.decrypt(seanse.encode('utf-8'), request.json['two'])
    #if text[0:16] == Rb
    return 0