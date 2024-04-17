from dot_mngr import *

from time import sleep

def	main():
	conf.load_packages()
	# conf.update_repo()
	# conf.info_package()
	# conf.packages["acl"].command.suite()
	# conf.packages["attr"].command.suite()
	# conf.packages["autoconf"].command.suite()
	# conf.packages["automake"].command.suite()
	# conf.packages["bc"].command.suite()
	conf.packages["bash"].command.suite()

if __name__ == "__main__":
	main()
