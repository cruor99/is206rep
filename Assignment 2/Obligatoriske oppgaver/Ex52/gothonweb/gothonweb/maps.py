from random import randint


class Room(object):
	
	def __init__(self, name, description, pic, number=None, tries=None):		
		self.name = name
		self.description = description
		self.paths = {}
		self.output = ""
		self.pic = pic
		
		#Random Escape Pod
		self.num = number
		self.guess = tries

	def go(self, direction):
		return self.paths.get(direction, None)

	def add_paths(self, paths):
		self.paths.update(paths)
	
	def options(self):
		if self.name == "Laser Weapon Armory" or self.name == "Escape Pod":
			return "You're on your own, bucko!"
		elif self.paths == {}:
			pass
		else:
			return self.paths.keys()
			
	def leet(self):
		hints = {'Laser Weapon Armory': "You pull out your pink colored anti-gravimetrical, semi-automatic, ultra-computational scanning device and manage to decipher two out of the three digits needed for the code %r and %r. The order, however is still a mystery" %(n1, n3),
		'Escape Pod': "You decide to play eenie-meenie-miny-moe with the escape pods. While wildy entertainining, it does nothing for you. So you just go with your gut that says choose pod %r" % self.num}
		
		if self.name in hints.keys():
			self.output = hints.get(self.name)
		else:
			self.output = "No hint available."
			
	def _help(self):
		self.output = """You are in %s. Your choices are listed above your input bar. For additional help, you can sometimes type 'l33t' for a hint, although it may not work for every room. Other commands are 'Restart', 'Save' and 'Quit'. There's also 'Credits'""" % (self.name)

def generate(num1, num2, num3):
	global n1
	n1 = num1
	global n2
	n2 = num2
	global n3
	n3 = num3
	return '%d%d%d' % (n1, n2, n3)
	
central_corridor = Room ("Central Corridor", 
"""
The Gothons of Planet Percal #25 have invaded your ship and destroyed
your entire crew. You are the last surviving member and your last
mission is to get the neutron bomb from the Weapons Armory,
put it in the bridge, and blow up the ship after getting into an
escape pod.

You're running down the central corridor to the Weapons Armory when
a Gothon jumps out, red scaly skin, dark grimy teeth, and an evil
clown costume flowing around his hate filled body. He's blocking the
door to the Armory and about to pull a weapon to blast you.
""", "corridor.gif")

laser_weapon_armory = Room("Laser Weapon Armory",
"""
Lucky for you they made you learn Gothon insults in the academy.
You tell the one Gothon joke your remember:
\"Lbhe zbgure vf fb sng, jura fur fvgf nebhaq gur ubhfr, fur fvgf nebhaq gur ubhfr!"
The Gothon stops, tries not to laugh, then bursts out laughing and can't move.
While he's laughing you run up and shoot him square in the head, then jump through
the Weapon Armory door.

You do a dive roll into the Weapon Armory, crouch and scan the room
for more Gothons that might be hiding. It's dead quiet... too quiet.
You stand up and run to the far side of the room and find the 
neutron bomb in its container. There's a keypad lock on the box
and you need the code to get the bomb out. Luckily, you have your
tricorder device which will return 3 possible codes you can use, but
you only have one chance at it, else the lock will close forever.
""", "armory.gif", generate(randint(0,9), randint(1,5), randint(0,9)), 10)

the_bridge = Room("The Bridge",
"""
The container clicks open and the seal breaks, letting gas out.
You grab the neutron bomb and run as fast as you can to to the
bridge where you must place it in the right spot.

You burst onto the Bridge with the neutron destruct bomb
under your arm and surprise 5 Gothons who are trying to
take control of your ship. Each of them has an even uglier
clown costume than the last. THey haven't pulled their
weapons out yet, as they see the active bomb under your arm
and don't want to set it off.
""", "bridge.gif")

escape_pod = Room("Escape Pod",
"""
You point your blaster at the bomb under your arm
and the Gothons put their hands up and start to sweat.
You inch backwards to the door, open it and then carefully
place the bomb on the floor, pointing your blaster at it.
You then jump back through the door, punch the close button
and blast the lock so the Gothons can't get out.
Now that the bomb is placed, you run to the escape pod to
get off this tin can.

You rush through the ship desperately trying to make it to 
the escape pod before the whole ship explodes. It seems like
hardly any Gothons are on the ship, so your run is clear of
interference. You get to the chamber with the escape pods, and
now need to pick one to take. Some of them could be damaged
but you don't have time to look. There's 5 pods, which one
do you take. (Remember, it's not very 'l33t' of you, should
you need a hint)
""", "escape_pod.gif", str(n2), 1)

the_end_winner = Room("The End",
"""
You jump into the pod and hit the eject button.
The pod easily slides out into space heading to
the planet below. As it flies to the planet, you look
back to se your ship implode then explode like a 
bright start, taking out the Gothon ship at the same time.
You won!
""", "win.gif")

the_end_loser = Room("The End",
"""
You jump into the pod and hit the eject button.
The pod escapes out into the void of space, then
implodes as the hull ruptures, crushing your body
into jelly jam.
""", "death.gif")


generic_death = Room("death", "You died!", "death.gif")

corridor_death1 = Room("death",
"""
Quick on the draw you yank out your blaster and fire it at the Gothon.
His clown costume is flowing and moving around his body, which throws
off your aim. Your laser hits his costume but misses entirely. This
completely ruins his brand new costume his mother bough him, which
makes him fly into an insane rage and blasts you repeatedly in the face until
you are dead. Then he eats you.""", "death.gif")

corridor_death2 = Room("death",
"""
Like a world class boxer you dodge, weave, slip and slide right
as the Gothon's blaster cranks a laser past your head.
In the middle of your artful dodge, your foot slips and you
bang your head on the metal wall and pass out.
You wake up shortly after only to die as the Gothon stomps on
your head and eats you.""", "death.gif")

armory_death = Room("death",
"""
The lock loudly buzzes as you hear a sickening melting sound.
The mechanism becomes fused together. You decide to sit there, and
finally the Gothons blow up your ship from theirs, and you die.
""", "death.gif")

bridge_death = Room("death",
"""
In a panic you throw the bomb at the group of Gothons
and make a leap for the door. Right as you drop it a
Gothon shoots you right in the back killing you.
As you die, you see another Gothon frantically try to disarm
the bomb. You die knowing they will probably blow up when
it goes off.""", "death.gif")

escape_pod.add_paths({
	'x': the_end_winner,
	'*': the_end_loser
})

the_bridge.add_paths({
	'throw the bomb': bridge_death,
	'slowly place the bomb': escape_pod
})

laser_weapon_armory.add_paths({
	'x' : the_bridge,
	'*' : armory_death
})

central_corridor.add_paths({
	'shoot': corridor_death1,
	'dodge': corridor_death2,
	'tell a joke': laser_weapon_armory
})



#  For testing purposes  #

START = central_corridor
SECOND = laser_weapon_armory
THIRD = the_bridge
FOURTH = escape_pod
END1 = the_end_winner
END2 = the_end_loser