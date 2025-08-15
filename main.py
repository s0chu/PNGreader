import sys
import chunks

file = open(sys.argv[1] , "rb")

signature = file.read(8)

while(1):
    chunk = chunks.Chunk(file)

    print(chunk.name)

    if(chunk.name == "IEND"):
        break
