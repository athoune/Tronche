#!/usr/bin/env python
# -*- coding: utf8 -*-

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(name='Tronche',
	version='0.1',
	license='GPL-3',
	description='Visualize collectd data',
	author='Mathieu Lecarme',
	author_email='mathieu@garambrogne.net',
	url='http://github.com/athoune/Tronche',
	packages=['tronche'],
	package_dir={'': 'src/'},
	package_data={'' : ['src/tronche/views/*.*', 'src/tronche/data/*.*']},
	#scripts=['src/toto'],
	install_requires=["pyrrd", "bottle"],
)
