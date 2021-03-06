#!/usr/bin/env python

import os
import os.path
from datetime import datetime

from rrd import RRD
__author__ = "mathieu@garambrogne.net"
__version__ = "0.1"

"""
Collectd data wrapper
"""

class Collectd(object):
	"Collectd contains domains"
	def __init__(self, path):
		self.path = path
		self.domains = os.listdir(os.path.join(path, 'rrd'))
	def domain(self, d):
		return Domain(os.path.join(self.path, 'rrd', d))
	def __iter__(self):
		for d in self.domains:
			yield self.domain(d)

class Domain(object):
	"Domain contains sondes"
	def __init__(self, path):
		self.path = path
		_, self.name = os.path.split(path)
		self.sondes = os.listdir(path)
	def sonde(self, s):
		return Sonde(os.path.join(self.path, s))
	def __iter__(self):
		for s in self.sondes:
			yield self.sonde(s)

class Sonde(object):
	"Sonde contains rrd"
	def __init__(self, path):
		self.path = path
		self.folder, self.name = os.path.split(path)
		self.rrds = []
		for r in os.listdir(path):
			name, ext = os.path.splitext(r)
			self.rrds.append(name)
	def rrd(self, key):
		return RRD(os.path.join(self.path, "%s.rrd" % key))
	def __repr__(self):
		return "<Sonde %s>" %self.name
	def __iter__(self):
		for r in self.rrds:
			yield self.rrd(r)

if __name__ == '__main__':
	import time
	chrono = time.time()
	for domain in Collectd('collectd/'):
		#print domain.sondes
		for r in domain.sonde('apache'):
			attrs = r.info()
			print attrs
			print
			"""
			print "last update", datetime.fromtimestamp(int(attrs["lastupdate"]))
			print "file name", attrs['filename']
			print "step", attrs['step']
			print "ds", len(r.ds)
			print "rra", len(r.rra)
			for ds in r.ds:
				data = ds.getData()
				print data['name'], data.keys()
			"""
	print (time.time() -chrono) *1000 , 'ms'
