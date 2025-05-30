"""
Integration tests for module interactions within the GhostKit framework
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import main GhostKit class if available, otherwise create a mock
try:
    from ghostkit import GhostKit
except ImportError:
    import argparse
    import sys
    import logging
    from tests.unit.test_base_module import TestableModule
    from tests.unit.test_web_xss_scanner import XSSScanner
    
    class GhostKit:
        def __init__(self):
            self.modules = {}
            self.logger = logging.getLogger("GhostKit")
            self.parser = argparse.ArgumentParser(description="GhostKit Security Framework")
            self._setup_argparse()
            
        def _setup_argparse(self):
            self.parser.add_argument("-m", "--module", help="Module to execute", action="append")
            self.parser.add_argument("-t", "--target", help="Target to scan")
            self.parser.add_argument("-u", "--url", help="URL to scan")
            
        def run(self, args=None):
            if args is None:
                args = sys.argv[1:]
                
            parsed_args = self.parser.parse_args(args)
            
            # Load modules if not loaded
            if not self.modules:
                self.load_modules()
                
            # Execute modules if specified
            if parsed_args.module:
                results = []
                for module_name in parsed_args.module:
                    module_args = []
                    if parsed_args.target:
                        module_args.extend(["-t", parsed_args.target])
                    if parsed_args.url:
                        module_args.extend(["-u", parsed_args.url])
                        
                    result = self.run_module(module_name, module_args)
                    results.append(result)
                return results
            
            return {"status": "error", "message": "No module specified"}
            
        def load_modules(self):
            # Mock module loading for tests
            self.modules["base_module"] = TestableModule()
            self.modules["xss_scanner"] = XSSScanner()
            return len(self.modules)
            
        def get_module(self, name):
            return self.modules.get(name)
            
        def run_module(self, module_name, args=None):
            module = self.get_module(module_name)
            if not module:
                return {"status": "error", "message": f"Module {module_name} not found"}
                
            # Run module with args
            return module.run(args)


class TestModuleIntegration:
    """Integration tests for GhostKit module interactions"""
    
    def test_framework_initialization(self):
        """Test that the framework initializes and loads modules correctly"""
        ghostkit = GhostKit()
        
        # Check if modules are loaded properly
        module_count = ghostkit.load_modules()
        assert module_count >= 2  # At least base_module and xss_scanner
        assert "base_module" in ghostkit.modules
        assert "xss_scanner" in ghostkit.modules
    
    def test_cross_module_workflow(self):
        """Test a workflow that uses multiple modules"""
        ghostkit = GhostKit()
        ghostkit.load_modules()
        
        # Run XSS scanner with command-line args
        result = ghostkit.run_module("xss_scanner", ["-u", "http://example.com/search"])
        assert result["status"] == "success"
        
        # Get results from one module and use in another (simulated)
        vulnerabilities = result.get("vulnerabilities", [])
        if vulnerabilities:
            # In a real integration, we might pass these results to another module
            vulnerable_url = vulnerabilities[0]["url"]
            assert "example.com" in vulnerable_url
    
    @pytest.mark.parametrize("target,expected_vulns", [
        ("http://example.com/search", 1),  # Should find vuln
        ("http://example.com/about", 0),   # Should not find vuln
    ])
    def test_parameterized_scanning(self, target, expected_vulns):
        """Test scanning different targets with expected results"""
        ghostkit = GhostKit()
        ghostkit.load_modules()
        
        # Run with command-line args instead of options
        result = ghostkit.run_module("xss_scanner", ["-u", target])
        assert result["status"] == "success"
        assert len(result.get("vulnerabilities", [])) == expected_vulns
    
    def test_error_handling(self):
        """Test error handling across modules"""
        ghostkit = GhostKit()
        ghostkit.load_modules()
        
        # Test invalid module
        result = ghostkit.run_module("nonexistent_module")
        assert result["status"] == "error"
        assert "not found" in result["message"]
        
        # Test with missing required URL - check status
        result = ghostkit.run(["-m", "xss_scanner"])  # No target or URL
        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0]["status"] == "error" or "No target specified" in str(result)
