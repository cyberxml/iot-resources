import pyDes
import os, sys

# Encryption key is a slightly variation of "NtgrBak"
KEY = [0x56-8, 0x74, 0x67, 0x72, 0x42, 0x61, 0x6b, 0x00]

def derive_des_key(ascii_key):
    def extract_by_offset(offset):
        byte_index = offset >> 3
        bit_index  = byte_index << 3

        v0 = (ascii_key[byte_index] << 8) | ascii_key[byte_index+1]
        v1 = 8 - (offset - bit_index)
        v0 >>= v1
        return v0 & 0xfe

    k = ""
    for i in range(0, 7*8, 7):
        k += chr(extract_by_offset(i))
    return k

def decrypt_block(block, key_bytes):
    k = derive_des_key(key_bytes)
    des = pyDes.des(k, pyDes.ECB)
    r = des.decrypt(block)
    return r

def main():
    data = sys.stdin.read()
    print("processing ... "+str(len(data)))
    assert (len(data) % 8) == 0

    current_key = KEY[:]

    r = ""
    for i in range(0, len(data), 8):
        current_key[0] += 8
        if current_key[0] > 0xff:
            current_key[0] = current_key[0] - 0x100
            current_key[1] += 1

        block = data[i:i+8]
        d = decrypt_block(block, current_key)

        r += d

    sys.stdout.write(r)


main()
