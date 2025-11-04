# Python API Guide

Use pysiphon as a library in your Python applications.

## Basic Usage

```python
from pysiphon import SiphonClient

# Create client (context manager handles cleanup)
with SiphonClient("localhost:50051") as client:
    # Initialize
    client.init_all("config.toml")
    
    # Use the client
    result = client.get_attribute("health")
    print(result["value"])
```

## Client Creation

### Default Server

```python
from pysiphon import SiphonClient

# Connects to localhost:50051
client = SiphonClient()
```

### Custom Server

```python
client = SiphonClient("192.168.1.100:50051")
```

### Context Manager (Recommended)

```python
with SiphonClient() as client:
    # Client automatically closes on exit
    pass
```

### Manual Management

```python
client = SiphonClient()
try:
    # Use client
    pass
finally:
    client.close()
```

## Initialization

### Quick Initialization

Initialize everything at once:

```python
success = client.init_all("config.toml", wait_time=2.0)
if not success:
    print("Initialization failed!")
```

### Step-by-Step Initialization

More control over each step:

```python
# 1. Set configuration
result = client.set_process_config("config.toml")
if not result["success"]:
    print(f"Config failed: {result['message']}")
    exit(1)

# 2. Initialize memory
result = client.initialize_memory()
print(f"Process ID: {result['process_id']}")

# 3. Initialize input
result = client.initialize_input()
# Or with specific window
result = client.initialize_input("Game Window")

# 4. Initialize capture
result = client.initialize_capture()
# Or with specific window
result = client.initialize_capture("Game Window")
```

### Check Status

```python
status = client.get_server_status()

if status["memory_initialized"]:
    print(f"Process ID: {status['process_id']}")

if status["capture_initialized"]:
    print(f"Capture ready")
```

## Attribute Operations

### Get Attribute

```python
result = client.get_attribute("health")

if result["success"]:
    value = result["value"]
    value_type = result["value_type"]  # "int", "float", "array", "bool"
    print(f"{value} ({value_type})")
else:
    print(f"Error: {result['message']}")
```

### Set Attribute

```python
# Integer
result = client.set_attribute("health", 100, "int")

# Float
result = client.set_attribute("speed", 1.5, "float")

# Boolean
result = client.set_attribute("enabled", True, "bool")

# Byte array (from hex string)
result = client.set_attribute("data", "6D DE AD BE EF", "array")

# Byte array (from bytes)
data = bytes([0x6D, 0xDE, 0xAD, 0xBE, 0xEF])
result = client.set_attribute("data", data, "array")
```

## Input Control

### Key Tap

Tap keys with timing control:

```python
# Single key
client.input_key_tap(["w"], hold_ms=50, delay_ms=0)

# Multiple keys
client.input_key_tap(["w", "a", "s", "d"], hold_ms=50, delay_ms=10)

# Key combination
client.input_key_tap(["ctrl", "c"], hold_ms=100, delay_ms=0)
```

### Key Toggle

Press or release keys:

```python
# Press shift
client.input_key_toggle("shift", True)

# Do something while shift is held
client.input_key_tap(["a"], 50, 0)

# Release shift
client.input_key_toggle("shift", False)
```

### Mouse Movement

```python
# Move mouse (delta_x, delta_y, steps)
client.move_mouse(100, 50, 10)

# Instant movement (1 step)
client.move_mouse(100, 50, 1)

# Smooth movement (more steps)
client.move_mouse(100, 50, 20)
```

## Screen Capture

### Capture as PIL Image

```python
# Returns PIL Image object
image = client.capture_frame(as_image=True)

if image:
    # Use PIL methods
    image.save("screenshot.png")
    image.show()
    width, height = image.size
```

### Capture Raw Data

```python
# Returns dictionary with raw data
frame_data = client.capture_frame(as_image=False)

if frame_data and frame_data["success"]:
    pixels = frame_data["pixels"]  # Raw BGRA bytes
    width = frame_data["width"]
    height = frame_data["height"]
```

### Direct Save

```python
# Capture and save in one call
success = client.capture_and_save("screenshot.png")
```

## Command Execution

Execute commands on the remote system:

```python
result = client.execute_command(
    command="python",
    args=["script.py", "arg1", "arg2"],
    working_directory="C:\\scripts",
    timeout_seconds=30,
    capture_output=True
)

if result["success"]:
    print(f"Exit code: {result['exit_code']}")
    print(f"Output: {result['stdout']}")
    if result['stderr']:
        print(f"Errors: {result['stderr']}")
    print(f"Time: {result['execution_time_ms']}ms")
```

## Recording

### Start Recording

```python
result = client.start_recording(
    attribute_names=["health", "mana", "position"],
    output_directory="./recordings",
    max_duration_seconds=30  # 0 = unlimited
)

if result["success"]:
    session_id = result["session_id"]
    print(f"Recording started: {session_id}")
else:
    print(f"Failed: {result['message']}")
```

### Check Status

```python
status = client.get_recording_status(session_id)

if status["is_recording"]:
    print(f"Frame: {status['current_frame']}")
    print(f"Elapsed: {status['elapsed_time_seconds']:.1f}s")
    print(f"Latency: {status['current_latency_ms']:.2f}ms")
    print(f"Dropped: {status['dropped_frames']}")
```

### Stop Recording

```python
stats = client.stop_recording(session_id)

if stats["success"]:
    print(f"Total frames: {stats['total_frames']}")
    print(f"Duration: {stats['actual_duration_seconds']:.1f}s")
    print(f"Average FPS: {stats['actual_fps']:.1f}")
    print(f"Dropped frames: {stats['dropped_frames']}")
    print(f"Average latency: {stats['average_latency_ms']:.2f}ms")
```

### Download Recording

```python
success = client.download_recording(
    session_id=session_id,
    output_path="recording.h5",
    show_progress=True
)

if success:
    print("Download complete!")
```

## Utility Functions

### Hex Conversion

```python
from pysiphon import hex_to_bytes, bytes_to_hex

# Hex string to bytes
data = hex_to_bytes("6D DE AD BE EF")  # bytes([0x6d, 0xde, ...])

# Bytes to hex string
hex_str = bytes_to_hex(data)  # "6d de ad be ef"
```

### Config Parsing

```python
from pysiphon import parse_config_file

process_name, window_name, attributes = parse_config_file("config.toml")

print(f"Process: {process_name}")
print(f"Window: {window_name}")
print(f"Attributes: {list(attributes.keys())}")
```

## Error Handling

All methods return dictionaries with consistent structure:

```python
result = client.get_attribute("health")

# Check success
if result["success"]:
    # Operation succeeded
    value = result["value"]
else:
    # Operation failed
    error_message = result["message"]
    print(f"Error: {error_message}")
```

### Common Error Patterns

```python
# Try-except for connection errors
try:
    result = client.get_attribute("health")
except Exception as e:
    print(f"Connection error: {e}")

# Check and handle errors
result = client.set_attribute("health", 100, "int")
if not result["success"]:
    if "not found" in result["message"]:
        print("Attribute doesn't exist")
    elif "not initialized" in result["message"]:
        print("Initialize memory first")
    else:
        print(f"Unknown error: {result['message']}")
```

## Complete Example

```python
from pysiphon import SiphonClient, bytes_to_hex
import time

def main():
    # Connect to server
    with SiphonClient("localhost:50051") as client:
        # Initialize all subsystems
        print("Initializing...")
        if not client.init_all("config.toml"):
            print("Initialization failed!")
            return
        
        # Check status
        status = client.get_server_status()
        print(f"Process ID: {status['process_id']}")
        
        # Read initial state
        health = client.get_attribute("health")
        mana = client.get_attribute("mana")
        print(f"Health: {health['value']}, Mana: {mana['value']}")
        
        # Modify attributes
        client.set_attribute("health", 999, "int")
        client.set_attribute("speed", 2.0, "float")
        
        # Input sequence
        print("Pressing keys...")
        for key in ["w", "a", "s", "d"]:
            client.input_key_tap([key], 50, 100)
        
        # Capture screenshot
        print("Capturing screenshot...")
        client.capture_and_save("screenshot.png")
        
        # Start recording
        print("Starting recording...")
        result = client.start_recording(
            attribute_names=["health", "mana"],
            output_directory="./recordings",
            max_duration_seconds=10
        )
        session_id = result["session_id"]
        
        # Monitor recording
        for i in range(5):
            time.sleep(2)
            status = client.get_recording_status(session_id)
            print(f"Frame {status['current_frame']}, "
                  f"FPS: {status['current_frame']/status['elapsed_time_seconds']:.1f}")
        
        # Stop and download
        print("Stopping recording...")
        stats = client.stop_recording(session_id)
        print(f"Recorded {stats['total_frames']} frames at {stats['actual_fps']:.1f} FPS")
        
        client.download_recording(session_id, "recording.h5")
        print("Complete!")

if __name__ == "__main__":
    main()
```

## Next Steps

- [Examples](examples.md) - More example code
- [Recording Guide](recording.md) - Detailed recording info
- [API Reference](../api/client.md) - Complete API docs

