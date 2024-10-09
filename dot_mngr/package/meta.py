from dot_mngr		import os
import dot_mngr		as dm
from dot_mngr		import p,  Json
from .type			import TPACK_META, TPACK_META_REF

class PackageMeta(object):

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

		if (self.link is None):
			self.file_name = None
			self.file_path = None
		else:
			self.file_name = f"{self.name}-{self.version}{self.suffix}"
			self.file_path = os.path.join(dm.DIR_CACHE, self.file_name)

		self.repo_status = None
