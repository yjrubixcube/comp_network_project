
# This is client code to receive video frames over UDP
import cv2, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
# BUFF_SIZE = 1024
# client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
# client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
# client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# host_name = socket.gethostname()
# host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
host_ip = input("Enter ip:")
print(host_ip)
port = 9090
message = b'Hello'
client_socket.connect((host_ip, port))

client_socket.sendall(message)
print("sent")
print("ctrl C to end video")
fps,st,frames_to_count,cnt = (0,0,20,0)
while True:
    try:
        # packet,_ = client_socket.recvfrom(BUFF_SIZE)
        packet = client_socket.recv(1024)
        start = packet.find(b'+++') + 3
        end = packet.find(b'+++', 1)
        # print(start, end)
        packet_len = packet[start:end]
        # print(packet)
        # packet_len = base64.b64decode(packet_len, " /")
        packet = packet[end+3:]
        remain = int(packet_len)
        # print(remain)
        while len(packet) < int(packet_len):
            p = client_socket.recv(remain)
            if p is None:
                break
            packet += p
            remain -= len(p)
        print("recv")
        # print(packet)
        # print(len(packet))
        data = base64.b64decode(packet,' /')
        # print(data)
        npdata = np.fromstring(data,dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)
        # print(not frame)
        print("dick")
        # frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.imshow("RECEIVING VIDEO",frame)
        print("shown")
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            # client_socket.close()
            break
        # cnt+=1
        client_socket.settimeout(2)
    except socket.timeout:
        print("timeout")
        # client_socket.close()
        break
    except KeyboardInterrupt:
        print("interrupt")
        break
    except Exception as e:
        print("error:", e)
        # break