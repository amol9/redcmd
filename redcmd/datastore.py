
from . import const


class DataStore:

	def __init__(self):
		pass


	def check_dir(self, data=True, autocomp=False, script=False, create=True):
		if not exists(const.data_dir):
			self.create_dir(const.data_dir, create=create)

		if autocomp and not exists(const.autocomp_dir):
			self.create_dir(const.autocomp_dir, create=create)


	def create_dir(self, path, create=True):
		if create:
			makedir(path)
		else:
			raise DataStoreError('%s does not exist'%path)


	def load_optiontree(self, cmdname):
		# check user dir and /var/local
		pass


	def save_optiontree(self, cmdname):
		pass


	def remove_optiontree(self, cmdname):
		pass


	def list_optiontree(self):
		pass


	def load_script(self):
		pass


	def save_script(self):
		pass

