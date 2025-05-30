#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web Security Core Module for GhostKit
Provides the foundation for web application security testing
"""

import argparse
import logging
import json
import os
import sys
import time
import random
import string
import threading
import urllib.parse
import re
from typing import List, Dict, Any, Optional, Tuple, Union, Set

# Try to import optional dependencies
try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

from modules.base_module import BaseModule


class WebTarget:
    """Represents a web target with methods for interaction"""

    def __init__(
        self,
        url: str,
        headers: Dict[str, str] = None,
        cookies: Dict[str, str] = None,
        proxy: str = None,
        timeout: int = 10,
        verify_ssl: bool = False,
    ):
        self.base_url = url
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GhostKit Web Security Scanner"
        }
        self.cookies = cookies or {}
        self.proxy = proxy
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session() if requests else None
        self.history = []

    def get(
        self, path: str = "", params: Dict[str, str] = None
    ) -> Optional[requests.Response]:
        """Send GET request to target"""
        if not self.session:
            return None

        url = urllib.parse.urljoin(self.base_url, path)
        try:
            response = self.session.get(
                url,
                params=params,
                headers=self.headers,
                cookies=self.cookies,
                proxies=(
                    {"http": self.proxy, "https": self.proxy} if self.proxy else None
                ),
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
            self._log_request("GET", url, params, None, response)
            return response
        except Exception as e:
            logging.error(f"Error in GET request to {url}: {str(e)}")
            return None

    def post(
        self, path: str = "", data: Any = None, json_data: Dict = None
    ) -> Optional[requests.Response]:
        """Send POST request to target"""
        if not self.session:
            return None

        url = urllib.parse.urljoin(self.base_url, path)
        try:
            response = self.session.post(
                url,
                data=data,
                json=json_data,
                headers=self.headers,
                cookies=self.cookies,
                proxies=(
                    {"http": self.proxy, "https": self.proxy} if self.proxy else None
                ),
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
            self._log_request("POST", url, None, data or json_data, response)
            return response
        except Exception as e:
            logging.error(f"Error in POST request to {url}: {str(e)}")
            return None

    def _log_request(
        self, method: str, url: str, params: Any, data: Any, response: requests.Response
    ) -> None:
        """Log request details"""
        request_data = {
            "timestamp": time.time(),
            "method": method,
            "url": url,
            "params": params,
            "data": data,
            "status_code": response.status_code if response else None,
            "response_size": len(response.content) if response else 0,
        }
        self.history.append(request_data)


class WebCrawler:
    """Web crawler for discovering site structure"""

    def __init__(self, target: WebTarget, max_depth: int = 3, max_pages: int = 100):
        self.target = target
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited_urls = set()
        self.queue = []
        self.pages = {}
        self.forms = {}
        self.parameters = set()

    def crawl(self, start_path: str = "") -> Dict[str, Any]:
        """Crawl the target site"""
        if not BeautifulSoup:
            return {"status": "error", "message": "BeautifulSoup module not available"}

        start_url = urllib.parse.urljoin(self.target.base_url, start_path)
        self.queue.append((start_url, 0))  # (url, depth)

        pages_visited = 0

        while self.queue and pages_visited < self.max_pages:
            url, depth = self.queue.pop(0)

            if url in self.visited_urls or depth > self.max_depth:
                continue

            logging.info(f"Crawling: {url} (depth: {depth})")
            print(f"Crawling: {url}")

            # Make request to the URL
            parsed_url = urllib.parse.urlparse(url)
            path = parsed_url.path
            params = dict(urllib.parse.parse_qsl(parsed_url.query))

            response = self.target.get(path, params)
            if not response or response.status_code != 200:
                continue

            self.visited_urls.add(url)
            pages_visited += 1

            # Parse response
            try:
                soup = BeautifulSoup(response.text, "html.parser")

                # Store page info
                self.pages[url] = {
                    "title": soup.title.text if soup.title else "",
                    "links": [],
                    "forms": [],
                    "depth": depth,
                }

                # Extract links
                for link in soup.find_all("a", href=True):
                    href = link["href"]
                    absolute_url = urllib.parse.urljoin(url, href)

                    # Only follow links to the same domain
                    if (
                        urllib.parse.urlparse(absolute_url).netloc
                        == urllib.parse.urlparse(url).netloc
                    ):
                        self.pages[url]["links"].append(absolute_url)
                        if absolute_url not in self.visited_urls:
                            self.queue.append((absolute_url, depth + 1))

                # Extract forms
                for i, form in enumerate(soup.find_all("form")):
                    form_data = {
                        "action": urllib.parse.urljoin(url, form.get("action", "")),
                        "method": form.get("method", "get").upper(),
                        "inputs": [],
                    }

                    # Process inputs
                    for input_field in form.find_all(["input", "textarea", "select"]):
                        input_type = input_field.get("type", "")
                        input_name = input_field.get("name", "")

                        if input_name:
                            form_data["inputs"].append(
                                {"name": input_name, "type": input_type}
                            )
                            self.parameters.add(input_name)

                    form_id = f"{url}#form{i}"
                    self.forms[form_id] = form_data
                    self.pages[url]["forms"].append(form_id)

                # Extract URL parameters
                if parsed_url.query:
                    for param_name, _ in urllib.parse.parse_qsl(parsed_url.query):
                        self.parameters.add(param_name)

            except Exception as e:
                logging.error(f"Error parsing {url}: {str(e)}")

        return {
            "status": "success",
            "pages_visited": pages_visited,
            "unique_urls": len(self.visited_urls),
            "forms_found": len(self.forms),
            "parameters_found": len(self.parameters),
        }

    def get_results(self) -> Dict[str, Any]:
        """Get crawling results"""
        return {
            "pages": self.pages,
            "forms": self.forms,
            "parameters": list(self.parameters),
        }


class WebScanner:
    """Base class for web vulnerability scanners"""

    def __init__(self, target: WebTarget):
        self.target = target
        self.findings = []

    def scan(self) -> List[Dict[str, Any]]:
        """Perform scan (to be implemented by subclasses)"""
        return []

    def add_finding(
        self,
        vulnerability_type: str,
        url: str,
        parameter: str = None,
        evidence: str = None,
        severity: str = "medium",
        confidence: str = "medium",
        description: str = None,
    ) -> None:
        """Add a vulnerability finding"""
        finding = {
            "type": vulnerability_type,
            "url": url,
            "parameter": parameter,
            "evidence": evidence,
            "severity": severity,
            "confidence": confidence,
            "description": description,
            "timestamp": time.time(),
        }
        self.findings.append(finding)


class Module(BaseModule):
    """Web Security Core Module for GhostKit"""

    def __init__(self):
        super().__init__()
        self.description = "Core web application security testing framework"
        self.args_parser = self._create_arg_parser()

        # Initialize results
        self.results = {}
        self.target = None
        self.crawler = None

    def _create_arg_parser(self) -> argparse.ArgumentParser:
        """Create argument parser for the web security module"""
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument("-u", "--url", required=True, help="Target URL")
        parser.add_argument(
            "-a",
            "--action",
            required=True,
            choices=[
                "crawl",
                "scan_all",
                "scan_xss",
                "scan_sqli",
                "scan_cmdi",
                "scan_auth",
                "scan_ssrf",
            ],
            help="Action to perform",
        )
        parser.add_argument(
            "-d", "--depth", type=int, default=3, help="Maximum crawl depth"
        )
        parser.add_argument(
            "-m", "--max-pages", type=int, default=100, help="Maximum pages to crawl"
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
            "-t", "--timeout", type=int, default=10, help="Request timeout in seconds"
        )
        parser.add_argument(
            "--no-verify-ssl", action="store_true", help="Disable SSL verification"
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
        """Run the web security module with the given arguments"""
        if not requests:
            self.logger.error(
                "Requests module not available. Install with: pip install requests"
            )
            return {"status": "error", "message": "Requests module not available"}

        parsed_args = self.args_parser.parse_args(args)

        # Initialize target
        cookies = self._parse_keyval_string(parsed_args.cookies)
        headers = self._parse_keyval_string(parsed_args.headers)

        self.target = WebTarget(
            url=parsed_args.url,
            headers=headers,
            cookies=cookies,
            proxy=parsed_args.proxy,
            timeout=parsed_args.timeout,
            verify_ssl=not parsed_args.no_verify_ssl,
        )

        # Initialize crawler
        self.crawler = WebCrawler(
            target=self.target,
            max_depth=parsed_args.depth,
            max_pages=parsed_args.max_pages,
        )

        # Perform action
        if parsed_args.action == "crawl":
            print(
                f"Starting crawler on {parsed_args.url} with depth {parsed_args.depth}"
            )
            result = self.crawler.crawl()

            if result["status"] == "success":
                print("\nCrawl Summary:")
                print(f"Pages visited: {result['pages_visited']}")
                print(f"Unique URLs: {result['unique_urls']}")
                print(f"Forms found: {result['forms_found']}")
                print(f"Parameters found: {result['parameters_found']}")

                # Save results
                crawler_results = self.crawler.get_results()
                self.results = {
                    "status": "success",
                    "target": parsed_args.url,
                    "crawl_stats": result,
                    "crawl_data": crawler_results,
                }
            else:
                self.results = result

        else:
            # If we're scanning, crawl first to discover attack surface
            print(
                f"Starting initial crawl on {parsed_args.url} to discover attack surface"
            )
            crawl_result = self.crawler.crawl()

            if crawl_result["status"] != "success":
                return crawl_result

            print("\nStarting vulnerability scan...")

            # For now, we just return crawl results
            # The actual vulnerability scanners will be implemented in separate modules
            self.results = {
                "status": "success",
                "message": "Scan completed. See specific scanner modules for results.",
                "target": parsed_args.url,
                "crawl_stats": crawl_result,
            }

        # Save results if requested
        if parsed_args.output:
            try:
                with open(parsed_args.output, "w") as f:
                    json.dump(self.results, f, indent=4)
                self.logger.info(f"Results saved to {parsed_args.output}")
            except Exception as e:
                self.logger.error(f"Error saving results: {str(e)}")

        return self.results


# If run directly, show help
if __name__ == "__main__":
    module = Module()
    print(module.get_help())
