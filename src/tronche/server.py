#!/usr/bin/env python

from datetime import datetime

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

@route('domain/:domain/all')
def all(domain):
	tas = {}
	for sonde in collectd.domain(domain):
		tas[sonde.name] = []
		for rrd in sonde:
			print rrd
			tas[sonde.name].append({rrd.name: rrd.info()['ds'].keys()})
	return tas

@route('domain/:domain')
def sonde(domain):
	return {'sondes': list(collectd.domain(domain).sondes)}

@route('rrd/:domain/:sonde/:rrd')
def rrd(domain, sonde, rrd):
	r = collectd.domain(domain).sonde(sonde).rrd(rrd)
	attrs = r.getData()
	return {
		"last update": attrs["lastupdate"],
		"file name": attrs['filename'],
		"step": attrs['step'],
		"ds": len(r.ds),
		"rra": len(r.rra)
	}

"""
@route('rrd/:domain/:sonde/:rrd/:method/:resolution/:start')
def query(domain, sonde, rrd, method, resolution, start):
"""

@route('/data/:filename')
def static(filename):
	send_file(filename, root='./data')

run(host='localhost', port=8080)