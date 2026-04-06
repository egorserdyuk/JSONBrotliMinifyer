# CLI Reference

JSONBrotliMinifyer provides a command-line interface (CLI) tool called `jsonbrotlim` for quick compression and decompression operations.

## Installation

The CLI tool is automatically installed when you install the package:

```bash
pip install jsonbrotliminifyer
```

Verify installation:

```bash
jsonbrotlim --help
```

## Usage

```bash
jsonbrotlim <command> [options]
```

## Commands

### compress

Compress JSON data from a file or stdin.

#### Syntax

```bash
jsonbrotlim compress [-i INPUT_FILE] [-o OUTPUT_FILE] [-q QUALITY]
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--input-file` | `-i` | Input JSON file to compress | stdin |
| `--output-file` | `-o` | Output compressed file | stdout |
| `--quality` | `-q` | Compression quality (0-11) | 11 |

#### Examples

```bash
# Compress a JSON file
jsonbrotlim compress -i data.json -o data.json.br

# Compress with custom quality
jsonbrotlim compress -i data.json -o data.fast.br -q 0

# Compress from stdin
echo '{"name": "test"}' | jsonbrotlim compress > output.br

# Compress from stdin to file
cat data.json | jsonbrotlim compress -o compressed.br
```

#### Exit Codes

- `0`: Success
- `1`: Error (invalid JSON, file not found, etc.)

---

### decompress

Decompress Brotli-compressed data from a file or stdin.

#### Syntax

```bash
jsonbrotlim decompress [-i INPUT_FILE] [-o OUTPUT_FILE]
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--input-file` | `-i` | Input compressed file to decompress | stdin |
| `--output-file` | `-o` | Output JSON file | stdout |

#### Examples

```bash
# Decompress a compressed file
jsonbrotlim decompress -i data.json.br -o restored.json

# Decompress from stdin
cat compressed.br | jsonbrotlim decompress

# Decompress from stdin to file
jsonbrotlim decompress -i compressed.br -o output.json
```

#### Exit Codes

- `0`: Success
- `1`: Error (invalid compressed data, file not found, etc.)

## Common Usage Patterns

### File Compression Workflow

```bash
# 1. Compress a large JSON file
jsonbrotlim compress -i large_dataset.json -o large_dataset.json.br -q 9

# 2. Verify file was created
ls -lh large_dataset.json*

# 3. Decompress to verify integrity
jsonbrotlim decompress -i large_dataset.json.br -o verified.json

# 4. Compare original and decompressed
diff large_dataset.json verified.json || echo "Files differ!"
```

### Pipeline Usage

```bash
# Compress API response
curl -s https://api.example.com/data | jsonbrotlim compress > response.br

# Decompress and format
jsonbrotlim decompress -i response.br | jq '.'
```

### Batch Processing with Shell

```bash
# Compress all JSON files in directory
for file in *.json; do
    jsonbrotlim compress -i "$file" -o "${file%.json}.br"
done

# Decompress all .br files
for file in *.br; do
    jsonbrotlim decompress -i "$file" -o "${file%.br}.json"
done
```

### Integration with Other Tools

```bash
# Compress and upload
jsonbrotlim compress -i config.json | aws s3 cp - s3://my-bucket/config.br

# Download and decompress
aws s3 cp s3://my-bucket/data.br - | jsonbrotlim decompress > data.json
```

## Advanced Options

### Quality Levels

The `--quality` parameter controls the compression speed vs. size tradeoff:

```bash
# Fastest compression (largest output)
jsonbrotlim compress -i data.json -o data.br -q 0

# Balanced (recommended for most cases)
jsonbrotlim compress -i data.json -o data.br -q 6

# Best compression (slowest, smallest output)
jsonbrotlim compress -i data.json -o data.br -q 11
```

### Error Handling

The CLI tool provides clear error messages:

```bash
# Invalid JSON input
echo '{"invalid": json}' | jsonbrotlim compress
# Error: Invalid JSON input: Expecting ',' delimiter: line 1 column 17

# Non-existent input file
jsonbrotlim compress -i nonexistent.json -o output.br
# Error: [Errno 2] No such file or directory: 'nonexistent.json'

# Invalid compressed data
echo "not compressed data" | jsonbrotlim decompress
# Error: Invalid Brotli-compressed data
```

## Performance Tips

### Large Files

For large files, ensure adequate memory:

```bash
# Monitor memory usage
/usr/bin/time -v jsonbrotlim compress -i large_file.json -o large_file.br
```

### Parallel Processing

For multiple files, use shell parallelism:

```bash
# Compress multiple files in parallel (4 at a time)
ls *.json | xargs -n 1 -P 4 -I {} jsonbrotlim compress -i {} -o {}.br
```

### I/O Optimization

For better performance with large files:

```bash
# Use ionice for I/O priority (Linux)
ionice -c 3 jsonbrotlim compress -i large.json -o large.br

# Use nice for CPU priority
nice -n 10 jsonbrotlim compress -i large.json -o large.br
```

## Integration Examples

### Docker Usage

```dockerfile
FROM python:3.9-slim

RUN pip install jsonbrotliminifyer

# Copy and compress configuration
COPY config.json /app/
RUN jsonbrotlim compress -i /app/config.json -o /app/config.br

# Runtime decompression
CMD jsonbrotlim decompress -i /app/config.br | myapp
```

### Shell Scripts

```bash
#!/bin/bash
# compress_backup.sh - Compress JSON backups

BACKUP_DIR="/backups"
COMPRESSED_DIR="/compressed"

mkdir -p "$COMPRESSED_DIR"

for json_file in "$BACKUP_DIR"/*.json; do
    if [[ -f "$json_file" ]]; then
        base_name=$(basename "$json_file" .json)
        compressed_file="$COMPRESSED_DIR/${base_name}.br"

        echo "Compressing $json_file -> $compressed_file"
        if jsonbrotlim compress -i "$json_file" -o "$compressed_file"; then
            echo "✓ Compressed successfully"
        else
            echo "✗ Compression failed"
            exit 1
        fi
    fi
done

echo "All backups compressed!"
```

### Python Integration

```python
import subprocess
import jsonbrotliminifyer

def compress_with_cli(data: dict, quality: int = 11) -> bytes:
    """Compress using CLI tool instead of library."""
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_input = f.name

    # Compress with CLI
    temp_output = temp_input + '.br'
    result = subprocess.run([
        'jsonbrotlim', 'compress',
        '-i', temp_input,
        '-o', temp_output,
        '-q', str(quality)
    ], capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"CLI compression failed: {result.stderr}")

    # Read compressed data
    with open(temp_output, 'rb') as f:
        compressed = f.read()

    # Cleanup
    os.unlink(temp_input)
    os.unlink(temp_output)

    return compressed

# Usage
data = {"test": "data"}
compressed = compress_with_cli(data)
```

## Troubleshooting

### Command Not Found

If `jsonbrotlim` is not found:

```bash
# Check if installed
pip list | grep jsonbrotliminifyer

# Reinstall
pip uninstall jsonbrotliminifyer
pip install jsonbrotliminifyer

# Check PATH
which jsonbrotlim
echo $PATH
```

### Permission Issues

```bash
# Ensure execute permissions (usually not needed)
chmod +x $(which jsonbrotlim)

# Check file permissions for input/output
ls -la input.json output.br
```

### Memory Issues

For very large files:

```bash
# Increase system limits (Linux)
ulimit -v unlimited

# Use swap file if needed
sudo fallocate -l 4G /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Encoding Issues

The CLI handles UTF-8 by default. For other encodings:

```bash
# Convert encoding first
iconv -f latin1 -t utf8 input.json | jsonbrotlim compress > output.br
```

## Exit Codes Summary

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid input, file issues, etc.) |
| 2 | Command-line argument error |

## Version Information

```bash
jsonbrotlim --version
# Displays version information
```

## Help System

```bash
# Main help
jsonbrotlim --help

# Command-specific help
jsonbrotlim compress --help
jsonbrotlim decompress --help
```</content>
<parameter name="filePath">docs/cli.md