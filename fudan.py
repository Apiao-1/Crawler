# coding:utf-8
import re
import requests

class urlManager(object):

	def __init__:
		self.new_urls = set()
		self.old_urls = set()

	def has_new_url (self):
		return len(self.new_urls)!=0

	def get_new_url(self):
		new_url = self.new_urls.pop()

	def add_new_url(self, url):
		if url is None:
			return 
		if url not in self.new_urls and url not in self.old_urls:
			self.new_urls.add(url)

class HtmlDownloader(object):

	def download(self, url):
		if url is None:
			return None
		user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
		headers = {'User_Agent':user_agent}
		r = requests.get(url, headers = headers)
		if r.status_code == 200:#响应状态码
			r.encoding = 'utf-8'
			return r.text
		return None

class HtmlParser(object):

	def parser(self,page_url, html_cont):
		if page_url is None or html_cont is None:
			return 
		new_urls = self._get_new_url(page_url, html_cont)
		new_data = self._get_new_data(page_url, html_cont)
		return new_urls,new_data

	def _get_new_url(self, page_url, html_cont):
		new_urls = set()
		links = html_cont.xpath("//html").extract()[0]  
		trans =re.findall('\'http:.*?\'' ,href_str)
		absolute_url = []
		http_url = []
		for url in trans:
		    http_url.append(re.sub(remove, '', url))
		for url in http_url:
			ext = tldextract.extract(url)
			if '.'.join(ext[1:3]) == 'fudan.edu.cn':
				absolute_url.append(url)
