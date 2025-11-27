import json
import brotli
from pathlib import Path
from typing import Any, Union, cast


def compress_json(json_obj: Any, quality: int = 11) -> bytes:
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
    json_bytes = json_str.encode("utf-8")
    compressed = brotli.compress(json_bytes, quality=quality)
    return cast(bytes, compressed)


def decompress_json(compressed_bytes: bytes) -> Any:
    """
    Decompress Brotli-compressed data back to a JSON object.

    Args:
        compressed_bytes: The compressed data as bytes

    Returns:
        The original JSON object

    Raises:
        ValueError: If the data is not valid Brotli-compressed data or does not decode to valid JSON
    """
    try:
        decompressed_bytes = brotli.decompress(compressed_bytes)
    except brotli.error as e:
        raise ValueError("Invalid Brotli-compressed data") from e
    try:
        json_str = decompressed_bytes.decode("utf-8")
        json_obj = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError("Decompressed data is not valid JSON") from e
    return json_obj


def compress_json_file(
    input_path: Union[str, Path], output_path: Union[str, Path], quality: int = 11
) -> None:
    """
    Compress a JSON file using Brotli compression.

    Args:
        input_path: Path to the input JSON file (str or Path)
        output_path: Path to the output compressed file (str or Path)
        quality: Compression quality level (0-11), default 11 (best compression)
    """
    with open(input_path, "r", encoding="utf-8") as f:
        json_obj = json.load(f)
    compressed = compress_json(json_obj, quality=quality)
    with open(output_path, "wb") as f:
        f.write(compressed)


def decompress_json_file(
    input_path: Union[str, Path], output_path: Union[str, Path]
) -> None:
    """
    Decompress a Brotli-compressed file back to a JSON file.

    Args:
        input_path: Path to the input compressed file (str or Path)
        output_path: Path to the output JSON file (str or Path)
    """
    with open(input_path, "rb") as f:
        compressed_bytes = f.read()
    json_obj = decompress_json(compressed_bytes)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_obj, f, indent=2)
