import json
from urllib.request import Request
from urllib.parse import urlparse

from datetime import datetime

from pprint import pprint

from dot_mngr import ENV
from dot_mngr import p, r, url_handler


class Scrap():
	def __init__(self):
		self.scrap_func = list()

		for key in Scrap.__dict__.keys():
			if key.startswith("scrap_"):
				self.scrap_func.append(key)

	def latest_link(self, package):
		ptype = package.type

		if "scrap_" + package.type in self.scrap_func:
			return Scrap.__dict__["scrap_" + package.type](self, package)
		else:
			p.warn(f"Scrap function not found for {package.name}, "
				+ package.type)

		return (None, None)

	def post_scrap_url(self, package, scrapped):
		if len(scrapped) == 0:
			return None
		if scrapped[0].startswith("https"):
			new_url = scrapped[0]
		else:
			m = r.url_parent.match(package.value)
			if m:
				new_url = f"{m.group(1)}/{scrapped[0]}"
			else:
				new_url = f"{package.value}/{scrapped[0]}"
		return new_url

	def post_scrap(self, package, scrapped):
		return self.post_scrap_version(
			package, self.post_scrap_url(package, scrapped)
		)

	def post_scrap_version(self, package, new_url):
		return (new_url, r.url_version(package, new_url))

	def post_scrap_github_tag(self, new_url, scrapped):
		version = r.version.findall(scrapped)

		if len(version) == 0:
			return (new_url, None)

		return (new_url, version[0])

	def scrap_apache(self, package):
		return self.scrap_website(package, f"{package.value}/?C=M&O=D")

	def scrap_apache_dir(self, package):
		html = url_handler.req(Request(package.value + "/?C=M&O=D"))
		scrapped = r.href_dir.findall(html)

		# 2 because of the parent directory
		if len(scrapped) < 2:
			return (None, None)

		scrapped.pop(0)

		if len(scrapped) == 0:
			return None
		if scrapped[0].startswith("https"):
			new_url = scrapped[0]
		else:
			new_url = f"{package.value}/{scrapped[0]}/"
			version = r.version.findall(new_url)
			if len(version) == 0:
				return (None, None)
			new_url += f"{package.prefix}{version[0]}{package.suffix}"
		return self.post_scrap_version(package, new_url)

	def scrap_apache_no_sort(self, package):
		html = url_handler.req(Request(package.value))
		scrapped = r.href(package, html)

		if len(scrapped) == 0:
			return (None, None)

		result = {}

		for scrap in scrapped:
			date = r.href_date(scrap, html)
			if len(date) > 0:
				if len(date[0][0]) > 0:
					ts = int(datetime.strptime(date[0][0], "%d-%b-%Y %H:%M").timestamp())
					result[ts] = scrap
				elif len(date[0][1]) > 0:
					ts = int(datetime.strptime(date[0][1], "%Y-%b-%d %H:%M:%S").timestamp())
					result[ts] = scrap

		new_url = None
		for k, v in sorted(result.items(), reverse=True):
			new_url = f"{package.value}/{v}"
			break

		return self.post_scrap_version(package, new_url)

	def scrap_github(self, package):
		req = Request(
			f"https://api.github.com/repos/{package.value}/releases/latest"
		)
		if ENV["GITHUB_PAT"]:
			req.add_header("Authorization", f"Bearer {ENV["GITHUB_PAT"]}")
		html = url_handler.req(req)
		tmp = json.loads(html)

		new_url = None
		for assets in tmp["assets"]:
			if r.is_package_url(package, assets["browser_download_url"]):
				new_url = assets["browser_download_url"]

		if not new_url:
			return (None, None)

		return self.post_scrap_version(package, new_url)

	def scrap_gitlab(self, package):
		url = urlparse(package.value)
		data = """{
			"operationName":"allReleases",
			"variables": {
				"fullPath":\"""" + url.path[1:] + """",
				"first":1,
				"sort":"RELEASED_AT_DESC"
			},
			"query":"query allReleases($fullPath:ID!,$first:Int,$last:Int,$before:String,$after:String,$sort:ReleaseSort){project(fullPath:$fullPath) {releases(first:$first last:$last before:$before after:$after sort:$sort){nodes{...Release}}}}fragment Release on Release{assets{sources{ nodes{url}}}}"}
		"""
		req = Request(
			f"{url.scheme}://{url.netloc}/api/graphql",
			data=data.encode("utf-8"),
			method="POST",
			headers={
				"Content-Type": "application/json"
			}
		)

		html = url_handler.req(req)
		html = json.loads(html)

		new_url = None
		for assets in html["data"]["project"]["releases"]["nodes"][0]["assets"]["sources"]["nodes"]:
			if r.is_package_url(package, assets["url"]):
				new_url = assets["url"]

		if not new_url:
			return (None, None)

		return self.post_scrap_version(package, new_url)

	def scrap_github_tag(self, package):
		html = url_handler.req(
			Request(f"https://github.com/{package.value}/tags")
		)
		scrapped = r.github_tag.findall(html)

		if len(scrapped) == 0:
			return (None, None)

		new_url = f"https://github.com/{package.value}/{scrapped[0]}"

		return self.post_scrap_github_tag(new_url, scrapped[0])

	def scrap_website(self, package, url = None):
		html = url_handler.req(Request(url or package.value))

		return self.post_scrap(package, r.href(package, html))

	def scrap_fossies(self, package):
		html = url_handler.req(Request(package.value))
		scrapped = r.href(package, html)

		if len(scrapped) == 0:
			return (None, None)

		if scrapped[0].startswith("https"):
			new_url = scrapped[0]
		else:
			match = r.url_parent_dir.match(package.value)
			if match:
				new_url = f"{match.group(0)}{scrapped[0]}"
			else:
				return (None, None)

		return self.post_scrap_version(package, new_url)

	def scrap_fossies_search(self, package):
		html = url_handler.req(Request(package.value))
		scrapped = r.href(package, html)

		if len(scrapped) == 0:
			return (None, None)

		if scrapped[0].startswith("https"):
			new_url = scrapped[0]
		else:
			new_url = f"https://fossies.org{scrapped[0]}"

		return self.post_scrap_version(package, new_url)

	def scrap_pypi(self, package):
		return self.scrap_website(package,
			f"https://pypi.org/project/{package.value}/#files")

	def scrap_sourceforge(self, package):
		html = url_handler.req(Request(package.value))

		return self.post_scrap(package, r.href_sourceforge(package, html))

	def scrap_no_scrap(self, package):
		return self.post_scrap_version(package, package.value)

scrap = Scrap()
