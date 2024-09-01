# dot_mngr

## Features

### Build a package

Thanks to the `command.py` file, you can build a package by `def`ining the
following functions:

- `configure` to configure the package
- `compile` to compile the package
- `check` to check the package
- `install` to install the package

Here's a simple example of a `command.py` file:

```python
#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	self.chroot()
	self.cmd_run(
		 "./configure"
		f" --prefix={PREFIX}"
		 " --disable-static"
	)

def compile(self):
	self.cmd_run("make")

def check(self):
	self.cmd_run("make check")

def install(self):
	self.cmd_run("make install")
```



### Update repo

Getting newer link to a tarball providing a link or a value to scrap, wich fit the best with one of the
following scrap techniques:
- apache
- apache_dir
- apache_no_sort
- github
- github_tag
- gitlab
- website
- fossies
- fossies_search
- pypi
- sourceforge
- no_scrap

Associated with a prefix and a suffix, dot_mngr will return the link and the
version of the newer package.

here is some exemple of meta.json from the main repos:

- <code><a href=https://github.com/Pixailz/dot_mngr_repo/blob/main/acl/meta.json>main@acl</a></code>
for a *files* section:

   - value with a `/` will be considered as a path to a file
   - others are considered as a cmd found in the **PATH** environment variable

- <code><a href=https://github.com/Pixailz/dot_mngr_repo/blob/main/coreutils/meta.json>main@coreutils</a></code>
for a *patchs* section:
   - with a patch name, for later reference
   - and a link to the patch

> [!NOTE]
> Try resolve dependencies for this package ;)

- <code><a href=https://github.com/Pixailz/dot_mngr_repo/blob/blfs/1_cryptsetup/meta.json>blfs@1_cryptsetup</a></code>
for a *dependencies* section:
   - with a section *required* that, for the moment, regroup required, run and build time, as well as recommended packages

- <code><a href=https://github.com/Pixailz/dot_mngr_repo/blob/lfs/1_linux/meta.json>lfs@1_linux</a></code>
for a *reference* section:
   - package with reference merge the meta.json of the current package on top of
   the reference package

## TODO

### P1

### P2

1. the doc
1. differences occure when package configure in `/etc/passwd` and `/etc/group`
   more generally, allow modification on `/etc/passwd` and `/etc/group`

### P3

1. workflows to update repo:
  1. split repo folder into githubs, referencing package as needed, provide
  with template, actions can update repo
1. Some test are not correctly checked and therefore considered as good
   1. Register check/test that don't pass
1. Review systemd unit install

### P4

1. meta.json: reference of reference not working
