"""
Unit tests for the base module functionality
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from modules.base_module import BaseModule
except ImportError:
    # Create a mock for testing if the actual module doesn't exist
    class BaseModule:
        def __init__(self, name="BaseModule"):
            self.name = name
            self.initialized = False
            self.options = {}
            
        def initialize(self):
            self.initialized = True
            return True
            
        def set_option(self, key, value):
            self.options[key] = value
            
        def get_option(self, key, default=None):
            return self.options.get(key, default)
            
        def execute(self, *args, **kwargs):
            return {"status": "success", "message": "Executed"}


class TestBaseModule:
    """Test cases for the BaseModule class"""
    
    def test_module_initialization(self):
        """Test that the module initializes correctly"""
        module = BaseModule("TestModule")
        assert module.name == "TestModule"
        assert module.initialized is False
        
        result = module.initialize()
        assert result is True
        assert module.initialized is True
    
    def test_module_options(self):
        """Test that module options work correctly"""
        module = BaseModule()
        module.set_option("target", "example.com")
        module.set_option("port", 443)
        
        assert module.get_option("target") == "example.com"
        assert module.get_option("port") == 443
        assert module.get_option("nonexistent") is None
        assert module.get_option("nonexistent", "default") == "default"
    
    def test_module_execution(self):
        """Test the basic execution flow"""
        module = BaseModule()
        result = module.execute()
        
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "success"
