# Installation

## Requirements

pysiphon requires Python 3.10 or higher.

## Installing from Source

Clone the repository and install:

```bash
# Clone the repository
git clone https://github.com/yourusername/pysiphon.git
cd pysiphon

# Install with pip
pip install -e .

# Or with uv (recommended)
uv pip install -e .
```

## Installing with Documentation Tools

If you want to build the documentation locally:

```bash
pip install -e ".[docs]"
```

## Verifying Installation

Test that pysiphon is installed correctly:

=== "CLI"

    ```bash
    pysiphon --help
    ```

=== "Python"

    ```python
    from pysiphon import SiphonClient
    print("✓ Installation successful!")
    ```

## Dependencies

pysiphon has the following runtime dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| grpcio | ≥1.59.0 | gRPC framework |
| grpcio-tools | ≥1.59.0 | Protobuf compiler |
| tomli | ≥2.0.1 | TOML config parsing |
| Pillow | ≥10.0.0 | Image handling |
| click | ≥8.1.0 | CLI framework |

### Optional Dependencies

For building documentation:

| Package | Version | Purpose |
|---------|---------|---------|
| mkdocs | ≥1.5.0 | Documentation generator |
| mkdocs-material | ≥9.4.0 | Material theme |
| mkdocstrings | ≥0.24.0 | API documentation |
| pymdown-extensions | ≥10.0 | Markdown extensions |

## Regenerating gRPC Code

If you modify `siphon_service.proto`, regenerate the Python code:

```bash
python -m grpc_tools.protoc -I. \
    --python_out=pysiphon/generated \
    --grpc_python_out=pysiphon/generated \
    siphon_service.proto
```

!!! note "Import Fix"
    After regenerating, update `pysiphon/generated/siphon_service_pb2_grpc.py`:
    
    Change:
    ```python
    import siphon_service_pb2 as siphon__service__pb2
    ```
    
    To:
    ```python
    from . import siphon_service_pb2 as siphon__service__pb2
    ```

## Troubleshooting

### Import Errors

If you get import errors:

1. Make sure you're running from the project root, or
2. The package is properly installed with `-e` flag

### gRPC Version Conflicts

If you encounter gRPC version warnings:

```bash
pip install --upgrade grpcio grpcio-tools
```

### Windows Path Issues

On Windows, if you have issues with long paths, enable long path support:

1. Run `regedit`
2. Navigate to `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`
3. Set `LongPathsEnabled` to `1`

## Next Steps

- [Quick Start Guide](quickstart.md) - Get started in 5 minutes
- [Configuration](configuration.md) - Set up your config file
- [Python API Guide](../guide/api.md) - Learn the API

