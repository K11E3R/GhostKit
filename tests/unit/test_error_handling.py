#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test the error handling system in the base module
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from modules.base_module import (
    BaseModule,
    GhostKitException,
    ModuleAuthenticationError,
    ModuleConfigError,
    ModuleConnectionError,
    ModulePermissionError,
    ModuleResult,
    ModuleRuntimeError,
    ModuleSeverity,
)


class TestableModule(BaseModule):
    """A testable implementation of BaseModule"""

    def _create_arg_parser(self):
        parser = super()._create_arg_parser()
        parser.add_argument("--test-arg", help="A test argument")
        return parser

    def run(self, args):
        if "--error-type" in args:
            error_type = args[args.index("--error-type") + 1]
            if error_type == "config":
                raise ModuleConfigError("Configuration error")
            elif error_type == "runtime":
                raise ModuleRuntimeError("Runtime error")
            elif error_type == "connection":
                raise ModuleConnectionError("Connection error")
            elif error_type == "auth":
                raise ModuleAuthenticationError("Authentication error")
            elif error_type == "permission":
                raise ModulePermissionError("Permission error")
            elif error_type == "generic":
                raise Exception("Generic error")

        return super().run(args)


class TestErrorHandling:
    """Test the error handling system"""

    def test_base_exception(self):
        """Test the base exception class"""
        exc = GhostKitException("Test error")
        assert str(exc) == "Test error"
        assert exc.severity == ModuleSeverity.MEDIUM

    def test_specific_exceptions(self):
        """Test the specific exception classes"""
        exc1 = ModuleConfigError("Config error", ModuleSeverity.HIGH)
        assert str(exc1) == "Config error"
        assert exc1.severity == ModuleSeverity.HIGH

        exc2 = ModuleRuntimeError("Runtime error")
        assert str(exc2) == "Runtime error"
        assert exc2.severity == ModuleSeverity.MEDIUM

    def test_module_result(self):
        """Test the ModuleResult class"""
        # Test successful result
        result = ModuleResult(
            success=True,
            message="Success",
            module_name="test_module",
            data={"key": "value"},
        )
        assert result.success is True
        assert result.message == "Success"
        assert result.module_name == "test_module"
        assert result.data == {"key": "value"}
        assert result.error is None

        # Test JSON serialization
        json_str = result.to_json()
        assert "success" in json_str
        assert "test_module" in json_str
        assert "key" in json_str

        # Test with error
        error = ValueError("Test error")
        result = ModuleResult(
            success=False,
            message="Failed",
            module_name="test_module",
            error=error,
            severity=ModuleSeverity.HIGH,
        )
        assert result.success is False
        assert result.message == "Failed"
        assert result.error == error
        assert result.severity == ModuleSeverity.HIGH

        # Test dictionary conversion
        result_dict = result.to_dict()
        assert result_dict["success"] is False
        assert result_dict["message"] == "Failed"
        assert result_dict["module"] == "test_module"
        assert result_dict["severity"] == "HIGH"
        assert "error" in result_dict
        assert result_dict["error"]["type"] == "ValueError"

    def test_module_error_handling(self):
        """Test error handling in modules"""
        module = TestableModule()

        # Test configuration error
        result = module.run(["--error-type", "config"])
        assert result.success is False
        assert "Configuration error" in result.message
        assert isinstance(result.error, ModuleConfigError)

        # Test runtime error
        result = module.run(["--error-type", "runtime"])
        assert result.success is False
        assert "Runtime error" in result.message
        assert isinstance(result.error, ModuleRuntimeError)

        # Test connection error
        result = module.run(["--error-type", "connection"])
        assert result.success is False
        assert "Connection error" in result.message
        assert isinstance(result.error, ModuleConnectionError)

        # Test authentication error
        result = module.run(["--error-type", "auth"])
        assert result.success is False
        assert "Authentication error" in result.message
        assert isinstance(result.error, ModuleAuthenticationError)

        # Test permission error
        result = module.run(["--error-type", "permission"])
        assert result.success is False
        assert "Permission error" in result.message
        assert isinstance(result.error, ModulePermissionError)

        # Test generic error
        result = module.run(["--error-type", "generic"])
        assert result.success is False
        assert "Generic error" in result.message
        assert isinstance(result.error, Exception)


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
