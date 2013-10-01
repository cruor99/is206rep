import ex45scene
import ex45routecontrol
import ex45memhandler

from sys import exit
from random import randint

class BadEnd(ex45scene.Scene):

    quips = [
        "YOU REACHED A BAD END, JUST LIKE THE REST",
        
    ]

    def enter(self):
		print BadEnd.quips[randint(0, len(self.quips)-1)]
		exit(1)