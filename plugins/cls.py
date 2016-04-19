#-*- coding:utf-8 -*-

from rplugins import clsBasePlugin
import os

class CLS( clsBasePlugin ):
	def run( self, *args ):
		os.system('cls' if os.name == 'nt' else 'clear')