# Installation

This guide covers how to install JSONBrotliMinifyer for different use cases and environments.

## Prerequisites

- **Python Version**: 3.9 or higher
- **Operating System**: Linux, macOS, or Windows
- **Memory**: At least 64MB RAM (more for large datasets)

## Installation Methods

### From PyPI (Recommended)

The easiest way to install JSONBrotliMinifyer is from PyPI:

```bash
pip install jsonbrotliminifyer
```

### From Source

If you want to install from the source code:

```bash
# Clone the repository
git clone https://github.com/egorserdyuk/JSONBrotliMinifyer.git
cd JSONBrotliMinifyer

# Install in development mode
pip install -e .
```

### Development Installation

For contributors or development work:

```bash
# Clone the repository
git clone https://github.com/egorserdyuk/JSONBrotliMinifyer.git
cd JSONBrotliMinifyer

# Install with development dependencies
pip install -e .[dev]
# or
pip install -r requirements_dev.txt
```

## Verification

After installation, verify that JSONBrotliMinifyer is working:

```bash
# Check Python import
python -c "import jsonbrotliminifyer; print('Installation successful!')"

# Check CLI tool
jsonbrotlim --help
```

## Dependencies

JSONBrotliMinifyer has minimal dependencies:

### Runtime Dependencies

- **brotli** (>= 1.0.0): Python bindings for the Brotli compression library

### Development Dependencies

- **ruff**: Code linting and formatting
- **pytest**: Testing framework
- **mypy**: Static type checking
- **pre-commit**: Git hooks for code quality

## Platform-Specific Notes

### Linux

Works out of the box on all major Linux distributions. The `brotli` package may be available through your package manager:

```bash
# Ubuntu/Debian
sudo apt-get install python3-brotli

# CentOS/RHEL
sudo yum install python3-brotli
```

### macOS

Install using Homebrew if needed:

```bash
brew install brotli
pip install jsonbrotliminifyer
```

### Windows

Works out of the box. No additional system packages required.

## Troubleshooting

### Import Errors

If you get import errors, ensure Python 3.9+ is being used:

```bash
python --version
# Should show Python 3.9.0 or higher
```

### Brotli Library Issues

If the brotli library fails to install, you may need to install system-level dependencies:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install build-essential python3-dev
```

**macOS:**
```bash
xcode-select --install
```

**Windows:**
Ensure you have Visual Studio Build Tools installed if compiling from source.

### Permission Issues

If you encounter permission errors during installation:

```bash
# Install to user directory
pip install --user jsonbrotliminifyer

# Or use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install jsonbrotliminifyer
```

## Virtual Environment

It's recommended to use virtual environments:

```bash
# Create virtual environment
python -m venv jsonbrotli_env

# Activate (Linux/macOS)
source jsonbrotli_env/bin/activate

# Activate (Windows)
jsonbrotli_env\Scripts\activate

# Install
pip install jsonbrotliminifyer
```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade jsonbrotliminifyer
```

## Uninstalling

To remove JSONBrotliMinifyer:

```bash
pip uninstall jsonbrotliminifyer
```</content>
<parameter name="filePath">docs/installation.md