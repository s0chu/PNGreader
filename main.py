import sys
import chunks
import decoder

file = open(sys.argv[1] , "rb")

signature = file.read(8)

decoder = decoder.Decoder()
chunk_counter = 0

while(1):
    chunk = chunks.Chunk(file)
    decoder.process(chunk)

    chunk_counter += 1
    print(f"Chunk #{chunk_counter}: {chunk.name}")

    if(chunk.name == "IEND"):
        break

chunks.ihdr[0].print()
decoder.solve_idat(chunks.ihdr[0])
chunks.ihdr[0].print()
decoder.print()