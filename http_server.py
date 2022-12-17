import http.server

class server(http.server.ThreadingHTTPServer):
    def __init__(self, server_address, RequestHandlerClass , bind_and_activate) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

s = server(("127.0.0.1", 8080), None, False)
s.serve_forever()