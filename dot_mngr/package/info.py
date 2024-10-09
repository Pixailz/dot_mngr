from dot_mngr import p

class PackageInfo(object):
	@staticmethod
	def info_col(
			name,
			update_status,
			status,
			version,
			reference,
			link
		):
		return p.col([
			(name, 20),
			(update_status, 15),
			(status, 15),
			(version, 15),
			(reference, 15),
			(link, 50),
		])

	@staticmethod
	def hdr_info():
		p.title(PackageInfo.info_col("Name","UpdateStatus", "Status", "Version", "reference", "link") + "\n")

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
			pfunc = p.ref
		pfunc(PackageInfo.info_col(
			self.name,
			status,
			"Installed" if self.is_installed() else "Not Installed",
			self.version,
			self.reference,
			self.link
		))

		# if self.dependencies:
		# 	p.title(f"  - Dependencies:")
		# 	if self.dependencies.get("required"):
		# 		p.title(f"    - Required:")
		# 		for i in self.dependencies["required"]:
		# 			print(f"      - {i}")
