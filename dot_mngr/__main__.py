from dot_mngr import *

def	main():
	config.update_repo()
	config.info_package()
	for pack in config.packages.values():
		pack.command.configure()
		pack.command.compile()
		pack.command.check()
		pack.command.install()
		print()

if __name__ == "__main__":
	# main()
	test()
