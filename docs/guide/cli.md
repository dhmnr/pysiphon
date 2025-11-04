# CLI Usage

The pysiphon CLI provides two modes: **interactive** and **single-command**.

## Interactive Mode

Launch an interactive REPL-style session:

```bash
pysiphon interactive
```

### Available Commands

When in interactive mode, you have access to all commands:

#### Initialization

| Command | Description |
|---------|-------------|
| `init <config_file>` | Load config and initialize all subsystems |
| `status` | Show server initialization status |
| `config <config_file>` | Load and send config only |
| `init-memory` | Initialize memory subsystem |
| `init-input [window]` | Initialize input subsystem |
| `init-capture [window]` | Initialize capture subsystem |

#### Attributes

| Command | Description |
|---------|-------------|
| `get <attribute>` | Get attribute value |
| `set <attr> <type> <value>` | Set attribute (types: int, float, array, bool) |

#### Input Control

| Command | Description |
|---------|-------------|
| `input <keys> <hold_ms> <delay_ms>` | Tap keys (comma-separated) |
| `toggle <key> <0\|1>` | Press (1) or release (0) key |
| `move <dx> <dy> <steps>` | Move mouse by delta |

#### Capture

| Command | Description |
|---------|-------------|
| `capture <filename>` | Capture frame to file |

#### Command Execution

| Command | Description |
|---------|-------------|
| `exec <command> [args...]` | Execute command on server |

#### Recording

| Command | Description |
|---------|-------------|
| `rec-start <dir> <attrs> [duration]` | Start recording |
| `rec-stop <session_id>` | Stop recording |
| `rec-status <session_id>` | Get recording status |
| `rec-download <session_id> <file>` | Download recording |

#### General

| Command | Description |
|---------|-------------|
| `quit` or `exit` | Exit interactive mode |

### Example Session

```
$ pysiphon interactive
gRPC Siphon Client v0.1.0 (Python)
Connected to: localhost:50051

> init config.toml
Loading config from: config.toml
Config loaded - Process: game.exe, Window: Game Window, Attributes: 5
Initializing memory subsystem...
Memory initialized (PID: 12345)
Input initialized
Capture initialized (1920x1080)

=== Initialization Complete! ===

> get health
health = 100 (int)

> set speed int 150
Attribute set successfully

> input w,a,s,d 50 10
Keys w,a,s,d inputted successfully

> capture screenshot.png
Frame saved to: screenshot.png

> status
=== Server Status ===
Config Set:          Yes
Memory Initialized:  Yes
Input Initialized:   Yes
Capture Initialized: Yes
Process Name:        game.exe
Window Name:         Game Window
Process ID:          12345
Message: All systems initialized

> quit
Goodbye!
```

## Single-Command Mode

Execute individual commands directly from the shell.

### Initialization

```bash
# Initialize all subsystems
pysiphon init config.toml

# Check server status
pysiphon status
```

### Attributes

```bash
# Get attribute
pysiphon get health

# Set integer
pysiphon set speed int 100

# Set float
pysiphon set multiplier float 1.5

# Set byte array (hex)
pysiphon set data array "6D DE AD BE EF"

# Set boolean
pysiphon set enabled bool 1
```

### Input Control

```bash
# Tap single key (hold 50ms, no delay)
pysiphon input w 50 0

# Tap multiple keys (hold 50ms, delay 10ms between)
pysiphon input w,a,s,d 50 10

# Press key
pysiphon toggle shift 1

# Release key
pysiphon toggle shift 0

# Move mouse
pysiphon move 100 50 10
```

### Capture

```bash
# Capture to PNG
pysiphon capture screenshot.png

# Capture to JPEG
pysiphon capture image.jpg

# Capture to BMP
pysiphon capture frame.bmp
```

### Command Execution

```bash
# Execute command
pysiphon exec notepad.exe

# Execute with arguments
pysiphon exec python script.py arg1 arg2

# Execute with quotes
pysiphon exec echo "Hello World"
```

### Recording

```bash
# Start recording (30 seconds max, health and mana attributes)
pysiphon rec-start ./recordings health,mana 30

# Start recording (unlimited duration)
pysiphon rec-start ./recordings health,mana,position 0

# Check status
pysiphon rec-status abc123

# Stop recording
pysiphon rec-stop abc123

# Download recording
pysiphon rec-download abc123 recording.h5
```

## Global Options

### Custom Server Address

Connect to a different server:

```bash
pysiphon --host 192.168.1.100:50051 interactive
pysiphon --host 192.168.1.100:50051 get health
```

### Help

Get help on any command:

```bash
# General help
pysiphon --help

# Command-specific help
pysiphon get --help
pysiphon rec-start --help
```

## Exit Codes

Single-command mode returns appropriate exit codes:

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | Failure |

Use in scripts:

```bash
#!/bin/bash

if pysiphon init config.toml; then
    echo "Initialization successful"
    pysiphon get health
else
    echo "Initialization failed"
    exit 1
fi
```

## Shell Integration

### Bash Completion

Generate completion script:

```bash
_PYSIPHON_COMPLETE=bash_source pysiphon > ~/.pysiphon-complete.bash
source ~/.pysiphon-complete.bash
```

Add to `.bashrc`:

```bash
echo 'source ~/.pysiphon-complete.bash' >> ~/.bashrc
```

### Zsh Completion

```bash
_PYSIPHON_COMPLETE=zsh_source pysiphon > ~/.pysiphon-complete.zsh
source ~/.pysiphon-complete.zsh
```

Add to `.zshrc`:

```bash
echo 'source ~/.pysiphon-complete.zsh' >> ~/.zshrc
```

## Scripting Examples

### Automated Testing

```bash
#!/bin/bash
set -e

pysiphon init config.toml

# Test attribute access
HEALTH=$(pysiphon get health | cut -d' ' -f3)
echo "Current health: $HEALTH"

# Modify and verify
pysiphon set health int 999
pysiphon get health

# Capture screenshot
pysiphon capture test_$(date +%s).png
```

### Monitoring Loop

```bash
#!/bin/bash

pysiphon init config.toml

while true; do
    pysiphon get health
    pysiphon get mana
    sleep 1
done
```

### Batch Operations

```bash
#!/bin/bash

# Initialize once
pysiphon init config.toml

# Perform multiple operations
for key in w a s d; do
    pysiphon input $key 50 100
done

# Capture final state
pysiphon capture final.png
```

## Tips and Tricks

!!! tip "Interactive Mode for Exploration"
    Use interactive mode when learning or testing. It's faster than running separate commands.

!!! tip "Single Commands for Scripts"
    Use single-command mode in scripts and automation for better error handling and exit codes.

!!! tip "Tab Completion"
    Install shell completion for faster command entry.

!!! warning "Process Attachment"
    Initialize only once per session. Repeated initialization may cause issues.

## Troubleshooting

### Command Not Found

Ensure pysiphon is installed:

```bash
pip install -e .
```

Or run directly:

```bash
python -m pysiphon.cli --help
```

### Connection Refused

Verify server is running:

```bash
pysiphon --host localhost:50051 status
```

### Unicode Errors (Windows)

The CLI uses ASCII-safe output for Windows compatibility. If you see encoding errors, ensure your terminal supports UTF-8:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## Next Steps

- [Python API Guide](api.md) - Programmatic usage
- [Examples](examples.md) - More usage examples
- [Recording Guide](recording.md) - Recording details

