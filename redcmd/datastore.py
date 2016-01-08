from os import mkdir, walk, remove
from os.path import exists, join as joinpath
from pickle import dump as pickledump, load as pickleload, PicklingError, UnpicklingError

from . import const


class DataStoreError(Exception):
	pass


class DataStore:
	ot_version = '1.0'

	def __init__(self):
		self.check_dir()


	def check_dir(self, data=True, autocomp=False, script=False, create=True):
		if not exists(const.data_dir):
			self.create_dir(const.data_dir, create=create)

		if autocomp and not exists(const.autocomp_dir):
			self.create_dir(const.autocomp_dir, create=create)

		if script and not exists(const.script_dir):
			self.create_dir(const.script_dir, create=create)


	def create_dir(self, path, create=True):
		if create:
			mkdir(path)
		else:
			raise DataStoreError('%s does not exist'%path)


	def save_optiontree(self, ot, cmdname):
		self.check_dir(data=False, autocomp=True)

		with open(joinpath(const.autocomp_dir, cmdname), 'wb') as f:
			try:
				pickledump([self.ot_version, ot], f)
			except PicklingError as e:
				print(e)
				raise DataStoreError('unable to save option tree')


	def load_optiontree(self, cmdname):
		filepath = joinpath(const.autocomp_dir, cmdname)

		if not exists(filepath):
			filepath = joinpath(const.root_data_dir, cmdname)
			if not exists(filepath):
				raise DataStoreError('unable to load option tree')

		with open(filepath, 'rb') as f:
			try:
				data = pickleload(f)
			except UnpicklingError as e:
				log.error(str(e))

			ot_version = data[0]
			if ot_version > self.ot_version:
				raise DataStoreError('cannot load greater ot_version, %s > %s'%(version, self.version))
			return data[1]


	def remove_optiontree(self, cmdname):
		filepath = joinpath(const.autocomp_dir, cmdname)
		self.remove_file(filepath)


	def remove_all_optiontrees(self):
		for name in self.list_optiontree():
			self.remove_optiontree(name)


	def remove_file(self, filepath):
		if exists(filepath):
			try:
				remove(filepath)
				return True
			except OSError as e:
				print(e)
				return False


	def list_optiontree(self):
		for _, _, files in walk(const.autocomp_dir):
			return files

