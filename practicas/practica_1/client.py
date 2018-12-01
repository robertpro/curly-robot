#!/usr/bin/env python

# socket_echo_client.py
import socket
import sys
import click

def connect():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    return sock


@click.command()
@click.option('--message', help="Message to send")
def send_message(message):
    """
    Send messages to server\n
    *Caution* "stop" message will stop the server
    """
    sock = connect()
    try:
    
        # Send data
        #message = b'This is the message.  It will be repeated.'
        #print('sending {!r}'.format(message))
        print('sending ' + message)
        sock.sendall(message.encode())
    
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
    
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received {!r}'.format(data))
    
    finally:
        print('closing socket')
        sock.close()

if __name__ == "__main__":
    send_message()
