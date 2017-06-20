from http.server import HTTPServer, BaseHTTPRequestHandler,SimpleHTTPRequestHandler
import cgi

#import curd operations and table name.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#bind our database to a engine that we can perform operation.
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()



def run(server_class=HTTPServer, handler_class = SimpleHTTPRequestHandler):
    try:
        server_address = ('', 8080)
        httpd = server_class(server_address, handler_class)
        print("Web server is running on port 8080")
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("^C interrupted, Stopping web server.")
        httpd.socket.close()


class WebServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header("Content-type", 'text/html')
                self.end_headers()
                message = ""
                message += '<html><body>Hello! I am great. try try and you will get success<br>' \
                           '<a href="http://localhost:8080/restaurants/new">Create a New Restaurant.</a>' \
                           '<br>%s</body></html>'

                items= session.query(Restaurant).all()
                restaurantString=''
                for item in items:
                    restaurantString += '%s<br><a href="http://localhost:8080/restaurants/%s/edit">Edit</a><br>' \
                                        '<a href="http://localhost:8080/restaurants/%s/delete">Delete</a><br><br>' % (item.name,item.id,item.id)
                message = message % restaurantString
                self.wfile.write(bytes(message, 'utf-8'))
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header("Content-type", 'text/html')
                self.end_headers()
                message = ""
                message += '<html><body>Hello! I am great. try try and you will get success<br>' \
                           '<form enctype="multipart/form-data"  method="post">' \
                           '<input type="text" name="restaurant" value=""><button type="submit" name="button"></button></form></body></html>'
                self.wfile.write(bytes(message, 'utf-8'))
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header("Content-type", 'text/html')
                self.end_headers()
                index=int(self.path.split('/')[2])
                data=session.query(Restaurant).filter_by(id=index).first()
                restaurantName=data.name

                message = ""
                message += '<!DOCTYPE html><html><head><meta charset="utf-8"><title>test</title>' \
                           '</head><body><form enctype="multipart/form-data" method="post"><h1>%s</h1>' \
                           '<input type="text" name="name" value="">' \
                           '<button type="submit" name="button" value="%s">submit</button></form></body></html>'
                self.wfile.write(bytes(message%(restaurantName,index), 'utf-8'))
                return
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header("Content-type", 'text/html')
                self.end_headers()
                index = int(self.path.split('/')[2])
                message = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>test</title>' \
                           '</head><body><form enctype="multipart/form-data" method="post">' \
                          '<h3>Are you sure you want to delete this</h3>' \
                          '<button type="submit" name="button" value="%s">Yes</button></form></body></html>'
                self.wfile.write(bytes(message%index,'utf-8'))
                return




        except IOError:
            self.send_error(404, "file not found %s" % self.path)


    def do_POST(self):
        # Doesn't do anything with posted data
        if self.path.endswith('/restaurants/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            if ctype == 'multipart/form-data':
                fields=cgi.parse_multipart(self.rfile, pdict)#here pdict gives boundary like from where to where is form.
                messagecontent = fields.get('restaurant')
                data = messagecontent[0].decode('utf-8')
                print(data)
                obje = Restaurant(name=data)
                session.add(obje)
                session.commit()
                self.send_response(301)
                self.send_header("Location", '/restaurants')
                self.end_headers()
                return

        if self.path.endswith("/edit"):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile,pdict)  # here pdict gives boundary like from where to where is form.
                messagecontent = fields.get('name')
                index = fields.get('button')
                restaName=messagecontent[0].decode('utf-8')
                index=int(index[0].decode('utf-8'))

                #Updating a record in SQLalchemy
                restObject=session.query(Restaurant).filter_by(id=index).one()
                restObject.name=restaName
                session.add(restObject)
                session.commit()#so easy

                self.send_response(301)
                self.send_header("Location", '/restaurants')
                self.end_headers()
                return

        if self.path.endswith('/delete'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile,
                                             pdict)  # here pdict gives boundary like from where to where is form.
                index = fields.get('button')[0].decode('utf-8')
                #update data
                restObj = session.query(Restaurant).filter_by(id=index).first()
                session.delete(restObj)
                session.commit()

                self.send_response(301)
                self.send_header("Location", '/restaurants')
                self.end_headers()
                return



if __name__ == "__main__":
    run(handler_class=WebServerHandler)
