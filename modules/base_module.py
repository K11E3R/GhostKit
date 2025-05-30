#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base Module Interface for GhostKit
All modules must inherit from this class and implement the required methods

This module defines the core architecture for all GhostKit components,
including the base exception hierarchy, module interface, and logging setup.
"""

import abc
import argparse
import json
import logging
import sys
import traceback
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar, Union, cast


class ModuleSeverity(Enum):
    """Severity levels for module operations and results"""

    INFO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class GhostKitException(Exception):
    """Base exception for all GhostKit errors"""

    def __init__(
        self, message: str, severity: ModuleSeverity = ModuleSeverity.MEDIUM
    ) -> None:
        self.message = message
        self.severity = severity
        super().__init__(self.message)


class ModuleConfigError(GhostKitException):
    """Raised when a module configuration is invalid"""

    pass


class ModuleRuntimeError(GhostKitException):
    """Raised when a module encounters a runtime error"""

    pass


class ModuleConnectionError(GhostKitException):
    """Raised when a module fails to connect to a target"""

    pass


class ModuleAuthenticationError(GhostKitException):
    """Raised when a module fails to authenticate"""

    pass


class ModulePermissionError(GhostKitException):
    """Raised when a module lacks necessary permissions"""

    pass


@dataclass
class ModuleResult:
    """Standardized result object for module operations"""

    success: bool
    message: str
    module_name: str
    severity: ModuleSeverity = ModuleSeverity.INFO
    data: Optional[Dict[str, Any]] = None
    error: Optional[Exception] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for serialization"""
        result = {
            "success": self.success,
            "message": self.message,
            "module": self.module_name,
            "severity": self.severity.name,
        }

        if self.data:
            result["data"] = self.data

        if self.error:
            result["error"] = {
                "type": self.error.__class__.__name__,
                "message": str(self.error),
                "traceback": (
                    traceback.format_exception(
                        type(self.error), self.error, self.error.__traceback__
                    )
                    if hasattr(self.error, "__traceback__")
                    else None
                ),
            }

        return result

    def to_json(self, pretty: bool = False) -> str:
        """Convert result to JSON string"""
        indent = 2 if pretty else None
        return json.dumps(self.to_dict(), indent=indent)


class BaseModule(abc.ABC):
    """Base class that all GhostKit modules must inherit from"""

    def __init__(self) -> None:
        name_value = getattr(self, "name", self.__class__.__name__)
        description_value = getattr(self, "description", "Base module interface")

        self.name: str = name_value
        self.description: str = description_value
        self.logger: logging.Logger = logging.getLogger(f"GhostKit.{self.name}")
        self.args_parser: argparse.ArgumentParser = self._create_arg_parser()
        self.config_file: Optional[Path] = None

        # --- Wrapping de la méthode `run` de la sous-classe ---
        original_run = self.run

        def wrapped_run(args: List[str]) -> ModuleResult:
            try:
                result = original_run(args)
                # Si le module a retourné un dict par erreur, on le transforme
                if not isinstance(result, ModuleResult):
                    return ModuleResult(
                        success=True,
                        message="Module executed successfully",
                        module_name=self.name,
                        data={"raw": result},
                    )
                return result
            except GhostKitException as gk:
                self.logger.error(f"[{gk.severity.name}] {gk.message}")
                return ModuleResult(
                    success=False,
                    message=gk.message,
                    module_name=self.name,
                    severity=gk.severity,
                    error=gk,
                )
            except Exception as exc:
                self.logger.exception("Unexpected error in module")
                return ModuleResult(
                    success=False,
                    message=f"Unexpected error: {str(exc)}",
                    module_name=self.name,
                    severity=ModuleSeverity.CRITICAL,
                    error=exc,
                )

        self.run = wrapped_run  # type: ignore

    @abc.abstractmethod
    def _create_arg_parser(self) -> argparse.ArgumentParser:
        """Create an argument parser for the module

        Returns:
            argparse.ArgumentParser: Configured argument parser for this module

        This method must be implemented by all subclasses to define their
        specific command-line arguments.
        """
        parser = argparse.ArgumentParser(description=self.description)
        return parser

    @abc.abstractmethod
    def run(self, args: List[str]) -> ModuleResult:
        """Run the module with the given arguments

        Args:
            args: List of command-line arguments to pass to the argument parser

        Returns:
            ModuleResult: Standardized result object containing success status,
                         message, and any relevant data or errors

        Raises:
            ModuleConfigError: If the module is incorrectly configured
            ModuleRuntimeError: If the module encounters a runtime error
            ModuleConnectionError: If the module fails to connect to a target
            ModuleAuthenticationError: If the module fails to authenticate
            ModulePermissionError: If the module lacks necessary permissions
        """
        parsed = self.args_parser.parse_args(args)
        return ModuleResult(
            success=True,
            message="Module executed successfully",
            module_name=self.name,
            data={"args": vars(parsed)},
        )

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
