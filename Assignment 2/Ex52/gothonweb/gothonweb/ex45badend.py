import ex45scene
import ex45routecontrol
import ex45memhandler

from sys import exit
from random import randint

class BadEnd(ex45scene.Scene):

    quips = [
        "IT WAS ALL A TRAP, THERE IS NO ESCAPE!",
        
    ]

    def enter(self):
		print BadEnd.quips[randint(0, len(self.quips)-1)]
		exit(1)