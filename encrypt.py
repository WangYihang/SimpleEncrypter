#!/usr/bin/env python
# coding:utf-8

from string import maketrans
import sys

SIZE = 0x10

def trans(text, intab, outtab):
    length = len(intab)
    for i in range(length):
        text = text.replace(intab[i], outtab[i])
    return text

def getInTable():
    '''
    临时密文可行域
    '''
    global SIZE
    inTable = []
    for i in range(SIZE):
        inTable.append(chr(i))
    return inTable

def getOutTable():
    '''
    密文可行域
    '''
    global SIZE
    outTable = []
    inTable = getInTable()
    for i in inTable:
        outTable.append(chr(ord(i) + ord("A")))
    return outTable

def replace(cipher, FLAG):
    '''
    将临时密文的所有字节映射到密文可行域
    '''
    intab = getInTable()
    outtab = getOutTable()
    if len(intab) != len(outtab):
        print "转换表长度不同"
        exit(2)
    if FLAG == "e":
        return trans(cipher, intab, outtab)
    elif FLAG == "d":
        return trans(cipher, outtab, intab)
    else:
        return cipher

def encrypt(plain):
    global SIZE
    cipher = ""
    for i in plain:
        # 0xAB
        cipher += chr((ord(i) / SIZE)) # A
        cipher += chr((ord(i) % SIZE)) # B
    cipher = replace(cipher, "e")
    return cipher

def decrypt(cipher):
    cipher = replace(cipher, "d")
    plain = ""
    for i in range(0, len(cipher), 2):
        plain += chr((ord(cipher[i])) * SIZE + (ord(cipher[i+1])))
    return plain

def printHelp():
    print "Usage : "
    print "        python encrypt.py [e|d] [FILE_PATH]"

def main():
    if (len(sys.argv) != 3):
        printHelp()
        exit(1)
    command = sys.argv[1]
    filename = sys.argv[2]
    if command == "e":
        with open(filename, "r") as f:
            plain = f.read()
        print "=" * 32
        print "[PLAIN] => [%s] : " % (str(len(plain)) + " Bytes")
        print plain
        cipher = encrypt(plain)
        print "=" * 32
        print "[CIPHER] => [%s] : " % (str(len(cipher)) + " Bytes")
        print cipher
        print "=" * 32
    elif command == "d":
        with open(filename, "r") as f:
            cipher = f.read()
        print "=" * 32
        print "[CIPHER] => [%s] : " % (str(len(cipher)) + " Bytes")
        print cipher
        plain = decrypt(cipher)
        print "=" * 32
        print "[PLAIN] => [%s] : " % (str(len(plain)) + " Bytes")
        print plain
        print "=" * 32
    else:
        printHelp()

if __name__ == "__main__":
    main()
