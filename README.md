# Codest

A simple and efficient tool to collect source code files into a single document.

## Installation

```bash
# Install from PyPI
pip install codest

# Install from GitHub
pip install git+https://github.com/yourusername/codest.git
```

## Usage

After installation, you can use the tool in two ways:

1. Command line interface:
```bash
codest .                        # Collect files from current directory
codest /path/to/directory -o output.txt  # Specify output file
codest . --max-size 2000       # Set maximum file size (KB)
```

2. Python API:
```python
from codest import create_source_document

create_source_document(
    root_dir=".",
    output_file="output.txt",
    max_file_size_kb=1000
)
```

## Features

- Collects source code files from a directory and its subdirectories
- Respects .gitignore patterns
- Configurable file size limits
- Supports various programming languages
- Generates a single markdown document with syntax highlighting

## License

MIT License
