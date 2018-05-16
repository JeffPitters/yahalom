#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
from app import app, diffie
import requests
import json
from datetime import datetime
key_alice = None
key_bob = None
seanse = None
alice = None
bob = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global key_alice
    global key_bob
    global seanse
    global alice
    global bob
    if key_alice == None and key_bob == None:
        dh()
        flash('Key Alice')
        flash(key_alice)
        flash('Key Bob')
        flash(key_bob)
        return render_template('index.html')
    elif seanse == None:
        flash('Key Alice')
        flash(key_alice)
        flash('Key Bob')
        flash(key_bob)
        flash('Waiting')
        return render_template('index.html')
    else:
        flash('Key Alice')
        flash(key_alice)
        flash('Key Bob')
        flash(key_bob)
        flash('Alice id')
        flash(alice)
        flash('Bob id')
        flash(bob)
        flash('Seanse key')
        flash(seanse)
    return render_template('index.html')

def dh():
    global key_alice
    global key_bob
    t, p, g, T = diffie.start()
    response = requests.post('http://server-alice/dh',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({"p": str(p), "g": str(g), "T": str(T)}))
    buf = json.loads(response.text)
    A = int(buf['A'])
    k = diffie.create_key(A, t, p)
    key_alice = k[0:16].encode('utf-8')
    t, p, g, T = diffie.start()
    response = requests.post('http://server-bob/dh',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({"p": str(p), "g": str(g), "T": str(T)}))
    buf = json.loads(response.text)
    B = int(buf['B'])
    k = diffie.create_key(B, t, p)
    key_bob = k[0:16].encode('utf-8')
    return 0
    

@app.route('/yahalom', methods=['POST'])
def yahalom():
    global seanse
    global key_alice
    global key_bob
    global alice
    global bob
    bob = request.json['id']
    enc = request.json['enc']
    #seanse = diffie.gen()
    seanse = 'SSSSSSSSSSSSSSSS'
    buf = diffie.decrypt(key_bob, enc.encode('utf-8'))
    alice = buf[0:16]
    RaRb = buf[16:]
    buf = seanse+RaRb
    enc = diffie.encrypt(key_alice, buf).decode('utf-8')
    buf = seanse+alice
    text = diffie.encrypt(key_bob, buf).decode('utf-8')
    requests.post('http://server-alice/end',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({"one": enc, "two": text}))
    return 0