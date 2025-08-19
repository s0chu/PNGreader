import decoder
import pixel

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

class IHDR(Chunk):
    def __init__(this , chunk):
        super().init(chunk)
        this.width =              int.from_bytes(this.data[ 0 :  4] , "big")
        this.height =             int.from_bytes(this.data[ 4 :  8] , "big")
        this.bit_depth =          int.from_bytes(this.data[ 8 :  9] , "big")
        this.color_type =         int.from_bytes(this.data[ 9 : 10] , "big")
        this.compression_method = int.from_bytes(this.data[10 : 11] , "big")
        this.filter_method =      int.from_bytes(this.data[11 : 12] , "big")
        this.interlace_method =   int.from_bytes(this.data[12 : 13] , "big")
    
    def print(this):
        print(f"Resolution: {this.height} X {this.width}")
        print(f"Color Type: {this.color_type}")
        print(f"Interlace: {True if this.interlace_method == 1 else False}")


class PLTE(Chunk):
    def __init__(this , chunk):
        super().init(chunk)
        
        if this.len % 3 != 0:
            raise Exception("PLTE chunk invalid")
        
        aux = decoder.Decoder()
        aux.sample_bit_iter = aux.sample_bit_func(this.data)

        palette_entries = this.len // 3
        this.palette = []

        for i in range(0 , palette_entries):
            color = pixel.Pixel_2(8 , aux.read_sample)
            this.palette.append(color)

    

idat = []
ihdr = []
plte = []

chunk_type = { "IDAT" : idat , "IHDR" : ihdr , "PLTE" : plte }
chunk_init = { "IDAT" : IDAT , "IHDR" : IHDR , "PLTE" : PLTE } 