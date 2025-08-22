def lzw_compress(input_file, output_file):
    """
    Compresses the contents of input_file using LZW compression
    and writes the compressed data as numbers to output_file in text format.
    """
    # Read the contents of the input file
    with open(input_file, 'r') as f:
        data = f.read()

    # Initialize the dictionary with all possible single-character keys
    dictionary = {chr(i): i for i in range(128)}  # ASCII table initialization
    next_code = 128  # The next code to be added to the dictionary
    current_string = ""  # Track the current sequence of characters
    compressed_data = []  # List to hold the compressed output

    # LZW Compression Algorithm
    for symbol in data:
        combined_string = current_string + symbol  # Create a new sequence
        if combined_string in dictionary:
            current_string = combined_string
        else:
            # Output the code for the sequence and add to dictionary
            compressed_data.append(str(dictionary[current_string]))
            dictionary[combined_string] = next_code
            next_code += 1
            current_string = symbol

    # Output the code for the last sequence if present
    if current_string:
        compressed_data.append(str(dictionary[current_string]))

    # Write compressed data as text (numbers separated by spaces)
    with open(output_file, 'w') as f:
        f.write(" ".join(compressed_data))

def lzw_decompress(input_file, output_file):
    """
    Decompresses the data from input_file (stored as numbers in text format)
    using LZW decompression and writes the decompressed text to output_file.
    """
    # Read the compressed data from the text file
    with open(input_file, 'r') as f:
        compressed_data = list(map(int, f.read().split()))

    # Initialize the dictionary with all single-character mappings
    dictionary = {i: chr(i) for i in range(128)}  # ASCII table initialization
    next_code = 128  # The next code to be added to the dictionary

    # Get the first code to start decompression
    current_code = compressed_data.pop(0)
    current_string = dictionary[current_code]
    decompressed_data = [current_string]  # Store the decompressed output

    # LZW Decompression Algorithm
    for code in compressed_data:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = current_string + current_string[0]
        else:
            raise ValueError("Invalid compressed code encountered.")

        decompressed_data.append(entry)
        dictionary[next_code] = current_string + entry[0]
        next_code += 1
        current_string = entry

    # Write decompressed data to the output file as text
    with open(output_file, 'w') as f:
        f.write("".join(decompressed_data))

lzw_compress("in.txt", "out.txt")

lzw_decompress("out.txt", "out2.txt")
