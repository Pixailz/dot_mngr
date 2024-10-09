from dot_mngr import CTYPE

class CheckBool(object):
	false_str = [
		"0", "false", "f", "n"
	]

	def IsFalse(string):
		ttype = type(string)

		if ttype == CTYPE["STR"]:
			return string.lower() in CheckBool.false_str
		elif ttype == CTYPE["BOOL"]:
			return string == False
		return True