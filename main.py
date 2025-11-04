"""
Example usage of pysiphon programmatic API.

For CLI usage, use: pysiphon --help
"""

from pysiphon import SiphonClient


def main():
    print("pysiphon - Python gRPC client for Siphon service")
    print("\nFor interactive CLI, run: pysiphon interactive")
    print("For single commands, run: pysiphon <command> [args...]")
    print("\nExample programmatic usage:")
    print("-" * 50)
    
    # Example code (will fail without server running)
    example_code = """
from pysiphon import SiphonClient

# Connect to server
with SiphonClient("localhost:50051") as client:
    # Initialize all subsystems
    client.init_all("config.toml")
    
    # Get attribute
    result = client.get_attribute("health")
    print(f"Health: {result['value']}")
    
    # Set attribute
    client.set_attribute("speed", 100, "int")
    
    # Capture screenshot
    client.capture_and_save("screenshot.png")
    
    # Input control
    client.input_key_tap(["w"], 50, 0)
    client.move_mouse(10, 20, 5)
"""
    print(example_code)
    
    print("\nSee README.md for complete documentation.")


if __name__ == "__main__":
    main()
