# '''
import socket

# Create client socket.
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server (replace 127.0.0.1 with the real server IP).
client_sock.connect(('127.0.0.1', 8080))

# Send some data to server.
# client_sock.sendall(b'Hello, world')
# client_sock.shutdown(socket.SHUT_WR)

msg = 'video_client'
msg = f"*{len(msg)}*{msg}"
msg = msg.encode()
total_sent = 0
while total_sent < len(msg):
    sent = client_sock.send(msg[total_sent:])
    if sent == 0:
        print("broken")
        break
    total_sent += sent

# Receive some data back.
chunks = []
while True:
    data = client_sock.recv(2048)
    print(data)
    if not data:
        break
    chunks.append(data)
print('Received', repr(b''.join(chunks)))

# Disconnect from server.
client_sock.close()
# '''

# import socket
# ClientMultiSocket = socket.socket()
# host = '127.0.0.1'
# port = 8080
# print('Waiting for connection response')
# try:
#     ClientMultiSocket.connect((host, port))
# except socket.error as e:
#     print(str(e))
# res = ClientMultiSocket.recv(1024)
# while True:
#     Input = input('Hey there: ')
#     ClientMultiSocket.send(str.encode(Input))
#     res = ClientMultiSocket.recv(1024)
#     print(res.decode('utf-8'))
# ClientMultiSocket.close()