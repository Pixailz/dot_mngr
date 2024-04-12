from urllib import request as urequest
import gzip
import os

from dot_mngr import WRITE_HTML, TERM_COLS, TERM_ROWS
from dot_mngr import p, a

PROMPT_RIGHT_SIZE = 60
PROMPT_PROGRESS_BAR_SIZE = PROMPT_RIGHT_SIZE - 10

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
		resp = urequest.urlopen(request)
	except urequest.HTTPError as e:
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


class Downloader():

	def __init__(self, file_path):
		self.file_path = os.path.basename(file_path)

	def progress_hook(self, block_num, block_size, total_size):
		pb_perc = (block_num * block_size) / total_size
		pb_full = "=" * (int(pb_perc * PROMPT_PROGRESS_BAR_SIZE) - 1)
		if int(pb_perc * 100) < 100:
			pb_full += ">"
			pb_status = a.P_INFO
			pb_perc = str("%.2f" % (pb_perc * 100)).rjust(6, " ")
		else:
			pb_full += "="
			pb_status = a.P_PASS
			pb_perc = "100.00"

		prompt_right = f"{pb_perc}% [{pb_full.ljust(PROMPT_PROGRESS_BAR_SIZE, " ")}]"
		pos_prompt_right = TERM_COLS - len(prompt_right) + 1

		print(
			f"\x1b[G\x1b[2K{pb_status} {self.file_path}"
			f"\x1b[{pos_prompt_right}G{prompt_right}"
			, end=""
		)

def download_package(package):
	if package.link == None:
		p.warn("Could not download package, not link found")
		return False
	pack = Downloader(package.tar_path)
	try:
		urequest.urlretrieve(package.link, package.tar_path, pack.progress_hook)
	except urequest.URLError:
		p.fail(f"Failed to download {package.name} from {package.link}")
		return False
	print()
	return True
