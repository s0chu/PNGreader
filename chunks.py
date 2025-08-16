from collections import deque

class Chunk:
    def CRC_validator(this):
        bin = ''.join(''.join(reversed(format(ord(j) , "08b"))) for j in this.name)
        bin = bin + ''.join(''.join(reversed(format(j , "08b"))) for j in this.data)
        bin = [(ord(j) - ord('0')) for j in bin]
        
  
        divisor = [0 for j in range(0 , 32)]

        for j in [26 , 23 , 22 , 16 , 12 , 11 , 10 , 8 , 7 , 5 , 4 , 2 , 1 , 0]:
            divisor[j] = 1
        
        divisor = [i for i in reversed(divisor)]
  
  
        rem = [1 for i in range(0 , 32)]

        for i in bin:
            rem[0] ^= i
            msb = rem.pop(0)
            rem.append(0)

            if(msb == 1):
                for i in range(0 , 32):
                    rem[i] = rem[i] ^ divisor[i]

        rem = [i for i in reversed(rem)]

        for i in range(0 , 32):
            rem[i] = 1 - rem[i]

        crc = ''.join(''.join(chr(i + ord('0')) for i in rem))
        return int(crc , 2) == this.CRC

    def __init__(this , file):
        this.len = int.from_bytes(file.read(4) , 'big')
        this.name = str(file.read(4) , encoding = "utf-8")
        this.data = file.read(this.len)
        this.CRC = int.from_bytes(file.read(4) , 'big')

        if(this.CRC_validator() == 0):
            raise Exception("CRC invalid, send was compromised")
    

