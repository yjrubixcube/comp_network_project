import socket, pyaudio, pickle, struct

# def audo():
p = pyaudio.PyAudio()
CHUNK = 4096
stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate=44100,
                output=True,
                frames_per_buffer=CHUNK)

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
host_ip = input("Enter ip:")
sock_addr = (host_ip, 9099)
client_sock.connect(sock_addr)
client_sock.sendall("hello".encode())
print("sent")
data = b''
p_sz = struct.calcsize("Q")
print("ctrl C to stop")
while 1:
    try:
        while len(data) < p_sz:
            packet = client_sock.recv(CHUNK)
            if not packet:
                break
            data += packet
        pms = data[:p_sz]
        data = data[p_sz:]
        msg_sz = struct.unpack("Q", pms)[0]
        while len(data) < msg_sz:
            # data += client_sock.recv(CHUNK)
            packet = client_sock.recv(CHUNK)
            if not packet:
                break
            data += packet
        frame_data = data[:msg_sz]
        data = data[msg_sz:]
        frame = pickle.loads(frame_data)
        stream.write(frame)
        client_sock.settimeout(2)
    except socket.timeout:
        print("timeout")
        break
    except KeyboardInterrupt:
        print("KBE")
        break
    except Exception as e:
        print("E", e)
        break
client_sock.close()

# audo()