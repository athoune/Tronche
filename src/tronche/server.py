#!/usr/bin/env python

from wsgiref.simple_server import make_server
from wsgiref.util import request_uri, FileWrapper
from urlparse import urlparse, parse_qs
import json
import os.path
import select
import urllib
from cStringIO import StringIO

__author__ = "mlecarme"
__version__ = "0.1"
