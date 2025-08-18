class Trie:

    def construct_huffman_codes(this , lengths , alphabet):
        L = {}
        
        for i in range(0 , len(alphabet)):
            L[alphabet[i]] = lengths[i]

        alphabet.sort()

        for i in range(0 , len(alphabet)):
            lengths[i] = L[alphabet[i]]
        
        H = 300

        freq = [0 for i in range(0 , H)]
        code = [0 for i in range(0 , H)]

        for i in lengths:
            freq[i] += 1

        code[1] = 0

        for i in range(2 , H):
            code[i] = (code[i - 1] + freq[i - 1]) * 2

        this.huffman_code = {}

        for i in range(0 , len(alphabet)):

            if lengths[i] == 0:
                continue

            this.huffman_code[alphabet[i]] = format(code[lengths[i]] , "0" + str(lengths[i]) + "b")
            code[lengths[i]] += 1

            if len(this.huffman_code[alphabet[i]]) != lengths[i]:
                raise Exception("code doesn't match len")

    def add(this , code , value):
        node = 1

        for bit in code:
            dig = ord(bit) - ord('0')

            if this.trie[node][dig] == -1:
                this.trie[node][dig] = this.free_node
                this.free_node += 1

            node = this.trie[node][dig]

        this.end_of_code[node] = value

    def __init__(this , lengths , alphabet):
        if len(lengths) != len(alphabet):
            raise Exception("Alphabet bad defined")
        
        this.construct_huffman_codes(lengths , alphabet)

        sum_len = 0

        for i in lengths:
            sum_len += i + 1

        this.trie = [[-1 , -1] for i in range(0 , (sum_len + 1))] #root is node 1
        this.end_of_code = [-1 for i in range((sum_len + 1))]
        this.free_node = 2

        for value , code in this.huffman_code.items():
            this.add(code , value)

