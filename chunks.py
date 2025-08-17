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
    
    def init(this , chunk):
        this.len = chunk.len
        this.name = chunk.name
        this.data = chunk.data
        this.CRC = chunk.CRC



class IDAT(Chunk):
    def __init__(this , chunk):
        super().init(chunk)

class Decoder:
    def __init__(this):
        this.idat = []
        this.chunk_type = { "IDAT" : this.idat }
        this.chunk_init = { "IDAT" : IDAT }

    def process(this , chunk):

        if chunk.name != "IDAT" : 
            return 0
        
        if chunk.name not in this.chunk_type:
            raise Exception("Chunk name unknwown")
        
        this.chunk_type[chunk.name].append(this.chunk_init[chunk.name](chunk))

    def solve_idat(this):
        data = b''

        for c in this.idat:
            data += c.data
        
        CMF = data[0]
        CM = (CMF & 0xF)
        CINFO = (CMF >> 4)

        if CM != 8:
            raise Exception("Unknown compression method")
        
        if CINFO != 7: 
            raise Exception("Unkonwn base")
        
        FLG = data[1]
        FCHECK = (FLG & 0x1F)
        FDICT = (FLG >> 5 & 1)
        FLEVEL = (FLG >> 6)

        if (CMF * 256 + FLG) % 31 != 0:
            raise Exception("FCHECK doesn't match")

        if FDICT == 1:
            raise Exception("Dict used")
        

        ADLER32 = int.from_bytes(data[len(data) - 4 : ] , 'big')
        data = data[2 : data[len(data) - 4]]
        