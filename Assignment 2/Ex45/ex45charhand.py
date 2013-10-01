import ex45main

################Defines the current character##################
class CharacterHandler(object):
	charName = "dummy"
	def __init__(self, charName):
		self.CharName = charName
		print charName +" This is a test for CharHandler"
		
	def charNameTest():
		print charName