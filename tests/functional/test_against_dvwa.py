#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functional tests for GhostKit against DVWA (Damn Vulnerable Web Application)
These tests require DVWA to be running locally or in a controlled environment.

IMPORTANT: This should only be run against applications you own or have explicit
permission to test against.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Test configuration - MODIFY THESE TO MATCH YOUR TEST ENVIRONMENT
DVWA_URL = "http://localhost:8080/dvwa"  # URL to your local DVWA instance
DVWA_USERNAME = "admin"  # Default DVWA username
DVWA_PASSWORD = "password"  # Default DVWA password


@pytest.mark.skipif(
    not os.environ.get("RUN_FUNCTIONAL_TESTS"),
    reason="Set RUN_FUNCTIONAL_TESTS=1 to run functional tests",
)
class TestDVWA:
    """
    Functional tests against DVWA

    These tests require:
    1. A running DVWA instance (Docker: docker run --rm -it -p 8080:80 vulnerables/web-dvwa)
    2. The RUN_FUNCTIONAL_TESTS environment variable to be set
    """

    @pytest.fixture(scope="class")
    def dvwa_session(self):
        """Verify DVWA is accessible and create a session"""
        import requests

        # Check if DVWA is running
        try:
            r = requests.get(DVWA_URL, timeout=5)
            if r.status_code != 200:
                pytest.skip(f"DVWA not available at {DVWA_URL}")
        except requests.exceptions.RequestException:
            pytest.skip(f"DVWA not available at {DVWA_URL}")

        # Create a session for further tests
        session = requests.Session()
        return session

    def test_xss_scanner(self, dvwa_session):
        """Test XSS scanner against DVWA's XSS vulnerable pages"""
        # Run GhostKit's XSS scanner against DVWA
        root_dir = Path(__file__).parent.parent.parent
        ghostkit_path = root_dir / "ghostkit.py"

        # Target the XSS reflected page in DVWA
        target_url = f"{DVWA_URL}/vulnerabilities/xss_r/"

        # Execute the command
        cmd = [
            "python",
            str(ghostkit_path),
            "-m",
            "web_xss_scanner",
            "-u",
            target_url,
            "--test-mode",  # If your tool has a test mode to prevent actual exploitation
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Check if the process ran successfully
        assert result.returncode == 0, f"Command failed with output: {result.stderr}"

        # Check if vulnerable XSS was detected in the output
        assert (
            "XSS" in result.stdout and "vulnerability" in result.stdout.lower()
        ), "XSS vulnerability should be detected in DVWA"

    def test_sqli_scanner(self, dvwa_session):
        """Test SQL Injection scanner against DVWA's SQLi vulnerable pages"""
        # Run GhostKit's SQLi scanner against DVWA
        root_dir = Path(__file__).parent.parent.parent
        ghostkit_path = root_dir / "ghostkit.py"

        # Target the SQL Injection page in DVWA
        target_url = f"{DVWA_URL}/vulnerabilities/sqli/"

        # Execute the command
        cmd = [
            "python",
            str(ghostkit_path),
            "-m",
            "web_injection_scanner",
            "-u",
            target_url,
            "--test-mode",  # If your tool has a test mode to prevent actual exploitation
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Check if the process ran successfully
        assert result.returncode == 0, f"Command failed with output: {result.stderr}"

        # Check if SQL injection was detected in the output
        assert (
            "SQL" in result.stdout and "injection" in result.stdout.lower()
        ), "SQL Injection vulnerability should be detected in DVWA"


# Stand-alone test runner
if __name__ == "__main__":
    # Simple check if DVWA is accessible
    import requests

    try:
        r = requests.get(DVWA_URL, timeout=5)
        if r.status_code == 200:
            print(f"✅ DVWA is accessible at {DVWA_URL}")
            print("Running tests...")
            # Set environment variable and run tests
            os.environ["RUN_FUNCTIONAL_TESTS"] = "1"
            pytest.main(["-xvs", __file__])
        else:
            print(f"❌ DVWA returned status code {r.status_code}")
            print(f"Please ensure DVWA is running at {DVWA_URL}")
            print(
                "You can start DVWA with Docker: docker run --rm -it -p 8080:80 vulnerables/web-dvwa"
            )
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to DVWA: {e}")
        print(f"Please ensure DVWA is running at {DVWA_URL}")
        print(
            "You can start DVWA with Docker: docker run --rm -it -p 8080:80 vulnerables/web-dvwa"
        )
