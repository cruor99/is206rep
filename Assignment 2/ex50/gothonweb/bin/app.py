import web

urls = (
  '/', 'Index'
)

app = web.application(urls, globals())

class index:
    def GET(self):
        greeting = "Hello World"
        return render.index(greeting = greeting)

if __name__ == "__main__":
    app.run()