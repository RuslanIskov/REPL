#-*- coding:utf-8 -*-

from rplugins import clsBasePlugin
from os import _exit

class Exit( clsBasePlugin ):
	def run( self, *args ):
		_exit(0)