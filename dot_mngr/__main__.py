from dot_mngr import *
from pprint import pprint

def git_clone(author, repo, branch=None, dest=None):
	cmd = f"git clone {author}@github.com"

def	main():
	# conf.load_packages()
	git_clone("Pixailz", "dot_mngr", dest="test")

	try:
		conf.load_repository()
	except Exception as e:
		p.fail(e)
		sys.exit(1)

	pprint(conf.parsing.args)

	print(f"{PREFIX     = }")
	print(f"{DRY_RUN    = }")
	print(f"{WRITE_HTML = }")
	print(f"{DO_CHECK   = }")
	print(f"{NB_PROC    = }")

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
