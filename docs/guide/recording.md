# Recording Guide

pysiphon can record attribute values to HDF5 format at 60 FPS for data collection and analysis.

## Quick Start

```python
from pysiphon import SiphonClient

with SiphonClient() as client:
    client.init_all("config.toml")
    
    # Start recording
    result = client.start_recording(
        attribute_names=["health", "mana", "position"],
        output_directory="./recordings",
        max_duration_seconds=30
    )
    session_id = result["session_id"]
    
    # ... perform actions ...
    
    # Stop recording
    stats = client.stop_recording(session_id)
    print(f"Recorded {stats['total_frames']} frames at {stats['actual_fps']:.1f} FPS")
    
    # Download recording files to directory
    client.download_recording(session_id, "./downloads")
```

## Starting a Recording

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `attribute_names` | List[str] | Attributes to record |
| `output_directory` | str | Directory to save recording on server |
| `max_duration_seconds` | int | Max duration (0 = unlimited) |

### Return Value

```python
{
    "success": bool,
    "message": str,
    "session_id": str  # Use this to control recording
}
```

### Example

```python
result = client.start_recording(
    attribute_names=["health", "mana", "position", "speed"],
    output_directory="C:\\recordings",
    max_duration_seconds=60  # Stop after 60 seconds
)

if result["success"]:
    session_id = result["session_id"]
    print(f"Recording {session_id}")
else:
    print(f"Failed: {result['message']}")
```

## Monitoring Recording

Check recording status in real-time:

```python
import time

# Start recording
result = client.start_recording(...)
session_id = result["session_id"]

# Monitor for 10 seconds
for i in range(10):
    status = client.get_recording_status(session_id)
    
    if status["is_recording"]:
        print(f"Frame: {status['current_frame']}")
        print(f"Time: {status['elapsed_time_seconds']:.1f}s")
        print(f"Latency: {status['current_latency_ms']:.2f}ms")
        print(f"Dropped: {status['dropped_frames']}")
        
        # Calculate FPS
        if status['elapsed_time_seconds'] > 0:
            fps = status['current_frame'] / status['elapsed_time_seconds']
            print(f"FPS: {fps:.1f}")
    
    time.sleep(1)
```

## Stopping a Recording

```python
stats = client.stop_recording(session_id)

print(f"Total frames: {stats['total_frames']}")
print(f"Duration: {stats['actual_duration_seconds']:.1f}s")
print(f"Average FPS: {stats['actual_fps']:.1f}")
print(f"Dropped frames: {stats['dropped_frames']}")
print(f"Average latency: {stats['average_latency_ms']:.2f}ms")

# Check performance
if stats['actual_fps'] < 55.0:
    print("⚠️  WARNING: FPS below target!")
```

## Downloading Recordings

Download recording files from server to a directory:

```python
success = client.download_recording(
    session_id=session_id,
    output_dir="./recordings",
    show_progress=True  # Show download progress
)

if success:
    print("Download complete!")
```

Progress output:
```
Downloading recording to: recordings
Downloading: recording.h5 (5097600 bytes)
  Progress: 45.2% (2304512/5097600 bytes)
  Progress: 100.0% (5097600/5097600 bytes)
✓ Completed: recording.h5 (5097600 bytes)
✓ Download complete!
  Files received: 1
  Total size: 5097600 bytes
  Saved to: recordings
```

The download can include multiple files (video, inputs, memory data) depending on the recording type.

## Reading HDF5 Files

Use h5py to read recorded data:

```python
import h5py
import numpy as np

with h5py.File("recording.h5", "r") as f:
    # List attributes
    print("Attributes:", list(f.keys()))
    
    # Read health data
    health = f["health"][:]
    timestamps = f["timestamps"][:]
    
    # Analyze
    print(f"Frames: {len(health)}")
    print(f"Duration: {timestamps[-1] - timestamps[0]:.2f}s")
    print(f"Min health: {health.min()}")
    print(f"Max health: {health.max()}")
    print(f"Avg health: {health.mean():.1f}")
```

## Performance Optimization

### Target: 60 FPS

Recording aims for 60 FPS. Factors affecting performance:

- **Number of attributes**: More attributes = more overhead
- **Attribute types**: Arrays are slower than integers
- **System load**: Other applications competing for resources
- **Network latency**: gRPC communication overhead

### Tips for Best Performance

1. **Record only needed attributes**
   ```python
   # Good: Only essential data
   client.start_recording(["health", "mana"], "./output", 30)
   
   # Bad: Recording everything
   client.start_recording(["health", "mana", "position", "velocity", ...], "./output", 30)
   ```

2. **Close other applications**: Reduce system load

3. **Use local server**: Minimize network latency

4. **Monitor dropped frames**: Check `dropped_frames` in stats

5. **Shorter durations**: Multiple short recordings better than one long

### Checking Performance

```python
stats = client.stop_recording(session_id)

if stats['dropped_frames'] > 0:
    drop_rate = (stats['dropped_frames'] / stats['total_frames']) * 100
    print(f"⚠️  Dropped {drop_rate:.1f}% of frames")

if stats['actual_fps'] < 55.0:
    print(f"⚠️  Actual FPS ({stats['actual_fps']:.1f}) below target (60)")
    print("Consider reducing attributes or system load")
```

## CLI Recording

### Start

```bash
pysiphon rec-start ./recordings health,mana,position 30
# Returns: Session ID: abc123def456
```

### Check Status

```bash
pysiphon rec-status abc123def456
```

### Stop

```bash
pysiphon rec-stop abc123def456
```

### Download

```bash
pysiphon rec-download abc123def456 ./recordings
```

## Complete Example

```python
from pysiphon import SiphonClient
import time

with SiphonClient() as client:
    # Initialize
    client.init_all("config.toml")
    
    # Start recording
    print("Starting recording...")
    result = client.start_recording(
        attribute_names=["health", "mana", "position"],
        output_directory="./recordings",
        max_duration_seconds=0  # Unlimited
    )
    
    if not result["success"]:
        print(f"Failed to start: {result['message']}")
        exit(1)
    
    session_id = result["session_id"]
    print(f"Recording: {session_id}")
    
    # Monitor for 30 seconds
    start_time = time.time()
    while time.time() - start_time < 30:
        status = client.get_recording_status(session_id)
        
        if status["is_recording"]:
            fps = status['current_frame'] / status['elapsed_time_seconds']
            print(f"Frame {status['current_frame']}, "
                  f"FPS: {fps:.1f}, "
                  f"Latency: {status['current_latency_ms']:.2f}ms")
        
        time.sleep(2)
    
    # Stop recording
    print("\nStopping recording...")
    stats = client.stop_recording(session_id)
    
    print(f"\n=== Recording Complete ===")
    print(f"Total frames: {stats['total_frames']}")
    print(f"Duration: {stats['actual_duration_seconds']:.1f}s")
    print(f"Average FPS: {stats['actual_fps']:.1f}")
    print(f"Dropped frames: {stats['dropped_frames']}")
    print(f"Average latency: {stats['average_latency_ms']:.2f}ms")
    
    # Download
    print("\nDownloading recording...")
    if client.download_recording(session_id, "./recordings"):
        print("Success! Files saved to ./recordings/")
    else:
        print("Download failed!")
```

## Troubleshooting

### Low FPS

**Symptoms**: `actual_fps` significantly below 60

**Solutions**:
- Reduce number of attributes
- Close other applications
- Check server performance
- Use shorter recording durations

### High Dropped Frames

**Symptoms**: Many `dropped_frames` in stats

**Solutions**:
- Same as low FPS
- Check network latency
- Ensure server has enough resources

### Download Fails

**Symptoms**: `download_recording` returns False

**Solutions**:
- Check session ID is correct
- Ensure recording was stopped
- Check disk space
- Verify network connection

## Next Steps

- [Examples](examples.md) - Recording examples
- [API Reference](../api/client.md) - Complete API docs

