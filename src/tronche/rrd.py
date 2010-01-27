#!/usr/bin/env python

from subprocess import Popen, PIPE
from datetime import datetime

def none_filter(stuff):
	return stuff

class Query(object):
	def __init__(self, consolidation='AVERAGE', resolution=None, start=None,
			end=None, filter=none_filter, column=None):
		self.consolidation = consolidation
		self.resolution = resolution
		self.start = start
		self.end = end
		self.filter = filter
		self.column = column
	def command(self):
		buff = self.consolidation
		if self.resolution != None:
			buff += ' -r %i' % self.resolution
		if self.start != None:
			buff += ' -s %s' % self.start
		if self.end != None:
			buff += ' -e %s' % self.end
		return buff
	def __call__(self, rrd):
		return rrd._query(self.command(), self.column, self.filter)

def AVERAGE(**args):
	return Query('AVERAGE', **args)
def MIN(**args):
	return Query('MIN', **args)
def MAX(**args):
	return Query('MAX', **args)
def LAST(**args):
	return Query('LAST', **args)

class RRD(object):
	def __init__(self, path):
		self.path = path
	def _query(self, command, column=None, filter=none_filter):
		env = os.environ
		env['LC_NUMERIC'] = 'en_US'
		return Result(Popen('rrdtool fetch %s %s ' % (self.path, command), env= env, shell=True, stdout=PIPE).stdout, column, filter)
	def query(self, *args, **dico):
		return Query(**dico)(self)

class Result(object):
	def __init__(self, raw, column = 0, filter = none_filter):
		self.raw = raw
		self.column = column
		self.filtr = filter
	def __iter__(self):
		cpt = 0
		for line in self.raw:
			cpt += 1
			if cpt > 2:
				ts, values = line[:-1].split(': ',1)
				value = values.split(' ')
				if value == 'nan':
					yield (datetime.fromtimestamp(int(ts)),  None)
				if self.column != None:
					yield (datetime.fromtimestamp(int(ts)), self.filtr(float(value[self.column])))
				else:
					r= []
					for v in value:
						if v == None:
							r.append(None)
						else:
							r.append(float(v))
					yield (datetime.fromtimestamp(int(ts)), self.filtr(r))


if __name__ == '__main__':
	import time
	import os
	chrono = time.time()
	for domain in os.listdir('collectd/rrd/') :
		print domain
		r = RRD('collectd/rrd/%s/load/load.rrd' % domain)
		query = AVERAGE(resolution=10, start='-10m', column=0, filter = lambda data: (1 - data))
		for ts, value in query(r):
			print ts, value
		print "----------------"
		for ts, value in r.query('AVERAGE', resolution=5, start='-5m'):
			print ts, value
		print "----------------"
		print list(query(r))[-3]
	print (time.time() -chrono) *1000 , 'ms'