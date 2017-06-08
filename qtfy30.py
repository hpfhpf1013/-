#-*-coding:utf-8-*-
from scrapy.selector import HtmlXPathSelector,XPathSelector
from scrapy.linkextractors import LinkExtractor 
from scrapy.spiders import CrawlSpider, Rule 
from scrapy.http import Request 
from scrapy import log 
import os, os.path 
import re


class Qtfy30Spider(CrawlSpider): 
	name = 'qtfy30' 
	allowed_domains = ['qtfy.cc'] 
	start_urls = ['http://www.qtfy.cc/']
	output_dir = "/data/www/"
	#rules = ( # Rule(SgmlLinkExtractor(allow=r'.html'), callback='parseitem', follow=True), #)
	rules = (
        #Rule(LinkExtractor(allow=('mjxz','ysyl','hjxz','jdyp','page'),deny=('99zhenren','hongyunguoji')), callback='parse_detail', follow=True),
		Rule(LinkExtractor(allow=('mjxz','ysyl','hjxz','jdyp','/page/2','/page/3','/page/4','/page/5','/page/6','/page/7','/page/8','/page/9','/page/10'),deny=('99zhenren','hongyunguoji')), callback='parse_detail', follow=True),
    )
	def parse_start_url(self, response): 
		"""first Request return to fetch start_url""" 
		self.parse_detail(response)
	def parse_detail(self, response):
		self.log('-=-=-=--=-=--=-= %s -=-=-=-=-=-=' % response.url) 
		outputfile = self._rtouch(response.url)
		if not outputfile: 
			self.log('download %s fail' % response.url) 
			return
		response = response.replace(body=response.body.replace('href="http://www.qtfy.cc','href="http://www.mirun.net/dy'))
		response = response.replace(body=response.body.replace("href='http://www.qtfy.cc","href='http://www.mirun.net/dy"))
		response = response.replace(body=response.body.replace("sblue2009@163.com","2391470649@qq.com"))
		response = response.replace(body=response.body.replace("我只有独自悄坐海边，谛听夏风轻吟！","您想看的电影都在这里"))
		response = response.replace(body=response.body.replace("且听风吟","小飞磁链"))
		response = response.replace(body=response.body.replace("且听","小飞磁链"))
		response = response.replace(body=response.body.replace('http://www.qtfy30.cn',"#"))
		response = response.replace(body=response.body.replace(r"http://www.qtfy.cc/wp-content/themes/yzipi/images/logo.png","http://www.mirun.net/dy/wp-content/themes/yzipi/images/logo.png"))
		response = response.replace(body=response.body.replace(r'http://www.qtfy.cc/wp-content/themes/yzipi/images/2014-12-06-1515289049.png','http://www.mirun.net/dy/wp-content/themes/yzipi/images/1490768343.png'))
		response = response.replace(body=response.body.replace(r'</body>','<script type="text/javascript">var cnzz_protocol = (("https:" == document.location.protocol) ? " https://" : " http://");document.write(unescape("%3Cspan id=\'cnzz_stat_icon_1261603918\'%3E%3C/span%3E%3Cscript src=\'" + cnzz_protocol + "s11.cnzz.com/z_stat.php%3Fid%3D1261603918%26show%3Dpic\' type=\'text/javascript\'%3E%3C/script%3E"));</script></body>'))
		response = response.replace(body=re.sub(r'<div id="soutab">([\s\S]*?)</div>',"",response.body))
		response = response.replace(body=re.sub(r'<div class="sitebar_list">([\s]*?)<h4 class="sitebar_title">链接表([\s\S]*?)</div>',"",response.body))
		response = response.replace(body=re.sub(r'<div class="sitebar_list">([\s]*?)<h4 class="sitebar_title">标签云([\s\S]*?)</div>',"",response.body))
		response = response.replace(body=re.sub(r'<div class="sitebar_list">([\s]*?)<h4 class="sitebar_title">最新评论([\s\S]*?)</div>',"",response.body))
		response = response.replace(body=re.sub(r'<div class="sitebar_list">([\s]*?)<h4 class="sitebar_title">文章归档([\s\S]*?)</div>',"",response.body))
		response = response.replace(body=re.sub(r'<form action="http://www.qtfy.cc/wp-comments-post.php"',"#",response.body))
		#response = response.replace(body=re.sub(r"<a href='([\s\S]*?)' class='([\s\S]*?)' title='([\s\S]*?)' style='([\s\S]*?)'>([\s\S]*?)</a>","",response.body))
		response = response.replace(body=re.sub(r'<select .*?></select>',"",response.body))
		#response = response.replace(body=re.sub(r'<script .*?></script>',"",response.body))
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
