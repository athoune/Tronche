#!/usr/bin/env python

from subprocess import Popen, PIPE
from datetime import datetime

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
	def execute(self, column = 0):
		buff = 'rrdtool fetch %s %s' % (self.path, self.consolidation)
		if self._resolution != None:
			buff += ' -r %i' % self._resolution
		if self._start != None:
			buff += ' -s %s' % self._start
		if self._end != None:
			buff += ' -e %s' % self._end
		return Result(Popen(buff, shell=True, stdout=PIPE).stdout, column)

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
		"""[FIXME] LC_NUMERIC doesn't works 
		"""
		env = os.environ
		env['LC_NUMERIC'] = 'en_US'
		return Popen('rrdtool fetch %s %s' % (self.path, query), shell=True, env= env, stdout=PIPE).stdout
	def query(self, query):
		query.path = self.path
		return query
class Result(object):
	def __init__(self, raw, column = 0):
		self.raw = raw
		self.column = column
	def __iter__(self):
		cpt = 0
		for line in self.raw:
			cpt += 1
			if cpt > 2:
				ts, values = line[:-1].split(': ',1)
				value = values.split(' ')[self.column]
				if value == 'nan':
					yield (datetime.fromtimestamp(int(ts)),  None)
				else:
					yield (datetime.fromtimestamp(int(ts)), float(value))


if __name__ == '__main__':
	import time
	import os
	chrono = time.time()
	for domain in os.listdir('collectd/collectd/rrd/') :
		print domain
		r = RRD('collectd/collectd/rrd/%s/load/load.rrd' % domain)
		for ts, value in r.query(AVERAGE().resolution(10).start('-10m')).execute(0):
			print ts, value
	print (time.time() -chrono) *1000 , 'ms'