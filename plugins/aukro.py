#-*- coding:utf-8 -*-

from rplugins import clsBasePlugin
import lxml.html as html
import re
import os
import time
import jinja2

class AukroPlugin( clsBasePlugin ):
	def __init__(self, *args):
		clsBasePlugin.__init__(self, *args)
		self._aukro = Aukro('39423847')
	def dubs( self, *args ):
		dubs = self._aukro.GetDubs()	
	def totals( self, *args ):
		self._aukro.GetStats()
	def user( self, *args ):
		try:
			user = args[0].lower()
		except:
			print('Укажите пользователя')
			return
		if user in ['rgbw']:
			self._aukro = Aukro('39423847')
			print('Done')
		else:
			print("Такого пользователя нет")
	def run(self, *args):
		print('Работаем с Аукро')
		print('-'*40)
		print('dubs - находим дубликаты лотов')
		print('totals - количество лотов на продаже и их стоимость')

class Aukro(object):
	def __init__(self, user_id):
		self._user_id = user_id
		self._url = 'http://aukro.ua/listing/user/listing.php?limit=180&us_id=' + user_id
	def reload(self):
		self._page = html.parse(self._url)
		self._items_list = []
		items = self._page.xpath(".//*/article")
		dubs_dict = {}
		for item in items:
			it = {}
			tag_a = item.xpath(".//h2/a")[0]
			it['title'] = tag_a.text_content()
			it['link'] = 'http://aukro.ua' + tag_a.attrib['href']
			tag_photo = item.xpath(".//*[@class='photo']")[0]
			imgs = eval( tag_photo.attrib['data-img'] )
			it['img-link'] = imgs[0][1]
			tag_buy = item.xpath(".//*[@class='buy-now dist']")
			if tag_buy:
				tag_buy = tag_buy[0]
				it['price'] = tag_buy.text_content()[17:-6]
			else:
				it['price'] = ''
			tag_amount = item.xpath(".//*[@class='amount']/span/strong")[0]
			it['amount'] = tag_amount.text_content()
			it['number'] = re.findall( 'i\d+', it['link'] )[0][1:]
			self._items_list.append(it)
	def GetDubs(self):
		self.reload()
		dubs_dict = {}
		for item in self._items_list:
			if item['title'] in dubs_dict:
				dubs_dict[item['title']].append(item)
			else:
				dubs_dict[item['title']] = [item]
		self._dubs_dict = {key:dubs_dict[key] for key in dubs_dict if len( dubs_dict[key] ) > 1}
		# ---
		curr_dir = os.path.dirname(__file__)
		tt = open(curr_dir + '\\aukro\\aukro_dubs.jinja').read()
		tmpl = jinja2.Template(tt)
		dubs_html = tmpl.render(dubs_dict = self._dubs_dict)
		out_file = open('aukro_dubs.html','w', encoding = 'utf-8')
		out_file.write(dubs_html)
		out_file.close()
		os.startfile('aukro_dubs.html')
		time.sleep(5)
		os.remove('aukro_dubs.html')
		
	def GetStats(self):
		self.reload()
		total_sum = 0
		total_positions = 0
		for item in self._items_list:
			total_positions += 1
			price = item['price']
			if price:
				price = price.replace(',','.')
				price = float(price)
			else:
				price = 0.0
			amount = item['amount']
			amount = int(amount)
			total_sum += price * amount
				
		print("Обработано позиций:", total_positions)
		print("Всего товаров на сумму:", total_sum)