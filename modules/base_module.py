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
        # Store any predefined values
        name_value = getattr(self, "name", self.__class__.__name__)
        description_value = getattr(self, "description", "Base module interface")

        # Set up the logger
        self.name = name_value
        self.logger = logging.getLogger(f"GhostKit.{self.name}")
        self.description = description_value
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
            "help": self.get_help(),
        }


# Concrete implementation of BaseModule for the base_module import
class ConcreteBaseModule(BaseModule):
    """Concrete implementation of BaseModule for testing and framework purposes"""

    def __init__(self):
        self.name = "base_module"
        self.description = "Base module providing core functionality"
        super().__init__()

    def _create_arg_parser(self) -> argparse.ArgumentParser:
        """Create an argument parser for the module"""
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument(
            "--info", action="store_true", help="Show module information"
        )
        return parser

    def run(self, args: List[str] = None) -> Dict[str, Any]:
        """Run the base module with the given arguments"""
        if args is None:
            args = []

        parsed_args = self.args_parser.parse_args(args)

        if parsed_args.info:
            return {"status": "success", "info": self.get_info()}

        return {"status": "success", "message": "Base module executed successfully"}


# For direct import compatibility
Module = ConcreteBaseModule
