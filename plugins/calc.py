#-*- coding:utf-8 -*-

from rplugins import clsBasePlugin

class Calc( clsBasePlugin ):
	def run( self, *args ):
		if args:
			print( eval(args[0]) )
		else:
			print('Простой калькулятор')
			print('Использование: calc <выражение>')