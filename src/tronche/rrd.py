#!/usr/bin/env python

__author__ = "mathieu@garambrogne.net"
__version__ = "0.1"

"""
Simple RRD wrapping for fetching data, when pyrrd is not enough
"""

from datetime import datetime
import os

try:
	import pexpect
	class RRDwrapper(object):
		def __init__(self):
			#LC_NUMERIC=en_US 
			self.spawn = pexpect.spawn('rrdtool -')
		def __call__(self, data):
			self.spawn.sendline(data)
			prems = True
			while True:
				self.spawn.expect('\r\n')
				if prems:
					prems = False
					continue
				line = self.spawn.before
				if line[:3] == 'OK ':
					return
				yield line
	rrd_wrapper = RRDwrapper()
except ImportError:
	from subprocess import Popen, PIPE
	import os
	def rrd_wrapper(command):
		env = os.environ
		env['LC_NUMERIC'] = 'en_US'
		return Popen('rrdtool %s ' % command, env= env, shell=True, stdout=PIPE).stdout

def none_filter(stuff):
	"A dummy filter wich does nothing"
	return stuff

class Query(object):
	"Querying round robin database"
	def __init__(self, consolidation='AVERAGE', resolution=None, start=None,
			end=None, filter=none_filter, column=None):
		self.consolidation = consolidation
		self.resolution = resolution
		self.start = start
		self.end = end
		self.filter = filter
		self.column = column
	def command(self):
		"command line option for 'rrd fetch'"
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
	"Average query"
	return Query('AVERAGE', **args)
def MIN(**args):
	"Min query"
	return Query('MIN', **args)
def MAX(**args):
	"Max query"
	return Query('MAX', **args)
def LAST(**args):
	"Last query"
	return Query('LAST', **args)

class RRD(object):
	"Round robin database"
	def __init__(self, path):
		self.path = path
		self.folder, self.name = os.path.split(path)
	def __repr__(self):
		return "<RRD %s>" % self.path
	def _query(self, command, column=None, filter=none_filter):
		#return Result(Popen('rrdtool fetch %s %s ' % (self.path, command), env= env, shell=True, stdout=PIPE).stdout, column, filter)
		return Result(rrd_wrapper('fetch %s %s' % (self.path, command)), column, filter)
	def fetch(self, *args, **dico):
		"""
r = RRD('toto.rrd')
for ts, value in r.fetch('AVERAGE', resolution=5, start='-5m'):
	print ts, value
"""
		return Query(**dico)(self)
	def info(self):
		info = {
			'ds'  :{},
			'rra' :{}}
		for line in rrd_wrapper('info %s' % self.path):
			k,v = line[:-1].split(' = ')
			if k[:3] == 'ds[':
				d,vv = k.split('.',1)
				kk = d[3:-1]
				if not info['ds'].has_key(kk):
					info['ds'][kk] = {}
				info['ds'][kk][vv] = v
			else:
				if k[:4] == 'rra[':
					r,vv = k.split('.',1)
					info['rra'][int(r[4:-1])] = vv
				else:
					info[k] = v
		return info

def float_or_none(data):
	"Convert a string to a float, or keep it as None"
	if data == None: return None
	else: return float(data)

class Result(object):
	"Querying a round robin database return a Result"
	def __init__(self, raw, column = 0, filter = none_filter):
		self.raw = raw
		self.column = column
		self.filtr = filter
	def __iter__(self):
		cpt = 0
		for line in self.raw:
			cpt += 1
			if cpt > 2:
				ts, values = line.split(': ',1)
				dt = datetime.fromtimestamp(int(ts))
				value = values.split(' ')
				if value == 'nan':
					yield dt,  None
				if self.column != None:
					yield dt, self.filtr(float(value[self.column]))
				else:
					yield dt, self.filtr(map(float_or_none, value))

if __name__ == '__main__':
	import time
	import os
	def query():
		for domain in os.listdir('collectd/rrd/') :
			print domain
			r = RRD('collectd/rrd/%s/load/load.rrd' % domain)
			query = AVERAGE(resolution=10, start='-10m', column=0, filter = lambda data: (1 - data))
			for ts, value in query(r):
				print ts, value
			print "----------------"
			for ts, value in r.fetch('AVERAGE', resolution=5, start='-5m'):
				print ts, value
			print "----------------"
			print list(query(r))[-3]
	def pipe():
		pipe = RRDwrapper()
		for domain in os.listdir('collectd/rrd/') :
			print datetime.fromtimestamp(int(list(pipe('last collectd/rrd/%s/load/load.rrd' % domain))[0]))
			print list(pipe('info collectd/rrd/%s/load/load.rrd' % domain))
	def info():
		for domain in os.listdir('collectd/rrd/') :
			print domain
			r = RRD('collectd/rrd/%s/load/load.rrd' % domain)
			print r.info()['ds'].keys()

	chrono = time.time()
	info()
	print (time.time() -chrono) *1000 , 'ms'