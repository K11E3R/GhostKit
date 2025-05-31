#!/usr/bin/env python3
"""
GhostKit Documentation Link Fixer
Analyzes and repairs broken internal links in Markdown documentation
"""

import glob
import os
import re
from pathlib import Path

# Configuration
DOCS_DIR = "docs"
VALID_SECTIONS = [
    "getting-started",
    "core-concepts",
    "modules",
    "advanced",
    "tradecraft",
    "development",
    "legal",
    "security",
]

# Pattern to match Markdown links: [link text](target)
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def get_existing_files():
    """Get all existing Markdown files in the docs directory"""
    docs_path = Path(DOCS_DIR)
    md_files = glob.glob(str(docs_path / "**/*.md"), recursive=True)
    md_files += glob.glob(str(docs_path / "*.md"))

    # Convert to relative paths within docs
    relative_paths = []
    for file_path in md_files:
        rel_path = os.path.relpath(file_path, DOCS_DIR)
        relative_paths.append(rel_path.replace("\\", "/"))

    return set(relative_paths)


def find_alternative_path(broken_path, existing_files):
    """Try to find an alternative path for a broken link"""
    # First check if file exists with different extension
    filename = os.path.basename(broken_path)
    name_without_ext = os.path.splitext(filename)[0]

    # Try to find files with the same basename
    candidates = []
    for existing in existing_files:
        existing_basename = os.path.basename(existing)
        existing_name = os.path.splitext(existing_basename)[0]

        if existing_name == name_without_ext:
            candidates.append(existing)

    if candidates:
        return candidates[0]  # Return first match

    # If no direct match, try to find semantically similar files
    # This is a simple implementation - could be enhanced with more sophisticated matching
    keywords = name_without_ext.split("-")
    best_match = None
    best_match_score = 0

    for existing in existing_files:
        score = 0
        for keyword in keywords:
            if keyword in existing:
                score += 1

        if score > best_match_score:
            best_match_score = score
            best_match = existing

    if best_match_score > 0:
        return best_match

    # If still no match, return a default path based on the section
    for section in VALID_SECTIONS:
        if section in broken_path:
            # Find any file in the same section
            for existing in existing_files:
                if section in existing:
                    return existing

    # Last resort - just link to index.md
    return "index.md"


def fix_links_in_file(file_path, existing_files):
    """Fix broken links in a single file"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    fixed_content = content
    replacements = []

    # Find all links in the content
    for match in LINK_PATTERN.finditer(content):
        link_text, target = match.groups()

        # Skip external links and anchors
        if target.startswith(("http://", "https://", "#")):
            continue

        # Skip image links that exist
        if target.startswith("../assets/images/") and "banner" in target:
            continue

        # Handle relative paths
        if target.startswith("../"):
            # Convert to docs-relative path
            current_dir = os.path.dirname(os.path.relpath(file_path, DOCS_DIR))
            target_path = os.path.normpath(os.path.join(current_dir, target))
            target_path = target_path.replace("\\", "/")
        else:
            # If it's already a docs-relative path
            target_path = target

        # Check if the target exists
        if target_path not in existing_files:
            # Find alternative
            alternative = find_alternative_path(target_path, existing_files)

            # Calculate relative path from current file to alternative
            current_dir = os.path.dirname(os.path.relpath(file_path, DOCS_DIR))
            rel_path = os.path.relpath(alternative, current_dir).replace("\\", "/")

            # Store replacement
            original = f"[{link_text}]({target})"
            replacement = f"[{link_text}]({rel_path})"
            replacements.append((original, replacement))

    # Apply all replacements
    for original, replacement in replacements:
        fixed_content = fixed_content.replace(original, replacement)

    # Write back only if changes were made
    if fixed_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(fixed_content)
        return len(replacements)

    return 0


def main():
    """Main function to fix all broken links"""
    print("GhostKit Documentation Link Fixer")
    print("==================================")

    # Get all existing Markdown files
    existing_files = get_existing_files()
    print(f"Found {len(existing_files)} Markdown files")

    # Get all Markdown files to process
    docs_path = Path(DOCS_DIR)
    md_files = glob.glob(str(docs_path / "**/*.md"), recursive=True)
    md_files += glob.glob(str(docs_path / "*.md"))

    # Fix links in each file
    total_fixed = 0
    for file_path in md_files:
        fixed = fix_links_in_file(file_path, existing_files)
        if fixed > 0:
            rel_path = os.path.relpath(file_path, ".")
            print(f"Fixed {fixed} links in {rel_path}")
            total_fixed += fixed

    print(f"\nTotal links fixed: {total_fixed}")
    print("Link fixing complete!")


if __name__ == "__main__":
    main()
