class LZ77Compressor:
    def __init__(self, window_size=20, buffer_size=15):
        self.window_size = window_size
        self.buffer_size = buffer_size

    def preprocess(self, data):
        return data.lower()

    def compress(self, data):
        data = self.preprocess(data)

        i = 0
        compressed_data = []
        while i < len(data):
            match_distance = 0
            match_length = 0
            match_symbol = ''

            start_window = max(0, i - self.window_size)
            end_buffer = min(i + self.buffer_size, len(data))

            for j in range(i - 1, start_window - 1, -1):
                length = 0
                while (j + length < i and i + length < end_buffer and
                       data[j + length] == data[i + length]):
                    length += 1

                if length > match_length:
                    match_length = length
                    match_distance = i - j

            if i + match_length < len(data):
                match_symbol = data[i + match_length]
            else:
                match_symbol = ''

            compressed_data.append((match_distance, match_length, match_symbol))
            i += match_length + 1

        return compressed_data

    def decompress(self, compressed_data):
        decompressed_data = []

        for match_distance, match_length, match_symbol in compressed_data:

            start_index = len(decompressed_data) - match_distance
            for j in range(match_length):
                decompressed_data.append(decompressed_data[start_index + j])


            if match_symbol:
                decompressed_data.append(match_symbol)

        return ''.join(decompressed_data)



data = input("Enter the data to compress: ")
compressor = LZ77Compressor(window_size=20, buffer_size=15)

compressed = compressor.compress(data)
print("Compressed Data:", compressed)

decompressed = compressor.decompress(compressed)
print("Decompressed Data:", decompressed)