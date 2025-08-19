# PNGreader

Purpose of the project:
    - learning Python
    - reading comprehension of raw documentation without any aditional help
    - training coding structure for big projects

Description
    This project wants to be a rudimentary PNG reader for educational purposes, a PNG decoder so to speak. Everything is implemented by me manually, without aditional help from external libraries. I am aware that it is slow being written in Python

    Informations that you can get:
        - Resolution of the file (H x W)
        - Color type (0 , 2 , 3 , 4 , 6)
        - Bit depth (1 , 2 , 4 , 8 , 16, according to the Color Type)
        - Interlace (True / False)
        - Chunks that build up the file
        - Number of blocks in the ZLIB format
        - Number of distinct pixels and the pixels themselves
            Pixel format: colored_square #RGB_code Opacity_percent
            RGB_code is in the following hex format: hex(R_value)hex(G_value)hex(B_value)
    
    ###### IMAGES AND VISUAL TUTORIAL

Implementation details
    There are 5 pixel classes, representing each Color Type. Each class has the same format so that they can be casted into a dictionary table in pairs (color_type : pixel_color_type_class)

    The implemention of each class has a constructor that regards bit depth and a reading generator function, that can facilitate the reading of bits

    Supported chunks: IHDR, PLTE, IDAT, IEND
        There is room for scalabity. You can further add support for other types of chunks by creating child classes of the Chunk class in chunks.py
        
        IHDR is straightforward in implementation, following the format and reading byte by byte the data

        PLTE does the same, with the mention that it uses Pixel_2 as palette entry. In fact, the palette is an array of size 2^color_depth of Pixel_2

        IDAT is reading byte by byte

    ZLIB decompress
        Putting IDAT data chunks together, the decompression starts by decoding each block of data.

        Each block uses 2 tries data structures, for Huffman decodings, one for literal/length and another one for distance
        
        The trie class has a constructor that creates a Huffman Trie with the following restriction: |huffman(alphabet_i)| = length_i, with a sorted alphabet
        The trie itself is implemented offline with static memory. Each node of the trie is an index into an array that has a size upper bound of sum(length_i)
        
        The huffman codes use numbers in base 2 for representing

        In case of a block that uses dynamic compression, a third trie is created for decoding the lengths arrays 

        For reading the bits in LSB -> MSB order, I used again a generator function that facilitates that, keeping track of the position in the byte

        Lengths and distances information are placed into 2 arrays that structured together under Table class: extra_bits and lengths, where extra_bits[value] = #extra_bits (lengths follows the same logic)



        The reasons for the tries being encoded into lenghts form is:
            1. Every interpretation of the code is unique, i.e there is a single possible code for a value of the alphabet
                This is happening because of the restrictions imposed on the lengths and the alphabet: 
                    - codes that have the same length must be lexicographically the same as its value in the alphabet
                        Being a single possible lexicographical order in the alphabet, the uniqueness is guaranteed
                    - codes with shorter length must be lexicographical smaller than the ones with bigger length
                        This restriction imposes the order in which the codes are given, so that the 000000...0 will be attributed to the smallest length in the alphabet, achieving uniqueness
            2. It disregards the need of knowing the alphabet in the encoding
            3. The tries themselves are well balanced, leading to approximately log_2(n) maximum code length, where n = |alphabet|

        After the block is decompressed, the tries get deleted from the memory and created again in the next run
   
    Interlation: not supported

    Colors in the terminal:
        Used ANSII escape codes in the following form: 
            Changing background color: ESC[48;2;R;G;Bm
            Changing foreground color: ESC[38;2;R;G;Bm]
            Reseting: ESC[m

Bibliography
    https://datatracker.ietf.org/doc/html/rfc1950
    https://www.rfc-editor.org/rfc/rfc1951.html 
    https://www.rfc-editor.org/rfc/rfc2083.html
    https://en.wikipedia.org/wiki/ANSI_escape_code   
    https://www.geeksforgeeks.org/python/inheritance-in-python/
