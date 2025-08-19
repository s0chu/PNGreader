import chunks
import trie
import math
import pixel
import time
import ansii

class Decoder:
    def __init__(this):
        return

    def process(this , chunk):

        if chunk.name not in chunks.chunk_type:
        #    raise Exception("Chunk name unknwown") 
            return
        #debugging purposes
        
        chunks.chunk_type[chunk.name].append(chunks.chunk_init[chunk.name](chunk))
    
    def next_bit(this):
        return next(this.bit_iter)
    
    def next_bit_func(this):
        this.curr_byte = 0

        while this.curr_byte < len(this.data):
            this.pos_bit = -1

            while this.pos_bit <= 6: 
                this.pos_bit += 1
                yield this.data[this.curr_byte] >> this.pos_bit & 1

            this.curr_byte += 1

        raise Exception("End of DATA")

    def is_border_bit(this):
        return this.pos_bit == 7
    
    def skip_byte(this):
        while this.is_border_bit() == 0:
            this.next_bit()
        
    def read(this , len , endian):
        res = []

        for i in range(0 , len):
            res += [this.next_bit()]

        if endian == "little":
            res = [i for i in reversed(res)]

        if endian != "little" and endian != "big":
            raise Exception("bad reading bytes")
        
        return ''.join([chr(i + ord('0')) for i in res])    
    
    def read_byte(this):
        return int(this.read(8 , 'little') , 2)

    def handle_no_compression(this):
        this.skip_byte()
        
        LEN_bits = this.read(16 , 'little')
        NLEN_bits = this.read(16 , 'little')

        for i in range(0 , 16):
            if(LEN_bits[i] == NLEN_bits[i]):
                raise Exception("No compression NLEN not complement")
            
        LEN = int(LEN_bits , 2)
        NLEN = int(NLEN_bits , 2)

        for i in range(LEN):
            this.png_data.append(this.read_byte())

    class Table:
        def __init__(this):
            return
        
    def prepare_for_reading(this):
        this.distance = Decoder.Table()
        this.length = Decoder.Table()

        this.length.extra_bits = [-1 for i in range(0 ,  300)]
        this.length.lengths = [-1 for i in range(0 ,  300)]

        bits = [0 , 0 , 0 , 0 , 0 , 0, 0 , 0 , 1 , 1 , 1 , 1 , 2 , 2 , 2 , 2 , 3 , 3 , 3 , 3 , 4 , 4 , 4 , 4 , 5 , 5 , 5 , 5 , 0]
        lens = [3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 13 , 15, 17 , 19 , 23 , 27 , 31 , 35 , 43 , 51 , 59 , 67 , 83 , 99 , 115 , 131 , 163 , 195 , 227 , 258]

        for i in range(0 , len(bits)):
            this.length.extra_bits[i + 257] = bits[i]
            this.length.lengths[i + 257] = lens[i]

        this.distance.extra_bits = [-1 for i in range(0 ,  30)]
        this.distance.lengths = [-1 for i in range(0 ,  30)]

        bits = [0 , 0 , 0 , 0 , 1 , 1 , 2 , 2 , 3 , 3 , 4 , 4 , 5 , 5 , 6 , 6 , 7 , 7 , 8 , 8 , 9 , 9, 10 , 10 , 11 , 11 , 12 , 12 , 13 , 13]
        lens = [1 , 2 , 3 , 4 , 5 , 7 , 9 , 13 , 17 , 25 , 33 , 49 , 65 , 97 , 129 , 193 , 257 , 385 , 513 , 769 , 1025 , 1537 , 2049 , 3073 , 4097 , 6145 , 8193 , 12289 , 16385 , 24577]
  
        for i in range(0 , len(bits)):
            this.distance.extra_bits[i] = bits[i]
            this.distance.lengths[i] = lens[i]

    def get_value(this , trie):
        node = 1
        code = []

        while trie.end_of_code[node] == -1:
            bit = ord(this.read(1 , 'big')[0]) - ord('0')
            code.append(bit)

            if bit not in [0 , 1]:
                raise Exception("bit error")
            
            if trie.trie[node][bit] == -1:
                #print(code)
                raise Exception("Bad Trie")
        
            node = trie.trie[node][bit]            
            
        #print(f'value: {trie.end_of_code[node]}  with code: {code}')
        return trie.end_of_code[node]

    def prepare_fixed_huffman_code(this):
        this.huffman_literal = Decoder.Table()
        this.huffman_dist = Decoder.Table()

        lens = [0 for i in range(0 , 288)]

        for i in range(0 , 144):
            lens[i] = 8

        for i in range(144 , 256):
            lens[i] = 9

        for i in range(256 , 280):
            lens[i] = 7

        for i in range(280 , 288):
            lens[i] = 8

        this.huffman_literal.alphabet = [i for i in range(0 , 288)]
        this.huffman_literal.lengths = lens

        this.huffman_dist.alphabet = [i for i in range(0 , 32)]
        this.huffman_dist.lengths = [5 for i in range(0 , 32)]

    def decode(this , trie_len , n):
        result = []

        while len(result) < n:
            value = this.get_value(trie_len)

            if value <= 15:
                result.append(value)
            elif value == 16:
                repeat = int(this.read(2 , "little") , 2) + 3
                
                for i in range(0 , repeat):
                    result.append(result[len(result) - 1])

            elif value == 17:
                repeat = int(this.read(3 , "little") , 2) + 3
                
                for i in range(0 , repeat):
                    result.append(0)
            elif value == 18:
                repeat = int(this.read(7 , "little") , 2) + 11
            
                for i in range(0 , repeat):
                    result.append(0)
            else:
                raise Exception("Uknown value")
        if len(result) > n:
            raise Exception(f"bad encoding of huffman lengths | {len(result)} | {n}")
        
        return result

    def prepare_dynamic_huffman_code(this):
        len_alphabet = [16 , 17 , 18 , 0 , 8 , 7 , 9 , 6 , 10 , 5 , 11 , 4 , 12 , 3 , 13 , 2 , 14 , 1 , 15]
        len_code = [0 for i in range(0 , len(len_alphabet))]
        
        HLIT  = int(this.read(5 , 'little') , 2)
        HDIST = int(this.read(5 , 'little') , 2)
        HCLEN = int(this.read(4 , 'little') , 2)

        for i in range(0 , HCLEN + 4):
            len_code[i] = int(this.read(3 , "little") , 2)

        #print(f'HLIT: {HLIT + 257} | HDIST: {HDIST + 1} | HCLEN: {HCLEN + 4}')

        len_code = len_code[0 : HCLEN + 4]
        len_alphabet = len_alphabet[0 : HCLEN + 4]

        trie_len = trie.Trie(len_code , len_alphabet)

        this.huffman_literal = Decoder.Table()
        this.huffman_dist = Decoder.Table()

        this.huffman_literal.alphabet = [i for i in range(0 , HLIT + 257)]
        this.huffman_dist.alphabet = [i for i in range(0 , HDIST + 1)]

        this.huffman_literal.lengths = this.decode(trie_len , HLIT + 257)
        this.huffman_dist.lengths = this.decode(trie_len , HDIST + 1)

        del trie_len

    def read_blocks(this):
        this.png_data = []
        this.bit_iter = this.next_bit_func();
        this.prepare_for_reading()
        count_block = 0

        start_time = time.time()

        while 1:
            header = this.read(1 , "little") + this.read(2 , "little")
            BFINAL = header[0]
            BTYPE = header[1:]

            count_block += 1
            #print(f'Block no. {count_block} >> Compression Method: {BTYPE}')

            if BTYPE == "11":
                raise Exception("Block error")
            if BTYPE == "00":
                this.handle_no_compression()
            else:
                if BTYPE == "10":
                    this.prepare_dynamic_huffman_code()
                else:
                    this.prepare_fixed_huffman_code()

                trie_len = trie.Trie(this.huffman_literal.lengths , this.huffman_literal.alphabet)
                trie_dist = trie.Trie(this.huffman_dist.lengths , this.huffman_dist.alphabet)

                values_read = 0

                while 1:
                    value = this.get_value(trie_len)

                    values_read += 1
                    #print(f"values read: {values_read}")
                    if value == 256:
                        break
                    elif value < 256:
                        this.png_data.append(value)
                    else:
                        length = this.length.lengths[value]
                        extra = this.length.extra_bits[value] 
                        
                        if extra != 0:
                            length += int(this.read(extra , 'little') , 2)

                        value = this.get_value(trie_dist)
                        distance = this.distance.lengths[value]
                        extra = this.distance.extra_bits[value]

                        if extra != 0:
                            distance += int(this.read(extra , 'little') , 2)

                        ind = len(this.png_data) - 1 - distance + 1

                        #print(f'{distance}')
                        
                        for i in range(0 , length):
                            this.png_data.append(this.png_data[ind])
                            ind += 1

                del trie_len
                del trie_dist

            if BFINAL == '1':
                break
            
        #this.read(3 , 'little')
        end_time = time.time()
        time_elapsed = end_time - start_time
        time_elapsed = f"{time_elapsed:.2f}"

        print(f"Blocks read: {ansii.color(255, 0, 98 , count_block)} in {ansii.color(0 , 255 , 191 , time_elapsed)} seconds")
    def ADLER32_validator(this , checksum):
        s1 = 1
        s2 = 0
        MOD = 65521

        for byte in this.png_data:
            s1 += byte
            s1 %= MOD

            s2 += s1
            s2 %= MOD
        
        adler = s2 * 65536 + s1
        #print(f'adler32: {checksum} | decompressed: {adler}')
        return adler == checksum
    
    def paeth_predictor(this , a , b , c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)

        if pa <= pb and pa <= pc:
            return a
        elif pb <= pc:
            return b
        else:
            return c
        
    def filter_method_0(this , scanlines , idx , bpp , value):
        return value
    
    def filter_method_1(this , scanlines , idx , bpp , value):
        return (value + (0 if idx - bpp < 0 else scanlines[1][idx - bpp])) % (1 << 8)

    def filter_method_2(this , scanlines , idx , bpp , value):
        return (value + scanlines[0][idx]) % (1 << 8)

    def filter_method_3(this , scanlines , idx , bpp , value):
        return (value + math.floor( (((0 if idx - bpp < 0 else scanlines[1][idx - bpp]) + scanlines[0][idx]) & 0xFF)  / 2 )) % (1 << 8)
    
    def filter_method_4(this , scanlines , idx , bpp , value):
        return (value + this.paeth_predictor( (0 if idx - bpp < 0 else scanlines[1][idx - bpp]) , scanlines[0][idx] , (0 if idx - bpp < 0 else scanlines[0][idx - bpp]) )) % (1 << 8)
    
    def sample_bit_func(this , bytestream):
        for byte in bytestream:
            pos = 8

            while pos > 0:
                pos -= 1
                yield byte >> pos & 1

    def sample_bit(this):
        return next(this.sample_bit_iter)
    
    def read_sample(this , n):
        sample = 0

        for i in range(0 , n):
            sample = sample * 2 + this.sample_bit()
        
        return sample
    
    def parse_png_data(this , IHDR):
        bpp_table = [ [0 for i in range(0 , 17)] for j in range(0 , 7) ]
        
        bpp_table[0][ 1] = 1
        bpp_table[0][ 2] = 1
        bpp_table[0][ 4] = 1
        bpp_table[0][ 8] = 1
        bpp_table[0][16] = 2

        bpp_table[2][ 8] = 3
        bpp_table[2][16] = 6

        bpp_table[3][1] = 1
        bpp_table[3][2] = 1
        bpp_table[3][4] = 1
        bpp_table[3][8] = 1

        bpp_table[4][ 8] = 2
        bpp_table[4][16] = 4 

        bpp_table[6][ 8] = 4
        bpp_table[6][16] = 8

        bpp = bpp_table[IHDR.color_type][IHDR.bit_depth]

        if bpp > 1:
            scanline_bytes = IHDR.width * bpp
        else:
            ppb = 8 // IHDR.bit_depth
            scanline_bytes = (IHDR.width + ppb - 1) // (ppb)
        #without filter byte

        unfilter = {0 : this.filter_method_0 , 1 : this.filter_method_1 , 2 : this.filter_method_2 , 3 : this.filter_method_3 , 4 : this.filter_method_4}
        decoded_scanlines = [[0 for i in range(0 , scanline_bytes)] for i in range(0 , 2)]
        curr_byte_png = 0
        
        this.pixel_table = []

        for i in range(0 , IHDR.height):
            filter_method = this.png_data[curr_byte_png]
            curr_byte_png += 1

            for j in range(0 , scanline_bytes):
                decoded_scanlines[1][j] = unfilter[filter_method](decoded_scanlines , j , bpp , this.png_data[curr_byte_png])
                curr_byte_png += 1

            this.sample_bit_iter = this.sample_bit_func(decoded_scanlines[1])

            for j in range(0 , IHDR.width):
                this.pixel_table.append(pixel.pixel_type[IHDR.color_type](IHDR.bit_depth , this.read_sample))

            decoded_scanlines[0] = decoded_scanlines[1]

    def make_unique_pixels(this):
        this.pixel_set = set()

        for j in this.pixel_table:
            this.pixel_set.add(j)
    
    def print(this):
        print(f"Distinct pixels: {ansii.color(0 , 255 , 60 , len(this.pixel_set))}")

        count = 0

        for j in this.pixel_set:
            count += 1
            j.print()

            if count > 50:
                print(f"({len(this.pixel_set) - count + 1} more)")
                break

    def solve_idat(this , IHDR):
        this.data = b''

        for c in chunks.idat:
            this.data += c.data
        
        CMF = this.data[0]
        CM = (CMF & 0xF)
        CINFO = (CMF >> 4)

        if CM != 8:
            raise Exception("Unknown compression method")
        
        if CINFO != 7: 
            raise Exception("Unkonwn base")
        
        FLG = this.data[1]
        FCHECK = (FLG & 0x1F) #useless
        FDICT = (FLG >> 5 & 1) 
        FLEVEL = (FLG >> 6)

        if (CMF * 256 + FLG) % 31 != 0:
            raise Exception("FCHECK doesn't match")

        if FDICT == 1:
            raise Exception("Dict used")
        
        ADLER32 = int.from_bytes(this.data[len(this.data) - 4 : ] , 'big')
        this.data = this.data[2 : len(this.data) - 4]
        
        this.read_blocks()

        if this.ADLER32_validator(ADLER32) == False:
            raise Exception("ADLER32 error")
         
        this.parse_png_data(IHDR)
        this.make_unique_pixels()