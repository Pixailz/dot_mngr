from dot_mngr import *

def	main():
	conf.update_repo()
	conf.info_package()
	conf.packages["bc"].command.suite()
	for pack in conf.packages.values():
		pack.command.suite()
		print()

if __name__ == "__main__":
	# main()
	test()
