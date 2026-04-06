# API Reference

This section provides detailed documentation for all public functions and classes in JSONBrotliMinifyer.

## Core Functions

### `compress_json(json_obj, quality=11)`

Compresses a JSON-serializable Python object using Brotli compression.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `json_obj` | `Any` | - | JSON-serializable Python object (dict, list, str, int, float, bool, None) |
| `quality` | `int` | `11` | Compression quality level (0-11). Higher values = better compression but slower |

#### Returns

`bytes` - The compressed data as bytes

#### Raises

- `ValueError` - If `quality` is not between 0 and 11

#### Examples

```python
import jsonbrotliminifyer

# Basic usage
data = {"name": "Alice", "age": 30}
compressed = jsonbrotliminifyer.compress_json(data)

# With custom quality
compressed_fast = jsonbrotliminifyer.compress_json(data, quality=0)
compressed_best = jsonbrotliminifyer.compress_json(data, quality=11)
```

#### Notes

- Quality levels: 0 (fastest) to 11 (best compression)
- Typical compression ratios: 3-8x depending on data structure
- JSON serialization is done internally with UTF-8 encoding

---

### `decompress_json(compressed_bytes)`

Decompresses Brotli-compressed data back to the original JSON object.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `compressed_bytes` | `bytes` | The compressed data as bytes |

#### Returns

`Any` - The original Python object

#### Raises

- `ValueError` - If data is not valid Brotli-compressed data or doesn't decode to valid JSON

#### Examples

```python
import jsonbrotliminifyer

# Assuming 'compressed' contains valid compressed data
try:
    original = jsonbrotliminifyer.decompress_json(compressed)
    print(original)
except ValueError as e:
    print(f"Decompression failed: {e}")
```

#### Notes

- Automatically detects invalid Brotli data
- Validates that decompressed data is valid JSON
- Returns the exact original Python object structure

---

### `compress_json_file(input_path, output_path, quality=11)`

Compresses a JSON file using Brotli compression with atomic write operations.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_path` | `Union[str, Path]` | - | Path to input JSON file |
| `output_path` | `Union[str, Path]` | - | Path to output compressed file |
| `quality` | `int` | `11` | Compression quality level (0-11) |

#### Raises

- `ValueError` - If input file doesn't exist, isn't readable, contains invalid JSON, or write fails
- `ValueError` - If path validation fails (path traversal attempts)

#### Examples

```python
import jsonbrotliminifyer

# Basic file compression
jsonbrotliminifyer.compress_json_file(
    "data.json",
    "data.json.br"
)

# With custom quality
jsonbrotliminifyer.compress_json_file(
    "large_data.json",
    "large_data.br",
    quality=6
)
```

#### Notes

- Uses atomic writes (temporary file + rename) to prevent corruption
- Validates JSON content before compression
- Path validation prevents directory traversal attacks

---

### `decompress_json_file(input_path, output_path)`

Decompresses a Brotli-compressed file back to a JSON file.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `input_path` | `Union[str, Path]` | Path to input compressed file |
| `output_path` | `Union[str, Path]` | Path to output JSON file |

#### Raises

- `ValueError` - If input file doesn't exist, isn't readable, or write fails
- `ValueError` - If path validation fails or decompressed data isn't valid JSON

#### Examples

```python
import jsonbrotliminifyer

# Basic file decompression
jsonbrotliminifyer.decompress_json_file(
    "data.json.br",
    "restored.json"
)
```

#### Notes

- Outputs nicely formatted JSON (2-space indentation)
- Atomic write operations prevent data corruption
- Validates decompressed content is valid JSON

---

### `compress_json_files(input_files, output_dir, quality=11, max_workers=None)`

Compresses multiple JSON files concurrently to an output directory.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_files` | `Sequence[Union[str, Path]]` | - | List of input JSON file paths |
| `output_dir` | `Union[str, Path]` | - | Directory to save compressed files |
| `quality` | `int` | `11` | Compression quality level (0-11) |
| `max_workers` | `Optional[int]` | `None` | Max worker threads (None = reasonable default) |

#### Returns

`List[Optional[Exception]]` - List of exceptions (None for success, Exception for failure)

#### Raises

- `ValueError` - If `max_workers` <= 0, duplicate input paths, or duplicate output paths

#### Examples

```python
import jsonbrotliminifyer

# Compress multiple files
input_files = ["file1.json", "file2.json", "file3.json"]
results = jsonbrotliminifyer.compress_json_files(
    input_files=input_files,
    output_dir="compressed/",
    quality=6,
    max_workers=4
)

# Check results
for i, result in enumerate(results):
    if result is None:
        print(f"✓ {input_files[i]} compressed successfully")
    else:
        print(f"✗ {input_files[i]} failed: {result}")
```

#### Notes

- Output files have `.br` extension
- Concurrent processing for better performance
- Creates output directory if it doesn't exist
- Returns per-file error status

---

### `decompress_json_files(input_files, output_dir, max_workers=None)`

Decompresses multiple Brotli-compressed files concurrently to an output directory.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_files` | `Sequence[Union[str, Path]]` | - | List of input compressed file paths |
| `output_dir` | `Union[str, Path]` | - | Directory to save decompressed JSON files |
| `max_workers` | `Optional[int]` | `None` | Max worker threads (None = reasonable default) |

#### Returns

`List[Optional[Exception]]` - List of exceptions (None for success, Exception for failure)

#### Raises

- `ValueError` - If `max_workers` <= 0, duplicate input paths, or duplicate output paths

#### Examples

```python
import jsonbrotliminifyer

# Decompress multiple files
compressed_files = ["file1.json.br", "file2.json.br", "file3.json.br"]
results = jsonbrotliminifyer.decompress_json_files(
    input_files=compressed_files,
    output_dir="restored/",
    max_workers=4
)

# Check results
for i, result in enumerate(results):
    if result is None:
        print(f"✓ {compressed_files[i]} decompressed successfully")
    else:
        print(f"✗ {compressed_files[i]} failed: {result}")
```

#### Notes

- Output files have `.json` extension
- Concurrent processing for better performance
- Creates output directory if it doesn't exist

## Internal Functions

### `_validate_path(path, base_dir=None)`

Validates that a path is safe and within base_dir if specified.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `Union[str, Path]` | - | Path to validate |
| `base_dir` | `Optional[str]` | `None` | Base directory for validation |

#### Raises

- `ValueError` - If path contains `..` or is outside base_dir

#### Notes

- Internal security function
- Prevents path traversal attacks
- Used by all file operations

## Type Definitions

The library uses the following type hints:

```python
from typing import Any, Union, List, Optional, Sequence, Tuple
from pathlib import Path
```

## Constants

The library doesn't define any public constants. All configuration is done through function parameters.

## Exceptions

All functions raise `ValueError` for invalid inputs or operation failures. Specific error conditions:

- **Invalid quality level**: `quality` not in range 0-11
- **Invalid Brotli data**: Data cannot be decompressed
- **Invalid JSON**: Decompressed data is not valid JSON
- **File access errors**: Permission or I/O issues
- **Path validation**: Path traversal attempts
- **Duplicate paths**: In batch operations

## Thread Safety

- **In-memory functions** (`compress_json`, `decompress_json`): Thread-safe
- **File functions**: Not thread-safe for same file paths (use different paths for concurrent access)
- **Batch functions**: Designed for concurrent use with `max_workers` parameter

## Memory Usage

- **Compression**: Memory usage scales with input data size
- **Decompression**: Memory usage scales with decompressed data size
- **File operations**: Minimal additional memory beyond data size
- **Batch operations**: Memory usage per worker thread

## Performance Characteristics

| Function | Time Complexity | Space Complexity |
|----------|----------------|------------------|
| `compress_json` | O(n) | O(n) |
| `decompress_json` | O(n) | O(n) |
| `compress_json_file` | O(n) + I/O | O(n) |
| `decompress_json_file` | O(n) + I/O | O(n) |
| `compress_json_files` | O(n) + I/O | O(n) per worker |
| `decompress_json_files` | O(n) + I/O | O(n) per worker |

Where n is the data size in bytes.

## Compatibility

- **Python versions**: 3.9+
- **Operating systems**: Linux, macOS, Windows
- **Brotli versions**: 1.0.0+
- **Threading**: Works with threading and multiprocessing</content>
<parameter name="filePath">docs/api.md