import json
import brotli


def compress_json(json_obj, quality=11):
    """
    Compress a JSON object using Brotli compression.

    Args:
        json_obj: A JSON-serializable Python object (dict, list, etc.)
        quality: Compression quality level (0-11), default 11 (best compression)

    Returns:
        bytes: The compressed data as bytes
    """
    if not (0 <= quality <= 11):
        raise ValueError("Quality must be between 0 and 11")
    json_str = json.dumps(json_obj)
    json_bytes = json_str.encode('utf-8')
    compressed = brotli.compress(json_bytes, quality=quality)
    return compressed


def decompress_json(compressed_bytes):
    """
    Decompress Brotli-compressed data back to a JSON object.

    Args:
        compressed_bytes: The compressed data as bytes

    Returns:
        The original JSON object
    """
    decompressed_bytes = brotli.decompress(compressed_bytes)
    json_str = decompressed_bytes.decode('utf-8')
    json_obj = json.loads(json_str)
    return json_obj


def compress_json_file(input_path, output_path, quality=11):
    """
    Compress a JSON file using Brotli compression.

    Args:
        input_path: Path to the input JSON file
        output_path: Path to the output compressed file
        quality: Compression quality level (0-11), default 11 (best compression)
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        json_obj = json.load(f)
    compressed = compress_json(json_obj, quality=quality)
    with open(output_path, 'wb') as f:
        f.write(compressed)


def decompress_json_file(input_path, output_path):
    """
    Decompress a Brotli-compressed file back to a JSON file.

    Args:
        input_path: Path to the input compressed file
        output_path: Path to the output JSON file
    """
    with open(input_path, 'rb') as f:
        compressed_bytes = f.read()
    json_obj = decompress_json(compressed_bytes)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_obj, f, indent=2)
