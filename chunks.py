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

        if chunk.name not in this.chunk_type:
        #    raise Exception("Chunk name unknwown") 
            return
        #debugging purposes
        
        this.chunk_type[chunk.name].append(this.chunk_init[chunk.name](chunk))
    
    def next_bit(this):
        this.curr_byte = 0

        while this.curr_byte < len(this.data):
            this.pos_bit = -1

            while this.pos_bit <= 6: 
                this.pos_bit += 1
                yield this.data[this.curr_byte] >> this.pos_bit & 1

            this.curr_byte += 1

    def is_border_bit(this):
        return this.pos_bit == 7
    
    def solve_idat(this):
        this.data = b''

        for c in this.idat:
            this.data += c.data
        
        CMF = this.data[0]
        CM = (CMF & 0xF)
        CINFO = (CMF >> 4)

        if CM != 8:
            raise Exception("Unknown compression method")
        
        if CINFO != 7: 
            raise Exception("Unkonwn base")
        
        FLG = this.data[1]
        FCHECK = (FLG & 0x1F) #useless, ales doar ca sa faca CMF | FLG M31
        FDICT = (FLG >> 5 & 1) 
        FLEVEL = (FLG >> 6)

        if (CMF * 256 + FLG) % 31 != 0:
            raise Exception("FCHECK doesn't match")

        if FDICT == 1:
            raise Exception("Dict used")
        

        ADLER32 = int.from_bytes(this.data[len(this.data) - 4 : ] , 'big')
        this.data = this.data[2 : this.data[len(this.data) - 4]]
