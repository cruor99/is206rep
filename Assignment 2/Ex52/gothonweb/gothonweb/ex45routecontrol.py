import ex45badend
import ex45encounter1
import ex45scene
import ex45routecontrol

	
class Map(object):


	scenes = {
		'first_encounter': ex45encounter1.MainEncounter(),
		'death': ex45badend.BadEnd()
	}

	def __init__(self, start_scene):
		self.start_scene = start_scene

	def next_scene(self, scene_name):
		return Map.scenes.get(scene_name)

	def opening_scene(self):
		return self.next_scene(self.start_scene)