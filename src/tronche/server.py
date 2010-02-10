#!/usr/bin/env python

from bottle import route, run, view, send_file

__author__ = "mlecarme"
__version__ = "0.1"

@route('/')
@view('index')
def index():
    return ''

@route('/data/:filename')
def static(filename):
	send_file(filename, root='./data')

run(host='localhost', port=8080)