from scrapy.selector import HtmlXPathSelector,XPathSelector
from scrapy.contrib.linkextractors import LinkExtractor 
from scrapy.spiders import CrawlSpider, Rule 
from scrapy.http import Request 
from scrapy import log 
import os, os.path 

from dianying.items import DianyingItem


class Bt1280Spider(CrawlSpider): 
	name = 'bt1280' 
	allowed_domains = ['bt1280.cn'] 
	start_urls = ['http://www.bt1280.cn/']
	output_dir = "./"
	#rules = ( # Rule(SgmlLinkExtractor(allow=r'.html'), callback='parseitem', follow=True), #)
	rules = (
        Rule(LinkExtractor(allow=(r'.html','/page/')), callback='parse_detail', follow=True),
    )
	def _init(self,start_url,args,*kwargs): 
		super(Bt1280Spider, self).__init(args, *kwargs) 
		self.start_urls = [] 
		self.start_urls.append('http://www.bt1280.cn/') 
		self.output_dir = self.output_dir
		self.allowed_domains = map(self._get_domain, self.start_urls) 
	
	def _get_domain(self, url): 
		first_dot = url.find('.') 
		if -1 == first_dot: 
			return None 
		first_slash = url.find('/', first_dot + 1) 
		if -1 == first_slash: 
			return url[first_dot + 1:] 
		return url[first_dot + 1: first_slash] 

	#def parse(self, response): 
		"""first Request return to fetch start_url""" 
		#self.parse_detail(response) 
		#yield Request(response.url, callback = self.parse_item)
	def errback(self,response):
		self.log('errback................')
		
	def parse_item(self, response): 
		self.log('-=-=-=--=-=--=-= %s -=-=-=-=-=-=' % response.url) 
		page_links = SgmlLinkExtractor(allow=(r'.html','/page/')).extract_links(response) 
		""" iterate two times for BFS; one for DFS""" 
		for link in page_links: 
			yield Request(link.url, callback = self.parse_detail)
		#for link in page_links: 
			#yield Request(link.url, callback = self.parse_item)
			#self.log('++++++++++++++ %s +++++++++++' % link.url) 

	def parse_detail(self, response):
		self.log('-=-=-=--=-=--=-= %s -=-=-=-=-=-=' % response.url) 
		outputfile = self._rtouch(response.url)
		if not outputfile: 
			self.log('download %s fail' % response.url) 
			return
		response = response.replace(body=response.body.replace('www.bt1280.cn','42.96.175.169/www.bt1280.cn'))  
		#response = response.body.replace('www.bt1280.cn','42.96.175.169/www.bt1280.cn')
		with open(outputfile, 'w') as f:f.write(response.body)
		self.log('download file: %s' % outputfile)

	def _rtouch(self, filepath):
		pos = filepath.find('://')
		if -1 != pos: 
			filepath = filepath[pos + 3:] 
		if ".html" != filepath[-5:]: 
			filepath += "/index.html" 
		opath = os.path.abspath(self.output_dir + "/" + filepath) 
		basedir = os.path.dirname(opath) 
		if not os.path.exists(basedir): 
			try: os.makedirs(basedir) 
			except Exception, msg: 
				self.log('++++++++++++++++++%s' % msg); 
				return None 
		return opath
