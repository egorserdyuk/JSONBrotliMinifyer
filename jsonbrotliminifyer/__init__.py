import json
import brotli
import os
import errno
import shutil
import logging
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

    Raises:
        ValueError: If the input file does not exist, is not readable, contains invalid JSON,
                   or if writing to the output file fails
    """
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            json_obj = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Input file does not exist: {input_path}")
    except PermissionError:
        raise ValueError(f"Permission denied reading input file: {input_path}")
    except OSError as e:
        raise ValueError(f"Error reading input file: {input_path} - {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Input file contains invalid JSON: {input_path} - {e}")

    compressed = compress_json(json_obj, quality=quality)

    output_path_str = str(output_path)
    temp_path = output_path_str + ".tmp"
    try:
        with open(temp_path, "wb") as temp_f:
            temp_f.write(compressed)
        try:
            fd = os.open(output_path_str, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            os.close(fd)
        except OSError as e:
            if e.errno == errno.ELOOP:
                raise ValueError(f"Refusing to overwrite symlink: {output_path_str}")
        os.replace(temp_path, output_path_str)
    except PermissionError:
        raise ValueError(f"Permission denied writing to output file: {output_path}")
    except OSError as e:
        if e.errno == errno.EXDEV:
            shutil.copy2(temp_path, output_path_str)
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
        else:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
            raise ValueError(f"Error writing to output file: {output_path} - {e}")


def decompress_json_file(
    input_path: Union[str, Path], output_path: Union[str, Path]
) -> None:
    """
    Decompress a Brotli-compressed file back to a JSON file.

    Args:
        input_path: Path to the input compressed file (str or Path)
        output_path: Path to the output JSON file (str or Path)

    Raises:
        ValueError: If the input file does not exist, is not readable, or if writing to the output file fails
    """
    try:
        with open(input_path, "rb") as f:
            compressed_bytes = f.read()
    except FileNotFoundError:
        raise ValueError(f"Input file does not exist: {input_path}")
    except PermissionError:
        raise ValueError(f"Permission denied reading input file: {input_path}")
    except OSError as e:
        raise ValueError(f"Error reading input file: {input_path} - {e}")

    json_obj = decompress_json(compressed_bytes)

    output_path_str = str(output_path)
    temp_path = output_path_str + ".tmp"
    try:
        with open(temp_path, "w", encoding="utf-8") as temp_f:
            json.dump(json_obj, temp_f, indent=2)
        try:
            fd = os.open(output_path_str, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            os.close(fd)
        except OSError as e:
            if e.errno == errno.ELOOP:
                raise ValueError(f"Refusing to overwrite symlink: {output_path_str}")
        os.replace(temp_path, output_path_str)
    except PermissionError:
        raise ValueError(f"Permission denied writing to output file: {output_path}")
    except OSError as e:
        if e.errno == errno.EXDEV:
            shutil.copy2(temp_path, output_path_str)
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception as cleanup_error:
                    logging.warning(
                        f"Failed to remove temp file {temp_path}: {cleanup_error}"
                    )
        else:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception as cleanup_error:
                    logging.warning(
                        f"Failed to remove temp file {temp_path}: {cleanup_error}"
                    )
            raise ValueError(f"Error writing to output file: {output_path} - {e}")
