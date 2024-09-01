from dot_mngr import os
from dot_mngr import Kernel
import dot_mngr as dm

def default_kernel_configure(self):
	self.chroot()
	self.cmd_run("make mrproper && make defconfig")
	config_dest = f"/sources/{os.path.basename(self.tar_folder)}/.config"
	config_source = f"/boot/config-{self.version}"
	self.cmd_run(
		f"if [ -f '{config_source}' ]; then"
		f"    cp -fv {config_source} {config_dest};"
		 " fi"
	)
	self.kernel = Kernel(config_dest)

def default_kernel_configure_kernel(self):
	p.warn(f"Configure Kernel command not found for {self.name}")

def default_kernel_compile(self):
	self.localversion = os.getenv("DISTRO_CODENAME")
	self.vmlinuz = os.getenv("VMLINUZ", "")
	self.vmlinuz += f"-{self.version}"
	self.vmlinuz_suffix = os.getenv("VMLINUZ_SUFFIX", "")
	if self.vmlinuz_suffix:
		self.vmlinuz += f"-{self.vmlinuz_suffix}"
	print(f"{self.vmlinuz      = }")

	print(f"{self.localversion = }")
	if self.localversion:
		self.kernel.config("LOCALVERSION", f'"-{self.localversion}"')
		self.kernel.config("LOCALVERSION_AUTO", "y")
	self.cmd_run(
		 "rm -rf"
		f" /boot/System.map-{self.version}"
		f" /boot/{self.vmlinuz}"
		f" /boot/config-{self.version}"
		f" {dm.PREFIX}/share/doc/linux-{self.version}"
	)
	self.cmd_run("yes '' | make")

def default_kernel_install(self):
	self.cmd_run("make modules_install")
	self.cmd_run(f"cp -fiv System.map /boot/System.map-{self.version}")
	self.cmd_run(f"cp -fiv arch/x86/boot/bzImage /boot/{self.vmlinuz}")
	self.cmd_run(f"cp -fiv .config /boot/config-{self.version}")
	self.cmd_run(f"cp -fr Documentation -T {dm.PREFIX}/share/doc/linux-{self.version}")

	self.cmd_run(f"tar -xf /sources/{self.file_name} -C {dm.PREFIX}/src")
	self.cmd_run(
		f'mv "{dm.PREFIX}/src/{os.path.basename(self.tar_folder)}"'
		f' "{dm.PREFIX}/src/kernel-{self.version}"'
	)
