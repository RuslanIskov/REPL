#-*- coding:utf-8 -*-

from rplugins import clsBasePlugin

from urllib.request import urlopen
import json

MAIN_CURRENCIES = ['USD','GBP','CAD','AUD','EUR']

class PrivatBank( clsBasePlugin ):
	def run( self, *args ):
		print('ПриватБанк')
		print('-'*40)
		print('usd - карточный курс доллара')
		print('all - карточный курс покупки основных валют')
	def usd( self, *args ):
		try:
			url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
			req = urlopen( url ).readline().decode('UTF-8')
			js = json.loads( req )
			for i in js:
				if i['ccy'] == 'USD':
					print( 'ПриватБанк: курс доллара (карточный)' )
					print( '-'*50 )
					sale, buy = i['sale'], i['buy']
					sale = round( float(  sale), 2 )
					buy = round( float( buy ), 2 )
					print( 'Купить : {:0.2f}'.format( sale ) )
					print( 'Продать: {:0.2f}'.format( buy ) )
			return True
		except:
			print( 'К сожалению что-то пошло не так...' )
			return False
			
	def all( self, *args ):
		try:
			url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=12'
			req = urlopen( url ).readline().decode('UTF-8')
			js = json.loads( req )
			for i in js:
				if i['ccy'] in MAIN_CURRENCIES:
					sale = i['sale']
					sale = round( float(  sale), 2 )
					print( '{0} : {1:0.2f}'.format( i['ccy'], sale ) )
			return True
		except:
			print( 'К сожалению что-то пошло не так...' )
			return False
		
if __name__ == '__main__':
	a = PrivatBank('сороктысячобезъянвжопусунулибанан')
	ret = a.usd()
	
		