# Examples

Real-world examples and patterns for common use cases.

## Health Monitor

Monitor player health and alert when low:

```python
from pysiphon import SiphonClient
import time

with SiphonClient() as client:
    client.init_all("config.toml")
    
    while True:
        result = client.get_attribute("health")
        health = result["value"]
        
        if health < 20:
            print(f"⚠️  LOW HEALTH: {health}")
            # Could trigger healing action
            client.input_key_tap(["h"], 50, 0)
        
        time.sleep(1)
```

## Auto-Clicker

Automated clicking with timing:

```python
from pysiphon import SiphonClient
import time

with SiphonClient() as client:
    client.init_all("config.toml")
    
    print("Auto-clicking... Press Ctrl+C to stop")
    try:
        while True:
            client.input_key_tap(["mouse_left"], 50, 0)
            time.sleep(0.1)  # 10 clicks per second
    except KeyboardInterrupt:
        print("\nStopped")
```

## Screenshot on Event

Capture screenshot when attribute changes:

```python
from pysiphon import SiphonClient
import time
from datetime import datetime

with SiphonClient() as client:
    client.init_all("config.toml")
    
    last_value = None
    
    while True:
        result = client.get_attribute("level")
        current_value = result["value"]
        
        if current_value != last_value and last_value is not None:
            # Level changed!
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"levelup_{timestamp}.png"
            client.capture_and_save(filename)
            print(f"Level changed: {last_value} → {current_value}")
            print(f"Screenshot saved: {filename}")
        
        last_value = current_value
        time.sleep(1)
```

## Data Logger

Log multiple attributes to CSV:

```python
from pysiphon import SiphonClient
import csv
import time
from datetime import datetime

with SiphonClient() as client:
    client.init_all("config.toml")
    
    with open("game_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "health", "mana", "position_x", "position_y"])
        
        try:
            while True:
                timestamp = datetime.now().isoformat()
                health = client.get_attribute("health")["value"]
                mana = client.get_attribute("mana")["value"]
                
                # Parse position array
                pos = client.get_attribute("position")["value"]
                pos_x = int.from_bytes(pos[0:4], "little")
                pos_y = int.from_bytes(pos[4:8], "little")
                
                writer.writerow([timestamp, health, mana, pos_x, pos_y])
                f.flush()
                
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nLogging stopped")
```

## Automated Combat

Simple combat automation:

```python
from pysiphon import SiphonClient
import time

with SiphonClient() as client:
    client.init_all("config.toml")
    
    def use_ability(key, cooldown):
        client.input_key_tap([key], 50, 0)
        time.sleep(cooldown)
    
    print("Combat bot active...")
    try:
        while True:
            # Check if in combat
            in_combat = client.get_attribute("in_combat")["value"]
            
            if in_combat:
                # Use abilities on cooldown
                use_ability("1", 1.5)  # Primary attack
                use_ability("2", 3.0)  # Secondary attack
                use_ability("3", 5.0)  # Special ability
                
                # Check health
                health = client.get_attribute("health")["value"]
                if health < 30:
                    use_ability("h", 10.0)  # Heal
            else:
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nCombat bot stopped")
```

## Training Data Collection

Collect data for machine learning:

```python
from pysiphon import SiphonClient
import json
import time

with SiphonClient() as client:
    client.init_all("config.toml")
    
    training_data = []
    
    print("Collecting training data... Perform actions in game")
    try:
        for i in range(1000):  # Collect 1000 samples
            # Capture state
            state = {
                "health": client.get_attribute("health")["value"],
                "mana": client.get_attribute("mana")["value"],
                "position": client.get_attribute("position")["value"].hex(),
            }
            
            # Capture screen
            image = client.capture_frame(as_image=True)
            if image:
                image.save(f"training/frame_{i:04d}.png")
            
            training_data.append(state)
            time.sleep(0.1)  # 10 Hz
            
            if i % 100 == 0:
                print(f"Collected {i} samples...")
    except KeyboardInterrupt:
        pass
    
    # Save metadata
    with open("training/metadata.json", "w") as f:
        json.dump(training_data, f, indent=2)
    
    print(f"Collected {len(training_data)} samples")
```

## Batch Screenshot Tool

Capture screenshots at regular intervals:

```python
from pysiphon import SiphonClient
import time
from datetime import datetime

with SiphonClient() as client:
    client.init_all("config.toml")
    
    interval = 5  # seconds
    count = 0
    
    print(f"Capturing screenshots every {interval}s...")
    try:
        while True:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/capture_{timestamp}.png"
            
            if client.capture_and_save(filename):
                count += 1
                print(f"[{count}] {filename}")
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\nCaptured {count} screenshots")
```

## State Machine Bot

Complex bot with state management:

```python
from pysiphon import SiphonClient
import time
from enum import Enum

class State(Enum):
    IDLE = 1
    FIGHTING = 2
    LOOTING = 3
    HEALING = 4

class Bot:
    def __init__(self, client):
        self.client = client
        self.state = State.IDLE
    
    def run(self):
        while True:
            if self.state == State.IDLE:
                self.check_for_enemies()
            elif self.state == State.FIGHTING:
                self.fight()
            elif self.state == State.LOOTING:
                self.loot()
            elif self.state == State.HEALING:
                self.heal()
            
            time.sleep(0.1)
    
    def check_for_enemies(self):
        enemy_nearby = self.client.get_attribute("enemy_nearby")["value"]
        if enemy_nearby:
            self.state = State.FIGHTING
    
    def fight(self):
        health = self.client.get_attribute("health")["value"]
        
        if health < 30:
            self.state = State.HEALING
            return
        
        in_combat = self.client.get_attribute("in_combat")["value"]
        if not in_combat:
            self.state = State.LOOTING
            return
        
        # Attack
        self.client.input_key_tap(["1"], 50, 0)
    
    def loot(self):
        self.client.input_key_tap(["f"], 50, 0)
        time.sleep(1)
        self.state = State.IDLE
    
    def heal(self):
        self.client.input_key_tap(["h"], 50, 0)
        time.sleep(5)
        self.state = State.IDLE

# Run bot
with SiphonClient() as client:
    client.init_all("config.toml")
    bot = Bot(client)
    
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\nBot stopped")
```

## Performance Testing

Test read performance:

```python
from pysiphon import SiphonClient
import time

with SiphonClient() as client:
    client.init_all("config.toml")
    
    # Warmup
    for _ in range(10):
        client.get_attribute("health")
    
    # Benchmark
    iterations = 1000
    start_time = time.time()
    
    for _ in range(iterations):
        client.get_attribute("health")
    
    elapsed = time.time() - start_time
    reads_per_sec = iterations / elapsed
    
    print(f"Performed {iterations} reads in {elapsed:.2f}s")
    print(f"Average: {reads_per_sec:.0f} reads/sec")
    print(f"Latency: {(elapsed/iterations)*1000:.2f}ms")
```

## Next Steps

- [Recording Guide](recording.md) - Advanced recording
- [CLI Usage](cli.md) - CLI examples
- [API Reference](../api/client.md) - Complete API

