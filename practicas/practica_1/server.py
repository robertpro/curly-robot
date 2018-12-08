#!/usr/bin/env python

# socket_echo_server.py
import socket
import sys
import fire

class Server(object):
    """
    The server its going to receive and reply all messages
    """
    
    def should_i_stop(self, message):
        if message.upper() == "STOP":
            print("Stopping server..!!")
            return True
        else:
            return False

    def start(self):
        """
        This function will start the server, to listen for messages
        """
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the port
        server_address = ('localhost', 10000)
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)
        
        # Listen for incoming connections
        sock.listen(1)
        
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = sock.accept()
            try:
                print('connection from', client_address)
        
                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    print('received {!r}'.format(data))
                    if data:
                        print('sending data back to the client')
                        connection.sendall(data)
                        if self.should_i_stop(data.decode()):
                            return None
                    else:
                        print('no data from', client_address)
                        break
        
            finally:
                # Clean up the connection
                connection.close()

if __name__ == "__main__":
    s = Server()
    fire.Fire(s)
