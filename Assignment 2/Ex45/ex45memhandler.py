import os
import glob

########################Handles "memory" of NPC and working with it#################
class MemoryHandler(object):
    


	

	
	def listCharacters(self):
		#workPath = os.getcwd()
		#os.chdir(workPath + "/Players")
		#print os.getcwd()
		fileList = []
		for files in glob.glob("*.txt"):
		#	print files
			fileList.append(files.rsplit(".", 1)[0])
		print fileList
		#	return fileList
			
  
