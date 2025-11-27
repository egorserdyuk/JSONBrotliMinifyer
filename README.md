# JSONBrotliMinifyer

A Python library for compressing and decompressing JSON data using the Brotli compression algorithm.

## Features

- Compress JSON-serializable Python objects (dicts, lists, strings, numbers, etc.) into compact byte representations.
- Decompress Brotli-compressed data back to the original JSON objects.
- Compress and decompress JSON files directly.
- Efficient lossless compression suitable for data storage and transmission.

## Installation

Install the library using pip:

```bash
pip install jsonbrotliminifyer
```

Or install from source:

```bash
git clone https://github.com/egorserdyuk/jsonbrotliminifyer.git
cd jsonbrotliminifyer
pip install -e .
```

## Usage

```python
import jsonbrotli

# Original JSON data
data = {
    "name": "John Doe",
    "age": 30,
    "items": ["apple", "banana", "cherry"],
    "active": True
}

# Compress the data (with default quality 11)
compressed = jsonbrotliminifyer.compress_json(data)
print(f"Compressed size: {len(compressed)} bytes")

# Compress with custom quality (0-11, lower = faster but larger)
compressed_fast = jsonbrotliminifyer.compress_json(data, quality=0)
print(f"Fast compression size: {len(compressed_fast)} bytes")

# Decompress the data
decompressed = jsonbrotliminifyer.decompress_json(compressed)
print(decompressed)  # Should match the original data
```

### File Compression

```python
import jsonbrotliminifyer

# Compress a JSON file (with default quality 11)
jsonbrotliminifyer.compress_json_file('input.json', 'output.br')

# Compress with custom quality
jsonbrotliminifyer.compress_json_file('input.json', 'output_fast.br', quality=0)

# Decompress a compressed file back to JSON
jsonbrotliminifyer.decompress_json_file('output.br', 'restored.json')
```

## API

### `compress_json(json_obj, quality=11)`

Compresses a JSON-serializable Python object.

- **Parameters**:
  - `json_obj` - Any JSON-serializable Python object
  - `quality` - Compression quality level (0-11), default 11 (best compression)
- **Returns**: `bytes` - The compressed data

### `decompress_json(compressed_bytes)`

Decompresses Brotli-compressed data back to the original JSON object.

- **Parameters**: `compressed_bytes` - The compressed data as bytes
- **Returns**: The original Python object

### `compress_json_file(input_path, output_path, quality=11)`

Compresses a JSON file using Brotli compression.

- **Parameters**:
  - `input_path` - Path to the input JSON file
  - `output_path` - Path to the output compressed file
  - `quality` - Compression quality level (0-11), default 11 (best compression)

### `decompress_json_file(input_path, output_path)`

Decompresses a Brotli-compressed file back to a JSON file.

- **Parameters**:
  - `input_path` - Path to the input compressed file
  - `output_path` - Path to the output JSON file

## Dependencies

- `brotli` - Python bindings for the Brotli compression library

## Testing

Run the tests using unittest:

```bash
python -m unittest tests.test_jsonbrotliminifyer
```

## License

MIT License