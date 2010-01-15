#!/usr/bin/env python

import os
import os.path

from pyrrd.rrd import DataSource, RRA, RRD

class Collectd(object):
	def __init__(self, path):
		self.path = path
		self.domains = {}

class Domain(object):
	def __init__(self, path):
		self.path = path
		self.sondes = {}
		for s in os.listdir(path):
			self.sondes[s] = Sonde(os.path.join(path, s))

class Sonde(object):
	def __init__(self, path):
		self.path = path
		self.folder, self.name = os.path.split(path)
		self.rrds = []
		for r in os.listdir(path):
			name, ext = os.path.splitext(path)
			self.rrds.append(name)
	def rrd(self, key):
		return RRD(os.path.join(self.path, "%s.rrd" % key), mode='r')
	def __repr__(self):
		return "<Sonde %s>" %self.name

if __name__ == '__main__':
	d = Domain('collectd/collectd/rrd/localhost.localdomain')
	#print d.sondes
	r = d.sondes['load'].rrd('load')
	print r.getData()
