from http.server import HTTPServer, BaseHTTPRequestHandler,SimpleHTTPRequestHandler
import cgi


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
            if self.path.endswith("/what"):
                self.send_response(200)
                self.send_header("Content-type", 'text/html')
                self.end_headers()
                message = ""
                message += "<html><body>Hello! I am great. try try and you will get success</body></html>"
                self.wfile.write(bytes(message, 'utf-8'))
                print(message)
                return

            if self.path.endswith("/namaste"):
                self.send_response(200)
                self.send_header("Content-type", 'text/html')
                self.end_headers()
                message = ""
                message += '<!DOCTYPE html><html><head><meta charset="utf-8"><title>test</title>' \
                           '</head><body><form enctype="multipart/form-data" action="/namaste" method="post"><h1>%s</h1><input type="text" name="name" value="">' \
                           '<button type="submit" name="button">submit</button></form></body></html>'
                self.wfile.write(bytes(message, 'utf-8'))
                return

        except IOError:
            self.send_error(404, "file not found %s" % self.path)


    def do_POST(self):
        # Doesn't do anything with posted data
        self.send_response(301)
        self.send_header("Content-type", 'text/html')
        self.end_headers()
        ctype,pdict=cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary']=bytes(pdict['boundary'],'utf-8')
        print(pdict)
        if ctype=='multipart/form-data':
            fields=cgi.parse_multipart(self.rfile, pdict)#here pdict gives boundary like from where to where is form.
            print(fields)
            messagecontent=fields.get('name')
            data=messagecontent[0].decode('utf-8')
            message = ""
            message += '<!DOCTYPE html><html><head><meta charset="utf-8"><title>test</title>' \
                       '</head><body><form enctype="multipart/form-data" action="/namaste" method="post"><h1>%s</h1><input type="text" name="name" value="">' \
                       '<button type="submit" name="button">submit</button></form></body></html>'%data
            self.wfile.write(bytes(message,'utf-8'))#it takes a byte object.
            return


if __name__ == "__main__":
    run(handler_class=WebServerHandler)
