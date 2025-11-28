# JSONBrotliMinifyer

A Python library for compressing and decompressing JSON data using the Brotli compression algorithm.

## Features

- Compress JSON-serializable Python objects (dicts, lists, strings, numbers, etc.) into compact byte representations.
- Decompress Brotli-compressed data back to the original JSON objects.
- Compress and decompress JSON files directly with atomic write operations to prevent data corruption.
- Efficient lossless compression suitable for data storage and transmission.

## Installation

Install the library using pip:

```bash
pip install jsonbrotliminifyer
```

Or install from source:

```bash
git clone https://github.com/egorserdyuk/JSONBrotliMinifyer.git
cd JSONBrotliMinifyer
pip install -e .
```

## Usage

```python
import jsonbrotliminifyer

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

### Command Line Interface

After installation, you can use the `jsonbrotlim` command to compress and decompress JSON data from the command line.

#### Compress JSON data

```bash
# Compress a JSON file
jsonbrotlim compress --input-file input.json --output-file output.br

# Compress with custom quality (0-11)
jsonbrotlim compress --input-file input.json --output-file output.br --quality 0

# Compress JSON from stdin
echo '{"name": "test"}' | jsonbrotlim compress > output.br
```

#### Decompress JSON data

```bash
# Decompress a compressed file
jsonbrotlim decompress --input-file output.br --output-file restored.json

# Decompress from stdin
cat output.br | jsonbrotlim decompress
```

## API

### `compress_json(json_obj, quality=11)`

Compresses a JSON-serializable Python object.

- **Parameters**:
  - `json_obj` - Any JSON-serializable Python object
  - `quality` - Compression quality level (0-11), default 11 (best compression)
- **Returns**: `bytes` - The compressed data
- **Raises**: `ValueError` - If quality is not between 0 and 11

### `decompress_json(compressed_bytes)`

Decompresses Brotli-compressed data back to the original JSON object.

- **Parameters**: `compressed_bytes` - The compressed data as bytes
- **Returns**: The original Python object
- **Raises**: `ValueError` - If the data is not valid Brotli-compressed data or does not decode to valid JSON

### `compress_json_file(input_path, output_path, quality=11)`

Compresses a JSON file using Brotli compression.

- **Parameters**:
  - `input_path` - Path to the input JSON file
  - `output_path` - Path to the output compressed file
  - `quality` - Compression quality level (0-11), default 11 (best compression)
- **Raises**: `ValueError` - If the input file does not exist, is not readable, contains invalid JSON, or if writing to the output file fails

### `decompress_json_file(input_path, output_path)`

Decompresses a Brotli-compressed file back to a JSON file.

- **Parameters**:
  - `input_path` - Path to the input compressed file
  - `output_path` - Path to the output JSON file
- **Raises**: `ValueError` - If the input file does not exist, is not readable, or if writing to the output file fails

## Dependencies

- Python >= 3.9
- `brotli` - Python bindings for the Brotli compression library

## Testing

Run the tests using unittest:

```bash
python -m unittest tests.test_jsonbrotliminifyer
```

Or using pytest

```bash
pytest tests/test_jsonbrotliminifyer.py
```

## License

MIT License
