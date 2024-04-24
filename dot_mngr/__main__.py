from dot_mngr import *

def	main():
	conf.load_packages()
	match conf.parsing.args.command:
		case "update":
			conf.update_repo()
		case "install":
			conf.install_package()
		case "info":
			conf.info_package()

	p.info("end")

if __name__ == "__main__":
	main()
