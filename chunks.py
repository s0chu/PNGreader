class Chunk:
    def CRC_validator(this):
        bin = ''.join(''.join(reversed(format(ord(j) , "08b"))) for j in this.name)
        bin = bin + ''.join(  ''.join(reversed(format(j , "08b"))) for j in this.data)
        bin = [(ord(j) - ord('0')) for j in bin]


        divisor = [0 for j in range(0 , 33)]
        
        for j in [32 , 26 , 23 , 22 , 16 , 12 , 11 , 10 , 8 , 7 , 5 , 4 , 2 , 1 , 0]:
            divisor[j] = 1
        
        for i in range(0 , len(bin)):
            if(bin[i] == 1 and i + len(divisor) - 1 < len(bin)):
                for j in range(i , i + len(divisor)):
                    bin[j] = bin[j] ^ divisor[j - i]    

        rem = [bin[i] for i in range((0 if 32 > len(bin) else len(bin) - 32) , len(bin))]
        print(f"dimension is {len(rem)}")

        for i in range(0 , 32):
            rem[i] = 1 - rem[i]

        crc = ''.join(reversed(''.join(chr(i + ord('0')) for i in rem)))
        print(int(crc , 2))
        print(this.CRC)
        return 1

    def __init__(this , file):
        this.len = int.from_bytes(file.read(4) , 'big')
        this.name = str(file.read(4) , encoding = "utf-8")
        this.data = file.read(this.len)
        this.CRC = int.from_bytes(file.read(4) , 'big')

        if(this.CRC_validator() == 0):
            raise Exception("CRC invalid, send was compromised")
    

    