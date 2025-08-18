import sys
import chunks

file = open(sys.argv[1] , "rb")

signature = file.read(8)

decoder = chunks.Decoder()

while(1):
    chunk = chunks.Chunk(file)
    decoder.process(chunk)
    print(chunk.name)

    if(chunk.name == "IEND"):
        break

decoder.solve_idat()
decoder.ihdr[0].print()