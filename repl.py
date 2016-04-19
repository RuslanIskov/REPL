#-*- coding:utf-8 -*-

import logging
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s %(message)s', level = logging.DEBUG)

from rplugins import RPlugins
from raliases import RAliases
from winsound import Beep
from configparser import ConfigParser

plugins = RPlugins()
commmands = RAliases()
params = {}
for pluginName in plugins.names:
	commmands.add( plugins[pluginName], [pluginName] )

config = ConfigParser()
config.read('repl.ini', encoding='utf-8' )
for sectionName in config:
	section = config[sectionName]
	if sectionName == 'PluginsAliases':
		section = config[sectionName]
		for pluginName in section:
			if pluginName in plugins:
				commmands.add( plugins[pluginName], section[pluginName].split() )
	else:
		params[sectionName] = RAliases()
		for paramName in section:
			params[sectionName].add( paramName, [paramName] )
			params[sectionName].add( paramName, section[paramName].split() )

PROMPT_PHRASE = ''
PROMPT_SIGN = '>>> '

while True:
	Beep( 2400, 25 )
	inp = input( PROMPT_PHRASE + PROMPT_SIGN )
	inp = inp.strip().lower().split()
	cmd = inp[0]
	args = inp[1:]
	cls, func = None, None
	cls = commmands.get(cmd)
	if not cls:
		print( 'Unknown command: "{0}"'.format(cmd) )
		continue
	if args:
		func_name = args[0]
		args = args[1:]
		func_name = params[cls.name].get(func_name)
	else:
		func_name = 'run'
	if not func_name in cls.methods:
		print('Неизвестный параметр')
		continue
	func = cls[func_name]
	if func:
		ret = func( *args )
	else:
		print( 'Unknown command' )
