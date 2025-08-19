import sys
import chunks
import decoder
import ansii

def print_all_chunks(chunks):

    print(f"{len(chunks)} chunks: " , end = " ")

    for i in chunks:
        print(ansii.color(255 , 123 , 0 , i) , end = " ")

    print()
file = open(sys.argv[1] , "rb")

signature = file.read(8)

decoder = decoder.Decoder()
chunk_counter = 0
all_chunks = []

while(1):
    chunk = chunks.Chunk(file)
    decoder.process(chunk)

    chunk_counter += 1
    #print(f"Chunk #{chunk_counter}: {chunk.name}")
    all_chunks.append(chunk.name)

    if(chunk.name == "IEND"):
        break

chunks.ihdr[0].print()
print_all_chunks(all_chunks)
decoder.solve_idat(chunks.ihdr[0])
decoder.print()