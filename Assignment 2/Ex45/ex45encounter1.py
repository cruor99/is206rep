import ex45scene
import ex45memhandler
import ex45routecontrol
import ex45scene
import ex45badend
import ex45main
import ex45charhand
class MainEncounter(ex45scene.Scene):

    def enter(self):
		print "You encounter a man sitting by a crossroads. He is chanting 'left, right, left, right."
		print "They all go one or the other."
		print "What will you do?"
		print "##Your options are the following:"
		print "##others; ask for others passing through"
		print "##ignore; ignore the man and walk straight"
	#	print "##left; go left"
	#	print "##right; go right"
		print "##who am I"
		action = raw_input("> ")
		
		
		if action == "who am I":
			print "You are %s" % ex45charhand.CharacterHandler.charName
			return 'death'
			
		if action == "others":
			print "Yes, others have come through here. Their names were"
			testVar = ex45memhandler.MemoryHandler()
			testVar.listCharacters()
			print "I will now add your name to the list"
			return 'death'
		if action == "ignore":
			print"you ignore the rambling old man, and walk straight ahead."
			open ("Players/" + ex45main.GameMain.currChar + ".txt", 'a+b').write("Action: Ignored")
			return 'death'

		else:
			print "DOES NOT COMPUTE!"
			return 'first_encounter'