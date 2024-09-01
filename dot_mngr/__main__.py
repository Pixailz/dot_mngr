from dot_mngr import *
from pprint import pprint

def	main():
	conf.load_repository()

	if DEBUG:
		print(f"{PREFIX            = }")
		print(f"{ROOT_PATH         = }")
		print(f"{DIR_BASE          = }")
		print(f"{DIR_CONFIG        = }")
		print(f"{DIR_REPO          = }")
		print(f"{DIR_CACHE         = }")
		print(f"{FORCE_INSTALL     = }")
		print(f"{DRY_RUN           = }")
		print(f"{WRITE_HTML        = }")
		print(f"{DO_CHECK          = }")
		print(f"{NB_PROC           = }")
		print(f"{TARGET_TRIPLET    = }")
		print(f"{ARCH              = }")

	match conf.parsing.args.command:
		case "update":
			conf.update_repo()
		case "install":
			conf.install_package()
		case "info":
			conf.info_package()

	p.info("end")

if __name__ == "__main__":
	# try:
	main()
	# except Exception as e:
	# 	p.fail(e)
	# 	sys.exit(1)
