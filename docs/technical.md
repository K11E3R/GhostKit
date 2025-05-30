# GhostKit Technical Documentation

## Core Architecture

GhostKit follows a modular, object-oriented architecture designed for maximum flexibility, extensibility, and operational security. This document provides technical details about each component and guidelines for effective usage.

## Module System

### Base Module Class

All modules extend the `BaseModule` class which provides:

- Standard initialization with module metadata
- Common utility methods
- Consistent interface for module interaction
- Logging and error handling

```python
class BaseModule:
    def __init__(self, name, description, author, version):
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        
    def run(self, args=None):
        """This method must be implemented by all modules"""
        raise NotImplementedError("Modules must implement the run method")
```

### Module Loading System

Modules are dynamically loaded at runtime based on the Python files present in the `modules/` directory. The main `GhostKit` class handles module discovery, loading, and execution:

```python
def load_modules(self):
    """Load all available modules from the modules directory"""
    modules_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules")
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)
        logger.warning(f"Created modules directory at {modules_dir}")
        return
        
    for filename in os.listdir(modules_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"modules.{module_name}")
                if hasattr(module, "Module"):
                    self.modules[module_name] = module.Module()
                    logger.info(f"Loaded module: {module_name}")
            except Exception as e:
                logger.error(f"Failed to load module {module_name}: {str(e)}")
```

## Core Modules Technical Details

### Exploit Engine (`exploit_engine.py`)

The exploit engine provides comprehensive exploitation capabilities including:

- Exploit generation for common vulnerabilities
- Payload creation and encoding
- Target validation and verification
- Exploit delivery mechanisms

Key components:
- `ExploitGenerator`: Creates customized exploits based on target info
- `PayloadFactory`: Generates various payload types (shellcode, reverse shells, etc.)
- `DeliveryManager`: Handles different exploit delivery methods

### Post-Exploitation (`post_exploitation.py`)

This module provides tools for maintaining access and performing lateral movement:

- Persistence mechanisms (registry, scheduled tasks, services)
- Credential harvesting and privilege escalation
- Network reconnaissance within compromised environments
- Lateral movement techniques

The module also includes memory manipulation capabilities for:
- Process injection (shellcode, DLL injection)
- DLL hijacking and side-loading
- Reflective loading techniques

### Web Security Suite

#### Web Core (`web_core.py`)

Provides foundation classes for web security testing:

- `WebTarget`: Encapsulates a web target with methods for interaction
- `WebCrawler`: Discovers site structure, forms, and parameters
- HTTP request handling and session management

#### Web Scanners

Three specialized scanners built on the Web Core:

1. **Web XSS Scanner** (`web_xss_scanner.py`):
   - Detection of reflected, stored, and DOM-based XSS
   - Context-aware payload generation
   - WAF bypass techniques

2. **Web Injection Scanner** (`web_injection_scanner.py`):
   - SQL injection detection (error-based, time-based, boolean-based)
   - Command injection detection
   - Custom error pattern recognition

3. **Web SSRF Scanner** (`web_ssrf_scanner.py`):
   - Server-Side Request Forgery detection
   - Internal service discovery
   - Various bypass techniques for restricted environments

### Hardware Interface (`hardware_interface.py`)

Provides tools for hardware and embedded device analysis:

- Serial/UART communication
- JTAG debugging interfaces
- I2C/SPI protocol analysis
- Firmware extraction and analysis

Key components:
- `SerialInterface`: For UART/serial communication
- `JTAGInterface`: For JTAG debugging
- `I2CInterface` and `SPIInterface`: For embedded bus protocols
- `FirmwareAnalyzer`: For firmware analysis

### Wireless Attacks (`wireless_attacks.py`)

Implements attacks against wireless protocols:

- WiFi network discovery and attacks
- Bluetooth device scanning and exploitation
- ZigBee protocol analysis

### Neural Swarm (`neural_swarm.py`)

Revolutionary AI-powered vulnerability analysis:

- Distributed agent-based architecture
- Biologically-inspired learning algorithms
- Consensus-based decision making for high-confidence results

Key components:
- `NeuralSwarmAgent`: Individual analysis agents with specialized roles
- `SwarmController`: Coordinates agent activities and aggregates results
- `BiologicallyInspiredLearner`: Implements evolutionary learning algorithms

## Advanced Usage Techniques

### Chaining Modules

Modules can be chained together for sophisticated attack sequences:

```python
# Example of module chaining (pseudocode)
scanner = web_xss_scanner.Module()
scan_results = scanner.run(["-u", "https://target.com"])

if scan_results.get("vulnerabilities"):
    exploit = exploit_engine.Module()
    exploit.run(["-t", "https://target.com", "-v", "xss", 
                 "--payload", scan_results["vulnerabilities"][0]["payload"]])
```

### Custom Module Development

To create a new module:

1. Create a new Python file in the `modules/` directory
2. Import the base module: `from modules.base_module import BaseModule`
3. Implement a `Module` class that extends `BaseModule`
4. Implement the required `run()` method

```python
# Example minimal module
from modules.base_module import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__(
            name="my_custom_module",
            description="My custom security module",
            author="YourName",
            version="1.0"
        )
        
    def run(self, args=None):
        # Parse arguments
        # Implement module functionality
        # Return results
        return {"status": "success", "result": "Module executed successfully"}
```

## Testing Against hub.zone01normandie.org

### Recommended Testing Workflow

For testing against hub.zone01normandie.org, follow this workflow:

1. **Initial Reconnaissance**:
   ```bash
   python ghostkit.py -m neural_swarm -m analyze -t hub.zone01normandie.org
   ```

2. **Web Vulnerability Scanning**:
   ```bash
   python ghostkit.py -m web_xss_scanner -u http://hub.zone01normandie.org
   python ghostkit.py -m web_injection_scanner -u http://hub.zone01normandie.org
   python ghostkit.py -m web_ssrf_scanner -u http://hub.zone01normandie.org
   ```

3. **Exploitation of Discovered Vulnerabilities**:
   Based on findings from steps 1-2, use the appropriate exploitation modules.

4. **Post-Exploitation**:
   If exploitation is successful, proceed with post-exploitation tasks.

### Important Testing Considerations

1. **Authorization**: Ensure you have proper authorization before testing
2. **Scope Limitations**: Respect testing scope boundaries
3. **Data Sensitivity**: Avoid accessing or exfiltrating sensitive data
4. **Testing Windows**: Adhere to agreed-upon testing timeframes
5. **Documentation**: Maintain detailed logs of all testing activities

## Performance Optimization

For optimal performance when running GhostKit:

1. Use selective module loading when only specific modules are needed
2. Implement rate limiting for web scanning to avoid triggering WAFs
3. Consider multi-threading for time-intensive operations
4. For large-scale scans, use the `-v` verbose flag to monitor progress

## Troubleshooting

### Common Issues

1. **Module Import Errors**:
   - Ensure all dependencies in requirements.txt are installed
   - Check for Python version compatibility (3.8+ recommended)

2. **Connection Timeouts**:
   - Verify network connectivity
   - Check if target is implementing rate limiting

3. **False Positives in Scans**:
   - Adjust sensitivity parameters for scanners
   - Validate findings manually when possible

## Security Considerations

When using GhostKit:

1. **Operational Security**:
   - Use appropriate proxies or VPNs to mask traffic
   - Consider using dedicated testing environments

2. **Data Handling**:
   - Securely store any sensitive data discovered during testing
   - Encrypt local logs and findings

3. **Legal Compliance**:
   - Ensure all testing activities comply with relevant laws and regulations
   - Maintain proper authorization documentation

---

## Appendix A: Module Command Reference

Detailed command-line reference for all modules:

### Web XSS Scanner
```
python ghostkit.py -m web_xss_scanner -u <target_url> [options]
  Options:
    --cookies "name1=value1;name2=value2"  Cookies to include
    --headers "name1:value1;name2:value2"  Custom headers
    --proxy http://127.0.0.1:8080          Proxy for requests
```

### Web Injection Scanner
```
python ghostkit.py -m web_injection_scanner -u <target_url> [options]
  Options:
    --param <parameter>                    Specific parameter to test
    --cookies "name1=value1;name2=value2"  Cookies to include
    --headers "name1:value1;name2:value2"  Custom headers
    --proxy http://127.0.0.1:8080          Proxy for requests
```

### Web SSRF Scanner
```
python ghostkit.py -m web_ssrf_scanner -u <target_url> [options]
  Options:
    --param <parameter>                    Specific parameter to test
    --cookies "name1=value1;name2=value2"  Cookies to include
    --headers "name1:value1;name2:value2"  Custom headers
    --proxy http://127.0.0.1:8080          Proxy for requests
```

### Hardware Interface
```
python ghostkit.py -m hardware_interface <subcommand> [options]
  Subcommands:
    serial    Serial interface tools
    usb       USB interface tools
    jtag      JTAG interface tools
    i2c       I2C interface tools
    spi       SPI interface tools
    firmware  Firmware analysis tools
```

### Neural Swarm
```
python ghostkit.py -m neural_swarm -m <mode> -t <target> [options]
  Modes:
    analyze   Analyze target for vulnerabilities
    learn     Train on new data
    evolve    Evolve new detection strategies
```

## Appendix B: Module Dependencies

Detailed dependencies for specific modules:

- **Web Security Suite**: requests, beautifulsoup4, lxml
- **Hardware Interface**: pyserial, pyusb, gpiozero
- **Neural Swarm**: numpy, tensorflow, scikit-learn
- **Wireless Attacks**: scapy, pyric, pybluez

---

<p align="center">
  <i>GhostKit Technical Documentation v1.0</i><br>
  <i>Classified: For Authorized Use Only</i>
</p>
