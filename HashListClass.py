import hashlib

class HashList:
	
	def __init__(self):
		self.hash_list = []

	def isDuplicate(self,file_text):
		hash = hashlib.md5()		
		hash.update(file_text)
		if hash.hexdigest() in self.hash_list:
			return True
		else:
			self.hash_list.append(hash.hexdigest())
			return False
					
