#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
from app import app, diffie
import requests
import json
from datetime import datetime
key = None
ident = None
Ra = None
seanse = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global key
    global ident
    global seanse
    global Ra
    if key == None:
        return render_template('index.html')
    else:
        if seanse == None:
            if ident == None:
                return redirect(url_for('yahalom', _external=True))
            else:
                flash('Key Alice and Trent')
                flash(key)
                flash('Identificator')
                flash(ident)
                flash('Waiting')
                return render_template('index.html')
        else:
            flash('Identificator')
            flash(ident)
            flash('Ra')
            flash(Ra)
            flash('seanse key')
            flash(seanse)
            return render_template('index.html')

@app.route('/dh', methods=['POST'])
def dh():
    global key
    p = int(request.json['p'])
    g = int(request.json['g'])
    T = int(request.json['T'])
    a, A = diffie.start(p, g)
    k = diffie.create_key(T, a, p)
    key = k[0:16].encode('utf-8')
    return jsonify({"A": str(A)})

@app.route('/yahalom', methods=['GET'])
def yahalom():
    global Ra
    global key
    global ident
    #ident = diffie.gen()
    #Ra = diffie.gen()
    ident = 'aaaaaaaaaaaaaaaa'
    Ra = 'AAAAAAAAAAAAAAAA'
    requests.post('http://server-bob/yahalom',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({"id": ident, "Ra": Ra}))
    return redirect(url_for('index', _external=True))

@app.route('/end', methods=['POST'])
def end():
    global Ra
    global seanse
    global key
    msg = request.json['one']
    buf = diffie.decrypt(key, msg.encode('utf-8'))
    if buf[16:32] == Ra:
        seanse = buf[0:16]
        text = diffie.encrypt(seanse.encode('utf-8'), buf[32:]).decode('utf-8')
        msg = request.json['two']
        requests.post('http://server-bob/end',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({"one": msg, "two": text}))
    return 0
