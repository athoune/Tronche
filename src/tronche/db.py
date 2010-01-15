#!/usr/bin/env python

import os
import os.path

from pyrrd.rrd import DataSource, RRA, RRD

class Collectd(object):
	def __init__(self, path):
		self.path = path
		self.domains = {}
		for d in os.listdir(os.path.join(path, 'rrd')):
			self.domains[d] = Domain(os.path.join(path, 'rrd', d))
	def __iter__(self):
		for d in self.domains.keys():
			yield self.domains[d]

class Domain(object):
	def __init__(self, path):
		self.path = path
		self.sondes = {}
		_, self.name = os.path.split(path)
		for s in os.listdir(path):
			self.sondes[s] = Sonde(os.path.join(path, s))
	def __iter__(self):
		for s in self.sondes.keys():
			yield self.sondes[s]

class Sonde(object):
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
	for domain in Collectd('collectd/collectd/'):
		#print domain.sondes
		for r in domain.sondes['load']:
			print r.getData()
