import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # For priority queue (heapq)
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(frequency):
    # Create a priority queue of nodes
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0] if heap else None


def build_huffman_codes(root, code="", codes=None):
    if codes is None:
        codes = {}
    if root is None:
        return codes
    if root.char is not None:
        codes[root.char] = code
    build_huffman_codes(root.left, code + "0", codes)
    build_huffman_codes(root.right, code + "1", codes)
    return codes


def huffman_compress(input_file, output_file):
    with open(input_file, 'r') as f:
        data = f.read()

    # Build frequency map and Huffman Tree
    frequency = Counter(data)
    root = build_huffman_tree(frequency)
    huffman_codes = build_huffman_codes(root)

    # Encode the data
    encoded_data = ''.join(huffman_codes[char] for char in data)

    # Save encoded data and Huffman dictionary
    with open(output_file, 'w') as f:
        f.write(encoded_data + '\n')
        f.write(str(huffman_codes))


def huffman_decompress(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    encoded_data = lines[0].strip()
    huffman_codes = eval(lines[1].strip())   # dictionary from file
    reverse_codes = {v: k for k, v in huffman_codes.items()}

    # Decode the data
    decoded_data = []
    current_code = ""
    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_codes:
            decoded_data.append(reverse_codes[current_code])
            current_code = ""

    with open(output_file, 'w') as f:
        f.write(''.join(decoded_data))


# Example usage:
huffman_compress("in.txt", "out.txt")
huffman_decompress("out.txt", "out2.txt")
