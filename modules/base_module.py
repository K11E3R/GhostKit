#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base Module Interface for GhostKit
All modules must inherit from this class and implement the required methods
"""

import abc
import logging
import argparse
from typing import List, Dict, Any, Optional

class BaseModule(abc.ABC):
    """Base class that all GhostKit modules must inherit from"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(f"GhostKit.{self.name}")
        self.description = "Base module interface"
        self.args_parser = self._create_arg_parser()
        
    @abc.abstractmethod
    def _create_arg_parser(self) -> argparse.ArgumentParser:
        """Create an argument parser for the module"""
        parser = argparse.ArgumentParser(description=self.description)
        return parser
        
    @abc.abstractmethod
    def run(self, args: List[str]) -> Dict[str, Any]:
        """
        Run the module with the given arguments
        
        Args:
            args: List of command-line arguments
            
        Returns:
            Dict containing the results of the module execution
        """
        parsed_args = self.args_parser.parse_args(args)
        return {"status": "not_implemented"}
    
    def validate_args(self, args: List[str]) -> bool:
        """
        Validate the arguments for the module
        
        Args:
            args: List of command-line arguments
            
        Returns:
            True if arguments are valid, False otherwise
        """
        try:
            self.args_parser.parse_args(args)
            return True
        except Exception:
            return False
            
    def get_help(self) -> str:
        """
        Get the help text for the module
        
        Returns:
            Help text as a string
        """
        return self.args_parser.format_help()
        
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the module
        
        Returns:
            Dict containing module information
        """
        return {
            "name": self.name,
            "description": self.description,
            "help": self.get_help()
        }
