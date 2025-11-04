# Configuration

pysiphon uses TOML configuration files to define process attributes and memory patterns.

## Configuration File Structure

A configuration file has two main sections:

1. **`[process_info]`** - Process identification
2. **`[attributes]`** - Memory attributes to track

## Basic Example

```toml
[process_info]
name = "game.exe"
window_name = "Game Window Title"

[attributes]
[attributes.health]
pattern = "48 8B 05 ?? ?? ?? ?? 48 85 C0"
offsets = [0x10, 0x20, 0x30]
type = "int"
length = 4
method = "pointer"

[attributes.position]
pattern = "F3 0F 10 05 ?? ?? ?? ??"
offsets = [0x0]
type = "array"
length = 12
method = "direct"
```

## Process Info Section

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Process executable name (e.g., "game.exe") |

### Optional Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `window_name` | string | Window title for input/capture targeting | `""` |

```toml
[process_info]
name = "game.exe"
window_name = "My Game - Level 1"
```

!!! tip "Window Name"
    If your game has a dynamic window title, you can update it at runtime using `initialize_input()` and `initialize_capture()` with window name parameters.

## Attributes Section

Each attribute defines how to find and read/write a value in memory.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `pattern` | string | Hex pattern to search (use `??` for wildcards) |
| `offsets` | array | Offset chain to follow from pattern match |
| `type` | string | Data type: `"int"`, `"float"`, `"array"`, or `"bool"` |

### Optional Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `length` | integer | Byte length (required for array type) | `0` |
| `method` | string | Resolution method: `"pointer"` or `"direct"` | `""` |

### Attribute Types

#### Integer (int)

32-bit signed integer value.

```toml
[attributes.health]
pattern = "48 8B 05 ?? ?? ?? ?? 48 85 C0"
offsets = [0x10, 0x20, 0x30]
type = "int"
length = 4
method = "pointer"
```

#### Float (float)

32-bit floating-point value.

```toml
[attributes.speed]
pattern = "F3 0F 11 05 ?? ?? ?? ??"
offsets = [0x0, 0x18]
type = "float"
length = 4
method = "pointer"
```

#### Array (array)

Arbitrary byte array (e.g., for coordinates, strings, or complex structures).

```toml
[attributes.position]
pattern = "F3 0F 10 05 ?? ?? ?? ??"
offsets = [0x0]
type = "array"
length = 12  # 3 floats (x, y, z)
method = "direct"
```

#### Boolean (bool)

Boolean value (stored as single byte).

```toml
[attributes.is_alive]
pattern = "80 3D ?? ?? ?? ?? 00"
offsets = [0x0]
type = "bool"
length = 1
method = "direct"
```

## Pattern Syntax

Patterns are hex byte sequences with optional wildcards:

- **Exact bytes**: `48 8B 05`
- **Wildcards**: `??` matches any byte
- **Spaces**: Optional, for readability

### Examples

```toml
# Match exact sequence
pattern = "488B0512345678"

# Match with wildcards
pattern = "48 8B 05 ?? ?? ?? ?? 48 85 C0"

# Complex pattern
pattern = "F3 0F 10 05 ?? ?? ?? ?? F3 0F 11 05 ?? ?? ?? ??"
```

!!! tip "Finding Patterns"
    Use tools like Cheat Engine, IDA Pro, or x64dbg to find memory patterns. Look for unique instruction sequences that remain stable across game updates.

## Offset Chains

Offsets define a pointer chain to follow from the pattern match:

```toml
# Direct access (no pointer following)
offsets = [0x0]

# Single pointer dereference
offsets = [0x10]

# Pointer chain: base -> +0x10 -> +0x20 -> +0x30
offsets = [0x10, 0x20, 0x30]
```

### How Offset Chains Work

1. Pattern found at address `A`
2. Read pointer at `A + offsets[0]` → `B`
3. Read pointer at `B + offsets[1]` → `C`
4. Read pointer at `C + offsets[2]` → `D`
5. Final value at address `D`

## Complete Example

```toml
[process_info]
name = "game.exe"
window_name = "Epic Game - Chapter 1"

# Player health (int)
[attributes.health]
pattern = "48 8B 05 ?? ?? ?? ?? 48 85 C0 74 ??"
offsets = [0x10, 0x20, 0x30, 0x0]
type = "int"
length = 4
method = "pointer"

# Player mana (int)
[attributes.mana]
pattern = "48 8B 05 ?? ?? ?? ?? 48 85 C0 74 ??"
offsets = [0x10, 0x20, 0x34, 0x0]  # Same base, different final offset
type = "int"
length = 4
method = "pointer"

# Movement speed multiplier (float)
[attributes.speed]
pattern = "F3 0F 11 05 ?? ?? ?? ?? 48 8B 45"
offsets = [0x0]
type = "float"
length = 4
method = "direct"

# Player position (array of 3 floats)
[attributes.position]
pattern = "F3 0F 10 05 ?? ?? ?? ?? F3 0F 11 45"
offsets = [0x0, 0x18]
type = "array"
length = 12
method = "pointer"

# God mode flag (bool)
[attributes.god_mode]
pattern = "80 3D ?? ?? ?? ?? 00 74 ??"
offsets = [0x0]
type = "bool"
length = 1
method = "direct"

# Inventory data (array)
[attributes.inventory]
pattern = "48 8D 0D ?? ?? ?? ?? E8 ?? ?? ?? ??"
offsets = [0x0]
type = "array"
length = 256
method = "direct"
```

## Using Configuration Files

### CLI

```bash
# Initialize with config
pysiphon init config.toml

# Or in interactive mode
> init config.toml
```

### Python API

```python
from pysiphon import SiphonClient

with SiphonClient() as client:
    # Full initialization
    client.init_all("config.toml")
    
    # Or step-by-step
    client.set_process_config("config.toml")
    client.initialize_memory()
```

## Configuration Tips

!!! tip "Pattern Stability"
    Choose patterns that are unlikely to change between game updates. Look for:
    
    - Unique instruction sequences
    - Function prologues/epilogues
    - String references
    - Static addresses

!!! warning "Offset Changes"
    Offsets may change between game versions. Always test after updates!

!!! info "Multiple Configs"
    You can create different config files for different games or versions:
    
    ```
    configs/
      ├── game_v1.toml
      ├── game_v2.toml
      └── another_game.toml
    ```

## Troubleshooting

### Pattern Not Found

- Verify the process is running
- Check pattern accuracy with memory scanner
- Try broader patterns with more wildcards
- Ensure pattern is in the correct module

### Wrong Values

- Verify offset chain is correct
- Check data type matches actual memory layout
- Confirm length is appropriate for type
- Test with Cheat Engine or similar tool first

### Access Violations

- Ensure process has necessary permissions
- Check if anti-cheat is blocking
- Verify offsets don't exceed allocation bounds

## Next Steps

- [Quick Start](quickstart.md) - Use your configuration
- [Python API Guide](../guide/api.md) - Programmatic usage
- [Examples](../guide/examples.md) - Real-world examples

