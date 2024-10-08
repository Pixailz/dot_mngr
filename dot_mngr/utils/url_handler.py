from	dot_mngr import	os
from	dot_mngr import	urllib

import	dot_mngr as		dm
from 	dot_mngr import	ProgressBar
from 	dot_mngr import	p
from 	dot_mngr import	gzip

from	dot_mngr import	Os

def req_decode(resp):
	if resp.info().get("Content-Encoding") == "gzip":
		raw = gzip.decompress(resp.read())
	else:
		raw = resp.read()
	resp.close()

	html = None
	try:
		html = raw.decode("utf-8")
	except UnicodeDecodeError:
		p.warn(f"Failed to decode {resp.geturl()}")
	return html

def req_open(request):
	try:
		resp = urllib.request.urlopen(request)
	except urllib.request.HTTPError as e:
		if e.code == 410 and request.host == "fossies.org":
			return req_decode(e)
		else:
			p.warn(f"Failed request, {e.code}, to {request.full_url}")
			return None

	return req_decode(resp)

def req(request):
	html = req_open(request)
	if dm.WRITE_HTML and html:
		with open("tmp.html", "w") as f:
			f.write(html)
	return html


def download_file(url, path):
	if url == None:
		p.warn(f"Could not download {path}, not link found")
		return False
	pb = ProgressBar(path)

	parent_dir = os.path.abspath(os.path.join(path, os.pardir))
	if not os.path.exists(parent_dir):
		Os.mkdir(parent_dir)

	try:
		urllib.request.urlretrieve(url, path, pb.download_hook)
	except urllib.request.URLError as e:
		msg = f"Could not download {path}"
		if getattr(e, "code", None):
			msg += f", code: {e.code}"
		p.warn(msg)
		return False

	return True

def download_package(self):
	return download_file(self.link, self.chrooted_get_path(self.file_path))
