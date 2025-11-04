# CLI API Reference

Command-line interface functions and commands.

## CLI Entry Point

The main CLI is built using Click and provides both interactive and single-command modes.

### Main Command Group

::: pysiphon.cli.cli
    options:
      show_root_heading: true

## Command Functions

All CLI commands are implemented as Click functions. See the [CLI Usage Guide](../guide/cli.md) for detailed usage examples.

### Available Commands

- `interactive` - Start interactive REPL mode
- `init` - Initialize all subsystems from config file
- `status` - Show server status
- `get` - Get attribute value
- `set` - Set attribute value
- `input` - Tap keys
- `toggle` - Toggle key state
- `capture` - Capture frame to image
- `move` - Move mouse
- `exec` - Execute command on server
- `rec-start` - Start recording session
- `rec-stop` - Stop recording session
- `rec-status` - Get recording status
- `rec-download` - Download recording file

## Helper Functions

::: pysiphon.cli.get_client
    options:
      show_root_heading: true
      show_source: true

