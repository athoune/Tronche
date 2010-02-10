#!/usr/bin/env python

from bottle import route, run, view, send_file
from collectd import Collectd

__author__ = "mlecarme"
__version__ = "0.1"

collectd = Collectd('collectd/')

@route('/')
@view('index')
def index():
    return ''
@route('domains')
def domain():
	return {'domains': list(collectd.domains)}

@route('domain/:domain')
def sonde(domain):
	return {'sondes': list(collectd.domain(domain).sondes)}

@route('/data/:filename')
def static(filename):
	send_file(filename, root='./data')

run(host='localhost', port=8080)