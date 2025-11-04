# Quick Start

Get started with pysiphon in 5 minutes!

## Prerequisites

- Python 3.10 or higher installed
- Siphon server running on `localhost:50051`
- A valid configuration file (see [Configuration](configuration.md))

## Interactive Mode

The interactive mode provides a REPL-style interface for exploring and testing:

```bash
pysiphon interactive
```

### Example Session

```
> init config.toml           # Initialize everything
> status                     # Check server status
> get health                 # Get an attribute
health = 100 (int)

> set speed int 150          # Set an attribute
Attribute set successfully

> capture screenshot.png     # Take a screenshot
Frame saved to: screenshot.png

> input w,a,s,d 50 10       # Press keys
Keys w,a,s,d inputted successfully

> quit                       # Exit
Goodbye!
```

## Single Command Mode

Execute individual commands directly:

=== "Initialization"

    ```bash
    # Initialize all subsystems from config
    pysiphon init config.toml
    
    # Check server status
    pysiphon status
    ```

=== "Attributes"

    ```bash
    # Get attribute value
    pysiphon get health
    
    # Set integer
    pysiphon set speed int 100
    
    # Set byte array
    pysiphon set data array "6D DE AD BE EF"
    
    # Set float
    pysiphon set multiplier float 1.5
    
    # Set boolean
    pysiphon set enabled bool 1
    ```

=== "Input Control"

    ```bash
    # Tap a single key
    pysiphon input w 50 0
    
    # Multiple keys (combo)
    pysiphon input w,a,s,d 50 10
    
    # Toggle key state
    pysiphon toggle shift 1    # Press
    pysiphon toggle shift 0    # Release
    
    # Move mouse
    pysiphon move 100 50 10
    ```

=== "Capture"

    ```bash
    # Capture to PNG
    pysiphon capture screenshot.png
    
    # Capture to JPEG
    pysiphon capture screenshot.jpg
    
    # Capture to BMP
    pysiphon capture screenshot.bmp
    ```

=== "Recording"

    ```bash
    # Start recording
    pysiphon rec-start ./output health,mana 30
    # Returns session ID
    
    # Check status
    pysiphon rec-status <session-id>
    
    # Stop recording
    pysiphon rec-stop <session-id>
    
    # Download recording file
    pysiphon rec-download <session-id> recording.h5
    ```

## Python API

Use pysiphon as a library in your Python scripts:

### Basic Usage

```python
from pysiphon import SiphonClient

# Create client with context manager
with SiphonClient("localhost:50051") as client:
    # Initialize all subsystems at once
    client.init_all("config.toml")
    
    # Get attribute
    result = client.get_attribute("health")
    print(f"Health: {result['value']}")
    
    # Set attribute
    client.set_attribute("speed", 100, "int")
    
    # Capture and save
    client.capture_and_save("screenshot.png")
```

### Full Example

```python
from pysiphon import SiphonClient

# Connect to server
with SiphonClient("localhost:50051") as client:
    # Initialize
    if not client.init_all("config.toml"):
        print("Initialization failed!")
        exit(1)
    
    # Read attributes
    health = client.get_attribute("health")
    mana = client.get_attribute("mana")
    
    print(f"Health: {health['value']}, Mana: {mana['value']}")
    
    # Modify attributes
    client.set_attribute("health", 999, "int")
    client.set_attribute("speed", 2.5, "float")
    
    # Input control
    client.input_key_tap(["w"], hold_ms=100, delay_ms=0)
    client.move_mouse(delta_x=10, delta_y=20, steps=5)
    
    # Capture screenshot
    image = client.capture_frame(as_image=True)
    image.save("screenshot.png")
    
    # Start recording
    result = client.start_recording(
        attribute_names=["health", "mana", "position"],
        output_directory="./recordings",
        max_duration_seconds=30
    )
    session_id = result["session_id"]
    print(f"Recording started: {session_id}")
    
    # ... do something ...
    
    # Stop and get stats
    stats = client.stop_recording(session_id)
    print(f"Recorded {stats['total_frames']} frames")
    print(f"Average FPS: {stats['actual_fps']:.1f}")
```

## Working with Different Data Types

### Integer Values

```python
# Get
result = client.get_attribute("health")
if result["success"] and result["value_type"] == "int":
    health = result["value"]

# Set
client.set_attribute("health", 100, "int")
```

### Float Values

```python
# Get
result = client.get_attribute("speed")
if result["success"] and result["value_type"] == "float":
    speed = result["value"]

# Set
client.set_attribute("speed", 1.5, "float")
```

### Byte Arrays

```python
from pysiphon import hex_to_bytes, bytes_to_hex

# Set from hex string
data = hex_to_bytes("6D DE AD BE EF")
client.set_attribute("buffer", data, "array")

# Get and convert to hex
result = client.get_attribute("buffer")
if result["success"] and result["value_type"] == "array":
    hex_str = bytes_to_hex(result["value"])
    print(hex_str)  # "6d de ad be ef"
```

### Boolean Values

```python
# Get
result = client.get_attribute("enabled")
if result["success"] and result["value_type"] == "bool":
    enabled = result["value"]

# Set
client.set_attribute("enabled", True, "bool")
```

## Error Handling

All methods return dictionaries with a `success` field:

```python
result = client.get_attribute("health")

if result["success"]:
    print(f"Value: {result['value']}")
else:
    print(f"Error: {result['message']}")
```

## Custom Server Address

Connect to a different server:

=== "CLI"

    ```bash
    pysiphon --host 192.168.1.100:50051 interactive
    pysiphon --host 192.168.1.100:50051 get health
    ```

=== "Python"

    ```python
    client = SiphonClient("192.168.1.100:50051")
    ```

## Next Steps

- [Configuration Guide](configuration.md) - Learn about config files
- [CLI Usage](../guide/cli.md) - Detailed CLI documentation
- [Python API](../guide/api.md) - Complete API guide
- [Examples](../guide/examples.md) - More examples and patterns

