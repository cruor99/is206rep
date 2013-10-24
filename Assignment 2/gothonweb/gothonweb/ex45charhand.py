import ex45main

################Defines the current character##################
class CharacterHandler(object):
	global charName
	charName = ""
	def __init__(self, charaName):
		self.charaName = charaName
	 	global charName
		charName = charaName
		print charName +" This is a test for CharHandler"
		
	def charNameTest():
		print charName