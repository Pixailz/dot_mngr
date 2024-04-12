from dot_mngr import *

def	main():
	config.update_repo()
	config.info_package()
	for package in config.packages.values():
		package.get_file()

if __name__ == "__main__":
	main()
