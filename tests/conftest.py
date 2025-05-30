"""
GhostKit Test Configuration
--------------------------
This file contains pytest fixtures and configuration for testing the GhostKit framework.
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def mock_requests_session():
    """Mock requests session for testing web modules without making actual requests."""
    with patch("requests.Session") as mock_session:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><form action='/login'><input name='username'><input name='password'></form></body></html>"
        mock_response.headers = {"Content-Type": "text/html"}
        mock_session.return_value.get.return_value = mock_response
        mock_session.return_value.post.return_value = mock_response
        yield mock_session


@pytest.fixture
def isolated_filesystem(tmpdir):
    """Provide a temporary directory for file operations during tests."""
    prev_dir = os.getcwd()
    os.chdir(tmpdir)
    yield tmpdir
    os.chdir(prev_dir)


@pytest.fixture
def mock_network_interface():
    """Mock network interface for wireless testing."""
    mock_interface = MagicMock()
    mock_interface.name = "wlan0"
    mock_interface.mac = "00:11:22:33:44:55"
    mock_interface.is_up.return_value = True
    return mock_interface


@pytest.fixture
def safe_test_target():
    """Return a safe test target that doesn't exist (for safe testing)."""
    return "https://ghostkit-safe-testing-domain-that-does-not-exist.local"
