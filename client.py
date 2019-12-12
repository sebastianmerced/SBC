import socket

def client(val0):
    host = socket.gethostname()  # get local machine name
    port = 8082 #debe ser el mismo port del server
    s = socket.socket()
    s.connect((host, port))
    string1 = val0
    print("Contacting server...")
    s.send(string1.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    print("Calculation Received from Server." )
    return data
    s.close()


