#!/usr/bin/python
from flask import Flask
from app import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)