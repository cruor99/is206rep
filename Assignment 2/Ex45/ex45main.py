import ex45scene
import ex45routecontrol
import ex45badend
import ex45encounter1
import ex45charhand
from sys import exit
from random import randint
import os
import ex45main
class GameMain(object):

################Bio Setup#######################    
	global workPath
	workPath = os.getcwd()
	global currChar
	currChar = ""
	def __init__(self, scene_map):
		global workPath
		workPath = os.getcwd()
		self.scene_map = scene_map
		char_name = raw_input("What is your name? ")

		print "Flavor text to start the game", char_name
		
		os.chdir(ex45main.workPath + "/ex45" + "/Players")
		char_bio = open(char_name + ".txt", 'w')
		global currChar
		currChar = char_name
		ex45charhand.CharacterHandler(char_name).charName = char_name
		print currChar + "Current Character Name"

		char_bio.write("Character Name: " + char_name + "\n")
	os.chdir("..")
	print os.getcwd()	
	def play(self):
		current_scene = self.scene_map.opening_scene()
		while True:
			print "\n--------"
			next_scene_name = current_scene.enter()
			current_scene = self.scene_map.next_scene(next_scene_name)
			
			
