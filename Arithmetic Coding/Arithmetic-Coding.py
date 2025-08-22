from decimal import Decimal, getcontext

# Set high precision for decimal operations (to avoid floating-point errors)
getcontext().prec = 50  # Precision: 50 decimal places


def calculate_probabilities(data):
    """Calculate symbol probabilities from input data."""
    freq = {}
    for char in data:  # Count frequency of each character
        freq[char] = freq.get(char, 0) + 1
    total = len(data)  # Total number of characters
    probabilities = {char: Decimal(freq[char]) / Decimal(total) for char in freq}
    return probabilities


def build_ranges(probabilities):
    """Assign probability ranges to each symbol."""
    ranges = {}
    low = Decimal(0.0)
    for symbol, prob in probabilities.items():
        high = low + prob
        # Each symbol gets a unique interval [low, high)
        ranges[symbol] = (low, high)
        low = high  # Move start of the next interval
    return ranges


def arithmetic_compress(data, output_file):
    """Compress data using Arithmetic Coding and save results to a file."""
    probabilities = calculate_probabilities(data)
    ranges = build_ranges(probabilities)

    # Initial interval [0, 1)
    low, high = Decimal(0.0), Decimal(1.0)
    for char in data:
        char_low, char_high = ranges[char]
        range_width = high - low
        # Narrow the interval based on the character range
        high = low + range_width * char_high
        low = low + range_width * char_low

    # Save encoded value, data length, and symbol ranges
    with open(output_file, 'w') as f:
        f.write(f"{low}\n")  # Encoded value
        f.write(f"{len(data)}\n")  # Original length
        for char, (char_low, char_high) in ranges.items():
            # Use repr to preserve spaces and special characters
            f.write(f"{repr(char)}:{char_low},{char_high}\n")


def arithmetic_decompress(encoded_file, output_file):
    """Decompress data encoded with Arithmetic Coding."""
    with open(encoded_file, 'r') as f:
        lines = f.readlines()

    # Read encoded values
    encoded_value = Decimal(lines[0].strip())
    data_length = int(lines[1].strip())
    ranges = {}
    for line in lines[2:]:
        char_repr, range_values = line.strip().split(':', 1)
        char = eval(char_repr)  # Restore original character (handles spaces, \n, etc.)
        char_low, char_high = map(Decimal, range_values.split(','))
        ranges[char] = (char_low, char_high)

    # Decode by iteratively finding the symbol corresponding to encoded_value
    decoded_data = []
    step = 0
    while len(decoded_data) < data_length:
        print(f"Step {step}: Current encoded value = {encoded_value}")  # Debugging
        for char, (char_low, char_high) in ranges.items():
            if char_low <= encoded_value < char_high:
                decoded_data.append(char)
                # Normalize encoded_value for next iteration
                encoded_value = (encoded_value - char_low) / (char_high - char_low)
                print(f"Matched {char}: New encoded value = {encoded_value}")  # Debugging
                break
        step += 1

    # Save decoded text
    with open(output_file, 'w') as f:
        f.write(''.join(decoded_data))
    print(f"Decoded data: {''.join(decoded_data)}")  # Debugging


def menu():
    """Menu interface for compression/decompression."""
    print("Arithmetic Compression and Decompression")
    print("1. Compress a file")
    print("2. Decompress a file")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        # Input and output file names
        input_file = "input.txt"
        output_file = "compressed.txt"

        # Read input data
        with open(input_file, 'r') as file:
            data = file.read()

        # Perform compression
        try:
            arithmetic_compress(data, output_file)
            print("Data compressed successfully!")
        except Exception as e:
            print(f"Error during compression: {e}")

    elif choice == "2":
        # Input and output file names
        input_file = "compressed.txt"
        output_file = "decompressed.txt"

        # Perform decompression
        try:
            arithmetic_decompress(input_file, output_file)
            print("Data decompressed successfully!")
        except Exception as e:
            print(f"Error during decompression: {e}")
    else:
        print("Invalid choice. Please enter 1 or 2.")


# Run the menu
if __name__ == "__main__":
    menu()
