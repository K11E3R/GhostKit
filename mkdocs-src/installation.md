# GhostKit Installation Guide

## System Requirements

GhostKit is designed to run on various platforms but performs best in Unix-like environments.

### Minimum Requirements
- **OS**: Linux (recommended), macOS, Windows with WSL
- **Python**: 3.8+ (3.10+ recommended)
- **RAM**: 4GB minimum
- **Storage**: 500MB for core tools
- **Network**: Internet connection for updates and certain modules

### Recommended Specifications
- **OS**: Kali Linux, ParrotOS, or similar security-focused distribution
- **Python**: 3.10+
- **RAM**: 8GB+
- **Storage**: 2GB+ with additional modules
- **Network**: Dedicated network interface with monitor mode support

### Optional Hardware
- Serial adapters for hardware interface module
- SDR equipment for wireless modules
- Network adapters with monitor mode support

## Installation Methods

### Method 1: Direct Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/K11E3R/GhostKit.git
cd GhostKit

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt

# Setup security git hooks
cp scripts/git-hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

# Verify installation
python ghostkit.py --check
```

### Method 2: Docker Installation

```bash
# Pull the Docker image
docker pull k11e3r/ghostkit:latest

# Run GhostKit in a container
docker run -it --network host k11e3r/ghostkit

# For persistence and data sharing, mount volumes
docker run -it -v "$(pwd)/data:/opt/ghostkit/data" --network host k11e3r/ghostkit
```

### Method 3: Installing from PyPI (Coming Soon)

```bash
# Install from PyPI
pip install ghostkit

# Run GhostKit
ghostkit --help
```

## Post-Installation Configuration

### Environment Setup

Create a `.env` file in the project root for sensitive configuration:

```
# API Keys
SHODAN_API_KEY=your_key_here
VIRUSTOTAL_API_KEY=your_key_here

# Proxy Settings (optional)
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=http://proxy.example.com:8080

# Module Configuration
MAX_THREADS=10
DEBUG_MODE=False
```

### Module Dependencies

Some modules require additional dependencies:

1. **Hardware Interface Module**:
   ```bash
   pip install pyserial pyusb
   ```

2. **Wireless Module**:
   ```bash
   pip install scapy pyshark
   ```

3. **AI Module**:
   ```bash
   pip install tensorflow scikit-learn
   ```

### Security Configuration

1. **API Keys**: Set up API keys for third-party services
2. **Network Configuration**: Configure proxies and VPNs
3. **Permission Settings**: Ensure proper permissions for hardware access

## Troubleshooting

### Common Installation Issues

| Issue | Solution |
|-------|----------|
| Python version conflict | Use a virtual environment with the correct Python version |
| Missing dependencies | Run `pip install -r requirements.txt` again |
| Permission errors | Run with appropriate privileges (e.g., `sudo` for hardware access) |
| Git hooks not working | Check permissions with `chmod +x .git/hooks/pre-commit` |

### Platform-Specific Issues

#### Linux
- **Serial port access**: Add user to the `dialout` group: `sudo usermod -a -G dialout $USER`
- **USB device access**: Create udev rules for specific hardware

#### Windows
- **WSL recommended**: Native Windows has limited hardware support
- **Path issues**: Ensure Python is in your PATH environment variable

#### macOS
- **Developer tools**: Install Xcode Command Line Tools
- **Homebrew packages**: Some hardware interfaces require additional drivers

## Security Considerations

- Always run GhostKit in a controlled environment
- Use isolated virtual environments for testing
- Regularly update dependencies with `pip install --upgrade -r requirements.txt`
- Review the output of security scans before use

## Next Steps

After installation:
1. Review the [Usage Guide](usage.md) for basic commands
2. Explore [Module Documentation](usage.md) for specific functionality
3. Set up your [Development Environment](development/plugin-development.md) if contributing

## Support

If you encounter issues not covered in this guide:
1. Check the [FAQ](index.md)
2. Search existing [GitHub Issues](https://github.com/K11E3R/GhostKit/issues)
3. Open a new issue with detailed information about your problem
