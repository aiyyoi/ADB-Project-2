import hashlib

class hashList:
	
	def __init__(self):
		self.hash_list = []

	def isDuplicate(self,file_path):
		hash = hashlib.md5()
		with open(file_path,"rb") as f:
			for block in iter(lambda: f.read(4096), b""):
				hash.update(block)
		if hash.hexdigest() in self.hash_list:
			return True
		else:
			self.hash_list.append(hash.hexdigest())
			return False
					
