import web
from gothonweb import maps

urls = (
	'/game', 'GameEngine',
	'/index', 'Index',
	'/', 'Index',
	'/credits', 'Credits'
)

app = web.application(urls, globals())
render = web.template.render('templates/', base="layout")


# A little hack so sessions works with debug mode on
if web.config.get('_session') is None:
	store = web.session.DiskStore('sessions')
	session = web.session.Session(app, store, initializer={'room': None})
	web.config._session = session
else:
	session = web.config._session





class Index(object):

	def GET(self):
		# setup the session with starting values then move to engine
		session.room = maps.START
		web.seeother("/game")
		
		
class Credits(object):

	def GET(self):
		return render.you_died()
	
		
class GameEngine(object):

	def __init__(self):
		self.commands = {'help': session.room._help, 'l33t': session.room.leet, 'restart': self.restart, 'save': self.save, 'quit': self.quit, 'credits': self.credits}
		
	def credits(self):
		session.room.output = "Main Programmer: Kjetil Andre Liknes. Graphics: The Internet. Main Concept: Zed A. Shaw."
	
	def restart(self):
		session.room = maps.START
		web.seeother('/game')
		
	def save(self):
		pass
		
	def quit(self):
		pass

	def GET(self):
		if session.room:
			return render.show_room(room=session.room)
		else:
			return render.you_died()

			
	def POST(self):
		form = web.input(action=None)
		
		# This gets ugly, but until I get better, its all I can do...
		if form.action and session.room:
			if '*' in session.room.paths:
				if form.action != session.room.num and form.action not in self.commands:
					session.room.guess -= 1
					session.room.output = "BZZZTT!! Access Denied. You have %d tries left" % session.room.guess
					if session.room.guess == 0:
						session.room = session.room.go('*')
				elif form.action == session.room.num:
					session.room = session.room.go('x')			
			else:
				transition = session.room.go(form.action)
				if transition == None:
					session.room.output = "You can't do that."
				elif transition != None:
					session.room = transition
				else:
					session.room.output = "Please enter a command."
		
		if form.action in self.commands:
			self.commands[form.action]()
	
		web.seeother('/game')

		
if __name__ == '__main__':
	app.run()