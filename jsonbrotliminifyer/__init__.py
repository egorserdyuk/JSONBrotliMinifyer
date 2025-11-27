import json
import brotli


def compress_json(json_obj):
    """
    Compress a JSON object using Brotli compression.

    Args:
        json_obj: A JSON-serializable Python object (dict, list, etc.)

    Returns:
        bytes: The compressed data as bytes
    """
    json_str = json.dumps(json_obj)
    json_bytes = json_str.encode('utf-8')
    compressed = brotli.compress(json_bytes)
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
