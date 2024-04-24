from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
	name="dot_mngr",
	version="0.0.1",
	author="Pix",
	packages=["dot_mngr"],
	entry_points={
		"console_scripts": [
			"dot_mngr = dot_mngr.__main__:main"
		]
	},
    description="A package manager for architecture and not for distribution",
	long_description=long_description,
	long_description_content_type="text/markdown",
	install_requires=required,
    url='http://pixailz.freeboxos.fr:3000/Pixailz/dot_mngr',
)
