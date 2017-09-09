import sys
import socket
import random
from hashlib import sha1
from Crypto.Util.number import *

HOST = 'ppc2.chal.ctf.westerns.tokyo'
PORT = 38264

n = 0xadd142708d464b5c50b936f2dc3a0419842a06741761e160d31d6c0330f2c515b91479f37502a0e9ddf30f7a18c71ef1eba993bdc368f7e90b58fb9fdbfc0d9ee0776dc629c8893a118e0ad8fc05633f0b9b4ab20f7c6363c4625dbaedf5a8d8799abc8353cb54bbfeab829792eb57837030900d73a06c4e87172599338fd5b1
g = 0x676ae3e2f70e9a5e35b007a70f4e7e113a77f0dbe462d867b19a67839f41b6e66940c02936bb73839d98966fc01f81b2b79c834347e71de6d754b038cb83f27bac6b33bf7ebd25de75a625ea6dd78fb973ed8637d32d2eaf5ae412b5222c8efea99b183ac823ab04219f1b700b207614df11f1f3759dea6d722635f45e453f6eae4d597dcb741d996ec72fe3e54075f6211056769056c5ad949c8becec7e179da3514c1f110ce65dc39300dfdce1170893c44f334a1b7260c51fb71b2d4dc6032e907bbaeebff763665e38cdfe418039dc782ae46f80e835bfd1ef94aeaba3ab086e61dab2ff99f600eb8d1cd3cf3fc952b56b561adc2de2097e7d04cb7c556
n2 = n * n
cipher = 0x2ab54e5c3bde8614bd0e98bf838eb998d071ead770577333cf472fb54bdc72833c3daa76a07a4fee8738e75eb3403c6bcbd24293dc2b661ab1462d6d6ac19188879f3b1c51e5094eb66e61763df22c0654174032f15613a53c0bed24920fd8601d0ac42465267b7eba01a6df3ab14dd039a32432003fd8c3db0501ae2046a76a8b1e56f456a2d40e2dd6e2e1ab77a8d96318778e8a61fe32d03407fc6a7429ec1fb66fc68c92e33310b3a574bde7818eb7089d392a30d07c85032a3d34fd589889ff6053fb19592dbb647a38063c5b403d64ee94859d9cf9b746041e5494ab7413f508d814c4b3bba29bca41d4464e1feb2bce27b3b081c85b455e035a138747

cbits = size(n2)
mbits = size(n)
shift = mbits // 2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def query(v):
    send = (hex(v) + '\n').encode('utf-8')
    print('<<<', hex(v))
    sock.send(send)
    line = b''
    while True:
        x = sock.recv(1)
        line += x
        if x == b'\n':
            break
    output = line.decode('utf-8').strip()
    print('>>>', output)
    return int(output)

bits = [0 for i in range(mbits + 1)]
bits[shift] = query(cipher)

# lower 
base = cipher
for i in range(1, shift + 1):
    add = pow(g, pow(2, shift - i), n2)
    res = query(base * add % n2)
    if res != bits[shift]:
        bits[shift - i] = 1
    else:
        bits[shift - i] = 0
        base = base * add % n2

# upper
base = cipher
inv2 = inverse(2, n)
message = 0
for i in range(shift + 1):
    if bits[i] == 1:
        message += 1 << i
x = 0
message_high = message
message_low = 0
for i in range(1, mbits - shift):
    base = pow(base, inv2, n2)
    inv2k = pow(inv2, i, n2)
    message_low += (message_high & 1) << (i - 1)
    message_high >>= 1
    res = query(base)
    expect = (message_high + message_low * inv2k) % n
    if ((expect >> shift) & 1) == res:
        bits[shift + i] = 0
    else:
        bits[shift + i] = 1
        message_high += 1 << shift
        message += 1 << (shift + i)


print('message:', hex(message))
print("TWCTF{" + sha1(str(message).encode("ascii")).hexdigest() + "}")