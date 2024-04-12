import re

class Regex():

	def __init__(self):
		self.re_quote = r'["\']'
		self.re_href = r'.*[hH][rR][eE][fF]=' + self.re_quote
		self.re_filter_version = r'(?!latest)'
		self.re_http = r'https?://'
		self.re_not_dot = r'(?:../)?'
		self.re_date_1 = r'\d{2}-[a-zA-Z]{3}-\d{4} \d{2}:\d{2}'
		self.re_date_2 = r'\d{4}-[a-zA-Z]{3}-\d{2} \d{2}:\d{2}:\d{2}'

		self.version = re.compile(r'v?(\d+(?:\.\d+)*)')
		self.github_tag = re.compile(r'archive/refs/tags/[^/]+\.tar\.gz')
		self.url_parent_dir = re.compile(self.re_http + r'.*/(?:.*?)/')
		self.url_parent = re.compile(r'(' + self.re_http + r'.*)/(?:.*?\.(html|php))')

		self.href_dir = re.compile(
			self.re_href + self.re_not_dot + r'(.*?' +
			self.re_filter_version + r'.*?)/".*'
		)

	def href(self, pack, html):
		try:
			return re.findall(
				self.re_href + self.re_not_dot + r'(.*?' + re.escape(pack.prefix) +
				self.re_filter_version + r'.*?' + re.escape(pack.suffix) + r')' +
				self.re_quote + r'.*'
				, html
			)
		except TypeError:
			return []

	def href_date(self, value, html):
		try:
			return re.findall(
				re.escape(value) + r'.*?(' + self.re_date_1 + r').*?|' +
				re.escape(value) + r'.*?(' + self.re_date_2 + r').*?'
				, html
			)
		except TypeError:
			return []

	def href_sourceforge(self, pack, html):
		try:
			return re.findall(
				self.re_href + self.re_not_dot + r'(.*?' + re.escape(pack.prefix) +
				self.re_filter_version + r'.*?' +
				re.escape(pack.suffix) + r')/download' + self.re_quote + r'.*'
				, html
			)
		except TypeError:
			return []

	def is_package_url(self, pack, url):
		try:
			return re.match(
				self.re_http + r'.*?' + re.escape(pack.prefix) + r'.*?' +
				re.escape(pack.suffix) + r'$',
				url
			)
		except TypeError:
			return []

	def url_version(self, pack, url):
		try:
			res = re.findall(
				r'.*' + re.escape(pack.prefix) + r'v?(.+?)' +
				re.escape(pack.suffix), url
			)
		except TypeError:
			return []

		if len(res) > 0:
			return res[0]
		return None

regex = Regex()
