#!/usr/bin/env python

from subprocess import Popen, PIPE

class Query(object):
	def __init__(self, consolidation, path):
		self.consolidation = consolidation
		self.path = path
		self._resolution = None
		self._start = None
		self._end = None
	def resolution(self, resolution):
		self._resolution = resolution
		return self
	def start(self, start):
		self._start = start
		return self
	def end(self, end):
		self._end = end
		return self
	def execute(self):
		buff = 'rrdtool fetch %s %s' % (self.path, self.consolidation)
		if self._resolution != None:
			buff += ' -r %i' % self._resolution
		if self._start != None:
			buff += ' -s %s' % self._start
		if self._end != None:
			buff += ' -e %s' % self._end
		return Popen(buff, shell=True, stdout=PIPE).stdout

def AVERAGE(path = None):
	return Query('AVERAGE', path)
def MIN(path):
	return Query('MIN', path)
def MAX(path):
	return Query('MAX', path)
def LAST(path):
	return Query('LAST', path)

class RRD(object):
	def __init__(self, path):
		self.path = path
	def fetch(self, query):
		return Popen('rrdtool fetch %s %s' % (self.path, query), shell=True, stdout=PIPE).stdout
	def query(self, query):
		query.path = path
		return query

if __name__ == '__main__':
	import time
	chrono = time.time()
	r = RRD('collectd/collectd/rrd/localhost.localdomain/load/load.rrd')
	#print r.fetch(' AVERAGE -r 10 -s -10m').read()
	path = 'collectd/collectd/rrd/localhost.localdomain/load/load.rrd'
	for line in r.query(AVERAGE().resolution(10).start('-10m')).execute():
		print line
	print (time.time() -chrono) *1000 , 'ms'
	