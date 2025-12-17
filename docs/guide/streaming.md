# Frame Streaming Guide

pysiphon provides two modes of frame streaming to suit different use cases.

## Streaming Modes

### 1. Blocking Stream with Callback

Best for simple frame processing where you want a straightforward callback pattern.

```python
from pysiphon import SiphonClient

with SiphonClient("localhost:50051") as client:
    def process_frame(frame_data):
        print(f"Frame {frame_data.frame_number}: {frame_data.width}x{frame_data.height}")
        # Return False to stop streaming
        return True
    
    result = client.stream_frames_to_callback(
        process_frame,
        format="jpeg",
        quality=85,
        max_frames=100
    )
    
    print(f"Processed {result['frames_received']} frames at {result['average_fps']:.1f} FPS")
```

**CLI Usage:**
```bash
pysiphon stream --format jpeg --quality 85 --max-frames 100
```

### 2. Non-Blocking Stream with Polling

Best for control loops, game AI, and automation where you need to:
- Poll for frames at your own pace
- Send commands between frame processing
- Maintain control flow in your main loop
- Read game state/attributes alongside frame processing

```python
from pysiphon import SiphonClient
import time

with SiphonClient("localhost:50051") as client:
    # Start background stream
    handle = client.start_frame_stream(format="jpeg", quality=85)
    
    start_time = time.time()
    frames_processed = 0
    
    # Control loop
    while time.time() - start_time < 10:  # Run for 10 seconds
        # Poll for latest frame (non-blocking)
        frame = client.get_latest_frame(handle)
        
        if frame:
            frames_processed += 1
            
            # Process frame (run AI, computer vision, etc.)
            print(f"Processing frame {frame.frame_number}")
            
            # Decode JPEG if needed
            from PIL import Image
            from io import BytesIO
            if frame.format == "jpeg":
                img = Image.open(BytesIO(frame.data))
                # Now analyze the image
            
            # Send commands based on analysis
            if frames_processed % 30 == 0:
                client.input_key_tap(["w"], 50, 0)
            
            # Read game state
            health = client.get_attribute("player_health")
            if health["success"] and health["value"] < 50:
                client.input_key_tap(["h"], 50, 0)  # Use healing
        else:
            # No new frame yet, sleep briefly
            time.sleep(0.005)
    
    # Stop stream
    client.stop_frame_stream(handle)
```

**CLI Usage:**
```bash
pysiphon stream-loop --format jpeg --quality 85 --duration 10
```

## Format Options

### JPEG Format (Recommended)
- **Compressed:** Much smaller data size (~10-50 KB per frame)
- **Quality adjustable:** 1-100 (85 is a good default)
- **Fast transmission:** Lower bandwidth usage
- **Use case:** Most real-time applications, network streaming

```python
handle = client.start_frame_stream(format="jpeg", quality=85)
```

### Raw Format
- **Uncompressed:** Raw BGRA pixel data (~8 MB for 1920x1080)
- **Maximum quality:** No compression artifacts
- **Higher bandwidth:** Requires fast connection
- **Use case:** When you need pixel-perfect data

```python
handle = client.start_frame_stream(format="raw", quality=0)
```

## Performance Tips

### 1. Frame Processing
Only process frames when you need to. Skip frames if your processing is slower than the incoming frame rate:

```python
frame_counter = 0
while running:
    frame = client.get_latest_frame(handle)
    if frame:
        frame_counter += 1
        # Only process every 3rd frame
        if frame_counter % 3 == 0:
            process_frame(frame)
    else:
        time.sleep(0.005)
```

### 2. Avoid Busy-Waiting
Always sleep briefly when no frame is available to reduce CPU usage:

```python
if frame:
    process_frame(frame)
else:
    time.sleep(0.005)  # 5ms sleep
```

### 3. Use JPEG for Network Streaming
JPEG compression drastically reduces bandwidth:
- Raw 1920x1080 frame: ~8 MB
- JPEG quality 85: ~30 KB (250x smaller!)

### 4. Latest Frame Only
The non-blocking stream automatically keeps only the latest frame and drops older ones. This ensures you're always processing the most recent game state.

## Common Patterns

### Game AI Loop
```python
handle = client.start_frame_stream(format="jpeg", quality=85)

while game_running:
    frame = client.get_latest_frame(handle)
    
    if frame:
        # Decode and analyze frame
        game_state = analyze_frame(frame)
        
        # Make decision
        action = ai_model.predict(game_state)
        
        # Execute action
        if action == "move_forward":
            client.input_key_tap(["w"], 50, 0)
        elif action == "jump":
            client.input_key_tap(["space"], 50, 0)
    else:
        time.sleep(0.005)

client.stop_frame_stream(handle)
```

### Screen Monitoring
```python
handle = client.start_frame_stream(format="jpeg", quality=90)

while monitoring:
    frame = client.get_latest_frame(handle)
    
    if frame:
        # Run OCR to read text
        text = ocr_engine.read_text(frame.data)
        
        # Check for specific conditions
        if "error" in text.lower():
            send_alert("Error detected on screen!")
    else:
        time.sleep(0.010)

client.stop_frame_stream(handle)
```

### Performance Benchmarking
```python
handle = client.start_frame_stream(format="jpeg", quality=85)

start_time = time.time()
frames_received = 0
duration = 60  # 1 minute test

while time.time() - start_time < duration:
    frame = client.get_latest_frame(handle)
    if frame:
        frames_received += 1
    else:
        time.sleep(0.001)

client.stop_frame_stream(handle)

elapsed = time.time() - start_time
print(f"Average FPS: {frames_received / elapsed:.2f}")
print(f"Total received: {handle.frames_received}")
print(f"Processing efficiency: {frames_received / handle.frames_received * 100:.1f}%")
```

## Comparison: Blocking vs Non-Blocking

| Feature | Blocking Stream | Non-Blocking Stream |
|---------|----------------|---------------------|
| **Control Flow** | Callback-based | Loop-based |
| **Frame Access** | Every frame via callback | Latest frame via polling |
| **Command Sending** | Only in callback | Anytime in loop |
| **Attribute Reading** | Only in callback | Anytime in loop |
| **CPU Usage** | Lower (no busy-wait) | Low (with sleep) |
| **Complexity** | Simple | Moderate |
| **Best For** | Simple logging/recording | Game AI, automation |
| **Dropped Frames** | None (processes all) | Automatic (keeps latest) |

Choose blocking for simple tasks, non-blocking for complex control loops.



