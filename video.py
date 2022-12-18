
# This is client code to receive video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
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
fps,st,frames_to_count,cnt = (0,0,20,0)
while True:
    try:
        # packet,_ = client_socket.recvfrom(BUFF_SIZE)
        packet = client_socket.recv(BUFF_SIZE)
        data = base64.b64decode(packet,' /')
        npdata = np.fromstring(data,dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)
        # frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.imshow("RECEIVING VIDEO",frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            # client_socket.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count/(time.time()-st))
                st=time.time()
                cnt=0
            except:
                pass
        cnt+=1
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
        break