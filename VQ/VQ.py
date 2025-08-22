import numpy as np
import cv2
import json
from sklearn.cluster import KMeans

def split_into_blocks(image, block_size):
    h, w = image.shape
    bh, bw = block_size
    blocks = []

    for i in range(0, h, bh):
        for j in range(0, w, bw):
            block = image[i:i+bh, j:j+bw]
            if block.shape == (bh, bw):  # Only keep fully filled blocks
                blocks.append(block.flatten())

    return np.array(blocks)

def generate_codebook(blocks, codebook_size, max_iter=50):
    """Generate a codebook using the k-means algorithm."""
    kmeans = KMeans(n_clusters=codebook_size, n_init=10, max_iter=max_iter, random_state=0)
    kmeans.fit(blocks)
    return kmeans.cluster_centers_, kmeans.labels_

def compress(image_path, block_size, codebook_size, output_file):
    """Compress the grayscale image."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Invalid image file.")

    h, w = image.shape
    blocks = split_into_blocks(image, block_size)

    # Generate the codebook
    codebook, labels = generate_codebook(blocks, codebook_size)

    # Save compressed data as JSON
    compressed_data = {
        "height": h,
        "width": w,
        "block_size": block_size,
        "codebook": codebook.tolist(),
        "labels": labels.tolist(),
    }

    with open(output_file, 'w') as f:
        json.dump(compressed_data, f)

    print(f"Compression complete. File saved at: {output_file}")

def decompress(compressed_file, output_image_path):
    """Decompress the image from the compressed file."""
    with open(compressed_file, 'r') as f:
        compressed_data = json.load(f)

    h = compressed_data["height"]
    w = compressed_data["width"]
    block_size = tuple(compressed_data["block_size"])
    codebook = np.array(compressed_data["codebook"])
    labels = np.array(compressed_data["labels"])

    bh, bw = block_size
    blocks_per_row = w // bw

    # Reconstruct the image from blocks
    blocks = codebook[labels]
    image = np.zeros((h, w), dtype=np.uint8)

    for idx, block in enumerate(blocks):
        i = (idx // blocks_per_row) * bh
        j = (idx % blocks_per_row) * bw
        image[i:i+bh, j:j+bw] = np.round(block.reshape((bh, bw))).astype(np.uint8)

    cv2.imwrite(output_image_path, image)
    print(f"Decompression complete. Image saved at: {output_image_path}")


# Example usage
# Compress
compress("grayscale_image.png", block_size=(4, 4), codebook_size=16, output_file="compressed_file.json")

# Decompress
decompress("compressed_file.json", "decompressed_image.png")
