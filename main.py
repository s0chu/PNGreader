import sys
import chunks
import decoder
import ansii
import time 
import os

def print_all_chunks(chunks):

    print(f"{len(chunks)} chunks: " , end = " ")

    for i in chunks:
        print(ansii.color(255 , 123 , 0 , i) , end = " ")

    print()

file = open(sys.argv[1] , "rb")
filename = os.path.basename(sys.argv[1])

signature = file.read(8)

decoder = decoder.Decoder()
chunk_counter = 0
all_chunks = []

start_time = time.time()

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

end_time = time.time()
time_elapsed = end_time - start_time
time_elapsed = f"{time_elapsed:.2f}"

print(f"{filename} parsed in {ansii.color(255 , 255 , 255 , time_elapsed)} seconds")