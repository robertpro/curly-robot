#!/usr/bin/env python3

import socket
import struct
import re

class EV3():
    def __init__(self, host: str):
        # listen on port 3015 for a UDP broadcast from the EV3
        UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPSock.bind(('', 3015))
        data, addr = UDPSock.recvfrom(67)

        # pick serial number, port, name and protocol
        # from the broadcast message
        matcher = re.search('Serial-Number: (\w*)\s\n' +
                            'Port: (\d{4,4})\s\n' +
                            'Name: (\w+)\s\n' +
                            'Protocol: (\w+)\s\n',
                            data.decode('utf-8'))
        serial_number = matcher.group(1)
        port = matcher.group(2)
        name = matcher.group(3)
        protocol = matcher.group(4)
        if serial_number.upper() != host.replace(':', '').upper():
            self._socket = None
            raise ValueError('found ev3 but not ' + host)

        # Send an UDP message back to the EV3
        # to make it accept a TCP/IP connection
        UDPSock.sendto(' '.encode('utf-8'), (addr[0], int(port)))
        UDPSock.close()

        # Establish a TCP/IP connection with EV3s address and port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((addr[0], int(port)))

        # Send an unlock message to the EV3 over TCP/IP
        msg = ''.join([
            'GET /target?sn=' + serial_number + 'VMTP1.0\n',
            'Protocol: ' + protocol
        ])
        self._socket.send(msg.encode('utf-8'))
        reply = self._socket.recv(16).decode('utf-8')
        if not reply.startswith('Accept:EV340'):
            raise IOError('No wifi connection to ' + name + ' established')

    def __del__(self):
        if isinstance(self._socket, socket.socket):
            self._socket.close()

    def send_direct_cmd(self, ops: bytes, local_mem: int=0, global_mem: int=0) -> bytes:
        cmd = b''.join([
            struct.pack('<h', len(ops) + 5),
            struct.pack('<h', 42),
            DIRECT_COMMAND_REPLY,
            struct.pack('<h', local_mem*1024 + global_mem),
            ops
        ])
        self._socket.send(cmd)
        print_hex('Sent', cmd)
        reply = self._socket.recv(5 + global_mem)
        print_hex('Recv', reply)
        return reply

def print_hex(desc: str, data: bytes) -> None:
    print(desc + ' 0x|' + ':'.join('{:02X}'.format(byte) for byte in data) + '|')

DIRECT_COMMAND_REPLY = b'\x00'
opNop = b'\x01'
my_ev3 = EV3('00:16:53:5E:89:BD')
ops_nothing = opNop
my_ev3.send_direct_cmd(ops_nothing)