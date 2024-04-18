from dot_mngr import *

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
		p.warn(f"Failed to decode {request.full_url}")
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
	if WRITE_HTML and html:
		with open("tmp.html", "w") as f:
			f.write(html)
	return html


def download_file(url, path):
	if url == None:
		p.warn(f"Could not download {path}, not link found")
		return False
	pb = ProgressBar(path)

	try:
		urllib.request.urlretrieve(url, path, pb.download_hook)
	except urllib.request.URLError as e:
		p.warn(f"Could not download {path}, error: {e.code}")
		return False

	return True

def download_package(package):
	return download_file(package.link, package.file_path)
