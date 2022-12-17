# python3
import os
import signal
import socket
import select
import time
from urllib.parse import unquote
import threading

# video streaming
import pickle
import cv2
import struct
import numpy
import math
import imutils
import base64
import pyaudio
import wave
# baking cookies
import secrets

thread_count = 0

# global udp_sock
# udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
# udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
# udp_sock.bind(("127.0.0.1", 9090))

# udp_sock.listen(10)


# Create server socket.
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind server socket to loopback network interface.
serv_sock.bind(('127.0.0.1', 8080))
serv_sock.setblocking(0)

# Turn server socket into listening mode.
serv_sock.listen(10)

sock_list = [serv_sock]
vid_sock = []

def long_wait(sock):
    print("waiting")
    time.sleep(10)
    print("awake")

def parse_req(message):
    message = message.split("\r\n")
    for m in message:
        if "Cookie:" in m:
            bis = m
            break
    else:
        bis = None
    return message[-1], bis

def format_html(args: str, biscuit: str):
    print("format args:", args)
    if args == '':
        # check for cookie status
        status, name = check_cookie(biscuit)
        if status == "in" and name != "":
            # get login info
            with open("data/user_data.txt", 'r') as f:
                lines = f.readlines()
                for line in lines:
                    usr, pw = line.strip("\n").split(",", 1)
                    if usr == name:
                        break

            with open("htmls/info.html", 'r') as f:
                content = f.read()
            return content.format(message="", name=name, password=pw), None
        else:
            with open("htmls/login.html", 'r') as f:
                content = f.read()
            return content.format(error_msg=""), None
        
    args = args.replace("+", " ")
    args = args.split("&")
    args = list(map(unquote, args))
    print("splitted:", args)
    if args[-1].startswith("signup="):
        # sign up
        print("signing up")
        if "%2C" in args[0][9:]:
            msg = f"Name cannot contain ','!"
            with open("htmls/login.html", 'r') as login_file:
                content = login_file.read()
            return content.format(error_msg=msg), None
        # print("no comma")
        with open("data/user_data.txt", 'r') as user_file:
            users = user_file.readlines()
            print(users)
            for user in users:
                print(user.strip("\n"))
            for user in users:
                user = user.strip("\n")
                username, pw = user.split(",", 1)
                print(username, pw)
                print(args[0][9:])
                print(username == args[0][9:])
                if username == args[0][9:]:
                    msg = f"Username taken"
                    break
            else:
                msg = f"Sign up success!"

        print("message:", msg)
        if msg == "Sign up success!":
            # status, name = check_cookie(biscuit)
            login_cookie(biscuit, args[0][9:])
            with open("data/user_data.txt", 'a') as user_file:
                user_file.write(f"{args[0][9:]},{args[1][9:]}\n")

            with open("htmls/info.html", 'r') as file:
                content = file.read()
            return content.format(message=msg, name=args[0][9:], password=args[1][9:]), args[0][9:]

        with open("htmls/login.html", 'r') as login_file:
            content = login_file.read()
            return content.format(error_msg=msg), None
            
    elif args[-1].startswith("login="):
        print("logging in")
        resp_name, resp_pw = args[0][9:], args[1][9:]

        password = get_pw(resp_name)
        if password == resp_pw:
            msg = "Welcome!"
            login_cookie(biscuit, resp_name)
            with open("htmls/info.html", 'r') as f:
                content = f.read()
            return content.format(message=msg, name=resp_name, password=resp_pw), resp_name
        else:
            msg = "Wrong username or password"
            with open("htmls/login.html", 'r') as html:
                content = html.read()
            return content.format(error_msg=msg), None

    elif args[-1].startswith("logout="):
        logout_cookie(biscuit, args[-1][7:])
        with open("htmls/login.html", 'r') as html:
            content = html.read()
        return content.format(error_msg=""), None

    elif args[-1].startswith("change_pw="):
        with open("htmls/change_pw.html", 'r') as html:
            content = html.read()
        return content.format(message="", name=args[0][10:]), args[0][10:]

    elif args[-1].startswith("confirm_pw="):
        resp_name, resp_old_pw, resp_new_pw = args[2][11:], args[0][7:], args[1][7:]
        print(resp_name, resp_old_pw, resp_new_pw)
        # flag = False

        password = get_pw(resp_name)

        if resp_old_pw == password:
            with open("data/user_data.txt", 'r') as user_file:
                lines = user_file.readlines()

            print(lines)
            with open("data/user_data.txt", 'w') as user_file:
                for line in lines:
                    if line.split(",")[0] == resp_name:
                        user_file.write(f"{resp_name},{resp_new_pw}\n")
                    else:
                        user_file.write(line)

            with open("htmls/info.html", 'r') as file:
                content = file.read()

            return content.format(message="Password changed!", name=resp_name, password=resp_new_pw), resp_name
        else:
            msg = "Wrong username or password!"
            with open("htmls/change_pw.html", 'r') as file:
                content = file.read()
                return content.format(message=msg, name=resp_name), resp_name
            
    elif args[-1].startswith("message="):
        with open("data/prev_msg.txt", 'r') as file:
            prev_msg = file.readlines()
            if len(prev_msg) > 15:
                prev_msg = prev_msg[-15:]
            prev_msg = "".join(prev_msg)
        
        with open("htmls/message.html", 'r') as file:
            content = file.read()
        return content.format(prev_msg=prev_msg, name=args[-1][8:]), args[-1][8:]

    elif args[-1].startswith("submit_msg="):
        resp_name, resp_msg = args[-1][11:], args[0][8:]
        if resp_msg == "":
            with open("data/prev_msg.txt", 'r') as file:
                prev_msg = file.readlines()
                if len(prev_msg) > 15:
                    prev_msg = prev_msg[-15:]
                prev_msg = "".join(prev_msg)
            
            with open("htmls/message.html", 'r') as file:
                content = file.read()
            return content.format(prev_msg=prev_msg, name=resp_name), resp_name
        with open("data/prev_msg.txt", 'a') as write_file:
            write_file.write(f"{time.ctime()}\t{resp_name}\t: {resp_msg}\n")
        
        with open("data/prev_msg.txt", 'r') as file:
            prev_msg = file.readlines()
            if len(prev_msg) > 15:
                prev_msg = prev_msg[-15:]
            prev_msg = "".join(prev_msg)
        print(prev_msg)
        
        with open("htmls/message.html", 'r') as file:
            content = file.read()
        return content.format(prev_msg=prev_msg, name=resp_name), resp_name

    elif args[-1].startswith("back_from_msg="):
        resp_name = args[-1][14:]
        print(resp_name)
        password = get_pw(resp_name)
        print(password)
        with open("htmls/info.html", 'r') as f:
            content = f.read()
        return content.format(message="", name=resp_name, password=password), resp_name

    elif args[-1].startswith("video="):
        resp_name = args[-1][6:]
        with open("htmls/video.html", 'r') as f:
            content = f.read()
        return content, resp_name

def get_pw(name):
    with open("data/user_data.txt", 'r') as file:
        users = file.readlines()
        for user in users:
            user_name, pw = user.strip("\n").split(",", 1)

            if name == user_name:
                return pw

def logout_cookie(biscuit, name):
    with open("data/cookie_data.txt", 'r') as file:
        lines = file.readlines()

    with open("data/cookie_data.txt", 'w') as file:
        for line in lines:
            b, n, s = line.strip("\n").split(",")
            if biscuit == b:
                file.write(f"{biscuit},,out\n")
            else:
                file.write(line)

def login_cookie(biscuit, name):
    with open("data/cookie_data.txt", 'r') as file:
        lines = file.readlines()

    with open("data/cookie_data.txt", 'w') as file:
        for line in lines:
            b, n, s = line.strip("\n").split(",")
            if biscuit == b:
                file.write(f"{biscuit},{name},in\n")
            else:
                file.write(line)

def check_cookie(biscuit):
    with open("data/cookie_data.txt", 'r') as file:
        lines = file.readlines()

    for line in lines:
        cooke, name, status = line.strip("\n").split(",")
        if biscuit == cooke:
            break
    else:
        print("cookie not found")

        with open("data/cookie_data.txt", 'a') as file:
            file.write(f"{biscuit},,out\n")
        
        return "out", ""
    
    return status, name

tds = []
def write_sock(sock, args, biscuit):
    # write to socket
    try:
        if biscuit is None:
            biscuit = f"Set-Cookie: {secrets.token_hex(16)}"
            login_status, name = check_cookie(biscuit[4:])
        else:
            login_status, name = check_cookie(biscuit)
        #     t = threading.Thread(target=long_wait, args=(sock,))
        #     t.start()
        #     tds.append(t)
        html_content, user = format_html(args, biscuit)

        # html_content = http_header + html_content
        http_header = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: 1024\r\n{biscuit}; Max-Age=86400\r\n\r\n"
        
        sock.sendall(http_header.encode())
        print("done")
        sock.sendall(html_content.encode())
        sock.close()
    except Exception as e:
        print(f"error: {e}")
        err_handle(sock, "404", "not found")

def err_handle(sock, code, msg):
    err_response = f'''HTTP/1.1 {code}
    Content-Type: text/html; charset=utf-8
    Content-Length: 1024

    
    <h1>{msg}</h1>

    '''
    try:
        # print(err_response)
        sock.sendall(err_response.encode())
    except:
        print("response err")

# def stream_video(sock, addr):
#     maxlen = 65536
    
#     # while 1:
#         # print("hello")
#         # vid = cv2.VideoCapture(0)
#         # indata, addr = sock.recvfrom(65536)
#     try:
#         print(addr)
#         WIDTH = 400
#         # print("revced")
#         vid = cv2.VideoCapture("never_gonna_give_you_up.mkv")
#         fps,st,frames_to_count,cnt = (0,0,20,0)
#         while vid.isOpened():
#             _,frame = vid.read()
#             if frame is None:
#                 # sock.close()
#                 break
#             frame = imutils.resize(frame,width=WIDTH)
#             encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
#             message = base64.b64encode(buffer)
#             sock.sendto(message,addr)
#             # frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
#             # cv2.imshow('TRANSMITTING VIDEO',frame)
#             key = cv2.waitKey(1) & 0xFF
#             if key == ord('q'):
#                 # sock.close()
#                 break
#             cnt+=1
#     except Exception as e:
#         print("video error:", e)
#         return
        # a = pickle.dumps(frame)
        # msg = struct.pack("Q", len(a))+a

        # sock.sendall(msg)

        # sock.sendto(frame.encode(), addr)

        # cv2.imshow("streaming", frame)

        # k = cv2.waitKey(1) & 0xff
        # if k == ord('q'):
        #     sock.close()
        #     break
    # vid.release()
    # vid_sock.remove(sock)
def stream_audio(sock):
    # s = socket.socket()
    # s.bind(("127.0.0.1", 9099))
    # s.listen(10)
    CHUNK = 4096
    print("streaming adu")
    try:

        wf = wave.open("never_gonna_give_you_up.wav", 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        input=True,
                        frames_per_buffer=CHUNK)
        # client_sock, addr = sock.accept()
        print("opened")
        while 1:
            data = wf.readframes(CHUNK)
            a = pickle.dumps(data)
            msg = struct.pack("Q", len(a))+a
            sock.sendall(msg)
    except Exception as e:
        print("audio error:", e)
        return

def stream_video(sock):
    maxlen = 65536
    try:
        # print(addr)
        WIDTH = 400
        # print("revced")
        vid = cv2.VideoCapture("never_gonna_give_you_up.mkv")
        fps,st,frames_to_count,cnt = (0,0,20,0)
        while vid.isOpened():
            _,frame = vid.read()
            if frame is None:
                # sock.close()
                break
            frame = imutils.resize(frame,width=WIDTH)
            encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)
            sock.sendall(message)
            # frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            # cv2.imshow('TRANSMITTING VIDEO',frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                # sock.close()
                break
            cnt+=1
    except Exception as e:
        print("video error:", e)
        return

# def video_splitter():
#     global udp_sock
#     while 1:
#         try:
#             _, addr = udp_sock.recvfrom(65536)
#             threading.Thread(target=stream_video, args=(udp_sock, addr)).start()
        
#         except KeyboardInterrupt:
#             print("ending threds")
#             break
#         except WindowsError as e:
#             print("winerror:", e)
#             udp_sock.close()
#             udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
#             udp_sock.bind(("127.0.0.1", 9090))
#             print("binded")
#         except Exception as e:
#             print("split error:", e)

def audio_splitter():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 9099))
    s.listen(10)

    while 1:
        try:
            cock, addr = s.accept()
            # cock.settimeout(10)
            data = cock.recv(65536)
            print("revced")
            threading.Thread(target=stream_audio, args=(cock, )).start()
        except KeyboardInterrupt:
            print("audio KBI")
            break
        except WindowsError as e:
            print("audio win error:", e)
        except Exception as e:
            print("audio split err:", e)

def video_splitter():
    # global udp_sock
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("127.0.0.1", 9090))
    udp_sock.listen(10)
    while 1:
        try:
            sock, addr = udp_sock.accept()
            sock.settimeout(10)
            data = sock.recv(65536)
            threading.Thread(target=stream_video, args=(sock,)).start()
        
        except KeyboardInterrupt:
            print("ending threds")
            break
        except WindowsError as e:
            print("winerror:", e)
            # udp_sock.close()
            # udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
            # udp_sock.bind(("127.0.0.1", 9090))
            print("binded")
        except Exception as e:
            print("split error:", e)

threading.Thread(target=video_splitter, args=()).start()
threading.Thread(target=audio_splitter, args=()).start()

print("server started, ctrl c to close")
while True:
    # Accept new connections in an infinite loop.

    # '''
    try:
        readable, writeable, errs = select.select(sock_list, [], sock_list, 1)

        for r in readable:
            if r == serv_sock:
                client_sock, client_addr = serv_sock.accept()
                client_sock.setblocking(0)
                sock_list.append(client_sock)
                print('New connection from', client_addr, client_sock)
            elif r not in vid_sock:
                data = r.recv(2048)

                print(data.decode())
                if (data.decode() == "video_client"):
                    vid_sock.append(r)
                    t = threading.Thread(target=stream_video, args=(r,))
                    t.start()
                    tds.append(t)
                else:
                    response, biscuit = parse_req(data.decode())
                    print(biscuit)
                    write_sock(r, response, biscuit)
                # r.close()

                
                sock_list.remove(r)
                print(vid_sock)

        for e in errs:
            print("error")
            sock_list.remove(e)
            e.close()
    except KeyboardInterrupt:
        print("purge everything")
        os.kill(os.getpid(), signal.SIGTERM)
        break