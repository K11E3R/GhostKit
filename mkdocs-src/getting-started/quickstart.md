# GhostKit Quickstart Guide

![GhostKit Quickstart](../assets/images/quickstart-banner.png)

> "The fastest path to exploitation" — GhostKit Team

This quickstart guide will get you up and running with GhostKit in under 10 minutes. For a more comprehensive setup, refer to the [Installation Guide](../installation.md).

## 60-Second Setup

```bash
# Clone and install in one command
git clone https://github.com/K11E3R/GhostKit.git && cd GhostKit && \
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && \
python ghostkit.py --check
```

## First Scan

Let's run a basic web scan against a test target:

```bash
# Quick XSS scan against a test site
python ghostkit.py -m web_xss_scanner -u http://testphp.vulnweb.com
```

You should see output similar to:

```
[+] GhostKit v3.1.4 initializing...
[+] Loading web_xss_scanner module
[+] Scanning http://testphp.vulnweb.com for XSS vulnerabilities
[+] Crawling site, discovered 23 unique URLs
[+] Testing input vectors on each page
[!] Potential XSS found in parameter 'searchFor' at http://testphp.vulnweb.com/search.php
[!] Potential XSS found in parameter 'artist' at http://testphp.vulnweb.com/artists.php
[+] Scan complete. Found 2 potential vulnerabilities.
[+] Results saved to reports/xss_scan_testphp.vulnweb.com_20250530.json
```

## Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--list-modules` | List all available modules | `python ghostkit.py --list-modules` |
| `-m MODULE` | Select a specific module to run | `python ghostkit.py -m network_scanner` |
| `-t TARGET` | Specify the target (host/network) | `python ghostkit.py -m network_scanner -t 192.168.1.0/24` |
| `-u URL` | Specify target URL for web modules | `python ghostkit.py -m web_sqli_scanner -u http://example.com` |
| `-o OUTPUT` | Output file for results | `python ghostkit.py -m nmap_wrapper -t 10.0.0.1 -o scan.json` |
| `--verbose` | Increase output verbosity | `python ghostkit.py -m dns_enum -t example.com --verbose` |

## Common Workflows

### 1. Network Reconnaissance

```bash
# Full network discovery and service enumeration
python ghostkit.py -m network_scanner -t 192.168.1.0/24 --service-detection

# OS fingerprinting on discovered hosts
python ghostkit.py -m os_fingerprint -f reports/network_scan_*.json
```

### 2. Web Application Testing

```bash
# Full web application assessment
python ghostkit.py -m web_scan_suite -u https://target-webapp.com --full-scan

# Targeted SQLi check
python ghostkit.py -m web_sqli_scanner -u https://target-webapp.com/search.php?id=1
```

### 3. Wireless Attacks

```bash
# WiFi network discovery
sudo python ghostkit.py -m wifi_scanner --interface wlan0mon

# Bluetooth device enumeration
python ghostkit.py -m bluetooth_scanner
```

### 4. Post-Exploitation

```bash
# Generate a reverse shell payload
python ghostkit.py -m payload_gen --type reverse_shell --lhost 192.168.1.5 --lport 4444 --format python

# Start a listener
python ghostkit.py -m multi_handler --port 4444
```

## Module Categories

GhostKit is organized into several module categories:

| Category | Description | Example Modules |
|----------|-------------|----------------|
| Reconnaissance | Information gathering | `network_scanner`, `subdomain_enum`, `port_scanner` |
| Web | Web application testing | `web_xss_scanner`, `web_sqli_scanner`, `web_dir_fuzzer` |
| Exploitation | Vulnerability exploitation | `exploit_engine`, `web_shell_upload`, `brute_force` |
| Post-Exploitation | Actions after access | `privilege_escalation`, `credential_harvest`, `lateral_movement` |
| Wireless | Wireless network testing | `wifi_scanner`, `bluetooth_attacks`, `rf_analyzer` |
| Hardware | Physical device testing | `hardware_interface`, `serial_sniffer`, `usb_analyzer` |

## Quick Tips

1. Use `--help` with any module for specific options:
   ```bash
   python ghostkit.py -m web_xss_scanner --help
   ```

2. Enable debug mode for detailed output:
   ```bash
   python ghostkit.py -m network_scanner -t 192.168.1.0/24 --debug
   ```

3. Save all results to JSON format for later analysis:
   ```bash
   python ghostkit.py -m subdomain_enum -t example.com --json
   ```

4. Chain modules together for complex workflows:
   ```bash
   python ghostkit.py --chain "network_scanner>port_scanner>service_enum" -t 10.0.0.0/24
   ```

5. Use templates for repeated tasks:
   ```bash
   python ghostkit.py --template web-full-audit -u https://target.com
   ```

## Visualization and Reporting

Generate a quick visual report of your findings:

```bash
# Generate an HTML report from scan results
python ghostkit.py --report-from reports/network_scan_*.json --format html

# Generate a PDF report with executive summary
python ghostkit.py --report-from reports/web_scan_*.json --format pdf --executive
```

## Next Steps

Now that you're up and running with GhostKit, you might want to:

- Explore [Core Concepts](../core-concepts/architecture.md) to understand the framework architecture
- Learn about [Advanced Usage](../advanced/threat-intelligence.md) for scripting and automation
- Check out [Tradecraft](../tradecraft/opsec.md) for operational security considerations
- Read [Module Documentation](overview.md) for detailed usage of each module

---

*Last updated: May 30, 2025*
