import ez_setup
ez_setup.use_setuptools()

import platform
import sys
from setuptools import setup, find_packages

from redcmd.version import __version__


entry_points = {}
entry_points['console_scripts'] = ['redcmd=redcmd.main:main']

setup(	
	name			= 'redcmd',
	version			= __version__,
	description		= 'A library to manage command line interface for an application.',
	author			= 'Amol Umrale',
	author_email 		= 'babaiscool@gmail.com',
	url			= 'http://pypi.python.org/pypi/redcmd/',
	packages		= find_packages(),
	include_package_data	= True,
	scripts			= ['ez_setup.py'],
	install_requires	= ['redlib>=1.5.6', 'zope.interface'],
	entry_points		= entry_points,
	classifiers		= [
					'Development Status :: 4 - Beta',
					'Environment :: Console',
					'License :: OSI Approved :: MIT License',
					'Natural Language :: English',
					'Operating System :: POSIX :: Linux',
					'Programming Language :: Python :: 2.7',
					'Programming Language :: Python :: 3.4',
					'Topic :: Software Development :: Libraries :: Application Frameworks'
				]
)

