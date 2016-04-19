#-*- coding:utf-8 -*-

from rplugins import clsBasePlugin
from configparser import ConfigParser

class Help( clsBasePlugin ):
	def run( self ):
		print('Available commands:')
		config = ConfigParser()
		config.read('repl.ini', encoding='utf-8' )
		section = config['PluginsAliases']
		cmds = [plugin for plugin in section]
		print(', '.join(sorted(cmds) ))