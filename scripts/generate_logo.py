#!/usr/bin/env python3
"""
Tactical Logo Generator for GhostKit
Creates a cyberpunk-themed logo for the framework.
"""

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


def create_cyberpunk_logo(output_path, size=512):
    """Create a cyberpunk-themed logo for GhostKit."""
    # Create a square image with transparent background
    img = Image.new("RGBA", (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Calculate dimensions
    center = size // 2
    outer_radius = size * 0.45
    inner_radius = size * 0.35

    # Draw outer circle (ghost outline)
    draw.ellipse(
        [
            (center - outer_radius, center - outer_radius),
            (center + outer_radius, center + outer_radius),
        ],
        outline=(0, 255, 255, 200),  # Cyan
        width=4,
    )

    # Draw inner circle (ghost head)
    draw.ellipse(
        [
            (center - inner_radius, center - inner_radius),
            (center + inner_radius, center + inner_radius),
        ],
        fill=(0, 0, 0, 180),
        outline=(255, 0, 128, 200),  # Neon pink
        width=3,
    )

    # Draw eyes (cyberpunk style)
    eye_radius = size * 0.07
    eye_offset = size * 0.12

    # Left eye
    draw.ellipse(
        [
            (center - eye_offset - eye_radius, center - eye_radius),
            (center - eye_offset + eye_radius, center + eye_radius),
        ],
        fill=(0, 255, 255, 220),  # Cyan
    )

    # Right eye
    draw.ellipse(
        [
            (center + eye_offset - eye_radius, center - eye_radius),
            (center + eye_offset + eye_radius, center + eye_radius),
        ],
        fill=(0, 255, 255, 220),  # Cyan
    )

    # Add digital glitch effects
    for i in range(10):
        x_offset = i * 5
        y_offset = size // 2 - 10 * i
        width = size // 3
        height = 4

        # Alternate glitch colors
        if i % 2 == 0:
            glitch_color = (255, 0, 128, 100)  # Pink
        else:
            glitch_color = (0, 255, 255, 100)  # Cyan

        draw.rectangle(
            [
                (center - width // 2 + x_offset, y_offset),
                (center + width // 2 + x_offset, y_offset + height),
            ],
            fill=glitch_color,
        )

    # Add "GK" letters in the center
    try:
        # Try to load a futuristic font if available
        font = ImageFont.truetype("Arial Bold", size // 4)
    except IOError:
        # Fallback to default font
        font = ImageFont.load_default().font_variant(size=size // 4)

    # Draw text with glow effect
    glow_color = (0, 255, 255, 100)  # Cyan glow
    text_color = (255, 255, 255, 230)  # White text

    for offset in range(1, 6, 2):
        draw.text(
            (center + offset, center + offset),
            "GK",
            font=font,
            fill=glow_color,
            anchor="mm",
        )

    draw.text((center, center), "GK", font=font, fill=text_color, anchor="mm")

    # Add subtle scanlines
    scanlines = Image.new("RGBA", (size, size), color=(0, 0, 0, 0))
    scanlines_draw = ImageDraw.Draw(scanlines)

    for y in range(0, size, 4):
        scanlines_draw.line([(0, y), (size, y)], fill=(0, 0, 0, 20), width=1)

    # Apply scanlines
    img = Image.alpha_composite(img, scanlines)

    # Save the image
    img.save(output_path)
    print(f"Created logo: {output_path}")
    return True


def main():
    """Generate the GhostKit logo."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    # Create logo in both mkdocs-src and docs directories
    for dir_name in ["mkdocs-src", "docs"]:
        output_dir = os.path.join(base_dir, dir_name, "assets", "images")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "ghostkit-logo.png")
        create_cyberpunk_logo(output_path)

    print("🔮 GhostKit Logo Generation Complete")


if __name__ == "__main__":
    main()
