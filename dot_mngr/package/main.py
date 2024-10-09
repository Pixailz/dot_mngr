from dot_mngr import os

import dot_mngr as dm

from dot_mngr import p
from dot_mngr import url_handler
from dot_mngr import get_real_name

from .prepare_archive	import PackagePrepareArchive
from .meta				import PackageMeta
from .info				import PackageInfo
from .cmd				import PackageCmd
from .cmd_utils			import PackageCmdUtils
from .update			import PackageUpdate
from .chroot			import PackageChroot
from .patch				import PackagePatch
from .utils				import PackageUtils

from .type				import TPACK_UNKNOWN

class Package(
		PackageMeta,
		PackagePrepareArchive,
		PackageInfo,
		PackageCmd,
		PackageCmdUtils,
		PackageUpdate,
		PackageChroot,
		PackagePatch,
		PackageUtils
	):
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

	def prepare(self):
		self.get_file()
		self.load_env()
		self.prepare_archive()

		self.f_log_out = open(self.log_out, "w")
		self.f_log_err = open(self.log_err, "w")

		self.take_archive_folder()

		self.prepared = True

	def get_file(self, chroot = None):
		if self.file_path is None:
			p.info(f"Package {self.name} doesn't have file to get")
			return
		if chroot is None:
			chroot = self.chrooted
		if not os.path.exists(self.chrooted_get_path(self.file_path, chroot)):
			if not url_handler.download_package(self):
				return False
			else:
				return True
		p.success(f"{self.file_name} already exists")
		return True
