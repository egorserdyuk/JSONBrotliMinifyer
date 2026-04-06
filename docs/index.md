# JSONBrotliMinifyer Documentation

Welcome to the official documentation for **JSONBrotliMinifyer**, a high-performance Python library for compressing and decompressing JSON data using the Brotli compression algorithm.

## Overview

JSONBrotliMinifyer provides efficient, lossless compression of JSON data for storage and transmission. It combines JSON serialization with Brotli compression to achieve excellent compression ratios while maintaining fast compression/decompression speeds.

### Key Features

- 🚀 **High Performance**: Fast compression and decompression using optimized Brotli algorithm
- 📦 **Lossless Compression**: Perfect fidelity - decompress to get identical JSON data
- 🛡️ **Type Safe**: Full type annotations and strict validation
- 🔧 **Flexible API**: In-memory objects, file operations, and batch processing
- 💻 **CLI Tool**: Command-line interface for quick operations
- 🧵 **Concurrent Processing**: Multi-threaded batch operations for large datasets
- 🔒 **Security**: Path validation and safe file operations

### Use Cases

- **Data Storage**: Compress large JSON datasets for efficient storage
- **API Responses**: Reduce bandwidth for JSON API responses
- **Configuration Files**: Compress application configuration data
- **Data Pipelines**: Efficient intermediate data storage in ETL processes
- **Caching**: Compressed JSON caching for web applications

## Quick Start

```python
import jsonbrotliminifyer

# Compress JSON data
data = {"users": [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]}
compressed = jsonbrotliminifyer.compress_json(data)

# Decompress back to original
original = jsonbrotliminifyer.decompress_json(compressed)
```

## Documentation Sections

- **[Installation](installation.md)**: How to install JSONBrotliMinifyer
- **[Usage Guide](usage.md)**: Detailed usage examples and patterns
- **[API Reference](api.md)**: Complete API documentation
- **[CLI Reference](cli.md)**: Command-line interface documentation
- **[Contributing](contributing.md)**: How to contribute to the project

## Performance Characteristics

| Operation | Performance | Typical Use Case |
|-----------|-------------|------------------|
| `compress_json()` | Fast (10-100MB/s) | In-memory compression |
| `decompress_json()` | Very Fast (100-500MB/s) | In-memory decompression |
| File operations | Fast with atomic writes | File-based workflows |
| Batch operations | Concurrent processing | Large dataset processing |

## Compression Quality Levels

Brotli compression quality ranges from 0 (fastest, largest output) to 11 (slowest, smallest output):

- **0**: Fastest compression, ~3-4x smaller
- **6**: Balanced speed/size (recommended for most use cases)
- **11**: Maximum compression, ~5-8x smaller (default)

## Requirements

- **Python**: 3.9+
- **Memory**: Minimal overhead (depends on data size)
- **Dependencies**: Only `brotli` library required

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/egorserdyuk/JSONBrotliMinifyer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/egorserdyuk/JSONBrotliMinifyer/discussions)
- **Repository**: [GitHub Repository](https://github.com/egorserdyuk/JSONBrotliMinifyer)</content>
<parameter name="filePath">docs/index.md