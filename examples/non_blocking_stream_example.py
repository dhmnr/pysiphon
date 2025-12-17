#!/usr/bin/env python3
"""
Example: Non-Blocking Frame Stream Control Loop

This demonstrates the non-blocking streaming pattern where you can:
- Receive frames continuously in a background thread
- Poll for the latest frame in your control loop
- Process frames (AI, computer vision, etc.)
- Send commands based on frame analysis
- All while maintaining control flow in your main loop

This pattern is ideal for game AI, automation, and real-time processing.
"""

import time
from pysiphon import SiphonClient


def main():
    # Connect to Siphon server
    with SiphonClient("localhost:50051") as client:
        
        # Initialize (assuming you have a config file)
        # client.init_all("config.toml")
        
        print("=== Non-Blocking Frame Stream Control Loop Demo ===\n")
        
        # Start non-blocking frame stream in background
        # This returns immediately and frames are received in a background thread
        stream_handle = client.start_frame_stream(format="jpeg", quality=85)
        
        start_time = time.time()
        frames_processed = 0
        commands_sent = 0
        duration = 10  # Run for 10 seconds
        
        print(f"Starting control loop for {duration} seconds...")
        print("Press Ctrl+C to stop early\n")
        
        try:
            # Main control loop - this is where your AI/automation logic goes
            while True:
                elapsed = time.time() - start_time
                
                # Check if we should stop
                if elapsed >= duration:
                    break
                
                # Poll for latest frame (non-blocking)
                frame = client.get_latest_frame(stream_handle)
                
                if frame:
                    # We got a new frame! Process it here
                    frames_processed += 1
                    
                    # === YOUR PROCESSING LOGIC GOES HERE ===
                    
                    # Example 1: Simple frame info logging
                    if frames_processed % 15 == 0:  # Log every 15 frames
                        fps = frames_processed / elapsed if elapsed > 0 else 0
                        data_size_kb = len(frame.data) / 1024.0
                        print(f"\rFrame #{frame.frame_number:4d} | "
                              f"Size: {frame.width}x{frame.height} | "
                              f"FPS: {fps:5.1f} | "
                              f"Data: {data_size_kb:6.1f} KB | "
                              f"Commands: {commands_sent:3d}", end='', flush=True)
                    
                    # Example 2: Decode and analyze frame
                    # You could use PIL, OpenCV, or other libraries to decode the JPEG:
                    """
                    from PIL import Image
                    from io import BytesIO
                    
                    if frame.format == "jpeg":
                        img = Image.open(BytesIO(frame.data))
                        # Now you can:
                        # - Run object detection
                        # - OCR to read text
                        # - Color analysis
                        # - Pattern matching
                        # - Whatever your use case needs
                    """
                    
                    # Example 3: Send commands based on frame analysis
                    if frames_processed % 30 == 0:  # Every ~2 seconds at 15fps
                        # Example: Press 'w' key for 50ms
                        # client.input_key_tap(["w"], 50, 0)
                        commands_sent += 1
                    
                    # Example 4: Read game state and react
                    """
                    # Get player health from memory
                    health = client.get_attribute("player_health")
                    
                    if health["success"] and health["value"] < 50:
                        # Health is low, use healing item
                        client.input_key_tap(["h"], 50, 0)
                    """
                    
                else:
                    # No new frame available yet
                    # Sleep briefly to avoid busy-waiting and reduce CPU usage
                    time.sleep(0.005)  # 5ms sleep
                
                # You can also perform other tasks in the loop:
                # - Read memory attributes
                # - Update internal state
                # - Check conditions
                # - Send periodic commands
                # - Log data
                
        except KeyboardInterrupt:
            print("\n\nControl loop interrupted by user")
        
        finally:
            # Always stop the stream when done
            client.stop_frame_stream(stream_handle)
            
            total_time = time.time() - start_time
            
            print("\n\n=== Control Loop Complete ===")
            print(f"Duration:         {total_time:.2f}s")
            print(f"Frames processed: {frames_processed}")
            
            if total_time > 0:
                avg_fps = frames_processed / total_time
                print(f"Average FPS:      {avg_fps:.2f}")
            
            print(f"Commands sent:    {commands_sent}")
            
            # Calculate efficiency
            if frames_processed > 0:
                stream_stats = stream_handle.frames_received
                efficiency = (frames_processed / stream_stats * 100) if stream_stats > 0 else 0
                print(f"Processing efficiency: {efficiency:.1f}% ({frames_processed}/{stream_stats})")


if __name__ == "__main__":
    main()



