#!/usr/bin/env python3
"""
Tactical Banner Generator for GhostKit Documentation
Creates cyberpunk-themed banner images for each section of the documentation.
"""

import os
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

# Banner titles from error logs
BANNER_TITLES = {
    "exploitation-banner.png": "EXPLOITATION TECHNIQUES",
    "threat-intel-banner.png": "THREAT INTELLIGENCE",
    "architecture-banner.png": "ARCHITECTURE",
    "api-banner.png": "API REFERENCE",
    "contribution-banner.png": "CONTRIBUTION GUIDE",
    "plugin-banner.png": "PLUGIN DEVELOPMENT",
    "ghostkit-banner.png": "GHOSTKIT FRAMEWORK",
    "quickstart-banner.png": "QUICKSTART",
    "legal-banner.png": "SECURITY ADVISORIES",
    "web-scanner-banner.png": "WEB SCANNER",
    "mitre-banner.png": "MITRE ATT&CK MAPPING",
    "opsec-banner.png": "OPERATIONAL SECURITY",
    "overview-banner.png": "GHOSTKIT OVERVIEW",
}


def create_cyberpunk_banner(title, output_path, width=1200, height=300):
    """Create a cyberpunk-themed banner with the given title."""
    # Create base image with black background
    img = Image.new("RGBA", (width, height), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Add grid pattern
    grid_color = (0, 80, 100, 50)
    grid_spacing = 20
    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # Add random digital glitch effects
    for _ in range(25):
        x = random.randint(0, width)
        y = random.randint(0, height)
        glitch_width = random.randint(50, 400)
        glitch_height = random.randint(5, 20)

        # Random cyberpunk color for the glitch
        glitch_colors = [
            (255, 0, 128, 128),  # Neon pink
            (0, 255, 255, 128),  # Cyan
            (128, 0, 255, 128),  # Purple
            (0, 255, 128, 128),  # Neon green
        ]

        glitch_color = random.choice(glitch_colors)
        draw.rectangle([x, y, x + glitch_width, y + glitch_height], fill=glitch_color)

    # Draw a main diagonal line
    line_color = (0, 255, 255, 200)  # Cyan with transparency
    draw.line([(0, height), (width, 0)], fill=line_color, width=10)

    # Add text shadow for depth
    try:
        # Try to load a futuristic font if available
        font = ImageFont.truetype("Arial Bold", 70)
    except IOError:
        # Fallback to default font
        font = ImageFont.load_default().font_variant(size=70)

    # Draw text shadow
    shadow_color = (0, 200, 255, 100)  # Cyan shadow
    for offset in range(1, 6, 2):
        draw.text(
            (width // 2 - 2 + offset, height // 2 - 2 + offset),
            title,
            font=font,
            fill=shadow_color,
            anchor="mm",
        )

    # Draw main text
    text_color = (255, 255, 255, 255)  # White
    draw.text((width // 2, height // 2), title, font=font, fill=text_color, anchor="mm")

    # Add scanlines effect
    scanlines = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
    scanlines_draw = ImageDraw.Draw(scanlines)
    for y in range(0, height, 4):
        scanlines_draw.line([(0, y), (width, y)], fill=(0, 0, 0, 50), width=1)

    # Compose the final image
    img = Image.alpha_composite(img, scanlines)

    # Save the image
    img.save(output_path)
    print(f"Created banner: {output_path}")


def main():
    """Generate all banners for the GhostKit documentation."""
    # Determine the output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(base_dir, "mkdocs-src", "assets", "images")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate each banner
    for banner_file, title in BANNER_TITLES.items():
        output_path = os.path.join(output_dir, banner_file)
        create_cyberpunk_banner(title, output_path)

    print(f"All {len(BANNER_TITLES)} banners generated successfully in: {output_dir}")


if __name__ == "__main__":
    main()
