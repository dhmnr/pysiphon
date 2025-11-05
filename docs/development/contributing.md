# Contributing to pysiphon

Thank you for your interest in contributing to pysiphon!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/dhmnr/pysiphon.git
   cd pysiphon
   ```

2. **Install in development mode**
   ```bash
   pip install -e ".[docs]"
   ```

3. **Verify installation**
   ```bash
   pysiphon --help
   python -c "from pysiphon import SiphonClient; print('OK')"
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions
- Keep functions focused and single-purpose

### Example

```python
def get_attribute(self, name: str) -> Dict[str, Any]:
    """
    Get attribute value from server.
    
    Args:
        name: Attribute name
    
    Returns:
        Dictionary with success, message, value, and value_type
    """
    # Implementation
```

## Adding Features

### 1. Add to Client

If adding a new RPC method:

```python
# In pysiphon/client.py

def new_method(self, param: str) -> Dict[str, Any]:
    """
    Description of what this does.
    
    Args:
        param: Parameter description
    
    Returns:
        Dictionary with results
    """
    try:
        request = pb2.NewRequest()
        request.param = param
        
        response = self.stub.NewMethod(request)
        
        return {
            "success": response.success,
            "message": response.message
        }
    except grpc.RpcError as e:
        return {
            "success": False,
            "message": f"RPC failed: {e.details()}"
        }
```

### 2. Add CLI Command

Add both interactive and single-command support:

```python
# In pysiphon/cli.py

# For interactive mode (in the interactive() function)
elif command == 'newcmd':
    if len(args) < 1:
        print("Usage: newcmd <param>")
        continue
    
    result = client.new_method(args[0])
    print(result["message"])

# For single-command mode
@cli.command()
@click.argument('param')
@click.pass_context
def newcmd(ctx, param):
    """Description of command."""
    client = get_client(ctx.obj['host'])
    result = client.new_method(param)
    click.echo(result["message"])
    if not result["success"]:
        sys.exit(1)
```

### 3. Update Documentation

Add documentation for the new feature:

- Update API reference (autodoc will handle most of this)
- Add examples to `docs/guide/examples.md`
- Update relevant guides

### 4. Test Your Changes

Test both programmatic API and CLI:

```python
# Test programmatic API
from pysiphon import SiphonClient

with SiphonClient() as client:
    result = client.new_method("test")
    assert result["success"]
```

```bash
# Test CLI
pysiphon newcmd test
```

## Adding Utilities

If adding helper functions:

```python
# In pysiphon/utils.py

def new_utility_function(input_data: str) -> str:
    """
    Brief description.
    
    Args:
        input_data: Description
    
    Returns:
        Result description
    """
    # Implementation
    return result
```

Export in `__init__.py`:

```python
from .utils import new_utility_function

__all__ = [..., "new_utility_function"]
```

## Documentation

### Building Docs

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Serve locally
mkdocs serve

# Build static site
mkdocs build
```

Visit http://127.0.0.1:8000 to view docs locally.

### Writing Docs

- Use clear, concise language
- Include code examples
- Add warnings/tips using admonitions
- Test all code examples

#### Admonitions

```markdown
!!! note
    Important information

!!! tip
    Helpful suggestion

!!! warning
    Caution required

!!! danger
    Critical warning
```

## Testing Checklist

Before submitting:

- [ ] Code follows style guidelines
- [ ] All functions have docstrings
- [ ] Type hints are used
- [ ] Programmatic API works
- [ ] CLI interactive mode works
- [ ] CLI single-command mode works
- [ ] Documentation is updated
- [ ] Examples are tested
- [ ] No linter errors

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Update documentation
6. Submit pull request

### PR Description

Include in your PR:

- Description of changes
- Motivation for changes
- Examples of new functionality
- Screenshots (if UI changes)
- Breaking changes (if any)

## Questions?

Open an issue on GitHub or reach out to maintainers.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

