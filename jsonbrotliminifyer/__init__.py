import json
import brotli
import os
import logging
import tempfile
import concurrent.futures
from pathlib import Path
from typing import Any, Union, cast, List, Optional, Sequence, Tuple


def _validate_path(path: Union[str, Path], base_dir: Optional[str] = None) -> None:
    """Validate that path is safe and within base_dir if specified."""
    path_str = str(path)
    if base_dir:
        # Ensure path is within base_dir
        abs_path = os.path.abspath(path_str)
        abs_base = os.path.abspath(base_dir)
        if not abs_path.startswith(abs_base):
            raise ValueError(f"Path {path_str} is outside allowed directory {base_dir}")
    # Check for dangerous path components (path traversal)
    if ".." in path_str:
        raise ValueError(f"Potentially dangerous path: {path_str}")


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
    _validate_path(input_path)
    _validate_path(output_path)
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
    temp_fd, temp_path = tempfile.mkstemp(
        dir=os.path.dirname(output_path_str), suffix=".tmp"
    )
    try:
        with os.fdopen(temp_fd, "wb") as temp_f:
            temp_f.write(compressed)
        os.replace(temp_path, output_path_str)
    except PermissionError:
        raise ValueError(f"Permission denied writing to output file: {output_path}")
    except OSError as e:
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
    _validate_path(input_path)
    _validate_path(output_path)
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
    temp_fd, temp_path = tempfile.mkstemp(
        dir=os.path.dirname(output_path_str), suffix=".tmp"
    )
    try:
        with os.fdopen(temp_fd, "w", encoding="utf-8") as temp_f:
            json.dump(json_obj, temp_f, indent=2)
        os.replace(temp_path, output_path_str)
    except PermissionError:
        raise ValueError(f"Permission denied writing to output file: {output_path}")
    except OSError as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as cleanup_error:
                logging.warning(
                    f"Failed to remove temp file {temp_path}: {cleanup_error}"
                )
        raise ValueError(f"Error writing to output file: {output_path} - {e}")


def compress_json_files(
    input_files: Sequence[Union[str, Path]],
    output_dir: Union[str, Path],
    quality: int = 11,
    max_workers: Optional[int] = None,
) -> List[Optional[Exception]]:
    """
    Compress multiple JSON files to an output directory concurrently.

    Output files will have the same name as input files but with .br extension.

    Args:
        input_files: List of input JSON file paths
        output_dir: Directory to save compressed files
        quality: Compression quality level (0-11), default 11
        max_workers: Maximum number of worker threads. If None, uses a reasonable default.

    Returns:
        List of exceptions for each file. None if successful, Exception if failed.
    """
    if max_workers is not None and max_workers <= 0:
        raise ValueError("max_workers must be positive")
    # Validate input files are unique
    input_paths = [str(p) for p in input_files]
    if len(input_paths) != len(set(input_paths)):
        raise ValueError("Duplicate input paths are not allowed")

    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Validate unique output paths
    output_paths = []
    tasks = []
    for input_file in input_files:
        input_path = Path(input_file)
        output_path = output_dir_path / (input_path.stem + ".br")
        output_paths.append(str(output_path))
        tasks.append((input_file, output_path))

    if len(output_paths) != len(set(output_paths)):
        raise ValueError("Duplicate output paths are not allowed")

    def compress_task(
        task: Tuple[Union[str, Path], Union[str, Path]],
    ) -> Optional[Exception]:
        input_file, output_path = task
        try:
            compress_json_file(input_file, output_path, quality)
            return None
        except Exception as e:
            logging.error(f"Failed to compress {input_file} to {output_path}: {e}")
            return e

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(compress_task, tasks))
    return results


def decompress_json_files(
    input_files: Sequence[Union[str, Path]],
    output_dir: Union[str, Path],
    max_workers: Optional[int] = None,
) -> List[Optional[Exception]]:
    """
    Decompress multiple Brotli-compressed files to an output directory concurrently.

    Output files will have the same name as input files but with .json extension.

    Args:
        input_files: List of input compressed file paths
        output_dir: Directory to save decompressed JSON files
        max_workers: Maximum number of worker threads. If None, uses a reasonable default.

    Returns:
        List of exceptions for each file. None if successful, Exception if failed.
    """
    if max_workers is not None and max_workers <= 0:
        raise ValueError("max_workers must be positive")
    # Validate input files are unique
    input_paths = [str(p) for p in input_files]
    if len(input_paths) != len(set(input_paths)):
        raise ValueError("Duplicate input paths are not allowed")

    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Validate unique output paths
    output_paths = []
    tasks = []
    for input_file in input_files:
        input_path = Path(input_file)
        output_path = output_dir_path / (input_path.stem + ".json")
        output_paths.append(str(output_path))
        tasks.append((input_file, output_path))

    if len(output_paths) != len(set(output_paths)):
        raise ValueError("Duplicate output paths are not allowed")

    def decompress_task(
        task: Tuple[Union[str, Path], Union[str, Path]],
    ) -> Optional[Exception]:
        input_file, output_path = task
        try:
            decompress_json_file(input_file, output_path)
            return None
        except Exception as e:
            logging.error(f"Failed to decompress {input_file} to {output_path}: {e}")
            return e

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(decompress_task, tasks))
    return results
