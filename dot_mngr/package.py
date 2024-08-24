from dot_mngr import os
from dot_mngr import tar
from dot_mngr import shutil
from dot_mngr import importlib
from dot_mngr import subprocess

import dot_mngr as dm

from dot_mngr import p, r, Os, Json
from dot_mngr import a_cmd
from dot_mngr import scrap
from dot_mngr import url_handler
from dot_mngr import default_configure
from dot_mngr import default_compile
from dot_mngr import default_check
from dot_mngr import default_install
from dot_mngr import default_uninstall
from dot_mngr import default_suite

from dot_mngr import pprint

from dot_mngr import REPO_SEP

# Package Type
TPACK_UNKNOWN = 0
TPACK_META = 1
TPACK_META_REF = 2
TPACK_COMMAND = 4

def get_real_name(pack_name: str):
	splitted = pack_name.split(dm.REPO_SEP)
	return splitted[1] if len(splitted) == 2 else splitted[0]

class Package():
	def __init__(self, name, dir_repo):
		self.real_name = name
		self.name = get_real_name(self.real_name)
		self.dir_repo = dir_repo
		self.d_base = os.path.join(self.dir_repo, get_real_name(self.name))
		self.f_meta = os.path.join(self.d_base, dm.FILE_META)
		self.f_command = os.path.join(self.d_base, dm.FILE_COMMAND)

		self.status = TPACK_UNKNOWN

		self.prepared = False
		self.log_out = os.path.join(dm.DIR_LOG, f"{self.name}.out.log")
		self.log_err = os.path.join(dm.DIR_LOG, f"{self.name}.err.log")
		self.f_log_out = None
		self.f_log_err = None

		self.chrooted = None

		self.load_metas()
		self.load_commands()

	def __del__(self):
		if self.f_log_out and not self.f_log_out.closed:
			self.f_log_out.close()
		if self.f_log_err and not self.f_log_err.closed:
			self.f_log_err.close()

	def set_meta_ref(self, key):
		self_value = getattr(self, key, None)
		if self_value is None:
			setattr(self, key, getattr(self.reference_pack, key, None))

	def load_metas_ref(self):
		splitted = self.reference.split(dm.REPO_SEP)
		repos = list()
		if len(splitted) == 2:
			if splitted[0] not in dm.conf.repository:
				p.fail(f"Unknown repository: {splitted[0]}")
			else:
				repos = [dm.conf.repository[splitted[0]]]
				splitted[0] = splitted[1]
		else:
			repos = dm.conf.repository

		self.reference_pack = None
		for repo in repos:
			for k, v in repo.packages.items():
				if k == splitted[0]:
					self.reference_pack = v
		if self.reference_pack is None:
			p.fail(f"Unknown package: {splitted[0]}")

		self.set_meta_ref("value")
		self.set_meta_ref("type")
		self.set_meta_ref("prefix")
		self.set_meta_ref("suffix")
		self.set_meta_ref("link")
		self.set_meta_ref("version")
		self.set_meta_ref("patchs")
		self.set_meta_ref("files")
		self.set_meta_ref("dependencies")

		self.file_name = self.reference_pack.file_name
		self.file_path = self.reference_pack.file_path

	def load_metas(self):
		meta = Json.load(self.f_meta)
		if not meta:
			return None
		self.status = TPACK_META
		self.reference = meta.get("reference")
		if self.reference:
			self.status = TPACK_META_REF

		self.value = meta.get("value")
		self.type = meta.get("type")
		self.prefix = meta.get("prefix")
		self.suffix = meta.get("suffix")
		self.link = meta.get("link")
		self.version = meta.get("version")
		self.patchs = meta.get("patchs")
		self.files = meta.get("files")
		self.dependencies = meta.get("dependencies")

		self.file_name = f"{self.name}-{self.version}{self.suffix}"
		self.file_path = os.path.join(dm.DIR_CACHE, self.file_name)

		self.repo_status = None

	def load_env(self):
		path = "/usr/bin:/usr/sbin"
		if os.path.exists("/bin") and not os.path.islink("/bin"):
			path = f"/bin:{path}"

		self.env = {
			"PATH": path,
		}

	def add_path(self, path):
		self.env["PATH"] = f"{path}:{self.env['PATH']}"

	def get_env(self, nb_proc = dm.NB_PROC):
		self.env["MAKEFLAGS"] = f"-j{nb_proc}"
		return self.env

	def add_env(self, env: dict):
		self.env.update(env)

	def load_command(self, cmd_name: str, default_cmd: callable):
		cmd = getattr(self.tmp_cmd, cmd_name, None)
		if cmd:
			self.cmd[cmd_name] = a_cmd(self, cmd, cmd_name)
		else:
			self.cmd[cmd_name] = a_cmd(self, default_cmd)

	def load_commands(self):
		self.cmd = dict()
		self.tmp_cmd = None
		if os.path.exists(self.f_command):
			spec = importlib.util.spec_from_file_location("command", self.f_command)
			self.tmp_cmd = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(self.tmp_cmd)

		self.load_command("configure",	default_configure)
		self.load_command("compile", 	default_compile)
		self.load_command("check",		default_check)
		self.load_command("install",	default_install)
		self.load_command("uninstall",	default_uninstall)
		self.load_command("suite",		default_suite)

	def prepare(self):
		from dot_mngr import conf

		self.get_file()
		self.load_env()
		self.prepare_tarball()
		self.conf = conf

		self.f_log_out = open(self.log_out, "a")
		self.f_log_err = open(self.log_err, "a")

		self.take_tar_folder()

		self.prepared = True

	def take_tar_folder(self):
		cwd = os.getcwd()
		if cwd != self.tar_folder:
			self.oldpwd = cwd
		os.chdir(self.tar_folder)

	def prepare_tarball_real(self, src: str, dest: str):
		ftar = tar.open(src, "r")
		ftar_names = ftar.getnames()
		have_dir = True
		if len(ftar_names) > 0:
			for i in range(0, 2):
				match = r.tar_dir.match(ftar_names[i])
				if match:
					break

			if match:
				self.tar_folder = os.path.join(dm.DIR_CACHE, match.group(1))
			else:
				self.tar_folder = os.path.join(dm.DIR_CACHE, self.name)
				have_dir = False

		if dest is None:
			if os.path.exists(self.tar_folder):
				shutil.rmtree(self.tar_folder)
				p.warn("Removing old tar folder")

			p.info(f"Extracting {self.name}")
			if have_dir:
				ftar.extractall(dm.DIR_CACHE)
			else:
				ftar.extractall(self.tar_folder)
			p.success(f"Extracted {self.name}")

		else:
			p.info(f"Extracting {self.name} into {dest}")
			ftar.extractall(dest)
			p.success(f"Extracted {self.name} into {dest}")

	def prepare_tarball(self, dest: str = None, chroot: str = None):
		if chroot is None:
			chroot = self.chrooted
		src = self.chrooted_get_path(self.file_path, chroot)
		if not tar.is_tarfile(src):
			return
		if dm.DRY_RUN:
			if dest is None:
				self.tar_folder = os.path.join(dm.DIR_CACHE, self.name)
				dest = self.tar_folder

			dest = self.chrooted_get_path(dest, chroot)
			Os.mkdir(dest)
			p.dr(f"Creating {dest}")

		else:
			self.prepare_tarball_real(src, self.chrooted_get_path(dest, chroot))

	@staticmethod
	def info_col(
			name,
			status,
			version,
			reference,
			link
		):
		return p.col([
			(name, 20),
			(version, 15),
			(status, 15),
			(reference, 15),
			(link, 50),
		])

	@staticmethod
	def hdr_info():
		p.title(Package.info_col("Name","Status", "Version", "reference", "link") + "\n")

	def info(self):
		pfunc = p.info
		status = "Untouched"
		if self.repo_status == 0:
			status = "Failed"
			pfunc = p.fail
		elif self.repo_status == 1:
			status = "Updated"
		elif self.repo_status == 2:
			status = "Up-to-date"

		if pfunc is not p.fail and self.reference:
			pfunc = p.warn
		pfunc(Package.info_col(self.name, status, self.version, self.reference, self.link))

		# if self.dependencies:
		# 	p.title(f"  - Dependencies:")
		# 	if self.dependencies.get("required"):
		# 		p.info(f"    - Required:")
		# 		for i in self.dependencies["required"]:
		# 			p.info(f"      - {i}")
		# 	if self.dependencies.get("optional"):
		# 		p.info(f"    - Optional:")
		# 		for i in self.dependencies["optional"]:
		# 			p.info(f"      - {i}")
		# 	print()

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
		self.file_name = f"{self.name}-{self.version}{self.suffix}"
		self.file_path = os.path.join(dm.DIR_CACHE, self.file_name)
		Json.dump({
			"value": self.value,
			"type": self.type,
			"prefix": self.prefix,
			"suffix": self.suffix,
			"link": self.link,
			"version": self.version,
			"patchs": self.patchs,
			"files": self.files,
			"dependencies": self.dependencies
		}, self.f_meta)

	def update(self):
		if not self.reference:
			self.new_link, self.new_version = scrap.latest_link(self)
			self.save_update()
		self.info()

	def get_file(self, chroot = None):
		if chroot is None:
			chroot = self.chrooted
		if not os.path.exists(self.chrooted_get_path(self.file_path, chroot)):
			if not url_handler.download_package(self):
				return False
			else:
				return True
		p.success(f"{self.file_name} already exists")
		return True

	def cmd_run_real(self, cmd: str, nb_proc: int):
		def p_out(line):
			self.f_log_out.write(line)
			p.cmdo(line.strip("\n"))

		def p_err(line):
			self.f_log_err.write(line)
			p.cmde(line.strip("\n"))

		proc = subprocess.Popen(cmd,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			env=self.get_env(nb_proc),
			universal_newlines=True,
			shell=True,
			close_fds=True,
		)

		os.set_blocking(proc.stdout.fileno(), False)
		os.set_blocking(proc.stderr.fileno(), False)

		while True:
			line_out = proc.stdout.readline()
			line_err = proc.stderr.readline()
			line_out_empty = line_out == ''
			line_err_empty = line_err == ''
			if line_out_empty and line_err_empty and proc.poll() is not None:
				break
			if not line_out_empty:
				p_out(line_out)
			if not line_err_empty:
				p_err(line_err)

		proc.wait()
		retv = proc.returncode

		if retv != 0:
			p.fail(f"Command failed:\n({retv})[{cmd}]")

		return retv

	def cmd_run(self, cmd: str, nb_proc: int = dm.NB_PROC):
		if dm.DRY_RUN:
			p.dr(cmd)
		else:
			return self.cmd_run_real(cmd, nb_proc)

	def chrooted_get_path(self, path = None, chroot = None):
		if chroot is None:
			chroot = self.chrooted
		if chroot and not path is None:
			if path.startswith(chroot):
				return path.removeprefix(chroot)
		return path

	def patch_get_path(self, name, chroot = None):
		if chroot is None:
			chroot = self.chrooted
		path = self.chrooted_get_path(self.tar_folder, chroot)
		return os.path.join(path, f"{name}.patch")

	def download_patch(self, name, path = None):
		url = self.patchs[name]
		if path is None:
			path = self.patch_get_path(name)
		if os.path.exists(path):
			return
		url_handler.download_file(url, path)

	def apply_patch(self, name, opt):
		# TODO:
		# 	- Check if patch is already downloaded
		path = self.patch_get_path(name)
		self.download_patch(name, path)
		self.cmd_run(f"patch {opt} -i {path}")

	def take_build(self):
		path = os.path.join(self.tar_folder, "build")
		if not self.chrooted is None:
			path = path.replace(self.chrooted, "")
		Os.take(path)

	def chroot(self, dest: str = None):
		self.real_root = os.open("/", os.O_RDONLY)

		if dest is None:
			dest = dm.PREFIX

		os.chroot(dest)
		os.chdir(".")
		self.chrooted = dest

	def unchroot(self):
		os.fchdir(self.real_root)
		os.chroot(".")
		os.close(self.real_root)
		if self.oldpwd:
			os.chdir(self.oldpwd)
		else:
			os.chdir(".")
		self.chrooted = None

	def copy(self, file_name: str, dest_path: str):
		file_path = os.path.join(self.tar_folder, file_name)
		copy_func = None
		if not os.path.exists(file_path):
			p.fail(f"File not found: {file_name}")
		elif os.path.isdir(file_path):
			copy_func = shutil.copytree
		else:
			copy_func = shutil.copy2

		copy_func(file_path, dest_path)
