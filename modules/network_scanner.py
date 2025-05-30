#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Network Scanner Module for GhostKit
Provides comprehensive network reconnaissance capabilities
"""

import argparse
import socket
import ipaddress
import time
import random
import threading
import queue
from typing import List, Dict, Any, Optional, Tuple
import logging

try:
    import scapy.all as scapy
    import nmap
except ImportError:
    logging.error(
        "Required dependencies not found. Install with: pip install scapy python-nmap"
    )

from modules.base_module import BaseModule


class Module(BaseModule):
    """Network Scanner Module for GhostKit"""

    def __init__(self):
        super().__init__()
        self.description = "Advanced network reconnaissance and port scanning"
        self.args_parser = self._create_arg_parser()
        self.results = {}
        self.scan_queue = queue.Queue()
        self.result_lock = threading.Lock()
        self.stop_scan = False

    def _create_arg_parser(self) -> argparse.ArgumentParser:
        """Create argument parser for the network scanner module"""
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument(
            "-t",
            "--target",
            required=True,
            help="Target IP address, range (CIDR notation), or hostname",
        )
        parser.add_argument(
            "-p",
            "--ports",
            default="1-1000",
            help="Port range to scan (e.g., '1-1000' or '22,80,443')",
        )
        parser.add_argument(
            "-s",
            "--scan-type",
            choices=["tcp", "syn", "udp", "arp", "ping"],
            default="tcp",
            help="Scan type: tcp (full connect), syn (half-open), udp, arp, or ping",
        )
        parser.add_argument(
            "--threads", type=int, default=10, help="Number of threads for scanning"
        )
        parser.add_argument(
            "--timeout",
            type=float,
            default=1.0,
            help="Timeout for connections in seconds",
        )
        parser.add_argument(
            "--delay", type=float, default=0.0, help="Delay between probes in seconds"
        )
        parser.add_argument(
            "--service-detection",
            action="store_true",
            help="Attempt to detect services on open ports",
        )
        parser.add_argument(
            "--os-detection", action="store_true", help="Attempt OS detection"
        )
        parser.add_argument(
            "--dns-lookup",
            action="store_true",
            help="Perform DNS lookups on discovered hosts",
        )
        parser.add_argument(
            "--stealth",
            action="store_true",
            help="Use stealth techniques (randomize ports, delays)",
        )
        parser.add_argument(
            "--output", help="Output file for scan results (JSON format)"
        )
        return parser

    def run(self, args: List[str]) -> Dict[str, Any]:
        """Run the network scanner with the given arguments"""
        parsed_args = self.args_parser.parse_args(args)

        self.logger.info(f"Starting network scan on target: {parsed_args.target}")

        # Parse target(s)
        targets = self._parse_targets(parsed_args.target)
        if not targets:
            self.logger.error("No valid targets specified")
            return {"status": "error", "message": "No valid targets specified"}

        # Parse ports
        ports = self._parse_ports(parsed_args.ports)
        if not ports:
            self.logger.error("No valid ports specified")
            return {"status": "error", "message": "No valid ports specified"}

        self.logger.info(f"Scanning {len(targets)} hosts across {len(ports)} ports")

        # Initialize results
        self.results = {
            "scan_info": {
                "start_time": time.time(),
                "scan_type": parsed_args.scan_type,
                "targets": parsed_args.target,
                "ports": parsed_args.ports,
            },
            "hosts": {},
        }

        # Choose scan method based on scan type
        if parsed_args.scan_type == "arp":
            self._arp_scan(targets)
        elif parsed_args.scan_type == "ping":
            self._ping_scan(targets)
        else:
            # For TCP, SYN, UDP scans
            self._port_scan(targets, ports, parsed_args)

        # Additional enumeration if requested
        if parsed_args.service_detection:
            self._service_detection(targets, ports)

        if parsed_args.os_detection:
            self._os_detection(targets)

        if parsed_args.dns_lookup:
            self._dns_lookup(targets)

        # Finalize results
        self.results["scan_info"]["end_time"] = time.time()
        self.results["scan_info"]["duration"] = (
            self.results["scan_info"]["end_time"]
            - self.results["scan_info"]["start_time"]
        )

        # Print summary
        self._print_summary()

        # Save results if output file specified
        if parsed_args.output:
            self._save_results(parsed_args.output)

        return self.results

    def _parse_targets(self, target_spec: str) -> List[str]:
        """Parse target specification into list of IP addresses"""
        targets = []

        # Check if it's a CIDR range
        try:
            network = ipaddress.ip_network(target_spec, strict=False)
            targets = [str(ip) for ip in network.hosts()]
            return targets
        except ValueError:
            pass

        # Check if it's a hostname
        try:
            ip = socket.gethostbyname(target_spec)
            targets.append(ip)
            return targets
        except socket.gaierror:
            pass

        # Check if it's a comma-separated list
        if "," in target_spec:
            for t in target_spec.split(","):
                t = t.strip()
                try:
                    ip = socket.gethostbyname(t)
                    targets.append(ip)
                except socket.gaierror:
                    self.logger.warning(f"Could not resolve hostname: {t}")

        return targets

    def _parse_ports(self, port_spec: str) -> List[int]:
        """Parse port specification into list of port numbers"""
        ports = []

        # Check if it's a range (e.g., "1-1000")
        if "-" in port_spec:
            start, end = port_spec.split("-")
            try:
                start_port = int(start.strip())
                end_port = int(end.strip())
                return list(range(start_port, end_port + 1))
            except ValueError:
                self.logger.error(f"Invalid port range: {port_spec}")
                return []

        # Check if it's a comma-separated list
        if "," in port_spec:
            for p in port_spec.split(","):
                try:
                    port = int(p.strip())
                    ports.append(port)
                except ValueError:
                    self.logger.warning(f"Invalid port: {p}")
        else:
            # Single port
            try:
                port = int(port_spec.strip())
                ports.append(port)
            except ValueError:
                self.logger.error(f"Invalid port: {port_spec}")

        return ports

    def _arp_scan(self, targets: List[str]) -> None:
        """Perform ARP scan to discover hosts on local network"""
        self.logger.info("Starting ARP scan...")

        try:
            for target in targets:
                # Create ARP request
                arp_request = scapy.ARP(pdst=target)
                broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
                arp_request_broadcast = broadcast / arp_request

                # Send packet and get response
                answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=0)[
                    0
                ]

                # Process responses
                for element in answered_list:
                    ip = element[1].psrc
                    mac = element[1].hwsrc

                    with self.result_lock:
                        if ip not in self.results["hosts"]:
                            self.results["hosts"][ip] = {
                                "status": "up",
                                "mac_address": mac,
                                "ports": {},
                            }

                    self.logger.info(f"Host discovered: {ip} ({mac})")
        except Exception as e:
            self.logger.error(f"Error during ARP scan: {str(e)}")

    def _ping_scan(self, targets: List[str]) -> None:
        """Perform ICMP ping scan to discover hosts"""
        self.logger.info("Starting ping scan...")

        try:
            for target in targets:
                # Create ICMP packet
                ping_request = scapy.IP(dst=target) / scapy.ICMP()

                # Send packet and get response
                response = scapy.sr1(ping_request, timeout=1, verbose=0)

                if response:
                    with self.result_lock:
                        if target not in self.results["hosts"]:
                            self.results["hosts"][target] = {
                                "status": "up",
                                "ports": {},
                            }

                    self.logger.info(f"Host is up: {target}")
        except Exception as e:
            self.logger.error(f"Error during ping scan: {str(e)}")

    def _port_scan(self, targets: List[str], ports: List[int], args) -> None:
        """Perform port scan on specified targets and ports"""
        self.logger.info(f"Starting {args.scan_type} scan on {len(targets)} hosts...")

        # Create worker threads
        threads = []
        for i in range(args.threads):
            t = threading.Thread(target=self._scan_worker, args=(args,))
            t.daemon = True
            t.start()
            threads.append(t)

        # Queue scan tasks
        for target in targets:
            # Add host to results
            with self.result_lock:
                if target not in self.results["hosts"]:
                    self.results["hosts"][target] = {"status": "unknown", "ports": {}}

            # Randomize ports if stealth mode is enabled
            scan_ports = ports.copy()
            if args.stealth:
                random.shuffle(scan_ports)

            for port in scan_ports:
                self.scan_queue.put((target, port))

                # Add delay if specified
                if args.delay > 0:
                    time.sleep(args.delay)

        # Wait for queue to be processed
        self.scan_queue.join()

        # Stop worker threads
        self.stop_scan = True
        for t in threads:
            t.join()

    def _scan_worker(self, args) -> None:
        """Worker thread for port scanning"""
        while not self.stop_scan:
            try:
                target, port = self.scan_queue.get(timeout=1)
            except queue.Empty:
                continue

            try:
                # Choose scan method based on scan type
                if args.scan_type == "tcp":
                    result = self._tcp_connect_scan(target, port, args.timeout)
                elif args.scan_type == "syn":
                    result = self._syn_scan(target, port, args.timeout)
                elif args.scan_type == "udp":
                    result = self._udp_scan(target, port, args.timeout)
                else:
                    result = False

                # Update results
                if result:
                    with self.result_lock:
                        self.results["hosts"][target]["status"] = "up"
                        self.results["hosts"][target]["ports"][port] = {
                            "state": "open",
                            "service": self._get_service_name(port),
                        }

                    self.logger.info(f"Port {port} is open on {target}")

                    # Try banner grabbing
                    banner = self._grab_banner(target, port)
                    if banner:
                        with self.result_lock:
                            self.results["hosts"][target]["ports"][port][
                                "banner"
                            ] = banner

            except Exception as e:
                self.logger.debug(f"Error scanning {target}:{port} - {str(e)}")
            finally:
                self.scan_queue.task_done()

    def _tcp_connect_scan(self, target: str, port: int, timeout: float) -> bool:
        """Perform TCP connect scan on a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            return result == 0
        except:
            return False

    def _syn_scan(self, target: str, port: int, timeout: float) -> bool:
        """Perform TCP SYN scan on a single port"""
        try:
            # Create SYN packet
            syn_packet = scapy.IP(dst=target) / scapy.TCP(dport=port, flags="S")

            # Send packet and get response
            response = scapy.sr1(syn_packet, timeout=timeout, verbose=0)

            if response and response.haslayer(scapy.TCP):
                # Check if SYN-ACK received (port open)
                if response[scapy.TCP].flags == 0x12:  # SYN-ACK
                    # Send RST to close connection
                    rst_packet = scapy.IP(dst=target) / scapy.TCP(dport=port, flags="R")
                    scapy.send(rst_packet, verbose=0)
                    return True

            return False
        except:
            return False

    def _udp_scan(self, target: str, port: int, timeout: float) -> bool:
        """Perform UDP scan on a single port"""
        try:
            # Create UDP packet
            udp_packet = scapy.IP(dst=target) / scapy.UDP(dport=port)

            # Send packet and get response
            response = scapy.sr1(udp_packet, timeout=timeout, verbose=0)

            # If no response, port might be open
            if response is None:
                return True

            # If ICMP "port unreachable" received, port is closed
            if response.haslayer(scapy.ICMP):
                if response[scapy.ICMP].type == 3 and response[scapy.ICMP].code == 3:
                    return False

            return True
        except:
            return False

    def _grab_banner(self, target: str, port: int) -> Optional[str]:
        """Attempt to grab service banner from an open port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target, port))

            # Send a generic request
            sock.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")

            # Receive response
            banner = sock.recv(1024)
            sock.close()

            return banner.decode("utf-8", errors="ignore").strip()
        except:
            return None

    def _service_detection(self, targets: List[str], ports: List[int]) -> None:
        """Perform service detection on open ports using nmap"""
        self.logger.info("Starting service detection...")

        try:
            nm = nmap.PortScanner()

            for target in targets:
                # Check if host has any open ports
                if target in self.results["hosts"]:
                    if self.results["hosts"][target]["ports"]:
                        # Get list of open ports
                        open_ports = list(self.results["hosts"][target]["ports"].keys())
                        port_str = ",".join(map(str, open_ports))

                        # Run nmap service detection
                        nm.scan(target, port_str, arguments="-sV")

                        # Update results with service info
                        for port in open_ports:
                            if target in nm.all_hosts():
                                if "tcp" in nm[target] and port in nm[target]["tcp"]:
                                    service_info = nm[target]["tcp"][port]

                                    with self.result_lock:
                                        self.results["hosts"][target]["ports"][port][
                                            "service"
                                        ] = service_info["name"]
                                        self.results["hosts"][target]["ports"][port][
                                            "product"
                                        ] = service_info["product"]
                                        self.results["hosts"][target]["ports"][port][
                                            "version"
                                        ] = service_info["version"]
        except Exception as e:
            self.logger.error(f"Error during service detection: {str(e)}")

    def _os_detection(self, targets: List[str]) -> None:
        """Perform OS detection on hosts"""
        self.logger.info("Starting OS detection...")

        try:
            nm = nmap.PortScanner()

            for target in targets:
                # Check if host is up
                if (
                    target in self.results["hosts"]
                    and self.results["hosts"][target]["status"] == "up"
                ):
                    # Run nmap OS detection
                    nm.scan(target, arguments="-O")

                    # Update results with OS info
                    if target in nm.all_hosts():
                        if "osmatch" in nm[target]:
                            os_matches = nm[target]["osmatch"]
                            if os_matches:
                                with self.result_lock:
                                    self.results["hosts"][target]["os"] = {
                                        "name": os_matches[0]["name"],
                                        "accuracy": os_matches[0]["accuracy"],
                                        "type": nm[target]
                                        .get("osclass", [{}])[0]
                                        .get("type", "unknown"),
                                    }
        except Exception as e:
            self.logger.error(f"Error during OS detection: {str(e)}")

    def _dns_lookup(self, targets: List[str]) -> None:
        """Perform DNS lookups on hosts"""
        self.logger.info("Starting DNS lookups...")

        for target in targets:
            try:
                hostname = socket.gethostbyaddr(target)[0]

                with self.result_lock:
                    if target in self.results["hosts"]:
                        self.results["hosts"][target]["hostname"] = hostname

                self.logger.info(f"DNS lookup for {target}: {hostname}")
            except socket.herror:
                self.logger.debug(f"No hostname found for {target}")
            except Exception as e:
                self.logger.error(f"Error during DNS lookup for {target}: {str(e)}")

    def _get_service_name(self, port: int) -> str:
        """Get service name for a well-known port"""
        try:
            return socket.getservbyport(port)
        except:
            return "unknown"

    def _print_summary(self) -> None:
        """Print summary of scan results"""
        print("\n" + "=" * 60)
        print(f"SCAN SUMMARY")
        print("=" * 60)

        # Count hosts and open ports
        total_hosts = len(self.results["hosts"])
        up_hosts = sum(
            1 for host in self.results["hosts"].values() if host["status"] == "up"
        )
        total_open_ports = sum(
            len(host["ports"]) for host in self.results["hosts"].values()
        )

        print(
            f"Scanned {total_hosts} hosts, {up_hosts} hosts up, {total_open_ports} open ports found"
        )
        print(f"Scan duration: {self.results['scan_info']['duration']:.2f} seconds")

        # Print hosts with open ports
        for ip, host_info in self.results["hosts"].items():
            if host_info["status"] == "up" and host_info["ports"]:
                hostname = host_info.get("hostname", "")
                hostname_str = f" ({hostname})" if hostname else ""

                print(f"\nHost: {ip}{hostname_str}")

                # Print OS info if available
                if "os" in host_info:
                    print(
                        f"OS: {host_info['os']['name']} ({host_info['os']['accuracy']}%)"
                    )

                # Print open ports
                print("Open ports:")
                for port, port_info in sorted(host_info["ports"].items()):
                    service = port_info.get("service", "unknown")
                    product = port_info.get("product", "")
                    version = port_info.get("version", "")

                    service_str = service
                    if product:
                        service_str += f" - {product}"
                        if version:
                            service_str += f" {version}"

                    print(f"  {port}/tcp\t{service_str}")

                    # Print banner if available
                    if "banner" in port_info:
                        banner_lines = port_info["banner"].split("\n")
                        if len(banner_lines) > 2:
                            # Truncate long banners
                            banner_display = "\n    ".join(banner_lines[:2]) + "..."
                        else:
                            banner_display = "\n    ".join(banner_lines)

                        print(f"    Banner: {banner_display}")

        print("\n" + "=" * 60)

    def _save_results(self, output_file: str) -> None:
        """Save scan results to a file"""
        import json

        try:
            with open(output_file, "w") as f:
                json.dump(self.results, f, indent=4)

            self.logger.info(f"Results saved to {output_file}")
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
