from dot_mngr import *

class Package():
	def __init__(self, name):
		self.name = name
		self.d_base = os.path.join(DIR_REPO, self.name)
		self.f_meta = os.path.join(self.d_base, FILE_META)
		self.f_command = os.path.join(self.d_base, FILE_COMMAND)

		self.load_meta()
		self.load_command()

	def load_meta(self):
		if os.path.exists(self.f_meta):
			f = open(self.f_meta, "r")
		else:
			return None
		try:
			meta = json.load(f)
		except json.JSONDecodeError:
			p.fail(f"Failed to load {f.name}")
			return None
		self.value = meta.get("value")
		self.type = meta.get("type")
		self.prefix = meta.get("prefix")
		self.suffix = meta.get("suffix")
		self.link = meta.get("link")
		self.version = meta.get("version")
		self.file_name = f"{self.name}-{self.version}{self.suffix}"
		self.file_path = os.path.join(DIR_CACHE, self.file_name)
		self.repo_status = None
		f.close()

	def load_command(self):
		if os.path.exists(self.f_command):
			spec = importlib.util.spec_from_file_location("command", self.f_command)
			tmp = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(tmp)
			self.command = tmp.Command(self)
		else:
			self.command = DefaultCommand(self)

	@staticmethod
	def info_col(info):
		string = str()
		for i in info:
			tmp = i[0] or ""
			string += tmp.ljust(i[1] - 1) + " "
		return string

	@staticmethod
	def hdr_info():
		p.info(Package.info_col([
			("Name", 20),
			("Version", 15),
			("Status", 8),
			("Link", 40),
		]) + "\n")

	def info(self):
		pfunc = p.info
		status = "UNTO"
		if self.repo_status == 0:
			status = "FAIL"
			pfunc = p.fail
		elif self.repo_status == 1:
			status = "UPDA"
		elif self.repo_status == 2:
			status = "UPTO"

		p.info(Package.info_col([
			(self.name, 20),
			(self.version, 15),
			(status, 8),
			(self.link, 40),
		]))

	def save_update(self):
		if self.new_link == None:
			self.repo_status = 0
			return
		elif self.new_link != self.link:
			self.repo_status = 1
		else:
			self.repo_status = 2

		self.link = self.new_link
		self.version = self.new_version if self.new_version else self.version
		with open(self.f_meta, "w") as f:
			json.dump({
				"value": self.value,
				"type": self.type,
				"prefix": self.prefix,
				"suffix": self.suffix,
				"link": self.link,
				"version": self.version,
			}, f, indent=4)

	def update(self):
		self.new_link, self.new_version = scrap.latest_link(self)
		self.save_update()
		self.info()

	def get_file(self):
		if not os.path.exists(self.file_path):
			if not url_handler.download_package(self):
				return False
			else:
				return True
		p.success(f"{self.file_name} already exists")
		return True
