#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostKit - Advanced Security Analysis Framework
Author: GhostShellX
License: MIT
"""

import argparse
import sys
import os
import logging
import importlib
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"ghostkit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("GhostKit")

# Banner
BANNER = r"""
  ▄████  ██░ ██  ▒█████    ██████ ▄▄▄█████▓ ██ ▄█▀ ██▓▄▄▄█████▓
 ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒ ██▄█▒ ▓██▒▓  ██▒ ▓▒
▒██░▄▄▄░▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░▓███▄░ ▒██▒▒ ▓██░ ▒░
░▓█  ██▓░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░ ▓██ █▄ ░██░░ ▓██▓ ░ 
░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░ ▒██▒ █▄░██░  ▒██▒ ░ 
 ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   ▒ ▒▒ ▓▒░▓    ▒ ░░   
  ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░    ░ ░▒ ▒░ ▒ ░    ░    
░ ░   ░  ░  ░░ ░░ ░ ░ ▒  ░  ░  ░    ░      ░ ░░ ░  ▒ ░  ░      
      ░  ░  ░  ░    ░ ░        ░           ░  ░    ░           
                                                               
Advanced Security Analysis Framework
"""

class GhostKit:
    def __init__(self):
        self.modules = {}
        self.load_modules()
        
    def load_modules(self):
        """Load all available modules from the modules directory"""
        modules_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules")
        if not os.path.exists(modules_dir):
            os.makedirs(modules_dir)
            logger.warning(f"Created modules directory at {modules_dir}")
            return
            
        for filename in os.listdir(modules_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f"modules.{module_name}")
                    if hasattr(module, "Module"):
                        self.modules[module_name] = module.Module()
                        logger.info(f"Loaded module: {module_name}")
                except Exception as e:
                    logger.error(f"Failed to load module {module_name}: {str(e)}")
    
    def list_modules(self):
        """List all available modules"""
        print("\nAvailable Modules:")
        print("=" * 50)
        for name, module in self.modules.items():
            print(f"[+] {name}: {module.description}")
        print("=" * 50)
    
    def run_module(self, module_name, args):
        """Run a specific module with arguments"""
        if module_name in self.modules:
            try:
                self.modules[module_name].run(args)
            except Exception as e:
                logger.error(f"Error running module {module_name}: {str(e)}")
        else:
            logger.error(f"Module '{module_name}' not found")
            print(f"Available modules: {', '.join(self.modules.keys())}")

def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description="GhostKit - Advanced Security Analysis Framework")
    parser.add_argument("-l", "--list", action="store_true", help="List all available modules")
    parser.add_argument("-m", "--module", help="Specify module to run")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--args", nargs=argparse.REMAINDER, help="Arguments to pass to the module")
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    ghostkit = GhostKit()
    
    if args.list:
        ghostkit.list_modules()
        return
    
    if args.module:
        module_args = args.args if args.args else []
        ghostkit.run_module(args.module, module_args)
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unhandled exception: {str(e)}")
        sys.exit(1)
