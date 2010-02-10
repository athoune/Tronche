#!/usr/bin/env python

import os
import os.path
from datetime import datetime

from pyrrd.rrd import DataSource, RRA, RRD

__author__ = "mathieu@garambrogne.net"
__version__ = "0.1"

"""
Collectd data wrapper
"""

class Collectd(object):
	"Collectd contains domains"
	def __init__(self, path):
		self.path = path
		self.domains = []
		self.domains = os.listdir(os.path.join(path, 'rrd'))
	def __iter__(self):
		for d in self.domains:
			yield Domain(os.path.join(self.path, 'rrd', d))

class Domain(object):
	"Domain contains sondes"
	def __init__(self, path):
		self.path = path
		self.sondes = {}
		_, self.name = os.path.split(path)
		for s in os.listdir(path):
			self.sondes[s] = Sonde(os.path.join(path, s))
	def __iter__(self):
		return iter(self.sondes.values())

class Sonde(object):
	"Sonde contains rrd"
	def __init__(self, path):
		self.path = path
		self.folder, self.name = os.path.split(path)
		self.rrds = []
		for r in os.listdir(path):
			name, ext = os.path.splitext(self.name)
			self.rrds.append(name)
	def rrd(self, key):
		return RRD(os.path.join(self.path, "%s.rrd" % key), mode='r')
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
		for r in domain.sondes['load']:
			attrs = r.getData()
			print "last update", datetime.fromtimestamp(int(attrs["lastupdate"]))
			print "file name", attrs['filename']
			print "step", attrs['step']
			print "ds", len(r.ds)
			print "rra", len(r.rra)
			for ds in r.ds:
				data = ds.getData()
				print data['name'], data.keys()
	print (time.time() -chrono) *1000 , 'ms'
