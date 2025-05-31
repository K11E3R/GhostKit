#!/usr/bin/env python3
"""
Post-build hook for MkDocs to copy files from site directory to docs directory
for GitHub Pages deployment compatibility.
"""

import logging
import os
import shutil
from pathlib import Path


def copy_to_docs(config, **kwargs):
    """
    Copy all files from site_dir to docs directory for GitHub Pages compatibility.

    Args:
        config: The MkDocs configuration
        **kwargs: Additional arguments passed by MkDocs
    """
    site_dir = config["site_dir"]
    base_dir = os.path.dirname(site_dir)
    docs_dir = os.path.join(base_dir, "docs")

    logging.info(
        f"🔮 GhostKit Tactical Deployment: Copying files from {site_dir} to {docs_dir}"
    )

    # Ensure the docs directory exists
    Path(docs_dir).mkdir(exist_ok=True)

    # Remove all files in the docs directory first (except .git if present)
    for item in os.listdir(docs_dir):
        if item == ".git":
            continue
        item_path = os.path.join(docs_dir, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.unlink(item_path)

    # Copy all files from site_dir to docs_dir
    for item in os.listdir(site_dir):
        s = os.path.join(site_dir, item)
        d = os.path.join(docs_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks=False, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    # Create .nojekyll file in docs directory
    with open(os.path.join(docs_dir, ".nojekyll"), "w") as f:
        pass

    logging.info("🔮 GhostKit Tactical Deployment: Copy complete")
    return True
