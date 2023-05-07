import socket
import select

port = int(input("type the server Port: ")) # the port you want to listen on

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set the SO_REUSEADDR option to allow the socket to reuse a local address
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to a port
s.bind((socket.gethostname(), port))

# listen for incoming connections
s.listen(20)

# set up a list of sockets to monitor for incoming data
inputs = [s]

while True:
    # use the select module to monitor the list of input sockets for incoming data
    read_sockets, _, _ = select.select(inputs, [], [])

    # loop through the list of sockets with incoming data
    for sock in read_sockets:
        # if the socket is the server socket, accept the incoming connection
        if sock == s:
            conn, addr = sock.accept()
            inputs.append(conn)
            print(f"New connection from {addr}")
            message = "Welcome to the server! Enter quit to exit \n"
            conn.send(message.encode("utf-8"))

        # if the socket is a client socket, receive and process the incoming data
        else:
            data = sock.recv(1024)
            if data:
                # check if the received message is "quit"
                if data.decode().strip() == "quit":
                    sock.send("Goodbye!".encode("utf-8"))
                    print(f"Closing connection with {sock.getpeername()}")
                    sock.close()
                    inputs.remove(sock)
                print(f"Received message: {data.decode()}")
            else:
                sock.close()
                inputs.remove(sock)


