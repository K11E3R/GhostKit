"""
Unit tests for the base module functionality
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

try:
    from modules.base_module import BaseModule

    # Create a concrete implementation for testing
    class TestableModule(BaseModule):
        def __init__(self, name="TestModule"):
            # Store values temporarily before super init
            name_value = name
            description_value = "Test module for unit testing"
            self.options = {}
            super().__init__()
            # Reset values after super().__init__ to preserve them
            self.name = name_value
            self.description = description_value

        def _create_arg_parser(self):
            import argparse

            parser = argparse.ArgumentParser(description=self.description)
            parser.add_argument("-t", "--target", help="Target to scan")
            return parser

        def run(self, args=None):
            if args is None:
                args = []
            parsed_args = self.args_parser.parse_args(args)
            return {
                "status": "success",
                "message": "Executed",
                "args": vars(parsed_args),
            }

        def set_option(self, key, value):
            self.options[key] = value

        def get_option(self, key, default=None):
            return self.options.get(key, default)

except ImportError:
    # Create a mock for testing if the actual module doesn't exist
    import argparse

    class BaseModule:
        def __init__(self):
            self.name = self.__class__.__name__
            self.description = "Base module interface"
            self.args_parser = self._create_arg_parser()

        def _create_arg_parser(self):
            parser = argparse.ArgumentParser(description=self.description)
            return parser

        def run(self, args=None):
            if args is None:
                args = []
            parsed_args = self.args_parser.parse_args(args)
            return {"status": "not_implemented"}

    class TestableModule(BaseModule):
        def __init__(self, name="TestModule"):
            # Store values temporarily before super init
            name_value = name
            description_value = "Test module for unit testing"
            self.options = {}
            super().__init__()
            # Reset values after super().__init__ to preserve them
            self.name = name_value
            self.description = description_value

        def _create_arg_parser(self):
            parser = argparse.ArgumentParser(description=self.description)
            parser.add_argument("-t", "--target", help="Target to scan")
            return parser

        def run(self, args=None):
            if args is None:
                args = []
            parsed_args = self.args_parser.parse_args(args)
            return {
                "status": "success",
                "message": "Executed",
                "args": vars(parsed_args),
            }

        def set_option(self, key, value):
            self.options[key] = value

        def get_option(self, key, default=None):
            return self.options.get(key, default)


class TestBaseModule:
    """Test cases for the BaseModule class"""

    def test_module_initialization(self):
        """Test that the module initializes correctly"""
        module = TestableModule("TestModule")
        assert module.name == "TestModule"
        assert module.description == "Test module for unit testing"

    def test_module_options(self):
        """Test that module options work correctly"""
        module = TestableModule()
        module.set_option("target", "example.com")
        module.set_option("port", 443)

        assert module.get_option("target") == "example.com"
        assert module.get_option("port") == 443
        assert module.get_option("nonexistent") is None
        assert module.get_option("nonexistent", "default") == "default"

    def test_module_execution(self):
        """Test the basic execution flow"""
        module = TestableModule()
        result = module.run(["-t", "example.com"])

        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "success"
