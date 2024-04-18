from dot_mngr import *

def	main():
	conf.load_packages()
	# conf.update_repo()
	# conf.info_package()

	# conf.packages["acl"].cmd["suite"]()
	# conf.packages["attr"].cmd["suite"]()
	# conf.packages["autoconf"].cmd["suite"]()
	# conf.packages["automake"].cmd["suite"]()
	# conf.packages["bash"].cmd["suite"]()
	# conf.packages["bc"].cmd["suite"]()
	# conf.packages["binutils"].cmd["suite"]()
	conf.packages["less"].cmd["suite"]()

if __name__ == "__main__":
	main()
