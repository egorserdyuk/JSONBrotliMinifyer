# Usage Guide

This guide provides comprehensive examples and patterns for using JSONBrotliMinifyer in your applications.

## Basic Usage

### In-Memory Compression

```python
import jsonbrotliminifyer

# Sample JSON data
data = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ],
    "metadata": {
        "version": "1.0",
        "created": "2024-01-01T00:00:00Z"
    }
}

# Compress with default quality (11 - best compression)
compressed = jsonbrotliminifyer.compress_json(data)
print(f"Original size: {len(json.dumps(data))} bytes")
print(f"Compressed size: {len(compressed)} bytes")
print(f"Compression ratio: {len(compressed) / len(json.dumps(data)):.2f}")

# Decompress back to original
original = jsonbrotliminifyer.decompress_json(compressed)
assert original == data  # Perfect fidelity
```

### Quality Levels

```python
import jsonbrotliminifyer

data = {"large": "x" * 10000}  # 10KB of data

# Different quality levels
for quality in [0, 6, 11]:
    compressed = jsonbrotliminifyer.compress_json(data, quality=quality)
    ratio = len(compressed) / len(json.dumps(data))
    print(f"Quality {quality}: {len(compressed)} bytes ({ratio:.2f}x)")
```

## File Operations

### Single File Compression

```python
import jsonbrotliminifyer

# Compress a JSON file
jsonbrotliminifyer.compress_json_file(
    input_path="data.json",
    output_path="data.json.br",
    quality=11
)

# Decompress back to JSON
jsonbrotliminifyer.decompress_json_file(
    input_path="data.json.br",
    output_path="restored.json"
)
```

### Batch File Processing

```python
import jsonbrotliminifyer
from pathlib import Path

# Compress multiple files concurrently
input_files = [
    "user_data.json",
    "config.json",
    "cache.json"
]

# Compress all files to output directory
results = jsonbrotliminifyer.compress_json_files(
    input_files=input_files,
    output_dir="compressed/",
    quality=6,  # Balanced speed/size
    max_workers=4  # Use 4 threads
)

# Check for errors
for i, result in enumerate(results):
    if result is not None:
        print(f"Failed to compress {input_files[i]}: {result}")
    else:
        print(f"Successfully compressed {input_files[i]}")

# Decompress all files
compressed_files = [f"compressed/{Path(f).stem}.br" for f in input_files]
results = jsonbrotliminifyer.decompress_json_files(
    input_files=compressed_files,
    output_dir="restored/",
    max_workers=4
)
```

## Advanced Patterns

### Streaming and Large Files

```python
import json
import jsonbrotliminifyer

def process_large_json_stream(file_path: str, chunk_size: int = 1000):
    """Process large JSON files in chunks to manage memory usage."""

    with open(file_path, 'r') as f:
        # Read file in chunks
        chunk = []
        for line_num, line in enumerate(f, 1):
            chunk.append(json.loads(line.strip()))

            if len(chunk) >= chunk_size:
                # Compress chunk
                compressed = jsonbrotliminifyer.compress_json(chunk)
                yield compressed, len(chunk)

                # Reset chunk
                chunk = []

        # Handle remaining items
        if chunk:
            compressed = jsonbrotliminifyer.compress_json(chunk)
            yield compressed, len(chunk)

# Usage
for compressed_chunk, item_count in process_large_json_stream("large_file.jsonl"):
    # Save or transmit compressed chunks
    with open(f"chunk_{hash(compressed_chunk)}.br", 'wb') as f:
        f.write(compressed_chunk)
```

### Caching Layer

```python
import jsonbrotliminifyer
import hashlib
from pathlib import Path

class CompressedJSONCache:
    """A simple compressed JSON caching system."""

    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_key(self, key: str) -> str:
        """Generate cache file path from key."""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return str(self.cache_dir / f"{hash_key}.br")

    def set(self, key: str, data: dict, quality: int = 6):
        """Store compressed data."""
        compressed = jsonbrotliminifyer.compress_json(data, quality=quality)
        cache_path = self._get_cache_key(key)
        with open(cache_path, 'wb') as f:
            f.write(compressed)

    def get(self, key: str) -> dict:
        """Retrieve and decompress data."""
        cache_path = self._get_cache_key(key)
        if not Path(cache_path).exists():
            raise KeyError(f"Cache key '{key}' not found")

        with open(cache_path, 'rb') as f:
            compressed = f.read()

        return jsonbrotliminifyer.decompress_json(compressed)

    def has(self, key: str) -> bool:
        """Check if key exists in cache."""
        return Path(self._get_cache_key(key)).exists()

# Usage
cache = CompressedJSONCache()

# Store user data
user_data = {"id": 123, "profile": {"name": "Alice", "preferences": {...}}}
cache.set("user_123", user_data)

# Retrieve user data
retrieved = cache.get("user_123")
assert retrieved == user_data
```

### API Response Compression

```python
from flask import Flask, request, Response
import jsonbrotliminifyer

app = Flask(__name__)

@app.route('/api/data')
def get_compressed_data():
    """API endpoint that serves compressed JSON data."""

    # Generate response data
    data = {
        "status": "success",
        "data": {
            "items": [...],  # Large dataset
            "metadata": {...}
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }

    # Check if client accepts Brotli compression
    accept_encoding = request.headers.get('Accept-Encoding', '')

    if 'br' in accept_encoding:
        # Compress response
        compressed = jsonbrotliminifyer.compress_json(data, quality=6)
        return Response(
            compressed,
            mimetype='application/json',
            headers={'Content-Encoding': 'br'}
        )
    else:
        # Return uncompressed JSON
        return data

if __name__ == '__main__':
    app.run()
```

### Data Pipeline Integration

```python
import jsonbrotliminifyer
from pathlib import Path
import logging

class DataPipeline:
    """Example data processing pipeline with compression."""

    def __init__(self, temp_dir: str = "temp"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def process_dataset(self, input_files: list, output_dir: str):
        """Process multiple JSON files with compression."""

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Stage 1: Compress all input files
        self.logger.info(f"Compressing {len(input_files)} files...")
        compressed_files = []
        results = jsonbrotliminifyer.compress_json_files(
            input_files=input_files,
            output_dir=str(self.temp_dir),
            quality=9,  # High compression for storage
            max_workers=8
        )

        # Collect successful compressions
        for i, result in enumerate(results):
            if result is None:
                compressed_files.append(
                    self.temp_dir / f"{Path(input_files[i]).stem}.br"
                )
            else:
                self.logger.error(f"Failed to compress {input_files[i]}: {result}")

        # Stage 2: Further processing (e.g., upload to cloud storage)
        self.logger.info(f"Processing {len(compressed_files)} compressed files...")

        for compressed_file in compressed_files:
            # Simulate processing/upload
            self.logger.info(f"Processing {compressed_file}")

            # Move to final destination
            final_path = output_path / compressed_file.name
            compressed_file.rename(final_path)

        return len(compressed_files)

# Usage
pipeline = DataPipeline()
processed = pipeline.process_dataset(
    input_files=["data1.json", "data2.json", "data3.json"],
    output_dir="processed"
)
print(f"Successfully processed {processed} files")
```

## Error Handling

```python
import jsonbrotliminifyer

def safe_compress_file(input_path: str, output_path: str) -> bool:
    """Compress a file with comprehensive error handling."""

    try:
        jsonbrotliminifyer.compress_json_file(input_path, output_path)
        print(f"Successfully compressed {input_path}")
        return True

    except ValueError as e:
        print(f"Validation error: {e}")
        return False

    except FileNotFoundError:
        print(f"Input file not found: {input_path}")
        return False

    except PermissionError:
        print(f"Permission denied accessing files")
        return False

    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def safe_decompress_data(compressed_bytes: bytes):
    """Decompress with error handling."""

    try:
        return jsonbrotliminifyer.decompress_json(compressed_bytes)

    except ValueError as e:
        if "Invalid Brotli-compressed data" in str(e):
            raise ValueError("Data is not valid Brotli compressed data")
        elif "not valid JSON" in str(e):
            raise ValueError("Decompressed data is not valid JSON")
        else:
            raise

    except Exception as e:
        raise RuntimeError(f"Decompression failed: {e}")
```

## Performance Optimization

### Memory Usage

```python
import jsonbrotliminifyer
import psutil
import os

def monitor_memory_usage(func, *args, **kwargs):
    """Monitor memory usage during compression/decompression."""

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    result = func(*args, **kwargs)

    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_delta = final_memory - initial_memory

    print(f"Memory usage: {initial_memory:.1f}MB → {final_memory:.1f}MB "
          f"(Δ{memory_delta:+.1f}MB)")

    return result

# Usage
large_data = {"data": "x" * 10_000_000}  # ~10MB string

compressed = monitor_memory_usage(
    jsonbrotliminifyer.compress_json,
    large_data,
    quality=6
)

decompressed = monitor_memory_usage(
    jsonbrotliminifyer.decompress_json,
    compressed
)
```

### Benchmarking

```python
import jsonbrotliminifyer
import time
import json

def benchmark_compression(data, quality: int = 11, iterations: int = 10):
    """Benchmark compression performance."""

    json_str = json.dumps(data)
    json_size = len(json_str.encode('utf-8'))

    # Benchmark compression
    compress_times = []
    compressed_sizes = []

    for _ in range(iterations):
        start = time.time()
        compressed = jsonbrotliminifyer.compress_json(data, quality=quality)
        compress_times.append(time.time() - start)
        compressed_sizes.append(len(compressed))

    # Benchmark decompression
    decompress_times = []
    for _ in range(iterations):
        start = time.time()
        jsonbrotliminifyer.decompress_json(compressed)
        decompress_times.append(time.time() - start)

    avg_compress_time = sum(compress_times) / len(compress_times)
    avg_decompress_time = sum(decompress_times) / len(decompress_times)
    avg_compressed_size = sum(compressed_sizes) / len(compressed_sizes)

    compression_ratio = avg_compressed_size / json_size

    print(f"Original size: {json_size} bytes")
    print(f"Compressed size: {avg_compressed_size:.0f} bytes")
    print(f"Compression ratio: {compression_ratio:.3f}x")
    print(f"Compress speed: {json_size / avg_compress_time / 1024 / 1024:.1f} MB/s")
    print(f"Decompress speed: {json_size / avg_decompress_time / 1024 / 1024:.1f} MB/s")

# Usage
test_data = {
    "users": [{"id": i, "data": "x" * 100} for i in range(1000)],
    "metadata": {"version": "1.0", "large_field": "y" * 50000}
}

benchmark_compression(test_data, quality=6)
```</content>
<parameter name="filePath">docs/usage.md