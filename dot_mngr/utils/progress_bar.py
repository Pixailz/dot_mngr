from dot_mngr import *

class ProgressBar():

	def __init__(self, file_path):
		self.file_path = os.path.basename(file_path)

	def __del__(self):
		print()

	def download_hook(self, block_num, block_size, total_size):
		pb_perc = (block_num * block_size) / total_size
		pb_full = "=" * (int(pb_perc * PROMPT_PROGRESS_BAR_SIZE) - 1)
		if int(pb_perc * 100) < 100:
			pb_full += ">"
			pb_status = a.P_INFO
			pb_perc = str("%.2f" % (pb_perc * 100)).rjust(6, " ")
		else:
			pb_full += "="
			pb_status = a.P_PASS
			pb_perc = "100.00"

		p_right = f"{pb_perc}% [{pb_full.ljust(PROMPT_PROGRESS_BAR_SIZE, ' ')}]"
		pos_p_right = TERM_COLS - len(p_right) + 1

		print(
			f"\x1b[G\x1b[2K{pb_status} {self.file_path}"
			f"\x1b[{pos_p_right}G{p_right}"
			, end=""
		)
