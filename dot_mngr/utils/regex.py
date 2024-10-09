from dot_mngr import *

RE_FILTER_VERSION = [
	"latest", "doc", "docs", "minimal"
	# "x86", "aarch64", "powerpc64le", "i686"
]

class Regex():
	def __init__(self):
		self.re_quote = r'["\']'
		self.re_href = r'.*[hH][rR][eE][fF]=' + self.re_quote

		self.re_filter_version = RE_FILTER_VERSION
		self.re_filter_version = ''.join([
			r'(?!' + re + r')'
			for re in self.re_filter_version
		])

		self.re_filter_version_behind = RE_FILTER_VERSION
		self.re_filter_version_behind = ''.join([
			r'(?<!' + re + r')'
			for re in self.re_filter_version_behind
		])

		self.re_http = r'https?://'
		self.re_not_dot = r'(?:../)?'

		d = r"\d{2}"
		b = r"[A-Z][a-z]{2}"
		Y = r"\d{4}"
		H = r"\d{2}"
		M = r"\d{2}"
		S = r"\d{2}"
		self.re_date_1 = f"{d}-{b}-{Y} {H}:{M}"
		self.re_date_2 = f"{Y}-{b}-{d} {H}:{M}:{S}"

		self.version = re.compile(r'v?(\d+(?:\.\d+)*)')
		self.github_tag = re.compile(r'archive/refs/tags/[^/]+\.tar\.gz')
		self.url_parent_dir = re.compile(self.re_http + r'.*/(?:.*?)/')
		self.url_parent = re.compile(r'(' + self.re_http + r'.*)/(?:.*?\.(html|php))')

		self.href_dir = re.compile(
			self.re_href + self.re_not_dot + r'(.*?' +
			self.re_filter_version + r'.*?)/".*'
		)
		self.archive_dir = re.compile(r'(.*?)/.*?')
		self.ransi = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
		# self.ransi = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

		self.cs_no_slash = r"[a-zA-Z0-9\_\-\.]+"

		self.re_fver = self.re_filter_version + self.cs_no_slash + self.re_filter_version_behind

	def href(self, pack, html):
		try:
			return re.findall(
				self.re_href + self.re_not_dot + r'(.*?' + re.escape(pack.prefix) +
				self.re_fver + re.escape(pack.suffix) + r')' +
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
				self.re_href + self.re_not_dot + r'(.*?' +
				re.escape(pack.prefix) + self.re_fver + re.escape(pack.suffix) +
				r')/download' + self.re_quote + r'.*', html
			)
		except TypeError:
			return []

	def is_package_url(self, pack, url):
		try:
			return re.match(
				self.re_http + r'.*?' +
				re.escape(pack.prefix) + self.re_fver + re.escape(pack.suffix) +
				r'$', url
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
