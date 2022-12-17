import socket
import threading
import time
import http.server

http_header = "HTTP/1.1 200 OK\r\n\Content-Type: text/html; charset=utf-8\r\nContent-Length: 1024\r\n\r\n"

users = []

def init_server():
    print("server init")
    global serv_sock
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.setblocking(1)

    try:
        serv_sock.bind(("127.0.0.1", 8080))
    except Exception as e:
        print(e)

    serv_sock.listen(10)

    print("done")
    run()

def new_connection(sock, addr):
    while 1:
        try:
            # data = sock.recv(2048)
            # print(data)
            # break
            sock.sendall(http_header.encode())
            print("send http")
            with open("login.html", 'r') as f:
                html_content = f.read()

            sock.sendall(html_content.encode())
            print("sned html")
            # time.sleep(1)
            # sock.close()
            # return
            data = sock.recv(4096)
            if data:
                print(data.decode())
            else:
                raise ZeroDivisionError
            # break
        
        except Exception as e:
            print(e)
            sock.close()
            return False

def run():
    # try:
        while 1:
            client_sock, client_addr = serv_sock.accept()
            print(client_addr, client_sock)
            data = client_sock.recv(2048)
            print(data)
            # users[client_addr] = client_sock
            t = threading.Thread(target=new_connection, args=(client_sock, client_addr))
            t.start()
            users.append(t)
            print(users)
    # except KeyboardInterrupt:
    #     print("stop")
    # finally:
    #     if serv_sock:
    #         serv_sock.close()
    #     for t in users:
    #         t.join()


if __name__ == "__main__":
    init_server()
    # while 1:
    #     c = input()
    #     if c == "exit":
    #         shutdown()
    #         break