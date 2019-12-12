import socket
def server():
   host = socket.gethostname()  # get local machine name
   port = 8082 #debe ser el mismo port del cliente

   s = socket.socket()
   s.bind((host, port))
   print("Server is ready and listening")
   while True:
      s.listen(1)
      c, addr = s.accept()
      print("Connection from: " + str(addr))

      while True:
         data = c.recv(1024).decode('utf-8')
         if not data:
            break
         dataToReturn = eval(data)
         c.send(str(dataToReturn).encode('utf-8'))
	
   c.close()


if __name__ == '__main__':
   server()
