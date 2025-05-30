#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hardware Interface Module for GhostKit
Provides tools for embedded device analysis, serial communication, and hardware hacking
"""

import argparse
import json
import logging
import os
import platform
import re
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# Try to import optional dependencies
try:
    import pyserial as serial
except ImportError:
    serial = None

try:
    import usb
except ImportError:
    usb = None

try:
    import gpiozero
except ImportError:
    gpiozero = None

try:
    from scapy.all import *
except ImportError:
    pass

from modules.base_module import BaseModule


class SerialInterface:
    """Class for interacting with devices via serial/UART"""

    def __init__(self, port: str, baudrate: int = 115200, timeout: int = 1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def connect(self) -> bool:
        """Connect to the serial device"""
        if not serial:
            logging.error(
                "pyserial module not available. Please install it with 'pip install pyserial'"
            )
            return False

        try:
            self.ser = serial.Serial(
                port=self.port, baudrate=self.baudrate, timeout=self.timeout
            )
            return True
        except Exception as e:
            logging.error(f"Error connecting to serial port {self.port}: {str(e)}")
            return False

    def disconnect(self) -> None:
        """Disconnect from the serial device"""
        if self.ser and self.ser.is_open:
            self.ser.close()

    def send(self, data: str) -> bool:
        """Send data to the serial device"""
        if not self.ser or not self.ser.is_open:
            return False

        try:
            self.ser.write(data.encode("utf-8") + b"\r\n")
            return True
        except Exception as e:
            logging.error(f"Error sending data to serial port: {str(e)}")
            return False

    def receive(self, timeout: int = None) -> str:
        """Receive data from the serial device"""
        if not self.ser or not self.ser.is_open:
            return ""

        if timeout:
            old_timeout = self.ser.timeout
            self.ser.timeout = timeout

        try:
            data = self.ser.readline().decode("utf-8", errors="ignore")
            return data
        except Exception as e:
            logging.error(f"Error receiving data from serial port: {str(e)}")
            return ""
        finally:
            if timeout:
                self.ser.timeout = old_timeout

    def interact(self) -> None:
        """Interactive serial console"""
        if not self.ser or not self.ser.is_open:
            print("Serial port not connected")
            return

        print(f"Connected to {self.port} at {self.baudrate} baud")
        print("Press Ctrl+C to exit")

        try:
            while True:
                # Check for incoming data
                if self.ser.in_waiting:
                    data = self.ser.readline().decode("utf-8", errors="ignore")
                    print(data, end="")

                # Check for user input
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = sys.stdin.readline()
                    self.ser.write(line.encode("utf-8"))
        except KeyboardInterrupt:
            print("\nExiting interactive console")

    def sniff_for_credentials(self, duration: int = 60) -> List[Dict[str, str]]:
        """Analyze serial traffic to look for credentials"""
        if not self.ser or not self.ser.is_open:
            return []

        found_credentials = []
        start_time = time.time()

        # Common credential patterns
        patterns = [
            r"(?i)user\s*[:=]\s*([^\s]+)",
            r"(?i)username\s*[:=]\s*([^\s]+)",
            r"(?i)pass\s*[:=]\s*([^\s]+)",
            r"(?i)password\s*[:=]\s*([^\s]+)",
            r"(?i)login\s*[:=]\s*([^\s]+)",
            r"(?i)key\s*[:=]\s*([^\s]+)",
            r"(?i)cred\s*[:=]\s*([^\s]+)",
            r"(?i)auth\s*[:=]\s*([^\s]+)",
        ]

        print(f"Sniffing for credentials for {duration} seconds...")

        try:
            while time.time() - start_time < duration:
                if self.ser.in_waiting:
                    data = self.ser.readline().decode("utf-8", errors="ignore")

                    for pattern in patterns:
                        match = re.search(pattern, data)
                        if match:
                            credential = {
                                "type": pattern.split("\\s")[0].replace("(?i)", ""),
                                "value": match.group(1),
                                "raw_data": data.strip(),
                            }

                            if credential not in found_credentials:
                                found_credentials.append(credential)
                                print(
                                    f"Potential credential found: {credential['type']} = {credential['value']}"
                                )
        except KeyboardInterrupt:
            print("\nSniffing interrupted")

        return found_credentials


class USBInterface:
    """Class for interacting with USB devices"""

    def __init__(self):
        self.devices = []

    def list_devices(self) -> List[Dict[str, Any]]:
        """List all connected USB devices"""
        if not usb:
            logging.error(
                "PyUSB module not available. Please install it with 'pip install pyusb'"
            )
            return []

        devices = []
        try:
            for device in usb.core.find(find_all=True):
                dev_info = {
                    "idVendor": device.idVendor,
                    "idProduct": device.idProduct,
                    "manufacturer": self._get_string(device, device.iManufacturer),
                    "product": self._get_string(device, device.iProduct),
                    "serial_number": self._get_string(device, device.iSerialNumber),
                }
                devices.append(dev_info)
        except Exception as e:
            logging.error(f"Error listing USB devices: {str(e)}")

        self.devices = devices
        return devices

    def _get_string(self, device, index) -> str:
        """Helper to get USB string descriptor"""
        try:
            if index and device.is_kernel_driver_active(0):
                device.detach_kernel_driver(0)
            return usb.util.get_string(device, index)
        except:
            return "Unknown"

    def find_device(self, vendor_id: int, product_id: int) -> Optional[Dict[str, Any]]:
        """Find a specific USB device by vendor and product ID"""
        if not usb:
            return None

        try:
            device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
            if device is None:
                return None

            return {
                "idVendor": device.idVendor,
                "idProduct": device.idProduct,
                "manufacturer": self._get_string(device, device.iManufacturer),
                "product": self._get_string(device, device.iProduct),
                "serial_number": self._get_string(device, device.iSerialNumber),
                "device": device,
            }
        except Exception as e:
            logging.error(f"Error finding USB device: {str(e)}")
            return None


class JTAGInterface:
    """Class for interacting with JTAG interfaces for hardware debugging"""

    def __init__(self, interface_type: str = "ftdi", port: str = None):
        self.interface_type = interface_type
        self.port = port
        self.connected = False

    def detect_pins(self) -> Dict[str, Any]:
        """Detect JTAG pins on a target device (simulation)"""
        # In a real implementation, this would use GPIO pins to detect JTAG
        print("Scanning for JTAG pins...")

        # Simulate pin detection
        return {
            "status": "success",
            "pins": {
                "TCK": "GPIO17",
                "TMS": "GPIO18",
                "TDI": "GPIO27",
                "TDO": "GPIO22",
                "TRST": "GPIO23",
            },
            "message": "JTAG pins detected. Use these pin mappings with OpenOCD or other JTAG tools.",
        }

    def connect(self) -> bool:
        """Connect to JTAG interface"""
        # This would typically use OpenOCD, urJTAG, or similar
        # For demonstration purposes only
        print(f"Connecting to JTAG interface ({self.interface_type})...")

        # Simulate connection
        time.sleep(1)
        self.connected = True
        return True

    def read_idcode(self) -> Dict[str, Any]:
        """Read JTAG IDCODE from target device"""
        if not self.connected:
            return {"status": "error", "message": "Not connected to JTAG interface"}

        # Simulate reading IDCODE
        return {
            "status": "success",
            "idcode": "0x4BA00477",
            "manufacturer": "ARM",
            "part": "Cortex-M4",
            "version": "1",
        }

    def dump_memory(self, address: int, size: int) -> Dict[str, Any]:
        """Dump memory from target device via JTAG"""
        if not self.connected:
            return {"status": "error", "message": "Not connected to JTAG interface"}

        # Simulate memory dump
        print(f"Dumping {size} bytes from address 0x{address:08X}...")

        # Generate some fake memory data
        memory_data = bytes([random.randint(0, 255) for _ in range(min(size, 1024))])

        return {
            "status": "success",
            "address": f"0x{address:08X}",
            "size": len(memory_data),
            "data": memory_data.hex(),
        }


class I2CInterface:
    """Class for interacting with I2C devices"""

    def __init__(self, bus: int = 1):
        self.bus = bus
        self.device = None

    def scan(self) -> List[int]:
        """Scan for I2C devices on the bus"""
        # This would typically use smbus or similar
        # For demonstration purposes only

        # Simulate I2C scan
        print(f"Scanning I2C bus {self.bus}...")

        # Generate some fake device addresses
        return [0x20, 0x27, 0x50, 0x68]

    def read(self, address: int, register: int, length: int = 1) -> Dict[str, Any]:
        """Read from I2C device"""
        # Simulate I2C read
        print(
            f"Reading {length} bytes from device 0x{address:02X}, register 0x{register:02X}..."
        )

        # Generate some fake data
        data = bytes([random.randint(0, 255) for _ in range(length)])

        return {
            "status": "success",
            "address": f"0x{address:02X}",
            "register": f"0x{register:02X}",
            "length": length,
            "data": data.hex(),
        }

    def write(self, address: int, register: int, data: bytes) -> Dict[str, Any]:
        """Write to I2C device"""
        # Simulate I2C write
        print(
            f"Writing {len(data)} bytes to device 0x{address:02X}, register 0x{register:02X}..."
        )

        return {
            "status": "success",
            "address": f"0x{address:02X}",
            "register": f"0x{register:02X}",
            "length": len(data),
        }


class SPIInterface:
    """Class for interacting with SPI devices"""

    def __init__(self, bus: int = 0, device: int = 0):
        self.bus = bus
        self.device = device

    def transfer(self, data: bytes) -> Dict[str, Any]:
        """Perform SPI transfer"""
        # Simulate SPI transfer
        print(f"Performing SPI transfer, {len(data)} bytes...")

        # Generate response data
        response = bytes([random.randint(0, 255) for _ in range(len(data))])

        return {
            "status": "success",
            "bus": self.bus,
            "device": self.device,
            "sent": data.hex(),
            "received": response.hex(),
        }

    def flash_dump(self, size: int = 1024) -> Dict[str, Any]:
        """Dump data from SPI flash"""
        # Simulate SPI flash dump
        print(f"Dumping {size} bytes from SPI flash...")

        # Generate fake flash data
        flash_data = bytes([random.randint(0, 255) for _ in range(min(size, 1024))])

        return {"status": "success", "size": len(flash_data), "data": flash_data.hex()}


class FirmwareAnalyzer:
    """Class for analyzing device firmware"""

    def __init__(self):
        pass

    def extract(self, firmware_path: str, output_dir: str) -> Dict[str, Any]:
        """Extract firmware contents"""
        if not os.path.exists(firmware_path):
            return {
                "status": "error",
                "message": f"Firmware file not found: {firmware_path}",
            }

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Try to identify firmware type
        firmware_type = self.identify(firmware_path)

        # Simulate extraction
        print(f"Extracting firmware {firmware_path} to {output_dir}...")

        # In a real implementation, this would use binwalk, firmware-mod-kit, etc.
        files = ["kernel.bin", "rootfs.bin", "bootloader.bin", "config.bin"]

        for file in files:
            # Simulate extracted file
            with open(os.path.join(output_dir, file), "wb") as f:
                f.write(os.urandom(1024))

        return {
            "status": "success",
            "firmware_type": firmware_type,
            "extracted_files": files,
        }

    def identify(self, firmware_path: str) -> str:
        """Identify firmware type"""
        # In a real implementation, this would examine file headers, strings, etc.
        # For demonstration purposes only

        # Simple file extension check
        ext = os.path.splitext(firmware_path)[1].lower()

        if ext == ".bin":
            return "raw_binary"
        elif ext == ".img":
            return "disk_image"
        elif ext == ".fw":
            return "firmware_package"
        elif ext == ".rom":
            return "rom_image"
        else:
            return "unknown"

    def analyze_strings(self, firmware_path: str) -> Dict[str, Any]:
        """Extract and analyze strings from firmware"""
        if not os.path.exists(firmware_path):
            return {
                "status": "error",
                "message": f"Firmware file not found: {firmware_path}",
            }

        # Simulate string extraction
        print(f"Extracting strings from {firmware_path}...")

        # In a real implementation, this would use binutils' strings command
        strings = [
            "root:x:0:0:root:/root:/bin/bash",
            "admin:password123",
            "BOOTLOADER_VERSION=1.2.3",
            "DEBUG_MODE=TRUE",
            "192.168.1.1",
            "https://example.com/update",
            "SSH_KEY=abcdef1234567890",
        ]

        # Search for interesting patterns
        credentials = []
        ips = []
        urls = []

        for s in strings:
            # Check for credentials
            if ":" in s and len(s.split(":")) == 2:
                credentials.append(s)

            # Check for IPs
            if re.match(r"\d+\.\d+\.\d+\.\d+", s):
                ips.append(s)

            # Check for URLs
            if s.startswith("http://") or s.startswith("https://"):
                urls.append(s)

        return {
            "status": "success",
            "interesting_strings": {
                "credentials": credentials,
                "ips": ips,
                "urls": urls,
            },
        }


class Module(BaseModule):
    """GhostKit Hardware Interface Module"""

    def __init__(self):
        super().__init__(
            name="hardware_interface",
            description="Hardware interface module for embedded device analysis",
            author="GhostShellX",
            version="1.0",
        )

    def run(self, args: List[str] = None) -> Dict[str, Any]:
        """Run the hardware interface module"""
        parser = argparse.ArgumentParser(description=self.description)
        subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

        # Serial interface command
        serial_parser = subparsers.add_parser("serial", help="Serial interface tools")
        serial_parser.add_argument(
            "-p", "--port", required=True, help="Serial port (e.g., COM1, /dev/ttyUSB0)"
        )
        serial_parser.add_argument(
            "-b",
            "--baudrate",
            type=int,
            default=115200,
            help="Baud rate (default: 115200)",
        )
        serial_parser.add_argument(
            "-a",
            "--action",
            choices=["connect", "interact", "sniff"],
            default="interact",
            help="Action to perform",
        )
        serial_parser.add_argument(
            "-t",
            "--timeout",
            type=int,
            default=60,
            help="Timeout/duration for operations in seconds",
        )

        # USB interface command
        usb_parser = subparsers.add_parser("usb", help="USB interface tools")
        usb_parser.add_argument(
            "-a",
            "--action",
            choices=["list", "find"],
            default="list",
            help="Action to perform",
        )
        usb_parser.add_argument(
            "-v",
            "--vendor",
            type=lambda x: int(x, 0),
            help="Vendor ID (for find action)",
        )
        usb_parser.add_argument(
            "-p",
            "--product",
            type=lambda x: int(x, 0),
            help="Product ID (for find action)",
        )

        # JTAG interface command
        jtag_parser = subparsers.add_parser("jtag", help="JTAG interface tools")
        jtag_parser.add_argument(
            "-a",
            "--action",
            choices=["detect", "connect", "idcode", "dump"],
            default="detect",
            help="Action to perform",
        )
        jtag_parser.add_argument(
            "-i", "--interface", default="ftdi", help="JTAG interface type"
        )
        jtag_parser.add_argument(
            "--address", type=lambda x: int(x, 0), help="Memory address for dump action"
        )
        jtag_parser.add_argument(
            "--size", type=int, default=1024, help="Size in bytes for dump action"
        )

        # I2C interface command
        i2c_parser = subparsers.add_parser("i2c", help="I2C interface tools")
        i2c_parser.add_argument(
            "-a",
            "--action",
            choices=["scan", "read", "write"],
            default="scan",
            help="Action to perform",
        )
        i2c_parser.add_argument(
            "-b", "--bus", type=int, default=1, help="I2C bus number"
        )
        i2c_parser.add_argument(
            "--address", type=lambda x: int(x, 0), help="I2C device address"
        )
        i2c_parser.add_argument(
            "--register", type=lambda x: int(x, 0), help="I2C register address"
        )
        i2c_parser.add_argument(
            "--length", type=int, default=1, help="Number of bytes to read"
        )
        i2c_parser.add_argument("--data", help="Data to write (hex string)")

        # SPI interface command
        spi_parser = subparsers.add_parser("spi", help="SPI interface tools")
        spi_parser.add_argument(
            "-a",
            "--action",
            choices=["transfer", "flash_dump"],
            default="transfer",
            help="Action to perform",
        )
        spi_parser.add_argument(
            "-b", "--bus", type=int, default=0, help="SPI bus number"
        )
        spi_parser.add_argument(
            "-d", "--device", type=int, default=0, help="SPI device number"
        )
        spi_parser.add_argument("--data", help="Data to transfer (hex string)")
        spi_parser.add_argument(
            "--size", type=int, default=1024, help="Size in bytes for flash dump"
        )

        # Firmware analysis command
        firmware_parser = subparsers.add_parser(
            "firmware", help="Firmware analysis tools"
        )
        firmware_parser.add_argument(
            "-a",
            "--action",
            choices=["extract", "identify", "strings"],
            default="identify",
            help="Action to perform",
        )
        firmware_parser.add_argument(
            "-f", "--file", required=True, help="Path to firmware file"
        )
        firmware_parser.add_argument(
            "-o", "--output", help="Output directory for extract action"
        )

        if args:
            args = parser.parse_args(args)
        else:
            args = parser.parse_args()

        # Handle serial interface commands
        if args.command == "serial":
            serial_interface = SerialInterface(args.port, args.baudrate)

            if args.action == "connect":
                if serial_interface.connect():
                    return {
                        "status": "success",
                        "message": f"Connected to {args.port} at {args.baudrate} baud",
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Failed to connect to {args.port}",
                    }

            elif args.action == "interact":
                if serial_interface.connect():
                    serial_interface.interact()
                    return {
                        "status": "success",
                        "message": "Interactive session completed",
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Failed to connect to {args.port}",
                    }

            elif args.action == "sniff":
                if serial_interface.connect():
                    credentials = serial_interface.sniff_for_credentials(args.timeout)
                    return {"status": "success", "credentials": credentials}
                else:
                    return {
                        "status": "error",
                        "message": f"Failed to connect to {args.port}",
                    }

        # Handle USB interface commands
        elif args.command == "usb":
            usb_interface = USBInterface()

            if args.action == "list":
                devices = usb_interface.list_devices()
                return {"status": "success", "devices": devices}

            elif args.action == "find":
                if not args.vendor or not args.product:
                    return {
                        "status": "error",
                        "message": "Vendor and product IDs are required for find action",
                    }

                device = usb_interface.find_device(args.vendor, args.product)
                if device:
                    return {"status": "success", "device": device}
                else:
                    return {"status": "error", "message": "Device not found"}

        # Handle JTAG interface commands
        elif args.command == "jtag":
            jtag_interface = JTAGInterface(args.interface)

            if args.action == "detect":
                return jtag_interface.detect_pins()

            elif args.action == "connect":
                if jtag_interface.connect():
                    return {
                        "status": "success",
                        "message": "Connected to JTAG interface",
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Failed to connect to JTAG interface",
                    }

            elif args.action == "idcode":
                if jtag_interface.connect():
                    return jtag_interface.read_idcode()
                else:
                    return {
                        "status": "error",
                        "message": "Failed to connect to JTAG interface",
                    }

            elif args.action == "dump":
                if not args.address:
                    return {
                        "status": "error",
                        "message": "Memory address is required for dump action",
                    }

                if jtag_interface.connect():
                    return jtag_interface.dump_memory(args.address, args.size)
                else:
                    return {
                        "status": "error",
                        "message": "Failed to connect to JTAG interface",
                    }

        # Handle I2C interface commands
        elif args.command == "i2c":
            i2c_interface = I2CInterface(args.bus)

            if args.action == "scan":
                devices = i2c_interface.scan()
                return {"status": "success", "devices": [f"0x{d:02X}" for d in devices]}

            elif args.action == "read":
                if not args.address or not args.register:
                    return {
                        "status": "error",
                        "message": "Device address and register are required for read action",
                    }

                return i2c_interface.read(args.address, args.register, args.length)

            elif args.action == "write":
                if not args.address or not args.register or not args.data:
                    return {
                        "status": "error",
                        "message": "Device address, register, and data are required for write action",
                    }

                try:
                    data = bytes.fromhex(args.data)
                except ValueError:
                    return {"status": "error", "message": "Invalid hex data format"}

                return i2c_interface.write(args.address, args.register, data)

        # Handle SPI interface commands
        elif args.command == "spi":
            spi_interface = SPIInterface(args.bus, args.device)

            if args.action == "transfer":
                if not args.data:
                    return {
                        "status": "error",
                        "message": "Data is required for transfer action",
                    }

                try:
                    data = bytes.fromhex(args.data)
                except ValueError:
                    return {"status": "error", "message": "Invalid hex data format"}

                return spi_interface.transfer(data)

            elif args.action == "flash_dump":
                return spi_interface.flash_dump(args.size)

        # Handle firmware analysis commands
        elif args.command == "firmware":
            firmware_analyzer = FirmwareAnalyzer()

            if args.action == "extract":
                if not args.output:
                    return {
                        "status": "error",
                        "message": "Output directory is required for extract action",
                    }

                return firmware_analyzer.extract(args.file, args.output)

            elif args.action == "identify":
                firmware_type = firmware_analyzer.identify(args.file)
                return {"status": "success", "firmware_type": firmware_type}

            elif args.action == "strings":
                return firmware_analyzer.analyze_strings(args.file)

        else:
            return {"status": "error", "message": "Unknown command"}


class Module(BaseModule):
    """GhostKit Hardware Interface Module"""

    def __init__(self):
        self.name = "hardware_interface"
        self.description = "Hardware interface tools for embedded device analysis"
        super().__init__()

    def _create_arg_parser(self) -> argparse.ArgumentParser:
        """Create an argument parser for the module"""
        parser = argparse.ArgumentParser(description=self.description)
        subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

        # Serial interface command
        serial_parser = subparsers.add_parser("serial", help="Serial interface tools")
        serial_parser.add_argument(
            "-p", "--port", required=True, help="Serial port (e.g., COM1, /dev/ttyUSB0)"
        )
        serial_parser.add_argument(
            "-b",
            "--baudrate",
            type=int,
            default=115200,
            help="Baud rate (default: 115200)",
        )
        serial_parser.add_argument(
            "-a",
            "--action",
            choices=["connect", "interact", "sniff"],
            default="interact",
            help="Action to perform",
        )
        serial_parser.add_argument(
            "-t",
            "--timeout",
            type=int,
            default=60,
            help="Timeout/duration for operations in seconds",
        )

        # USB interface command
        usb_parser = subparsers.add_parser("usb", help="USB interface tools")
        usb_parser.add_argument(
            "-a",
            "--action",
            choices=["list", "find"],
            default="list",
            help="Action to perform",
        )
        usb_parser.add_argument(
            "-v",
            "--vendor",
            type=lambda x: int(x, 0),
            help="Vendor ID (for find action)",
        )
        usb_parser.add_argument(
            "-p",
            "--product",
            type=lambda x: int(x, 0),
            help="Product ID (for find action)",
        )

        # JTAG interface command
        jtag_parser = subparsers.add_parser("jtag", help="JTAG interface tools")
        jtag_parser.add_argument(
            "-a",
            "--action",
            choices=["detect", "connect", "idcode", "dump"],
            default="detect",
            help="Action to perform",
        )
        jtag_parser.add_argument(
            "-i", "--interface", default="ftdi", help="JTAG interface type"
        )
        jtag_parser.add_argument(
            "--address", type=lambda x: int(x, 0), help="Memory address for dump action"
        )
        jtag_parser.add_argument(
            "--size", type=int, default=1024, help="Size in bytes for dump action"
        )

        return parser

    def run(self, args: List[str] = None) -> Dict[str, Any]:
        """Run the hardware interface module"""
        if args is None:
            args = []

        if args:
            args = self.args_parser.parse_args(args)
        else:
            args = self.args_parser.parse_args()

        # Handle serial interface commands
        if hasattr(args, "command") and args.command == "serial":
            serial_interface = SerialInterface(args.port, args.baudrate)

            if args.action == "connect":
                if serial_interface.connect():
                    return {
                        "status": "success",
                        "message": f"Connected to {args.port} at {args.baudrate} baud",
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Failed to connect to {args.port}",
                    }

            elif args.action == "interact":
                if serial_interface.connect():
                    serial_interface.interact()
                    return {
                        "status": "success",
                        "message": "Interactive session completed",
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Failed to connect to {args.port}",
                    }

            elif args.action == "sniff":
                if serial_interface.connect():
                    credentials = serial_interface.sniff_for_credentials(args.timeout)
                    return {"status": "success", "credentials": credentials}
                else:
                    return {
                        "status": "error",
                        "message": f"Failed to connect to {args.port}",
                    }

        return {"status": "error", "message": "Invalid or missing command"}


if __name__ == "__main__":
    module = Module()
    result = module.run()
    print(json.dumps(result, indent=2))
